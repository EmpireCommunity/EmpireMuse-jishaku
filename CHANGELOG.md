# Changelog

Todas as mudanças relevantes deste fork ficam aqui. O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e as versões seguem o [PEP 440](https://peps.python.org/pep-0440/) (`2.6.6.post1` = base 2.6.6 do disnake-jishaku mais o sufixo do fork).

## [Não lançado]

## [2.6.6.post1] - 2026-10-25

Primeira versão do fork da EmpireCommunity, a partir do commit `14d2dbd51d61382c687af8d8655f54f41674c0eb` do zRitsu/jishaku.

### Adicionado

- Pacote `empiremuse-jishaku` (nome distinto dos do PyPI), versão lida de `jishaku/meta.py`, `pyproject.toml` no lugar do `setup.py`.
- CI com lint (ruff), testes em Python 3.10 a 3.13 e construção da wheel com instalação num ambiente limpo; workflow de release que publica a wheel e o `SHA256SUMS`.
- README em português, `CHANGELOG.md` e testes automatizados (o fork original não tinha nenhum).

### Alterado

- Branch padrão renomeada de `master` para `main`.
- Python mínimo 3.10 (era 3.8) e `disnake` entre 2.12 e 3.
- Removidos arquivos herdados que não se aplicam ao fork (`FUNDING.yml`, modelos de issue e de PR, arte do projeto original, `requirements/*.txt`, `.flake8`).
