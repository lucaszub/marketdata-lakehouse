#!/bin/bash
set -e

ACR_NAME="marketdataregistry"
IMAGE_NAME="marketdata-streamlit"
ACR_SERVER="${ACR_NAME}.azurecr.io"

echo "==> Getting ACR token..."
TOKEN=$(az acr login --name "$ACR_NAME" --expose-token --query accessToken -o tsv)

echo "==> Logging into ACR..."
echo "$TOKEN" | docker login "$ACR_SERVER" \
  --username 00000000-0000-0000-0000-000000000000 \
  --password-stdin

echo "==> Building image..."
docker build -t "$IMAGE_NAME" "$(dirname "$0")/.."

echo "==> Tagging..."
docker tag "$IMAGE_NAME" "${ACR_SERVER}/${IMAGE_NAME}:latest"

echo "==> Pushing..."
docker push "${ACR_SERVER}/${IMAGE_NAME}:latest"

echo "==> Deploying new revision on Azure Container Apps..."
az containerapp update \
  --name ca-marketdata-streamlit \
  --resource-group rg-marketdata \
  --image "${ACR_SERVER}/${IMAGE_NAME}:latest" \
  --revision-suffix "$(date +%s)" \
  --output none

echo "==> Done: ${ACR_SERVER}/${IMAGE_NAME}:latest"
