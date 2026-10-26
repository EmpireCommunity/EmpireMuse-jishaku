"""Compatibilidade com Python 3.13/3.14: carregar o pacote e a cog não pode emitir avisos de APIs removidas."""

import asyncio
import sys
import warnings

import disnake
from disnake.ext import commands


def test_importar_o_pacote_e_carregar_a_cog_sem_avisos_de_deprecacao():
    for name in [name for name in sys.modules if name == "jishaku" or name.startswith("jishaku.")]:
        del sys.modules[name]  # força a importação de novo, com os avisos ligados

    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)

        async def carregar():
            bot = commands.Bot(command_prefix="!", intents=disnake.Intents.none())
            bot.load_extension("jishaku")
            nomes = {command.qualified_name for command in bot.walk_commands()}
            await bot.close()
            return nomes

        nomes = asyncio.run(carregar())

    assert {"jishaku", "jishaku py", "jishaku shell", "jishaku cat"} <= nomes
