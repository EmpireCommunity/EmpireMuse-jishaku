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

### Corrigido

- `jsk py` com `return` ou `del` quebrava no Python 3.14 (`ast.Str` e `ast.NameConstant` removidos); `jsk dis` quebrava no Python 3.13 (usava funções privadas do `dis`).
- Avisos de depreciação do Python 3.12+ (`datetime.utcnow`, `asyncio.get_event_loop`), que viram erro no 3.14.
- `jsk curl` lia a resposta inteira na memória; agora lê no máximo 8 MiB.
- `natural_size` falhava com zero e com valores acima de YiB; `jsk invite` usava o domínio antigo do Discord.

### Segurança

- Token e segredos do ambiente passam a ser mascarados em toda saída enviada ao Discord (resultado curto e longo do `jsk py`, `pyi`, `dis`, `sh`, `cat`, `curl`, `src`, tracebacks e erros de `load`/`unload`); antes só o resultado curto do `jsk py` era tratado. Desligue com `JISHAKU_MASK_SECRETS=false`.
- `jsk sh`, `git` e `pip` rodam com ambiente mínimo em vez de herdar o do bot (`JISHAKU_SHELL_ENV_ALLOW` libera nomes extras; `JISHAKU_SHELL_INHERIT_ENV=true` restaura o comportamento antigo).
- Novas travas opcionais na guarda dos comandos: `JISHAKU_OWNER_IDS` e `JISHAKU_DM_ONLY`.

### Alterado

- Branch padrão renomeada de `master` para `main`.
- Python mínimo 3.10 (era 3.8) e `disnake` entre 2.12 e 3.
- Removidos arquivos herdados que não se aplicam ao fork (`FUNDING.yml`, modelos de issue e de PR, arte do projeto original, `requirements/*.txt`, `.flake8`).
