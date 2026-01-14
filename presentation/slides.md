---
title: Promocao de Imagens Docker entre Ambientes
sub_title: GitOps com Argo CD e Kargo
author: Marcell Martini
---


# Bem-vindos!

## Promocao de Imagens Docker entre Ambientes
### GitOps com Argo CD e Kargo

**Marcell Martini**

<!-- pause -->

- Instagram: @marcellmartini
- LinkedIn: /in/marcellmartini
- GitHub: github.com/marcellmartini

<!-- end_slide -->

# Agenda

| Tempo | Topico |
|-------|--------|
| 10min | Introducao e Contexto |
| 10min | Kubernetes e GitOps |
| 10min | Helm e Kustomize |
| 10min | Argo CD |
| 10min | Kargo |
| 05min | Arquitetura do Projeto |
| 30min | Demo ao Vivo |
| 05min | Conclusao e Q&A |

<!-- end_slide -->

# O Problema

## Como voce faz deploy hoje?

<!-- pause -->

- SSH no servidor e `git pull`?
- Scripts bash que "funcionam"?
- Jenkins com 47 plugins?
- "Roda na minha maquina!"

<!-- pause -->

## Spoiler: existe um jeito melhor

<!-- end_slide -->

# O Cenario Real

```
┌─────────────────────────────────────────────────┐
│                   DESENVOLVIMENTO               │
│  "Funcionou no meu PC, sobe pra producao!"      │
└─────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│                   HOMOLOGACAO                   │
│  "Ops, esqueci de atualizar a variavel..."      │
└─────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│                    PRODUCAO                     │
│  "Por que ta diferente do staging?!"            │
└─────────────────────────────────────────────────┘
```

<!-- end_slide -->

# Os Desafios

## Promover artefatos entre ambientes e GARANTIR:

<!-- pause -->

- **Consistencia**: Mesma imagem em todos os ambientes

<!-- pause -->

- **Rastreabilidade**: Saber exatamente o que esta rodando

<!-- pause -->

- **Automacao**: Menos intervencao manual = menos erros

<!-- pause -->

- **Controle**: Aprovacoes antes de ir para producao

<!-- pause -->

- **Rollback**: Voltar rapido quando algo da errado

<!-- end_slide -->

# A Solucao

## GitOps + Argo CD + Kargo

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│   Git    │───▶│ Argo CD  │───▶│  Kargo   │───▶│   K8s    │
│  (SSOT)  │    │   (CD)   │    │(Promocao)│    │ (Deploy) │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

<!-- pause -->

**SSOT** = Single Source of Truth

O Git e a unica fonte de verdade!

<!-- end_slide -->


# Kubernetes

## O que e?

<!-- pause -->

- Orquestrador de containers
- Criado pelo Google (Borg -> Kubernetes)
- Open source desde 2014
- Padrao de mercado

<!-- end_slide -->

# Kubernetes - Conceitos Basicos

## Pod
A menor unidade deployavel (1+ containers)

## Deployment
Gerencia ReplicaSets e Pods

## Service
Expoe Pods para rede (ClusterIP, NodePort, LoadBalancer)

## Namespace
Isolamento logico de recursos

<!-- end_slide -->

# Kubernetes - Manifests

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: dev
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
  template:
    spec:
      containers:
        - name: backend
          image: marcellmartini/backend:abc123
          ports:
            - containerPort: 8000
```

<!-- end_slide -->

# GitOps

## O que e?

<!-- pause -->

> "GitOps e uma forma de fazer Continuous Delivery
> usando Git como fonte de verdade para
> infraestrutura declarativa."
>
> -- Weaveworks (2017)

<!-- end_slide -->

# GitOps - Principios

## 1. Declarativo
Toda a configuracao e descrita de forma declarativa

<!-- pause -->

## 2. Versionado
Git armazena todo o estado desejado

<!-- pause -->

## 3. Automatico
Agentes aplicam mudancas automaticamente

<!-- pause -->

## 4. Observavel
Sistema detecta e corrige divergencias

<!-- end_slide -->

# GitOps - Fluxo

```
┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│ Desenvolvedor│────▶│     Git     │────▶│  Operador   │
│  faz commit  │     │  (PR/Merge) │     │  (Argo CD)  │
└──────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               ▼
                                         ┌─────────────┐
                                         │ Kubernetes  │
                                         │  (Cluster)  │
                                         └─────────────┘
