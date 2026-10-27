# -*- coding: utf-8 -*-

"""
jishaku.meta
~~~~~~~~~~~~

Meta information about jishaku.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""
from collections import namedtuple

__all__ = (
    '__author__',
    '__copyright__',
    '__docformat__',
    '__license__',
    '__title__',
    '__version__',
    'version_info'
)

# pylint: disable=invalid-name
VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
version_info = VersionInfo(major=2, minor=6, micro=6, releaselevel='post', serial=3)

__author__ = 'Gorialis, Kraots, zRitsu, EmpireCommunity'
__copyright__ = 'Copyright 2021 Devon (Gorialis) R'
__docformat__ = 'restructuredtext en'
__license__ = 'MIT'
__title__ = 'jishaku'

# Versão PEP 440 do fork: 2.6.6 (base do disnake-jishaku do Kraots) + .post2. Literal de propósito: o setuptools
# lê este valor sem importar o pacote (o import exigiria o disnake instalado). Mantenha `version_info` em sincronia;
# tests/test_meta.py confere.
__version__ = '2.6.6.post3'
