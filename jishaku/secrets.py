# -*- coding: utf-8 -*-

"""
jishaku.secrets
~~~~~~~~~~~~~~~

Mascaramento de segredos (tokens, senhas, URLs de webhook e de banco) na saída que o Jishaku manda para o Discord.

Os valores vêm do token do bot, do ambiente do processo e do ``bot.config`` (quando for um mapeamento), escolhidos pelo
NOME da chave. Qualquer ocorrência desses valores na saída de ``jsk py``, ``jsk sh``, ``jsk cat`` etc. é trocada por ``MASK``.

:license: MIT, see LICENSE for more details.

"""

import collections.abc
import os
import re
import typing

__all__ = ('MASK', 'MIN_SECRET_LENGTH', 'collect_secret_values', 'mask_secrets', 'bot_secret_values')

MASK = "[secret omitted]"

# Abaixo disso o valor vira falso positivo (um "true" ou um "0" no meio de qualquer saída).
MIN_SECRET_LENGTH = 6

SECRET_NAME = re.compile(
    r"TOKEN|SECRET|PASS|KEY|MONGO|WEBHOOK|COOKIE|CREDENTIAL|AUTH|REFRESH|LAVALINK_NODE|SPOTIFY_CLIENT|LASTFM|DSN|DATABASE_URL",
    re.IGNORECASE,
)


def collect_secret_values(*sources: typing.Mapping[str, object]) -> typing.FrozenSet[str]:
    """
    Valores textuais de segredo (pelo nome da chave) das fontes dadas, sem os vazios nem os curtos demais.
    """

    values = set()

    for source in sources:
        for key, value in source.items():
            if isinstance(value, str) and len(value) >= MIN_SECRET_LENGTH and SECRET_NAME.search(str(key)):
                values.add(value)

    return frozenset(values)


def mask_secrets(text: str, secrets: typing.Iterable[str]) -> str:
    """
    Troca cada valor de ``secrets`` em ``text`` por ``MASK``, do mais longo para o mais curto.
    """

    for secret in sorted(set(secrets), key=len, reverse=True):
        if secret:
            text = text.replace(secret, MASK)

    return text


def bot_secret_values(bot: typing.Any) -> typing.FrozenSet[str]:
    """
    Os segredos conhecidos de um bot: o token, o ambiente do processo e o ``bot.config`` (se for um mapeamento).
    """

    sources = [os.environ]

    config = getattr(bot, 'config', None)
    if isinstance(config, collections.abc.Mapping):
        sources.append(config)

    values = set(collect_secret_values(*sources))

    token = getattr(getattr(bot, 'http', None), 'token', None)
    if isinstance(token, str) and token:
        values.add(token)

    return frozenset(values)
