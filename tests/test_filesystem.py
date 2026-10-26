"""`jsk curl`: a resposta é lida em pedaços e abandonada se passar do limite, em vez de ir inteira para a memória."""

import asyncio

from jishaku.features.filesystem import read_limited


class RespostaFalsa:
    def __init__(self, pedacos):
        self.content = self
        self.lidos = 0
        self._pedacos = pedacos

    async def iter_chunked(self, tamanho):
        for pedaco in self._pedacos:
            self.lidos += len(pedaco)
            yield pedaco


def ler(pedacos, limite):
    resposta = RespostaFalsa(pedacos)
    return asyncio.run(read_limited(resposta, limite)), resposta


def test_resposta_dentro_do_limite_volta_inteira():
    dados, _ = ler([b"ab", b"cd"], 4)
    assert dados == b"abcd"


def test_resposta_acima_do_limite_e_abandonada_sem_ler_o_resto():
    dados, resposta = ler([b"abc", b"def", b"ghi", b"jkl"], 4)
    assert dados is None
    assert resposta.lidos == 6  # parou no segundo pedaço, os demais nem foram lidos


def test_resposta_vazia():
    assert ler([], 10)[0] == b""
