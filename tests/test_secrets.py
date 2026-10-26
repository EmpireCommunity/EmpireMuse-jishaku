"""Mascaramento de segredos: nada do que o Jishaku manda ao Discord pode levar o token nem os segredos do ambiente."""

import asyncio
import contextlib
import sys

import disnake
from disnake.ext import commands

from jishaku import Jishaku
from jishaku.exception_handling import send_traceback
from jishaku.flags import Flags
from jishaku.secrets import MASK, bot_secret_values, collect_secret_values, mask_secrets

TOKEN = "MTIzNDU2Nzg5MDEyMzQ1Njc4.abcdef.token-de-teste-1234567890"
SEGREDO_DO_AMBIENTE = "valor-secreto-do-ambiente-9876"
VARIAVEL_SECRETA = "MY_PASSWORD"


class CtxFalso:
    """Só o que os comandos usam para responder: sem servidor, então a saída longa vira arquivo."""

    guild = None

    def __init__(self):
        self.enviados = []
        self.author = disnake.Object(id=1)

    async def send(self, content=None, **kwargs):
        self.enviados.append((content, kwargs))

    def texto(self) -> str:
        partes = []
        for content, kwargs in self.enviados:
            partes.append(content or "")
            if kwargs.get("file") is not None:
                partes.append(kwargs["file"].fp.read().decode("utf-8"))
        return "\n".join(partes)


def rodar(principal):
    """O disnake 2.12 só cria o bot dentro de um laço do asyncio; roda a corrotina `principal(cog)`."""

    async def executar():
        bot = commands.Bot(command_prefix="!", intents=disnake.Intents.none())
        bot.http.token = TOKEN
        bot.config = {"MONGO": "mongodb://usuario:senha@host"}
        return await principal(Jishaku(bot=bot))

    return asyncio.run(executar())


@contextlib.contextmanager
def mascara_desligada():
    Flags.MASK_SECRETS = False
    try:
        yield
    finally:
        Flags.flag_map["MASK_SECRETS"].override = None


def test_so_valores_de_chaves_com_nome_de_segredo_e_tamanho_minimo():
    valores = collect_secret_values(
        {"BOT_TOKEN": "abcdef123", "PREFIX": "!!comando", "MONGO": "mongodb://u:p@h", "API_KEY": "curta", "SENHA": 12345}
    )
    assert valores == {"abcdef123", "mongodb://u:p@h"}


def test_mascara_do_mais_longo_para_o_mais_curto():
    assert mask_secrets("a segredo-longo b segredo", ["segredo", "segredo-longo"]) == f"a {MASK} b {MASK}"


def test_segredos_do_bot_incluem_token_ambiente_e_config(monkeypatch):
    monkeypatch.setenv(VARIAVEL_SECRETA, SEGREDO_DO_AMBIENTE)

    async def principal(cog):
        return bot_secret_values(cog.bot)

    assert {TOKEN, SEGREDO_DO_AMBIENTE, "mongodb://usuario:senha@host"} <= rodar(principal)


def test_resultado_curto_e_longo_do_jsk_py_saem_sem_o_token(monkeypatch):
    monkeypatch.setenv(VARIAVEL_SECRETA, SEGREDO_DO_AMBIENTE)
    ctx = CtxFalso()

    async def principal(cog):
        await cog.jsk_python_result_handling(ctx, f"curto {TOKEN} {SEGREDO_DO_AMBIENTE}")
        await cog.jsk_python_result_handling(ctx, ("x" * 3000) + f" {TOKEN} " + ("y" * 100))

    rodar(principal)

    enviado = ctx.texto()
    assert TOKEN not in enviado and SEGREDO_DO_AMBIENTE not in enviado
    assert enviado.count(MASK) == 3


def test_token_none_nao_derruba_o_comando():
    ctx = CtxFalso()

    async def principal(cog):
        cog.bot.http.token = None
        await cog.jsk_python_result_handling(ctx, "resultado qualquer")

    rodar(principal)
    assert ctx.texto() == "resultado qualquer"


def test_mascara_pode_ser_desligada():
    ctx = CtxFalso()

    async def principal(cog):
        await cog.jsk_python_result_handling(ctx, f"token {TOKEN}")

    with mascara_desligada():
        rodar(principal)

    assert TOKEN in ctx.texto()


def test_traceback_sai_mascarado():
    class Destino:
        def __init__(self):
            self.paginas = []

        async def send(self, content):
            self.paginas.append(content)

    destino = Destino()

    async def principal(cog):
        try:
            raise RuntimeError(f"falhou com {TOKEN}")
        except RuntimeError:
            await send_traceback(destino, 0, *sys.exc_info(), mask=cog.mask)

    rodar(principal)

    saida = "\n".join(destino.paginas)
    assert TOKEN not in saida and MASK in saida


def test_conteudo_de_arquivo_sai_mascarado_e_binario_fica_como_esta():
    async def principal(cog):
        assert TOKEN.encode() not in cog.mask_bytes(f"TOKEN={TOKEN}\n".encode())
        assert cog.mask_bytes(b"\xff\xfe binario") == b"\xff\xfe binario"

    rodar(principal)
