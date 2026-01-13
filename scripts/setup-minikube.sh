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
echo "=== Minikube configurado! ==="
echo "IP do Minikube: $(minikube ip)"
echo ""
echo "Próximos passos:"
echo "  ./scripts/setup-argocd.sh"
echo "  ./scripts/setup-kargo.sh"
