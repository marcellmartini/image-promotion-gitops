# PROJECT.md - Image Promotion GitOps

## Visão Geral

**Nome do Projeto:** image-promotion-gitops
**Repositório:** `marcellmartini/image-promotion-gitops`
**Autor:** Marcell Martini
**Licença:** MIT

**Título da Palestra:** Promoção de Imagens Docker entre Ambientes com GitOps, Argo CD e Kargo

**Descrição:** Projeto demonstrativo para palestra sobre como mover com segurança e automação imagens Docker dos ambientes de desenvolvimento para homologação e produção, utilizando práticas de GitOps com Argo CD e Kargo.

---

## Informações do Evento

| Item | Detalhe |
|------|---------|
| **Data** | 16/01/2026 |
| **Horário** | 19:00 |
| **Duração** | 1h 30min |
| **Formato** | Meetup/Conferência |
| **Público** | Diversificado (iniciantes a avançados) |
| **Tipo de Demo** | Ao vivo |

---

## Contato do Autor

| Rede | Link |
|------|------|
| **Instagram** | https://www.instagram.com/marcellmartini/ |
| **LinkedIn** | https://www.linkedin.com/in/marcellmartini/ |

---

## Objetivos da Palestra

1. Ensinar práticas de GitOps usando Argo CD e Kargo
2. Demonstrar o pipeline completo: build → tag → push → promoção → deploy
3. Garantir visibilidade, rastreabilidade e consistência nas promoções de artefatos
4. Apresentar desafios comuns e como superá-los em contexto Kubernetes
5. Mostrar como equipes podem ter entregas mais rápidas com menos riscos operacionais

---

## Stack Tecnológica

### Aplicação

| Componente | Tecnologia | Observação |
|------------|------------|------------|
| **Frontend** | React + Vite | Interface de gestão de usuários com tema Catppuccin |
| **Backend** | FastAPI (Python) | API REST com autenticação JWT e RBAC |
| **Banco de Dados** | PostgreSQL | Rodando via docker-compose no host |

### Funcionalidades Implementadas

#### Backend
- **CRUD de Usuários:** Create, Read, Update, Delete completo
- **Autenticação JWT:** Login com tokens de acesso
- **RBAC:** Controle de acesso baseado em roles (admin/user)
- **Campo birth_date:** Data de nascimento no cadastro de usuários
- **Endpoint /stats:** Estatísticas do sistema
- **CORS:** Configurado para permitir acesso do frontend
- **Migrations:** Alembic configurado com migrations versionadas

#### Frontend
- **Tema Catppuccin:** Interface com design consistente
- **Gestão de Usuários:** Listagem, criação, edição e visualização
- **Autenticação:** Login com persistência de tokens no localStorage
- **Campo birth_date:** Input de data no formulário de usuários

### Infraestrutura

| Componente | Tecnologia | Versão |
|------------|------------|--------|
| **Orquestração** | Minikube | Latest |
| **GitOps CD** | Argo CD | stable (manifest install) |
| **Promoção** | Kargo | 1.8.4 |
| **Certificados** | cert-manager | v1.16.2 |
| **Templates** | Helm + Kustomize | Latest |
| **Registry** | Docker Hub | - |
| **CI** | GitHub Actions | - |

### Ferramentas de Apresentação

| Componente | Tecnologia | Observação |
|------------|------------|------------|
| **Slides** | Presenterm | Binário pré-compilado |
| **Terminal** | Kitty + tmux + sesh | Splits para código/terminal/logs |
| **Editor** | Neovim | - |

---

## Arquitetura do Projeto

### Estrutura de Diretórios (Atualizada)

