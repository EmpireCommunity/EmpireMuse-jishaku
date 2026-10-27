"""O REPL do `jsk py`: o executor assíncrono e as reescritas de `return` e `del` (sem APIs removidas do `ast`)."""

import asyncio
import warnings

from jishaku.functools import AsyncSender
from jishaku.repl import AsyncCodeExecutor, Scope


def run(code: str, scope: Scope = None) -> list:
    async def collect() -> list:
        return [result async for _, result in AsyncSender(AsyncCodeExecutor(code, scope or Scope()))]

    return asyncio.run(collect())


def test_expressao_final_vira_resultado():
    assert run("1 + 1") == [2]


def test_return_com_valor_vira_yield():
    assert run("x = 5\nreturn x * 2") == [10]


def test_del_de_variavel_do_escopo_retido():
    scope = Scope()
    run("y = 3", scope)
    assert "y" in scope.globals
    assert run("del y\n7", scope) == [7]
    assert "y" not in scope.globals


def test_yield_e_await():
    assert run("yield 1\nyield 2") == [1, 2]
    assert run("await asyncio.sleep(0)\n'ok'") == ["ok"]


def test_reescritas_nao_usam_apis_do_ast_removidas_no_python_314():
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        assert run("return 1") == [1]
        assert run("z = 2\ndel z\n3") == [3]


def test_executor_pode_ser_criado_fora_de_uma_corrotina():
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        executor = AsyncCodeExecutor("1")
    assert executor.loop is None

    async def collect():
        return [result async for _, result in AsyncSender(executor)]

    assert asyncio.run(collect()) == [1]


def test_import_expression_resolve_modulo_com_ponto_de_exclamacao():
    """`modulo!.attr` importa o módulo na hora (regressão do import_expression no Python 3.14)."""
    import os

    assert run("os!.getcwd()") == [os.getcwd()]
    assert run("x = json!.dumps({'a': 1})\nx") == ['{"a": 1}']
