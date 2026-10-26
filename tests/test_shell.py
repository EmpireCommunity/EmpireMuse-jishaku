"""`jsk sh`: o comando roda com ambiente mínimo, sem herdar tokens e senhas do processo do bot."""

import asyncio
import sys

import pytest

from jishaku.shell import SHELL_ENV_ALLOWLIST, ShellReader, build_shell_env

posix = pytest.mark.skipif(sys.platform == "win32", reason="usa o shell POSIX")


def saida_de(comando: str) -> str:
    async def principal() -> str:
        with ShellReader(comando) as reader:
            return "\n".join([linha async for linha in reader])

    return asyncio.run(principal())


def test_allowlist_pura_deixa_so_o_que_o_shell_precisa():
    ambiente = {"PATH": "/bin", "HOME": "/h", "BOT_TOKEN": "segredo-1234", "MONGO": "mongodb://x", "EXTRA": "ok"}
    assert build_shell_env(ambiente, windows=False) == {"PATH": "/bin", "HOME": "/h"}
    assert build_shell_env(ambiente, ["EXTRA"], windows=False) == {"PATH": "/bin", "HOME": "/h", "EXTRA": "ok"}
    assert set(SHELL_ENV_ALLOWLIST) >= {"PATH", "HOME", "LANG"}


def test_no_windows_os_nomes_nao_diferenciam_maiusculas():
    ambiente = {"SYSTEMROOT": r"C:\Windows", "ComSpec": "cmd.exe", "BOT_TOKEN": "segredo-1234"}
    assert build_shell_env(ambiente, windows=True) == {"SYSTEMROOT": r"C:\Windows", "ComSpec": "cmd.exe"}


@posix
def test_comando_nao_enxerga_segredos_do_ambiente(monkeypatch):
    monkeypatch.setenv("MY_SECRET_TOKEN", "valor-que-nao-pode-vazar")
    saida = saida_de("env")
    assert "MY_SECRET_TOKEN" not in saida and "valor-que-nao-pode-vazar" not in saida
    assert "PATH=" in saida


@posix
def test_variaveis_extras_liberadas_por_flag(monkeypatch):
    monkeypatch.setenv("MINHA_VARIAVEL", "liberada")
    monkeypatch.setenv("JISHAKU_SHELL_ENV_ALLOW", "MINHA_VARIAVEL, OUTRA")
    assert "MINHA_VARIAVEL=liberada" in saida_de("env")


@posix
def test_herdar_o_ambiente_inteiro_so_com_a_flag_explicita(monkeypatch):
    monkeypatch.setenv("MY_SECRET_TOKEN", "valor-herdado")
    monkeypatch.setenv("JISHAKU_SHELL_INHERIT_ENV", "true")
    assert "MY_SECRET_TOKEN=valor-herdado" in saida_de("env")
