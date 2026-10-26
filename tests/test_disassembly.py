"""`jsk dis`: o desassemblador usa só a API pública do `dis` e funciona em todas as versões do Python."""

from jishaku.repl.disassembly import disassemble


def test_desassembla_codigo_assincrono():
    linhas = list(disassemble("a = 1\nawait asyncio.sleep(0)"))
    texto = "\n".join(linhas)
    assert linhas and "asyncio" in texto and "STORE_FAST" in texto


def test_expressao_final_vira_retorno():
    assert "RETURN" in "\n".join(disassemble("1 + 1"))
