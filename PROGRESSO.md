# Progresso

## Etapa atual
**0 - Setup** (em andamento)

## Etapas concluídas
_nenhuma ainda_

## Decisões tomadas
- 2026-11-05: Estrutura de pastas: `src/market_brief/` (código), `data/` (snapshots JSON),
  `site/` (GitHub Pages), `tests/` (pytest).
- 2026-11-05: Segredos ficam em `.env` (local) e GitHub Secrets (CI); `.env.example` documenta os nomes.
- 2026-11-05: `requirements.txt` sem versões fixas por enquanto; fixar (pin) antes da etapa 9 (Actions)
  para o CI ser reprodutível.
- 2026-11-05: Repositório público (requisito do GitHub Pages gratuito).
- 2026-11-05: Branch principal `main` (padrão do GitHub e dos exemplos de Actions/Pages).

## Dúvidas pendentes
_nenhuma_
