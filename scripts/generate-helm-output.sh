#!/bin/bash
# Regenera manifests do Helm para uso com Kustomize
# Execute da raiz do projeto

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$ROOT_DIR"

echo "Gerando output do Helm..."

helm template backend ./helm/backend > k8s/base/helm-output/backend/all.yaml
echo "  - backend: OK"

helm template frontend ./helm/frontend > k8s/base/helm-output/frontend/all.yaml
echo "  - frontend: OK"

echo ""
echo "Validando com Kustomize..."

kustomize build k8s/overlays/dev > /dev/null && echo "  - dev: OK"
kustomize build k8s/overlays/stg > /dev/null && echo "  - stg: OK"
kustomize build k8s/overlays/prod > /dev/null && echo "  - prod: OK"

echo ""
echo "Helm output regenerado com sucesso!"
