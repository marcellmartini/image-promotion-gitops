# Runbook da Apresentacao

## Pre-Apresentacao (30min antes)

### Checklist

```bash
# 1. Verificar Minikube
minikube status

# 2. Verificar PostgreSQL (docker-compose)
docker compose ps

# 3. Verificar Argo CD
kubectl get pods -n argocd

# 4. Verificar Kargo
kubectl get pods -n kargo

# 5. Verificar namespaces
kubectl get ns | grep -E "dev|stg|prod|image-promotion"

# 6. Verificar Applications
kubectl get applications -n argocd

# 7. Verificar Kargo resources
kubectl get warehouse,stages,freight -n image-promotion
```

### Port-forwards (abrir em terminais separados)

```bash
# Terminal 1: Argo CD
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Terminal 2: Kargo
kubectl port-forward svc/kargo-api -n kargo 3000:443
```

### Credenciais

```bash
# Argo CD
# URL: https://localhost:8080
# User: admin
# Pass:
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Kargo
# URL: https://localhost:3000
# User: admin
# Pass: admin
```

---

## Demo 1: CI Pipeline (10min)

### Mostrar codigo atual

```bash
cd ~/repos/personal/image-promotion-gitops
git log --oneline -5
```

### Criar PR da feature

```bash
gh pr create --base main --head feature/change-role \
  --title "feat: add role change support" \
  --body "Permite alterar a role do usuario na edicao"
```

### Mostrar GitHub Actions

Abrir: https://github.com/marcellmartini/image-promotion-gitops/actions

### Aprovar e Mergear

```bash
gh pr merge --merge
```

### Mostrar imagem no Docker Hub

Abrir: https://hub.docker.com/r/marcellmartini/image-promotion-backend/tags

---

## Demo 2: Deploy em DEV (5min)

### Verificar Warehouse detectou imagem

```bash
kubectl get warehouse -n image-promotion
kubectl get freight -n image-promotion
```

### Verificar promocao automatica

```bash
kubectl get promotions -n image-promotion
kubectl get stages -n image-promotion
```

### Verificar Argo CD

```bash
# CLI
kubectl get applications -n argocd

# Ou abrir UI: https://localhost:8080
```

### Verificar pods em dev

```bash
kubectl get pods -n dev
kubectl get pods -n dev -o wide
```

### Testar aplicacao

```bash
# Se tiver ingress configurado
curl http://dev.app.local/health

# Ou port-forward
kubectl port-forward svc/backend -n dev 8000:8000
curl http://localhost:8000/health
```

---

## Demo 3: Promocao para STG (5min)

### Verificar stage aguardando

```bash
kubectl get stages -n image-promotion
```

### Obter freight alias

```bash
kubectl get freight -n image-promotion -o jsonpath='{.items[0].metadata.labels.kargo\.akuity\.io/alias}'
```

### Promover para STG

```bash
# Substituir <alias> pelo valor obtido acima
kargo promote --project image-promotion --stage stg --freight <alias>
```

### Ou via UI do Kargo

1. Abrir https://localhost:3000
2. Selecionar projeto "image-promotion"
3. Clicar no stage "stg"
4. Clicar em "Promote"
5. Selecionar o freight

### Verificar promocao

```bash
kubectl get promotions -n image-promotion | grep stg
kubectl get pods -n stg
```

---

## Demo 4: Promocao para PROD (5min)

### Promover para PROD

```bash
kargo promote --project image-promotion --stage prod --freight <alias>
```

### Verificar

```bash
kubectl get promotions -n image-promotion | grep prod
kubectl get pods -n prod
```

### Mostrar todas as replicas

```bash
echo "=== DEV (1 replica) ==="
kubectl get pods -n dev

echo "=== STG (2 replicas) ==="
kubectl get pods -n stg

echo "=== PROD (3 replicas) ==="
kubectl get pods -n prod
```

---

## Demo 5: Rollback (5min)

### Criar PR com erro

```bash
gh pr create --base main --head feature/error \
  --title "feat: update health check" \
  --body "Atualiza endpoint de health check"
```

### Mergear

```bash
gh pr merge --merge
```

### Aguardar CI e promocao automatica para dev

```bash
# Monitorar
watch kubectl get pods -n dev
```

### Mostrar erro

```bash
kubectl get pods -n dev
# STATUS: CrashLoopBackOff

kubectl logs -n dev -l app=backend --tail=20
```

### Mostrar Argo CD degradado

Abrir UI: https://localhost:8080
- dev-app deve estar "Degraded"

### Criar PR com fix

```bash
gh pr create --base main --head feature/fix \
  --title "fix: fix health check" \
  --body "Corrige endpoint de health check"
```

### Mergear

```bash
gh pr merge --merge
```

### Mostrar recuperacao

```bash
watch kubectl get pods -n dev
# STATUS: Running
```

---

## Comandos Uteis Durante a Demo

### Status geral

```bash
kubectl get warehouse,freight,stages,promotions -n image-promotion
```

### Logs de promocao

```bash
kubectl get promotions -n image-promotion -o yaml | grep -A 30 "status:"
```

### Verificar branch atualizado

```bash
git fetch origin env/dev
git log origin/env/dev --oneline -3
```

### Resetar stage (se necessario)

```bash
kubectl delete stage dev -n image-promotion
kubectl apply -f gitops/kargo/stages/dev.yaml
```

---

## Troubleshooting

### Kargo nao promove

```bash
# Verificar logs do controller
kubectl logs -n kargo -l app.kubernetes.io/name=kargo -f

# Verificar secret do GitHub
kubectl get secret github-creds -n image-promotion
```

### Argo CD nao sincroniza

```bash
# Verificar logs
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-application-controller -f

# Forcar sync
kubectl patch application dev-app -n argocd --type merge -p '{"operation":{"sync":{}}}'
```

### Pod nao sobe

```bash
kubectl describe pod -n dev -l app=backend
kubectl logs -n dev -l app=backend --previous
```

---

## Plano de Contingencia

Se algo der errado durante a demo:

1. **CI falha**: Mostrar run anterior bem-sucedido
2. **Kargo nao detecta**: Mostrar freight existente
3. **Promocao falha**: Usar UI do Kargo
4. **Pods nao sobem**: Usar videos de backup

### Videos de Backup

```
videos/backup/
├── 01-ci-pipeline.mp4
├── 02-deploy-dev.mp4
├── 03-promotion-stg.mp4
├── 04-promotion-prod.mp4
└── 05-rollback.mp4
```

---

## Pos-Apresentacao

### Limpar recursos (opcional)

```bash
# Deletar promotions
kubectl delete promotions --all -n image-promotion

# Resetar stages
kubectl delete stages --all -n image-promotion
kubectl apply -f gitops/kargo/stages/

# Ou resetar tudo
minikube delete
```

### Compartilhar

- Repositorio: github.com/marcellmartini/image-promotion-gitops
- Slides: No repositorio em `presentation/slides.md`