```
image-promotion-gitops/
├── docker-compose.yaml               # Orquestra todos os serviços
├── PROJECT.md
├── README.md
├── LICENSE
├── .github/
│   └── workflows/
│       └── ci.yml
├── apps/
│   ├── frontend/
│   │   ├── src/
│   │   ├── Dockerfile                # Multi-stage: Node + Nginx
│   │   ├── nginx.conf                # Proxy API + SPA routing
│   │   ├── .dockerignore
│   │   ├── package.json
│   │   └── vite.config.ts
│   └── backend/
│       ├── alembic/                  # Migrations
│       ├── src/                      # Código fonte
│       ├── scripts/                  # Scripts auxiliares
│       ├── Dockerfile                # Multi-stage: Poetry
│       ├── entrypoint.sh             # Migrations + uvicorn
│       ├── .dockerignore
│       ├── compose.yaml              # PostgreSQL standalone
│       ├── pyproject.toml
│       └── poetry.lock
├── k8s/                              # Manifests Kubernetes
├── helm/                             # Helm charts
├── gitops/                           # Argo CD + Kargo
├── scripts/                          # Scripts de setup
├── presentation/                     # Slides
├── videos/                           # Backup videos
└── docs/                             # Documentação
```

Estrutura original (planejada):
```
image-promotion-gitops/
├── README.md
├── PROJECT.md
├── LICENSE
├── .github/
│   └── workflows/
│       └── ci.yml
├── apps/
│   ├── frontend/
│   │   ├── src/
│   │   ├── package.json
│   │   ├── vite.config.ts
│   │   └── Dockerfile
│   └── backend/
│       ├── alembic
│       │   └── .gitkeep
│       ├── compose.yaml
│       ├── .env-example
│       ├── .gitignore
│       ├── poetry.lock
│       ├── pyproject.toml
│       ├── scripts
│       └── src
│           ├── api
│           │   ├── dependencies.py
│           │   ├── __init__.py
│           │   ├── main.py
│           │   ├── __pycache__
│           │   ├── routes.py
│           │   └── schemas.py
│           ├── application
│           │   ├── __init__.py
│           │   ├── __pycache__
│           │   └── services
│           ├── domain
│           │   ├── builder
│           │   ├── exceptions.py
│           │   ├── __init__.py
│           │   ├── __pycache__
│           │   ├── storage
│           │   └── value_objects.py
│           ├── infrastructure
│           │   └── storage
│           └── main.py
├── database/
│   └── docker-compose.yml
├── k8s/
│   ├── base/
│   │   └── helm-output/
│   │       ├── frontend/
│   │       └── backend/
│   └── overlays/
│       ├── dev/
│       │   └── kustomization.yaml
│       ├── stg/
│       │   └── kustomization.yaml
│       └── prod/
│           └── kustomization.yaml
├── helm/
│   ├── frontend/
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   └── templates/
│   └── backend/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
├── gitops/
│   ├── argocd/
│   │   └── applications/
│   │       ├── dev.yaml
│   │       ├── stg.yaml
│   │       └── prod.yaml
│   └── kargo/
│       ├── project.yaml
│       ├── projectconfig.yaml
│       ├── warehouse.yaml
│       └── stages/
│           ├── dev.yaml
│           ├── stg.yaml
│           └── prod.yaml
├── scripts/
│   ├── setup-minikube.sh
│   ├── setup-argocd.sh
│   ├── setup-kargo.sh
│   ├── generate-helm-output.sh
│   └── demo-helpers.sh
├── presentation/
│   ├── slides.md
│   ├── images/
│   └── runbook.md
├── videos/
│   └── backup/
│       ├── 01-ci-pipeline.mp4
│       ├── 02-deploy-dev.mp4
│       ├── 03-promotion-stg.mp4
│       ├── 04-promotion-prod.mp4
│       └── 05-rollback.mp4
└── docs/
    ├── kubernetes.md
    ├── argocd.md
    ├── kargo.md
    ├── gitops.md
    ├── helm.md
    ├── kustomize.md
    └── helm-kustomize-pros-cons.md
```

### Estrutura de Ambientes (Namespaces)

```
minikube cluster
├── cert-manager (namespace)     # Certificados TLS
├── argocd (namespace)           # Argo CD controller + UI
├── kargo (namespace)            # Kargo controller + UI
├── image-promotion (namespace)  # Kargo Project (Warehouse, Stages)
├── dev (namespace)
│   ├── frontend
│   └── backend
├── stg (namespace)
│   ├── frontend
│   └── backend
└── prod (namespace)
    ├── frontend
    └── backend
```

