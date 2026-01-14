#!/bin/bash
# Instala Kargo no cluster
set -e

KARGO_VERSION="1.8.4"
CERT_MANAGER_VERSION="v1.16.2"
GITHUB_REPO="https://github.com/marcellmartini/image-promotion-gitops.git"

# Solicita o GitHub PAT no início
echo "=== Configuração do GitHub PAT ==="
echo "O Kargo precisa de um Personal Access Token (PAT) do GitHub para fazer push nos branches de ambiente."
echo ""
echo "Requisitos do PAT:"
echo "  - Classic: escopo 'repo' (Full control)"
echo "  - Fine-grained: 'Contents: Read and Write' no repositório"
echo ""
read -sp "Digite seu GitHub PAT: " GITHUB_PAT
echo ""

if [ -z "$GITHUB_PAT" ]; then
    echo "Erro: GitHub PAT não pode ser vazio!"
    exit 1
fi

echo ""
echo "=== Instalando cert-manager ${CERT_MANAGER_VERSION} ==="
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/${CERT_MANAGER_VERSION}/cert-manager.yaml

echo ""
echo "=== Aguardando cert-manager ficar ready ==="
kubectl wait --for=condition=Available deployment --all -n cert-manager --timeout=300s

echo ""
echo "=== Instalando Kargo ${KARGO_VERSION} ==="
kubectl create namespace kargo --dry-run=client -o yaml | kubectl apply -f -

helm upgrade --install kargo \
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

echo ""
echo "=== Criando secret do GitHub para git-push ==="
kubectl create secret generic github-creds \
  --namespace=image-promotion \
  --from-literal=repoURL="${GITHUB_REPO}" \
  --from-literal=username=x-access-token \
  --from-literal=password="${GITHUB_PAT}" \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl label secret github-creds -n image-promotion kargo.akuity.io/cred-type=git --overwrite
echo "Secret github-creds criado com sucesso!"

echo ""
echo "=== Aplicando demais configurações ==="
kubectl apply -f gitops/kargo/projectconfig.yaml
kubectl apply -f gitops/kargo/warehouse.yaml
kubectl apply -f gitops/kargo/stages/

echo ""
echo "=== Kargo instalado! ==="
