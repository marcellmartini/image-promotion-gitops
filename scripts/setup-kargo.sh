#!/bin/bash
# Instala Kargo no cluster
set -e

KARGO_VERSION="1.8.4"
CERT_MANAGER_VERSION="v1.16.2"

echo "=== Instalando cert-manager ${CERT_MANAGER_VERSION} ==="
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/${CERT_MANAGER_VERSION}/cert-manager.yaml

echo ""
echo "=== Aguardando cert-manager ficar ready ==="
kubectl wait --for=condition=Available deployment --all -n cert-manager --timeout=300s

echo ""
echo "=== Instalando Kargo ${KARGO_VERSION} ==="
kubectl create namespace kargo --dry-run=client -o yaml | kubectl apply -f -

helm install kargo \
  oci://ghcr.io/akuity/kargo-charts/kargo \
  --namespace kargo \
  --version ${KARGO_VERSION} \
  --set 'api.adminAccount.passwordHash=$2y$10$yyn0qGSBWLkIcGRuenZgteJHEoWD0VHw1oX.awaSPanX9RRw8K.nG' \
  --set api.adminAccount.tokenSigningKey='iwishthat-itwasabetter-signingkey1' \
  --wait

echo ""
echo "=== Aguardando pods ficarem ready ==="
kubectl wait --for=condition=Ready pods --all -n kargo --timeout=300s

echo ""
echo "=== Credenciais do Kargo ==="
echo "Usuário: admin"
echo "Senha: admin"

echo ""
echo "=== Expondo Kargo (port-forward) ==="
echo "Execute em outro terminal:"
echo "  kubectl port-forward svc/kargo-api -n kargo 8443:443"
echo ""
echo "Acesse: https://localhost:8443"

echo ""
echo "=== Aplicando configurações do Kargo ==="
echo "Criando projeto (o namespace é criado automaticamente)..."
kubectl apply -f gitops/kargo/project.yaml
sleep 2
kubectl apply -f gitops/kargo/projectconfig.yaml
kubectl apply -f gitops/kargo/warehouse.yaml
kubectl apply -f gitops/kargo/stages/

echo ""
echo "=== Kargo instalado! ==="