### Conexão com PostgreSQL

O PostgreSQL roda fora do cluster via docker-compose. A conexão é feita usando nip.io:

```
pg.192.168.x.x.nip.io → PostgreSQL no host
```

---

## Ambiente de Desenvolvimento Local (Docker)

### Arquivos Docker

| Arquivo | Descrição |
|---------|-----------|
| `docker-compose.yaml` | Orquestra todos os serviços (postgres, backend, frontend) |
| `apps/backend/Dockerfile` | Multi-stage build com Poetry, inclui alembic |
| `apps/backend/entrypoint.sh` | Executa migrations e inicia uvicorn |
| `apps/frontend/Dockerfile` | Multi-stage build Node + Nginx |
| `apps/frontend/nginx.conf` | Proxy para API + SPA routing |

### Comandos

```bash
# Na raiz do projeto (/image-promotion-gitops)

# Iniciar todos os serviços
docker compose up -d

# Ver logs (todos)
docker compose logs -f

# Ver logs (específico)
docker compose logs -f backend

# Ver status
docker compose ps

# Rebuild após mudanças
docker compose up -d --build

# Parar tudo
docker compose down

# Parar e remover volumes (reset completo)
docker compose down -v
```

### URLs Locais

| Serviço | URL |
|---------|-----|
| **Frontend** | http://localhost:3000 |
| **Backend API** | http://localhost:8000 |
| **Swagger Docs** | http://localhost:8000/docs |
| **PostgreSQL** | localhost:5432 |

### Variáveis de Ambiente

| Variável | Descrição | Default |
|----------|-----------|---------|
| `DATABASE_URL` | URL de conexão PostgreSQL | `postgresql://postgres:postgres@postgres:5432/users_db` |
| `JWT_SECRET_KEY` | Chave secreta para tokens JWT | `super-secret-key-for-dev` |

### Fluxo de Inicialização

1. PostgreSQL inicia e aguarda healthcheck
2. Backend aguarda PostgreSQL estar healthy
3. Backend executa `alembic upgrade head` (migrations)
4. Backend inicia uvicorn na porta 8000
5. Frontend (nginx) inicia e faz proxy de `/api/` para backend

### Criar Primeiro Usuário Admin

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Admin","email":"admin@example.com","password":"admin123","role":"admin"}'
```

### Tamanho das Imagens

| Imagem | Tamanho |
|--------|---------|
| `image-promotion-backend:local` | ~295 MB |
| `image-promotion-frontend:local` | ~63 MB |

---

## Estrutura de Branches

```
main (produção)
├── feature/create-user    # Já implementado na main inicialmente
├── feature/update-user    # Funcionalidade de atualização
├── feature/delete-user    # Funcionalidade de remoção
├── feature/error          # Branch para demonstrar rollback automático
└── feature/fix            # Branch que corrige o error
```

### Propósito de Cada Branch

| Branch | Propósito na Demo |
|--------|-------------------|
| `main` | Código estável, base inicial com create-user |
| `feature/update-user` | Demonstrar nova feature sendo promovida |
| `feature/delete-user` | Segunda feature para demonstrar fluxo |
| `feature/error` | Código com erro intencional para demonstrar rollback |
| `feature/fix` | Correção do erro, demonstra recovery |

### Regras de Commits

**OBRIGATÓRIO:** Cada commit deve conter apenas UMA feature/componente.

```bash
# CORRETO - commits separados:
git add helm/ && git commit -m "feat(helm): add Helm charts"
git add k8s/ && git commit -m "feat(kustomize): add overlays"
git add gitops/argocd/ && git commit -m "feat(argocd): add Applications"

