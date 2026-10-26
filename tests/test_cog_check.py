"""A guarda do Jishaku: só o dono do bot, opcionalmente só quem está em JISHAKU_OWNER_IDS e só em mensagem direta."""

import asyncio
from types import SimpleNamespace

import disnake
import pytest
from disnake.ext import commands

from jishaku import Jishaku


def verificar(*, dono: bool, autor_id: int = 10, em_servidor: bool = False):
    """Roda o cog_check; devolve True ou o erro levantado."""

    async def principal():
        bot = commands.Bot(command_prefix="!", intents=disnake.Intents.none())

        async def is_owner(user):
            return dono

        bot.is_owner = is_owner
        ctx = SimpleNamespace(bot=bot, author=SimpleNamespace(id=autor_id), guild=object() if em_servidor else None)
        try:
            return await Jishaku(bot=bot).cog_check(ctx)
        except commands.CheckFailure as erro:
            return erro

    return asyncio.run(principal())


def test_quem_nao_e_dono_do_bot_e_negado():
    assert isinstance(verificar(dono=False), commands.NotOwner)


def test_dono_passa_por_padrao_inclusive_em_servidor():
    assert verificar(dono=True) is True
    assert verificar(dono=True, em_servidor=True) is True


def test_lista_de_ids_exclui_donos_que_nao_estao_nela(monkeypatch):
    monkeypatch.setenv("JISHAKU_OWNER_IDS", "10, 11")
    assert verificar(dono=True, autor_id=10) is True
    assert isinstance(verificar(dono=True, autor_id=99), commands.NotOwner)
    assert isinstance(verificar(dono=False, autor_id=10), commands.NotOwner)


@pytest.mark.parametrize("valor", ["abc", "10,abc", "10;11"])
def test_lista_invalida_nega_todo_mundo(monkeypatch, valor):
    monkeypatch.setenv("JISHAKU_OWNER_IDS", valor)
    assert isinstance(verificar(dono=True, autor_id=10), commands.NotOwner)


def test_so_mensagem_direta_quando_pedido(monkeypatch):
    monkeypatch.setenv("JISHAKU_DM_ONLY", "true")
    assert verificar(dono=True) is True
    assert isinstance(verificar(dono=True, em_servidor=True), commands.PrivateMessageOnly)
