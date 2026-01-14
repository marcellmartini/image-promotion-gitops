#!/bin/bash
# Inicializa minikube com configurações adequadas para a demo
set -e

echo "=== Iniciando Minikube ==="
minikube start --cpus=4 --memory=4096 --driver=docker

echo ""
echo "=== Habilitando addons ==="
minikube addons enable ingress
minikube addons enable metrics-server

echo ""
echo "=== Criando namespaces ==="
kubectl create namespace dev --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace stg --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace prod --dry-run=client -o yaml | kubectl apply -f -

echo ""
echo "=== Configurando Docker Hub credentials ==="
echo "Crie um Access Token em: https://hub.docker.com/settings/security"
echo ""
read -p "Digite seu Docker Hub username: " DOCKERHUB_USERNAME
read -sp "Digite seu Docker Hub token: " DOCKERHUB_TOKEN
echo ""

if [ -z "$DOCKERHUB_USERNAME" ] || [ -z "$DOCKERHUB_TOKEN" ]; then
    echo "Aviso: Docker Hub credentials não configuradas. Pode haver rate limit."
else
    for ns in dev stg prod; do
        kubectl create secret docker-registry dockerhub-creds \
            --docker-server=https://index.docker.io/v1/ \
            --docker-username="$DOCKERHUB_USERNAME" \
            --docker-password="$DOCKERHUB_TOKEN" \
            -n $ns --dry-run=client -o yaml | kubectl apply -f -
    done
    echo "Secret dockerhub-creds criado em dev, stg e prod!"
fi

echo ""
echo "=== Minikube configurado! ==="
echo "IP do Minikube: $(minikube ip)"
echo ""
echo "Próximos passos:"
echo "  ./scripts/setup-argocd.sh"
echo "  ./scripts/setup-kargo.sh"
