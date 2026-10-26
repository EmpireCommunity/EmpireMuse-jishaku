# EmpireMuse-jishaku

Fork do [jishaku](https://github.com/scarletcafe/jishaku) para o **[disnake](https://github.com/DisnakeDev/disnake)**, mantido pela organização EmpireCommunity para uso no [EmpireMuse](https://github.com/EmpireCommunity/EmpireMuse).

O jishaku é uma extensão para quem desenvolve bots: executa e inspeciona código Python no próprio bot, roda comandos de shell, recarrega extensões, lê arquivos e mais, tudo por comandos do Discord. No EmpireMuse ele é **opcional e vem desligado** (`ENABLE_JISHAKU=false`); ligue só em desenvolvimento ou numa janela de manutenção, porque dá controle total do processo a quem for dono do bot.

## Origem e créditos

Este repositório descende de uma cadeia de forks, e cada elo mantém a autoria original (licença MIT, veja [`LICENSE`](LICENSE)):

| Elo | Contribuição |
| :--- | :--- |
| [scarletcafe/jishaku](https://github.com/scarletcafe/jishaku) | Projeto original (`discord.py`), de Devon (Gorialis) R e colaboradores. |
| [Kraots/jishaku](https://github.com/Kraots/jishaku) | Porte para o disnake (`disnake-jishaku`), base da versão 2.6.x. |
| [zRitsu/jishaku](https://github.com/zRitsu/jishaku) | Fork usado pelo [MuseHeart-MusicBot](https://github.com/zRitsu/MuseHeart-MusicBot): `importlib.metadata` no lugar de `pkg_resources` e suporte ao Python 3.14. |
| **EmpireCommunity/EmpireMuse-jishaku** | Este fork: correções de compatibilidade e de segurança, CI, wheel verificável. Veja o [`CHANGELOG.md`](CHANGELOG.md). |

O fork parte do commit `14d2dbd51d61382c687af8d8655f54f41674c0eb` do zRitsu, que está 29 commits à frente e 204 atrás do upstream. As mudanças do upstream (voltadas ao `discord.py`) **não** foram trazidas em bloco.

## Versão e nome

- Distribuição: **`empiremuse-jishaku`** (nome distinto de `jishaku` e `disnake-jishaku` do PyPI, para que nenhuma instalação por nome troque este pacote por outro).
- Pacote importável: **`jishaku`** (o mesmo do original; não instale os dois no mesmo ambiente).
- Versão PEP 440 `2.6.6.post1`: base 2.6.6 (Kraots) mais o sufixo `.post` do fork. A fonte única é `jishaku/meta.py`.

## Instalação

O fork **não é publicado no PyPI**. Cada release no GitHub traz a wheel e um `SHA256SUMS`; instale pela URL do asset conferindo o hash:

```bash
pip install --no-deps --require-hashes -r requirements-jishaku.txt
```

com um arquivo como

```text
empiremuse-jishaku @ https://github.com/EmpireCommunity/EmpireMuse-jishaku/releases/download/v2.6.6.post1/empiremuse_jishaku-2.6.6.post1-py3-none-any.whl \
    --hash=sha256:<valor do SHA256SUMS do release>
```

O `--no-deps` é de propósito no EmpireMuse, que já fixa `disnake`, `click`, `braceexpand` e `import-expression` no próprio lock com hash. Fora dele, o `pip` instala as dependências normalmente.

Carregue a extensão antes de iniciar o bot:

```python
bot.load_extension("jishaku")
```

Extras opcionais: `empiremuse-jishaku[voice]` (comandos de voz) e `empiremuse-jishaku[procinfo]` (uso de CPU e memória no `jsk`).

Requisitos: Python 3.10 ou superior; testado com `disnake` 2.12.2 em Python 3.10 a 3.14.

## Comandos

Todos ficam sob o grupo `jsk` (ou `jishaku`) e só respondem a donos do bot.

| Comando | O que faz |
| :--- | :--- |
| `jsk py <código>` / `jsk pyi` | Executa código Python (com `await` e `yield`) no contexto do bot; `pyi` mostra a inspeção do resultado. Variáveis disponíveis: `_ctx`, `_bot`, `_author`, `_channel`, `_guild`, `_message` e atalhos de `disnake.utils`. |
| `jsk retain on/off` | Mantém as variáveis entre execuções do `jsk py`. |
| `jsk dis <código>` | Mostra o bytecode do código, sem executá-lo. |
| `jsk sh <comando>` (e `git`, `pip`) | Roda um comando no shell do sistema, com a saída ao vivo; `jsk cancel` interrompe. |
| `jsk load` / `reload` / `unload` | Carrega, recarrega ou descarrega extensões (`jsk reload ~` recarrega todas). |
| `jsk cat <arquivo>` / `jsk curl <url>` | Lê um arquivo local ou o conteúdo de uma URL. |
| `jsk exec` / `debug` / `repeat` | Executa outro comando como outro usuário ou canal, com cronômetro e traceback, ou repetido. |
| `jsk permtrace <canal> <alvos…>` | Explica de onde vem cada permissão num canal. |
| `jsk rtt`, `jsk invite`, `jsk shutdown` | Latência até a API, link de convite do bot e desligamento ordenado. |
| `jsk voice …` | Entra, sai e toca áudio em canais de voz. |

## Configuração

As opções são variáveis de ambiente lidas na importação do `jishaku` (valores booleanos: `true`/`false`):

| Variável | Efeito |
| :--- | :--- |
| `JISHAKU_HIDE` | Esconde o grupo `jsk` da ajuda. |
| `JISHAKU_RETAIN` | Liga o modo de retenção de variáveis por padrão. |
| `JISHAKU_NO_UNDERSCORE` | Tira o prefixo `_` das variáveis (`ctx` em vez de `_ctx`). |
| `JISHAKU_FORCE_PAGINATOR` | Usa sempre o paginador, não a pré-visualização de arquivo do Discord. |
| `JISHAKU_NO_DM_TRACEBACK` | Envia tracebacks ao canal em vez de DM. |
| `JISHAKU_USE_BRAILLE_J` | Usa o "J" em braille no `jsk shutdown`. |
| `JISHAKU_EMBEDDED_JSK` / `JISHAKU_EMBEDDED_JSK_COLOUR` | Mostra o resumo do `jsk` num embed (cor em `0x…`, `#…`, `rgb(…)` ou nome de `disnake.Colour`). |
| `JISHAKU_PY_RES` | Com `false`, desliga o tratamento automático de resultados especiais (`Message`, `File`, `Embed`, paginadores) no `jsk py`. |
| `JISHAKU_MASK_SECRETS` | Padrão `true`: troca por `[secret omitted]` o token do bot e os valores de variáveis de ambiente (e de `bot.config`) cujo nome sugere segredo (`TOKEN`, `SECRET`, `PASS`, `KEY`, `MONGO`, `WEBHOOK`…) em tudo que o jishaku envia ao Discord. |
| `JISHAKU_SHELL_ENV_ALLOW` | Nomes de variáveis (separados por vírgula) que o `jsk sh` recebe além da lista mínima (`PATH`, `HOME`, `LANG`, `LC_ALL`, `TZ`, `USER`, `LOGNAME`, `GIT_DIR`; no Windows também `SystemRoot`, `COMSPEC`…). |
| `JISHAKU_SHELL_INHERIT_ENV` | Com `true`, o `jsk sh` herda o ambiente inteiro do processo (comportamento antigo; **evite**). |
| `JISHAKU_OWNER_IDS` | IDs separados por vírgula. Quando definido, além de ser dono do bot o autor precisa estar na lista (deixa de fora, por exemplo, a equipe do aplicativo no Discord). Lista inválida nega todo mundo. |
| `JISHAKU_DM_ONLY` | Com `true`, os comandos só funcionam em mensagem direta. |

## Desenvolvimento

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,procinfo]"
ruff check .
python -m pytest
python -m build --wheel
```

O CI (`.github/workflows/ci.yml`) roda lint, a suíte em Python 3.10–3.14 e a construção da wheel com instalação num ambiente limpo. Uma tag `vX.Y.Z[.postN]` em `main` dispara o `release.yml`, que publica a wheel e o `SHA256SUMS`. Mudanças seguem [Conventional Commits](https://www.conventionalcommits.org/pt-br/) e entram no [`CHANGELOG.md`](CHANGELOG.md).

Problemas de segurança: siga a [política do EmpireMuse](https://github.com/EmpireCommunity/EmpireMuse/blob/main/.github/SECURITY.md); não abra issue pública com detalhes exploráveis.

## Licença

MIT, com os avisos de direitos autorais de todos os autores acima preservados em [`LICENSE`](LICENSE).
