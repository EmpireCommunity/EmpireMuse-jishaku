"""Versão do fork: PEP 440 válida e `version_info` em sincronia com o texto (o pyproject lê `__version__`)."""

import re

from jishaku import meta

PEP_440_POST = re.compile(r"^\d+\.\d+\.\d+\.post\d+$")


def test_versao_e_pep_440_com_sufixo_post():
    assert PEP_440_POST.match(meta.__version__)


def test_version_info_acompanha_a_versao_em_texto():
    info = meta.version_info
    assert meta.__version__ == f"{info.major}.{info.minor}.{info.micro}.{info.releaselevel}{info.serial}"
