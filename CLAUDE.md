# CLAUDE.md

## Projeto

**image-promotion-gitops** - Demo para palestra sobre promoção de imagens Docker entre ambientes usando GitOps, Argo CD e Kargo.

**Apresentação:** 16/01/2026 às 19:00 (Meetup, 1h30min)

## Stack

- **Backend:** FastAPI (Python 3.11) + SQLAlchemy + Alembic + JWT
- **Frontend:** React 19 + Vite + TypeScript + Tailwind + Zustand
- **Database:** PostgreSQL 16
- **Infra:** Minikube + Argo CD + Kargo + Helm + Kustomize
- **CI:** GitHub Actions

## Estrutura

```
apps/backend/    → API REST com auth JWT e RBAC
apps/frontend/   → Interface React (tema Catppuccin)
k8s/             → Manifests Kubernetes
helm/            → Helm charts
gitops/          → Argo CD + Kargo configs
```

## Convenções

- Backend: Poetry para deps, Alembic para migrations
- Frontend: npm, componentes em `src/features/`
- Commits: mensagens em inglês, descritivas
- Código: comentários em português quando necessário

## Comandos úteis

```bash
# Rodar ambiente local (na raiz)
docker compose up -d

# Backend dev (em apps/backend/)
source .venv/bin/activate
PYTHONPATH=src uvicorn api.main:app --reload

# Frontend dev (em apps/frontend/)
npm run dev

# Migrations
cd apps/backend && source .venv/bin/activate
alembic upgrade head
```

## Status atual

**Concluído:**
- Backend (CRUD + JWT + RBAC)
- Frontend (gestão de usuários)
- Dockerfiles + docker-compose.yaml
- Alembic migrations

**Pendente:**
- GitHub Actions (CI)
- Helm charts
- Kustomize overlays
- Argo CD + Kargo setup
- Branches de demo
- Slides + Runbook

## Documentação completa

Para detalhes sobre arquitetura, runbook da apresentação, cronograma e plano de contingência, consulte `PROJECT.md`.