```

<!-- end_slide -->

# GitOps vs Tradicional

| Aspecto | Tradicional | GitOps |
|---------|-------------|--------|
| Deploy | Push (CI faz deploy) | Pull (agente aplica) |
| Auditoria | Logs espalhados | Git history |
| Rollback | Scripts manuais | `git revert` |
| Drift | Nao detectado | Auto-corrigido |
| Seguranca | CI precisa acesso | Cluster puxa |

<!-- end_slide -->


# Helm

## O "Package Manager" do Kubernetes

<!-- pause -->

- **Charts**: Pacotes de recursos K8s
- **Values**: Configuracoes parametrizaveis
- **Templates**: Go templates para manifests
- **Releases**: Instancias de charts

<!-- end_slide -->

# Helm - Estrutura de Chart

```
helm/backend/
├── Chart.yaml          # Metadados do chart
├── values.yaml         # Valores padrao
└── templates/
    ├── deployment.yaml # Template do Deployment
    ├── service.yaml    # Template do Service
    └── secret.yaml     # Template do Secret
```

<!-- end_slide -->

# Helm - Templates

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
```

<!-- end_slide -->

# Helm - Values

```yaml
# values.yaml
replicaCount: 1

image:
  repository: marcellmartini/backend
  tag: latest

resources:
  limits:
    cpu: 100m
    memory: 128Mi
```

<!-- end_slide -->

# Kustomize

## Customizacao sem Templates

<!-- pause -->

- Nativo do kubectl (`kubectl apply -k`)
- Patches e overlays
- Sem linguagem de template
- Composicao de recursos

<!-- end_slide -->

# Kustomize - Estrutura

```
k8s/
├── base/
│   ├── kustomization.yaml
│   └── helm-output/
│       ├── backend/
│       └── frontend/
└── overlays/
    ├── dev/
    │   └── kustomization.yaml   # 1 replica
    ├── stg/
    │   └── kustomization.yaml   # 2 replicas
    └── prod/
        └── kustomization.yaml   # 3 replicas
```

<!-- end_slide -->

# Kustomize - Overlay

```yaml
# overlays/prod/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base

replicas:
  - name: backend
    count: 3
  - name: frontend
    count: 3

images:
  - name: marcellmartini/backend
    newTag: abc12345
```

<!-- end_slide -->

# Helm + Kustomize

## Por que usar os dois?

<!-- pause -->

| Helm | Kustomize |
|------|-----------|
| Templates complexos | Patches simples |
| Reusabilidade | Customizacao |
| Dependencias | Composicao |

<!-- pause -->

## Nossa estrategia:

```
Helm (gera base) → Kustomize (aplica overlays)
```

<!-- end_slide -->


# Argo CD

## GitOps Operator para Kubernetes

<!-- pause -->

- Declarativo e versionado
- UI Web intuitiva
- Multi-cluster
- SSO e RBAC
- Webhooks e auto-sync
- Health checks

<!-- end_slide -->

# Argo CD - Arquitetura

```
┌────────────────────────────────────┐
│                   Argo CD          │
│  ┌─────────────┐  ┌─────────────┐  │
│  │   API       │  │    Repo     │  │
│  │  Server     │  │   Server    │  │
│  └─────────────┘  └─────────────┘  │
│         │                │         │
│         ▼                ▼         │
│  ┌──────────────────────────────┐  │
│  │     Application Controller   │  │
│  └──────────────────────────────┘  │
└────────────────────────────────────┘
                   │
                   ▼
           ┌───────────────┐
           │  Kubernetes   │
           │   Clusters    │
           └───────────────┘
```

<!-- end_slide -->

# Argo CD - Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: dev-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/user/repo.git
    targetRevision: env/dev
    path: .
  destination:
    server: https://kubernetes.default.svc
    namespace: dev
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

<!-- end_slide -->

# Argo CD - Sync Status

## Estados de uma Application

| Status | Descricao |
|--------|-----------|
| **Synced** | Cluster = Git |
| **OutOfSync** | Cluster != Git |
| **Unknown** | Erro ao verificar |

## Health Status

| Status | Descricao |
|--------|-----------|
| **Healthy** | Todos recursos OK |
| **Progressing** | Aguardando pods |
| **Degraded** | Algum recurso falhou |

<!-- end_slide -->

# Argo CD - Sync Policies

## Manual Sync
- Usuario clica em "Sync"
- Controle total

<!-- pause -->

## Auto Sync
```yaml
syncPolicy:
  automated:
    prune: true      # Remove recursos deletados
    selfHeal: true   # Corrige drift automatico
```

<!-- end_slide -->


# Kargo

## Promocao de Artefatos para Kubernetes

<!-- pause -->

- Criado pela Akuity (fundadores do Argo)
- Complementa Argo CD
- Promocao progressiva (dev → stg → prod)
- Aprovacoes e gates
- Rastreabilidade completa

