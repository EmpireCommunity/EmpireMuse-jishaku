"""Comando raiz do `jsk`: tamanhos legíveis."""

import pytest

from jishaku.features.root_command import natural_size


@pytest.mark.parametrize(
    ("bytes_", "texto"),
    [(0, "0 B"), (1, "1.00 B"), (1023, "1023.00 B"), (1024, "1.00 KiB"), (12345678, "11.77 MiB"), (1024**9, "1024.00 YiB")],
)
def test_tamanho_legivel_sem_estourar_nos_extremos(bytes_, texto):
    assert natural_size(bytes_) == texto
