# Progresso

## Etapa atual
**1 - Coleta do Banco Central (SGS)** (a iniciar)

## Etapas concluídas
- [x] 0 - Setup: repositório `beapama/market-brief` (público, branch `main`), venv,
  estrutura de pastas, `.env`/`.gitignore`. Commit `c311b3b`.

## Decisões tomadas
- 2026-11-05: Estrutura de pastas: `src/market_brief/` (código), `data/` (snapshots JSON),
  `site/` (GitHub Pages), `tests/` (pytest).
- 2026-11-05: Segredos ficam em `.env` (local) e GitHub Secrets (CI); `.env.example` documenta os nomes.
- 2026-11-05: `requirements.txt` sem versões fixas por enquanto; fixar (pin) antes da etapa 9 (Actions)
  para o CI ser reprodutível.
- 2026-11-05: Repositório público (requisito do GitHub Pages gratuito).
- 2026-11-05: `CLAUDE.md` fora do repositório (no `.gitignore`).
- 2026-11-05: Branch principal `main` (padrão do GitHub e dos exemplos de Actions/Pages).
- 2026-11-05: Idioma: código, docstrings, comentários e commits em **inglês**; termos do domínio
  mantêm o nome original (selic, ipca, ptax, focus); conteúdo para o usuário (briefing, Telegram,
  site) em **português**; README em inglês com resumo em PT (confirmar na etapa 11).
- 2026-11-06: Ruff para formatação e lint, configurado no `pyproject.toml` (linha de 100 caracteres;
  regras E, W, F, I, B, UP).

- 2026-11-06: Docstrings ficam no código (o que a função faz); contexto e decisões ficam em
  `docs/<módulo>.md` (o porquê), linkados no README.

## Dúvidas pendentes
- Selic (série 432) vem com datas futuras: como apresentar no briefing e nos gráficos?
- Criar `.gitattributes` (`* text=auto eol=lf`) para normalizar fim de linha? (proposto, aguardando decisão)
