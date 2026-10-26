"""Comandos de gerenciamento do `jsk`: o link de convite."""

import asyncio
from types import SimpleNamespace

import disnake
from disnake.ext import commands

from jishaku import Jishaku


def test_convite_usa_o_dominio_atual_do_discord():
    enviados = []

    async def principal():
        bot = commands.Bot(command_prefix="!", intents=disnake.Intents.none())

        async def application_info():
            return SimpleNamespace(id=123)

        bot.application_info = application_info

        async def send(conteudo):
            enviados.append(conteudo)

        ctx = SimpleNamespace(send=send)
        cog = Jishaku(bot=bot)
        await cog.jsk_invite.callback(cog, ctx, "administrator")

    asyncio.run(principal())
    assert "https://discord.com/oauth2/authorize?client_id=123" in enviados[0]
    assert "permissions=8" in enviados[0]