# ERRADO - tudo junto:
git add . && git commit -m "feat: add all infrastructure"
```

**Motivo:** Facilita revisão de PRs, rollback granular e histórico limpo.

---

## Pipeline CI (GitHub Actions)

### Trigger

- **PR aberta/atualizada:** Executa validações (sem push de imagem)
- **Merge para main:** Executa validações + build + push para Docker Hub

### Etapas do Pipeline

```yaml
1. pyright      # Type checking
2. pylint       # Linting
3. black        # Formatação de código
4. snyk         # Análise de segurança
5. test         # Testes automatizados
6. build        # Build da imagem Docker
7. push         # Push para Docker Hub (apenas no merge)
```

### Estratégia de Tags

As tags das imagens são baseadas no hash do commit de merge:

```
marcellmartini/image-promotion-backend:<commit-sha>
marcellmartini/image-promotion-frontend:<commit-sha>
```

---

## Pipeline CD (Argo CD + Kargo)

### Fluxo de Promoção

```
┌─────────────────────────────────────────────────────────────────┐
│                      GitHub Actions (CI)                         │
│  PR → pyright → pylint → black → snyk → test → build → push     │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Kargo Warehouse                               │
│              Detecta nova imagem no Docker Hub                   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DEV (Automático)                            │
│         Kargo promove automaticamente para dev                   │
│         Argo CD sincroniza o namespace dev                       │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼ (Aprovação QA)
┌─────────────────────────────────────────────────────────────────┐
│                      STG (Aprovação QA)                          │
│         QA aprova promoção no Kargo                              │
│         Argo CD sincroniza o namespace stg                       │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼ (Aprovação PO)
┌─────────────────────────────────────────────────────────────────┐
│                     PROD (Aprovação PO)                          │
│         PO aprova promoção no Kargo                              │
│         Argo CD sincroniza o namespace prod                      │
└─────────────────────────────────────────────────────────────────┘
```

### Política de Aprovação

| Ambiente | Aprovação | Responsável |
|----------|-----------|-------------|
| **dev** | Automática | - |
| **stg** | Manual | QA |
| **prod** | Manual | PO |

### Rollback Automático

- Configurado health checks no Argo CD
- Em caso de falha de chamada/health check, rollback automático
- Branch `feature/error` demonstra esse comportamento
- Branch `feature/fix` demonstra a correção

---

## Helm + Kustomize: Estratégia

### Motivação

Usar Helm para templating e Kustomize para customizações por ambiente.

### Fluxo de Geração

```bash
# 1. Gera output do Helm
helm template frontend ./helm/frontend > k8s/base/helm-output/frontend/all.yaml
helm template backend ./helm/backend > k8s/base/helm-output/backend/all.yaml

# 2. Kustomize aplica overlays por ambiente
kubectl kustomize k8s/overlays/dev
kubectl kustomize k8s/overlays/stg
kubectl kustomize k8s/overlays/prod
```

### Prós e Contras (Helm + Kustomize)

#### Prós

1. **Separação de responsabilidades:** Helm gerencia complexidade, Kustomize gerencia ambientes
2. **GitOps-friendly:** Manifests renderizados são versionados no Git
3. **Auditabilidade:** Fácil ver exatamente o que será aplicado
4. **Flexibilidade:** Patches específicos por ambiente sem alterar templates
5. **Reprodutibilidade:** Mesmo output sempre, sem surpresas de versão de chart

#### Contras

1. **Complexidade adicional:** Duas ferramentas para aprender
2. **Processo de build:** Necessário regenerar helm-output quando chart muda
3. **Duplicação potencial:** Manifests renderizados ocupam espaço no repo
4. **Manutenção:** Atualização de charts requer regeneração manual

---

## Documentação Técnica (docs/)

Cada arquivo na pasta `docs/` conterá explicação detalhada sobre o tema:

| Arquivo | Conteúdo |
|---------|----------|
| `kubernetes.md` | Conceitos básicos de K8s, namespaces, deployments, services |
| `argocd.md` | O que é Argo CD, conceitos, instalação, Applications |
| `kargo.md` | O que é Kargo, Projects, Warehouses, Stages, Promotions |
| `gitops.md` | Princípios de GitOps, benefícios, práticas recomendadas |
| `helm.md` | O que é Helm, Charts, Values, Templates |
| `kustomize.md` | O que é Kustomize, bases, overlays, patches |
| `helm-kustomize-pros-cons.md` | Análise detalhada da combinação Helm+Kustomize |

---

## Runbook da Apresentação

### Estrutura da Palestra (1h 30min)

| Tempo | Duração | Tópico |
|-------|---------|--------|
| 00:00 | 10min | Introdução e contexto do problema |
| 00:10 | 10min | Conceitos: Kubernetes, GitOps |
| 00:20 | 10min | Conceitos: Helm, Kustomize e a combinação |
| 00:30 | 10min | Conceitos: Argo CD |
| 00:40 | 10min | Conceitos: Kargo |
| 00:50 | 05min | Arquitetura do projeto demo |
| 00:55 | 10min | Demo: CI Pipeline (PR → merge → build) |
| 01:05 | 05min | Demo: Deploy automático em DEV |
| 01:10 | 05min | Demo: Promoção para STG (aprovação QA) |
| 01:15 | 05min | Demo: Promoção para PROD (aprovação PO) |
| 01:20 | 05min | Demo: Rollback automático |
| 01:25 | 05min | Conclusão, Q&A e redes sociais |

### Passos da Demo ao Vivo

#### Parte 1: CI Pipeline

```bash
# 1. Mostrar código atual na main
git log --oneline -5

