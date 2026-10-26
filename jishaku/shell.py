# -*- coding: utf-8 -*-

"""
jishaku.shell
~~~~~~~~~~~~~

Tools related to interacting directly with the shell.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

import asyncio
import os
import pathlib
import re
import subprocess
import sys
import time
import typing

from jishaku.flags import Flags

SHELL = os.getenv("SHELL") or "/bin/bash"
WINDOWS = sys.platform == "win32"

# Variables a shell command needs to work. Everything else (tokens, database URLs...) is NOT passed on.
SHELL_ENV_ALLOWLIST = ("PATH", "HOME", "LANG", "LC_ALL", "TZ", "USER", "LOGNAME", "GIT_DIR")
SHELL_ENV_ALLOWLIST_WINDOWS = ("SystemRoot", "COMSPEC", "PATHEXT", "TEMP", "TMP", "USERPROFILE")


def build_shell_env(
    environ: typing.Mapping[str, str],
    extra: typing.Iterable[str] = (),
    *,
    windows: bool = WINDOWS
) -> typing.Dict[str, str]:
    """
    A copy of ``environ`` with only the allowlisted variables (on Windows the names are case-insensitive).
    """

    allowed = SHELL_ENV_ALLOWLIST + (SHELL_ENV_ALLOWLIST_WINDOWS if windows else ()) + tuple(extra)

    if windows:
        wanted = {name.casefold() for name in allowed}
        return {key: value for key, value in environ.items() if key.casefold() in wanted}

    return {name: environ[name] for name in allowed if name in environ}


def default_shell_env() -> typing.Optional[typing.Dict[str, str]]:
    """
    The environment for shell commands: ``None`` (inherit everything) only with ``JISHAKU_SHELL_INHERIT_ENV``.
    """

    if Flags.SHELL_INHERIT_ENV:
        return None

    extra = [name.strip() for name in Flags.SHELL_ENV_ALLOW.split(',') if name.strip()]
    return build_shell_env(os.environ, extra)


def background_reader(stream, loop: asyncio.AbstractEventLoop, callback):
    """
    Reads a stream and forwards each line to an async callback.
    """

    for line in iter(stream.readline, b''):
        loop.call_soon_threadsafe(loop.create_task, callback(line))


class ShellReader:
    """
    A class that passively reads from a shell and buffers results for read.

    Example
    -------

    .. code:: python3

        # reader should be in a with statement to ensure it is properly closed
        with ShellReader('echo one; sleep 5; echo two') as reader:
            # prints 'one', then 'two' after 5 seconds
            async for x in reader:
                print(x)
    """

    def __init__(self, code: str, timeout: int = 120, loop: asyncio.AbstractEventLoop = None, env: typing.Optional[typing.Mapping[str, str]] = None):
        if WINDOWS:
            # Check for powershell
            if pathlib.Path(r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe").exists():
                sequence = ['powershell', code]
                self.ps1 = "PS >"
                self.highlight = "powershell"
            else:
                sequence = ['cmd', '/c', code]
                self.ps1 = "cmd >"
                self.highlight = "cmd"
        else:
            sequence = [SHELL, '-c', code]
            self.ps1 = "$"
            self.highlight = "sh"

        self.process = subprocess.Popen(
            sequence, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=default_shell_env() if env is None else env
        )
        self.close_code = None

        self.loop = loop or asyncio.get_running_loop()
        self.timeout = timeout

        self.stdout_task = self.make_reader_task(self.process.stdout, self.stdout_handler)
        self.stderr_task = self.make_reader_task(self.process.stderr, self.stderr_handler)

        self.queue = asyncio.Queue(maxsize=250)

    @property
    def closed(self):
        """
        Are both tasks done, indicating there is no more to read?
        """

        return self.stdout_task.done() and self.stderr_task.done()

    async def executor_wrapper(self, *args, **kwargs):
        """
        Call wrapper for stream reader.
        """

        return await self.loop.run_in_executor(None, *args, **kwargs)

    def make_reader_task(self, stream, callback):
        """
        Create a reader executor task for a stream.
        """

        return self.loop.create_task(self.executor_wrapper(background_reader, stream, self.loop, callback))

    @staticmethod
    def clean_bytes(line):
        """
        Cleans a byte sequence of shell directives and decodes it.
        """

        text = line.decode('utf-8').replace('\r', '').strip('\n')
        return re.sub(r'\x1b[^m]*m', '', text).replace("``", "`\u200b`").strip('\n')

    async def stdout_handler(self, line):
        """
        Handler for this class for stdout.
        """

        await self.queue.put(self.clean_bytes(line))

    async def stderr_handler(self, line):
        """
        Handler for this class for stderr.
        """

        await self.queue.put(self.clean_bytes(b'[stderr] ' + line))

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.process.kill()
        self.process.terminate()
        self.close_code = self.process.wait(timeout=0.5)

    def __aiter__(self):
        return self

    async def __anext__(self):
        last_output = time.perf_counter()

        while not self.closed or not self.queue.empty():
            try:
                item = await asyncio.wait_for(self.queue.get(), timeout=1)
            except asyncio.TimeoutError as exception:
                if time.perf_counter() - last_output >= self.timeout:
                    raise exception
            else:
                last_output = time.perf_counter()
                return item

        raise StopAsyncIteration()
