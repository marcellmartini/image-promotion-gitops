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

## Git Workflow

**IMPORTANTE:** Todos os commits devem ser mergeados na main via Pull Request.

1. Criar branch: `git checkout -b feature/<nome>`
2. **SEPARAR COMMITS POR FEATURE** (NUNCA fazer um commit único com várias features)
3. Push: `git push -u origin feature/<nome>`
4. Criar PR: `gh pr create`
5. Merge via GitHub (squash ou merge commit)

### Regra de Commits

**OBRIGATÓRIO:** Cada commit deve conter apenas UMA feature/componente. Exemplos:

```bash
# CORRETO - commits separados:
git add helm/ && git commit -m "feat(helm): add Helm charts"
git add k8s/ && git commit -m "feat(kustomize): add overlays"
git add gitops/argocd/ && git commit -m "feat(argocd): add Applications"
git add gitops/kargo/ && git commit -m "feat(kargo): add Warehouse and Stages"

# ERRADO - tudo junto:
git add . && git commit -m "feat: add all GitOps infrastructure"
```

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
- GitHub Actions (CI)
- Helm charts (backend + frontend)
- Kustomize overlays (dev, stg, prod)
- Argo CD Applications
- Kargo setup (Project, Warehouse, Stages)
- Scripts de setup (minikube, argocd, kargo)

**Pendente:**
- Branches de demo (feature/update-user, feature/error, feature/fix)
- Slides + Runbook
- Vídeos de backup (opcional)

## Estrutura GitOps

```
helm/
├── backend/     → Chart com Deployment, Service, Secret
└── frontend/    → Chart com Deployment, Service, ConfigMap (nginx)

k8s/
├── base/        → helm-output gerado
└── overlays/
    ├── dev/     → 1 replica
    ├── stg/     → 2 replicas
    └── prod/    → 3 replicas

gitops/
├── argocd/applications/   → dev-app, stg-app, prod-app
└── kargo/
    ├── project.yaml       → Cria namespace image-promotion
    ├── projectconfig.yaml → Políticas (dev=auto, stg/prod=manual)
    ├── warehouse.yaml     → Monitora Docker Hub
    └── stages/            → dev → stg → prod
```

## Comandos de Setup (Minikube)

```bash
./scripts/setup-minikube.sh   # Cluster + namespaces
./scripts/setup-argocd.sh     # Argo CD + Applications
./scripts/setup-kargo.sh      # cert-manager + Kargo + configs
```

## Acessos

```bash
# Argo CD (terminal 1)
kubectl port-forward svc/argocd-server -n argocd 8080:443
# https://localhost:8080 - admin / (kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)

# Kargo (terminal 2)
kubectl port-forward svc/kargo-api -n kargo 3000:443
# https://localhost:3000 - admin / admin
```

## Regenerar Helm Output

```bash
./scripts/generate-helm-output.sh
```

## Documentação completa

Para detalhes sobre arquitetura, runbook da apresentação, cronograma e plano de contingência, consulte `PROJECT.md`.