# 2. Criar PR da feature/update-user
gh pr create --base main --head feature/update-user

# 3. Mostrar GitHub Actions executando
# (split no terminal: código | actions | logs)

# 4. Aprovar e fazer merge da PR
gh pr merge --merge

# 5. Mostrar build e push da imagem
# Tag: <commit-sha>
```

#### Parte 2: Deploy em DEV (Automático)

```bash
# 1. Mostrar Kargo detectando nova imagem
kubectl get freight -n image-promotion

# 2. Mostrar promoção automática para dev
kubectl get promotions -n image-promotion

# 3. Verificar Argo CD sincronizando
argocd app get dev-app

# 4. Verificar pods no namespace dev
kubectl get pods -n dev

# 5. Testar aplicação em dev
curl http://dev.app.192.168.x.x.nip.io/api/users
```

#### Parte 3: Promoção para STG (Aprovação QA)

```bash
# 1. Mostrar stage aguardando aprovação
kubectl get stages -n image-promotion

# 2. Aprovar promoção via UI ou CLI (simulando QA)
# Via UI: https://localhost:3000 → image-promotion → stg → Promote
# Via CLI:
kargo promote --project image-promotion --stage stg --freight <freight-id>

# 3. Mostrar Argo CD sincronizando stg
argocd app get stg-app

# 4. Verificar aplicação em stg
curl http://stg.app.192.168.x.x.nip.io/api/users
```

#### Parte 4: Promoção para PROD (Aprovação PO)

```bash
# 1. Aprovar promoção (simulando PO)
kargo promote --project image-promotion --stage prod --freight <freight-id>

# 2. Mostrar Argo CD sincronizando prod
argocd app get prod-app

# 3. Verificar aplicação em prod
curl http://prod.app.192.168.x.x.nip.io/api/users
```

#### Parte 5: Demonstrar Rollback

```bash
# 1. Fazer merge do branch feature/error
gh pr create --base main --head feature/error
gh pr merge --squash

# 2. Mostrar CI passando (erro é em runtime)

# 3. Mostrar deploy em dev falhando
kubectl get pods -n dev
kubectl logs -n dev <pod-com-erro>

# 4. Mostrar Argo CD detectando falha
argocd app get dev-app

# 5. Mostrar rollback automático
kubectl get replicasets -n dev

# 6. Fazer merge do fix
gh pr create --base main --head feature/fix
gh pr merge --squash

