#!/bin/bash
# Instala Argo CD no cluster
set -e

echo "=== Instalando Argo CD ==="
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

echo ""
echo "=== Ajustando probes para Minikube (recursos limitados) ==="
sleep 5
kubectl patch deployment argocd-repo-server -n argocd --type='json' -p='[
  {"op": "replace", "path": "/spec/template/spec/containers/0/livenessProbe/timeoutSeconds", "value": 15},
  {"op": "replace", "path": "/spec/template/spec/containers/0/livenessProbe/initialDelaySeconds", "value": 60},
  {"op": "replace", "path": "/spec/template/spec/containers/0/readinessProbe/timeoutSeconds", "value": 15},
  {"op": "replace", "path": "/spec/template/spec/containers/0/readinessProbe/initialDelaySeconds", "value": 30}
]'

echo ""
echo "=== Aguardando pods ficarem ready ==="
kubectl wait --for=condition=Ready pods --all -n argocd --timeout=300s

echo ""
echo "=== Obtendo senha inicial do admin ==="
ARGOCD_PASSWORD=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
echo "Usuário: admin"
echo "Senha: $ARGOCD_PASSWORD"

echo ""
echo "=== Expondo Argo CD (port-forward) ==="
echo "Execute em outro terminal:"
echo "  kubectl port-forward svc/argocd-server -n argocd 8080:443"
echo ""
echo "Acesse: https://localhost:8080"

echo ""
echo "=== Aplicando Applications ==="
kubectl apply -f gitops/argocd/applications/

echo ""
echo "=== Argo CD instalado! ==="
echo "Próximos passos:"
echo "  ./scripts/setup-kargo.sh"