<!-- end_slide -->

# Kargo - Conceitos

## Project
Namespace logico para recursos Kargo

<!-- pause -->

## Warehouse
Monitora registries por novas imagens

<!-- pause -->

## Freight
Artefato (imagem + versao) a ser promovido

<!-- pause -->

## Stage
Ambiente (dev, stg, prod) com regras de promocao

<!-- end_slide -->

# Kargo - Fluxo

```
┌───────────┐     ┌───────────┐     ┌───────────┐
│ Warehouse │────▶│  Freight  │────▶│   Stage   │
│  (watch)  │     │ (artefato)│     │   (env)   │
└───────────┘     └───────────┘     └───────────┘
                                          │
                  ┌───────────────────────┴───────┐
                  ▼                               ▼
            ┌───────────┐                   ┌───────────┐
            │    DEV    │                   │    STG    │
            │  (auto)   │                   │  (manual) │
            └───────────┘                   └───────────┘
                                                  │
                                                  ▼
                                            ┌───────────┐
                                            │   PROD    │
                                            │  (manual) │
                                            └───────────┘
```

<!-- end_slide -->

# Kargo - Warehouse

```yaml
apiVersion: kargo.akuity.io/v1alpha1
kind: Warehouse
metadata:
  name: image-promotion
  namespace: image-promotion
spec:
  subscriptions:
    - image:
        repoURL: docker.io/marcellmartini/backend
        allowTags: ^[a-f0-9]{8}$  # Apenas commit hashes
    - image:
        repoURL: docker.io/marcellmartini/frontend
        allowTags: ^[a-f0-9]{8}$
```

<!-- end_slide -->

# Kargo - Stage

```yaml
apiVersion: kargo.akuity.io/v1alpha1
kind: Stage
metadata:
  name: dev
  namespace: image-promotion
spec:
  requestedFreight:
    - origin:
        kind: Warehouse
        name: image-promotion
      sources:
        direct: true
  promotionTemplate:
    spec:
      steps:
        - uses: git-clone
        - uses: kustomize-set-image
        - uses: kustomize-build
        - uses: git-commit
        - uses: git-push
        - uses: argocd-update
```

<!-- end_slide -->

# Kargo - Politicas de Promocao

## Auto Promotion (Dev)
```yaml
# projectconfig.yaml
promotionPolicies:
  - stage: dev
    autoPromotionEnabled: true
```

<!-- pause -->

## Manual Promotion (Stg/Prod)
```yaml
promotionPolicies:
  - stage: stg
    autoPromotionEnabled: false
  - stage: prod
    autoPromotionEnabled: false
```

<!-- end_slide -->

# Argo CD + Kargo

## Responsabilidades

| Ferramenta | Funcao |
|------------|--------|
| **Argo CD** | Sincroniza Git → Cluster |
| **Kargo** | Promove artefatos entre ambientes |

<!-- pause -->

## Integracao

```yaml
# Anotacao na Application do Argo CD
metadata:
  annotations:
    kargo.akuity.io/authorized-stage: image-promotion:dev
```

<!-- end_slide -->


# Arquitetura do Projeto Demo

## Stack

| Componente | Tecnologia |
|------------|------------|
| Backend | FastAPI + PostgreSQL |
| Frontend | React + Vite |
| CI | GitHub Actions |
| CD | Argo CD |
| Promocao | Kargo |
| Cluster | Minikube |

<!-- end_slide -->

# Estrutura de Ambientes

```
minikube cluster
├── argocd (namespace)
│   └── Argo CD Controller
├── kargo (namespace)
│   └── Kargo Controller
├── image-promotion (namespace)
│   └── Warehouse, Stages
├── dev (namespace)
│   ├── backend (1 replica)
│   └── frontend (1 replica)
├── stg (namespace)
│   ├── backend (2 replicas)
│   └── frontend (2 replicas)
└── prod (namespace)
    ├── backend (3 replicas)
    └── frontend (3 replicas)
```

<!-- end_slide -->

# Estrategia de Branches

```
Branches:
├── main           → Codigo fonte (PROTEGIDO)
├── env/dev        → Manifests renderizados para dev
├── env/stg        → Manifests renderizados para stg
└── env/prod       → Manifests renderizados para prod
```

<!-- pause -->

## Por que branches separados?

- Branch `main` permanece protegido
- Isolamento entre ambientes
- Historico de deployments separado
- Recomendado pelos mantenedores do Kargo

<!-- end_slide -->

# Pipeline Completo