# 7. Mostrar deploy bem-sucedido
kubectl get pods -n dev
```

---

## Plano de Contingência

### Vídeos de Backup

Em caso de falha durante a demo ao vivo, usar vídeos pré-gravados:

| Cenário | Vídeo |
|---------|-------|
| CI não executa | `videos/backup/01-ci-pipeline.mp4` |
| Deploy dev falha | `videos/backup/02-deploy-dev.mp4` |
| Promoção stg falha | `videos/backup/03-promotion-stg.mp4` |
| Promoção prod falha | `videos/backup/04-promotion-prod.mp4` |
| Rollback não funciona | `videos/backup/05-rollback.mp4` |

### Checklist Pré-Apresentação

```markdown
- [ ] Minikube rodando com recursos suficientes
- [ ] PostgreSQL rodando via docker-compose
- [ ] Argo CD instalado e acessível
- [ ] Kargo instalado e configurado
- [ ] Imagens base já no Docker Hub
- [ ] Branches criadas e testadas
- [ ] GitHub Actions com secrets configurados
- [ ] Presenterm instalado e testado
- [ ] Kitty/tmux layout configurado
- [ ] Internet estável
- [ ] Vídeos de backup prontos
- [ ] Slides revisados
```

---

## Scripts de Automação

### setup-minikube.sh

```bash
#!/bin/bash
# Inicializa minikube com configurações adequadas
minikube start --cpus=4 --memory=4096 --driver=docker
minikube addons enable ingress
minikube addons enable metrics-server
# Cria namespaces dev, stg, prod
```

### setup-argocd.sh

```bash
#!/bin/bash
# Instala Argo CD no cluster via manifest oficial
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl wait --for=condition=Ready pods --all -n argocd --timeout=300s
# Aplica Applications (dev-app, stg-app, prod-app)
kubectl apply -f gitops/argocd/applications/
```

### setup-kargo.sh

```bash
#!/bin/bash
# Instala cert-manager (dependência do Kargo)
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.16.2/cert-manager.yaml
kubectl wait --for=condition=Available deployment --all -n cert-manager --timeout=300s

# Instala Kargo v1.8.4 via Helm
helm install kargo oci://ghcr.io/akuity/kargo-charts/kargo \
  --namespace kargo --create-namespace \
  --version 1.8.4 \
  --set api.adminAccount.passwordHash='...' \
  --set api.adminAccount.tokenSigningKey='...' \
  --wait

# Aplica configurações do projeto (Project cria o namespace automaticamente)
kubectl apply -f gitops/kargo/project.yaml
kubectl apply -f gitops/kargo/projectconfig.yaml
kubectl apply -f gitops/kargo/warehouse.yaml
kubectl apply -f gitops/kargo/stages/
```

### generate-helm-output.sh

```bash
#!/bin/bash
# Regenera manifests do Helm e valida com Kustomize
helm template backend ./helm/backend > k8s/base/helm-output/backend/all.yaml
helm template frontend ./helm/frontend > k8s/base/helm-output/frontend/all.yaml
kustomize build k8s/overlays/dev > /dev/null && echo "dev: OK"
kustomize build k8s/overlays/stg > /dev/null && echo "stg: OK"
kustomize build k8s/overlays/prod > /dev/null && echo "prod: OK"
```

---

## Apresentação (Presenterm)

### Instalação

```bash
# Download do binário (Linux)
wget https://github.com/mfontanini/presenterm/releases/latest/download/presenterm-x86_64-unknown-linux-gnu.tar.gz
tar -xzf presenterm-x86_64-unknown-linux-gnu.tar.gz
sudo mv presenterm /usr/local/bin/

# Verificar instalação
presenterm --version
```

### Execução

```bash
cd presentation/
presenterm slides.md
```

### Estrutura dos Slides

Os slides estão em `presentation/slides.md` em formato Markdown compatível com Presenterm, incluindo:

- Syntax highlighting para código
- Imagens (compatível com Kitty)
- Transições suaves
- Execução de comandos inline (se necessário)

---

## Cronograma de Desenvolvimento

### Semana 1 (06/01 - 12/01)

- [x] Setup inicial do repositório
- [x] Backend FastAPI (CRUD usuários + JWT + RBAC)
- [x] Frontend React + Vite (tema Catppuccin)
- [x] Docker Compose para PostgreSQL
- [x] Alembic migrations configurado
- [x] Dockerfiles para frontend e backend
- [x] Docker Compose completo (postgres + backend + frontend)

### Semana 2 (13/01 - 15/01)

- [x] GitHub Actions (CI completo)
- [x] Helm charts (backend + frontend)
- [x] Kustomize overlays (dev, stg, prod)
- [x] Scripts de setup (minikube, argocd, kargo, generate-helm-output)
- [x] Configuração Argo CD (Applications)
- [x] Configuração Kargo (Project, ProjectConfig, Warehouse, Stages)
- [x] Kargo detectando imagens do Docker Hub (Freight criado)
- [x] GitHub PAT configurado para Kargo git-push
- [x] Estratégia de branches por ambiente implementada (env/dev, env/stg, env/prod)
- [x] Promoção automática para dev funcionando
- [ ] Branches de demonstração (feature/update-user, feature/error, feature/fix)
- [ ] Slides da apresentação
- [ ] Runbook final
- [ ] Gravação dos vídeos de backup
- [ ] Testes completos do fluxo (stg, prod)
- [ ] Documentação (docs/)

### Dia da Apresentação (16/01)

- [ ] Checklist pré-apresentação
- [ ] Setup do ambiente
- [ ] Apresentação às 19:00

---

## Status Atual (13/01/2026)

### Kargo Promotion - FUNCIONANDO ✅

O fluxo completo de promoção está funcionando:
- ✅ Warehouse detecta imagens no Docker Hub
- ✅ Freight é criado automaticamente
- ✅ GitHub PAT configurado no secret `github-creds`
- ✅ Promoção automática para dev funcionando
- ✅ Argo CD sincroniza automaticamente

### Próximos Passos

1. Testar promoção para stg (aprovação manual)
2. Testar promoção para prod (aprovação manual)
3. Criar branches de demo (feature/update-user, feature/error, feature/fix)
4. Criar slides e runbook

---

## Decisões Técnicas e Arquitetura

### Estratégia de Branches por Ambiente (Environment-Specific Branches)

**Data:** 13/01/2026
**Referência:** https://docs.kargo.io/user-guide/patterns/#storage-options

**Problema:** O branch `main` estava protegido no GitHub, impedindo push direto pelo Kargo.

**Solução adotada:** Usar branches específicos por ambiente, conforme recomendação dos mantenedores do Kargo (Opção 1 - "decidedly the maintainers' preferred approach").

**Branches criados (órfãos):**
- `env/dev` - Manifests renderizados para ambiente dev
- `env/stg` - Manifests renderizados para ambiente stg
- `env/prod` - Manifests renderizados para ambiente prod

**Arquivos modificados:**

1. **Kargo Stages** (`gitops/kargo/stages/*.yaml`):
   - `git-clone`: checkout do branch de ambiente + main
   - `git-clear`: limpa branch de ambiente
   - `kustomize-set-image`: atualiza tags das imagens
   - `kustomize-build`: renderiza manifests finais
   - `git-commit` + `git-push`: commit dos manifests renderizados

2. **Kargo Warehouse** (`gitops/kargo/warehouse.yaml`):
   - `allowTags: ^[a-f0-9]{8}$` - filtra apenas tags de commit hash (8 chars)

3. **Argo CD Applications** (`gitops/argocd/applications/*.yaml`):
   - `targetRevision: env/<ambiente>` para branches de ambiente
   - `path: .` - branch contém apenas manifests renderizados na raiz
   - Anotação `kargo.akuity.io/authorized-stage: image-promotion:<ambiente>`

4. **CI** (`.github/workflows/ci.yml`):
   - `git rev-parse --short=8` para gerar tag de 8 caracteres
   - Removida tag `latest`

**Fluxo resultante:**
```
1. git-clone      → checkout env/dev (output) + main (source)
2. git-clear      → limpa branch de ambiente
3. kustomize-set-image → atualiza tags das imagens
4. kustomize-build → renderiza manifests finais para ./out
5. git-commit     → commit dos manifests renderizados
6. git-push       → push para branch de ambiente
7. argocd-update  → sincroniza Argo CD
```

**Vantagens:**
- Branch `main` permanece protegido
- Isolamento entre ambientes (falhas não afetam outros)
- Clareza na separação código fonte vs estado de deployment
- Sem necessidade de merge entre branches (funcionam como storage)
- Auditoria facilitada do histórico de deployments

**Desvantagens:**
- 3 branches extras para gerenciar
- Pode parecer GitFlow (mas não é - sem merges)

### GitHub PAT Configuration

**Secret criado:**
```bash
kubectl create secret generic github-creds \
  --namespace=image-promotion \
  --from-literal=repoURL=https://github.com/marcellmartini/image-promotion-gitops.git \
  --from-literal=username=x-access-token \
  --from-literal=password=<GITHUB_PAT>

kubectl label secret github-creds -n image-promotion kargo.akuity.io/cred-type=git
```

**Requisitos do PAT:**
- Tipo: Classic ou Fine-grained
- Escopo: `repo` (Full control) para Classic
- Para Fine-grained: `Contents: Read and Write` no repositório específico

### Kargo Authorized Stage Annotation

Para permitir que o Kargo faça refresh nas Applications do Argo CD, é necessário adicionar a anotação:
```yaml
metadata:
  annotations:
    kargo.akuity.io/authorized-stage: <namespace>:<stage>
```

Exemplo: `kargo.akuity.io/authorized-stage: image-promotion:dev`

### Sync Policy por Ambiente

**Problema:** Ao criar branches `env/*` a partir da main, o Argo CD sincronizou automaticamente stg e prod porque os manifests já existiam.

**Solução:** Remover `syncPolicy.automated` de stg-app e prod-app.

| App | Sync Policy | Motivo |
|-----|-------------|--------|
| dev-app | automated | Promoção automática pelo Kargo |
| stg-app | manual | Aguarda promoção + sync via Kargo argocd-update |
| prod-app | manual | Aguarda promoção + sync via Kargo argocd-update |

O step `argocd-update` do Kargo força o sync após promoção bem-sucedida, então não é necessário auto-sync para stg e prod.

---

## Comandos Úteis para Troubleshooting

### Verificar status do Kargo
```bash
kubectl get warehouse,freight,stages,promotions -n image-promotion
```

### Recriar stage para forçar nova promoção
```bash
kubectl delete stage dev -n image-promotion
kubectl apply -f gitops/kargo/stages/dev.yaml
```

### Verificar logs de promoção
```bash
kubectl get promotions -n image-promotion -o yaml | grep -A 20 "status:"
```

### Verificar se branch foi atualizado
```bash
git fetch origin env/dev && git log origin/env/dev --oneline -3
```

### Verificar secret do GitHub
```bash
kubectl get secret github-creds -n image-promotion -o jsonpath='{.data}' | jq
```

---

## Requisitos do Sistema (para rodar a demo)

| Recurso | Mínimo | Recomendado |
|---------|--------|-------------|
| **CPU** | 4 cores | 6+ cores |
| **RAM** | 8 GB | 16 GB |
| **Disco** | 20 GB livres | 40 GB livres |
| **SO** | Linux (Ubuntu/Fedora) | - |

### Softwares Necessários

- Docker
- Minikube
- kubectl
- Helm
- kustomize
- GitHub CLI (gh)
- Presenterm
- Kitty Terminal
- tmux + sesh
- Neovim

---

## Entregáveis Finais

1. **Repositório GitHub** com todo o código fonte
2. **Apresentação** em slides (Presenterm)
3. **Documentação completa** em português
4. **Vídeos de backup** para contingência
5. **Runbook** passo-a-passo da demo
6. **Scripts de automação** para setup rápido

---

## Referências

- [Argo CD Documentation](https://argo-cd.readthedocs.io/)
- [Kargo Documentation](https://kargo.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Kustomize Documentation](https://kustomize.io/)
- [GitOps Principles](https://opengitops.dev/)
- [Presenterm](https://github.com/mfontanini/presenterm)