```
┌──────────────────────────────────────────────────────────┐
│                    GitHub Actions (CI)                   │
│   PR → lint → test → build → push (Docker Hub)           │
└──────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│                    Kargo Warehouse                       │
│              Detecta nova imagem (tag: abc12345)         │
└──────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   ┌─────────┐           ┌─────────┐           ┌─────────┐
   │   DEV   │──────────▶│   STG   │──────────▶│  PROD   │
   │  (auto) │           │ (manual)│           │ (manual)│
   └─────────┘           └─────────┘           └─────────┘
```

<!-- end_slide -->


# Demo Time!

## O que vamos ver:

1. CI Pipeline (PR → merge → build)
2. Deploy automatico em DEV
3. Promocao para STG (aprovacao)
4. Promocao para PROD (aprovacao)
5. Rollback automatico

<!-- end_slide -->

# Demo 1: CI Pipeline

## Fluxo

```bash
# 1. Criar PR
gh pr create --base main --head feature/change-role

# 2. GitHub Actions executa:
- pyright (type check)
- pylint (lint)
- black (format)
- tests
- build & push (apos merge)

# 3. Merge da PR
gh pr merge --merge
```

<!-- end_slide -->

# Demo 2: Deploy em DEV

## Kargo detecta nova imagem

```bash
# Verificar Warehouse
kubectl get warehouse -n image-promotion

# Verificar Freight criado
kubectl get freight -n image-promotion

# Verificar promocao automatica
kubectl get promotions -n image-promotion

# Verificar pods em dev
kubectl get pods -n dev
```

<!-- end_slide -->

# Demo 3: Promocao para STG

## Aprovacao Manual (QA)

```bash
# Via CLI
kargo promote --project image-promotion \
              --stage stg \
              --freight <freight-alias>

# Verificar sincronizacao
kubectl get pods -n stg

# Ou via UI do Kargo
# https://localhost:3000
```

<!-- end_slide -->

# Demo 4: Promocao para PROD

## Aprovacao Manual (PO)

```bash
# Via CLI
kargo promote --project image-promotion \
              --stage prod \
              --freight <freight-alias>

# Verificar sincronizacao
kubectl get pods -n prod
```

<!-- end_slide -->

# Demo 5: Rollback

## Cenario: Deploy com erro

```bash
# 1. Merge de codigo com bug
gh pr create --base main --head feature/error
gh pr merge --merge

# 2. CI passa (erro e em runtime)
# 3. Deploy em dev falha (health check)
kubectl get pods -n dev
# STATUS: CrashLoopBackOff

# 4. Argo CD mostra status Degraded

# 5. Merge do fix
gh pr create --base main --head feature/fix
gh pr merge --merge

# 6. Novo deploy bem-sucedido
kubectl get pods -n dev
# STATUS: Running
```

<!-- end_slide -->


# Recapitulando

## O que aprendemos:

<!-- pause -->

- **GitOps**: Git como fonte de verdade

<!-- pause -->

- **Argo CD**: Sincroniza Git → Cluster

<!-- pause -->

- **Kargo**: Promove artefatos entre ambientes

<!-- pause -->

- **Helm + Kustomize**: Templates + Customizacao

<!-- end_slide -->

# Beneficios

## Com essa arquitetura:

- **Consistencia**: Mesma imagem em todos os ambientes
- **Rastreabilidade**: Historico completo no Git
- **Automacao**: CI/CD sem intervencao manual
- **Controle**: Aprovacoes para stg/prod
- **Rollback**: Rapido e confiavel
- **Auditoria**: Quem aprovou, quando, o que

<!-- end_slide -->

# Proximos Passos

## Para implementar no seu projeto:

1. Configure Argo CD no seu cluster
2. Defina estrutura de branches/ambientes
3. Crie Helm charts ou Kustomize bases
4. Instale e configure Kargo
5. Defina politicas de promocao
6. Treine o time!

<!-- end_slide -->

# Recursos

## Links Uteis

- **Argo CD**: https://argo-cd.readthedocs.io
- **Kargo**: https://kargo.io
- **GitOps Principles**: https://opengitops.dev
- **Helm**: https://helm.sh
- **Kustomize**: https://kustomize.io

<!-- end_slide -->

# Obrigado!

## Perguntas? Q&A

Perguntas sobre:
- GitOps
- Argo CD
- Kargo
- Kubernetes
- CI/CD
- Qualquer coisa!
 
<!-- pause -->

<!-- end_slide -->

# Redes Sociais
## Marcell Martini

- **Instagram**: @marcellmartini
- **LinkedIn**: /in/marcellmartini
- **GitHub**: github.com/marcellmartini

### Repositorio da Demo

```
github.com/marcellmartini/image-promotion-gitops
```
