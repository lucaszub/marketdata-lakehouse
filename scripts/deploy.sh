#!/bin/bash
set -e

set -a && source "$(dirname "$0")/../.env" && set +a

APP_DIR="marketdata-lakehouse"

echo "==> Pushing to GitHub..."
git push

echo "==> Deploying on VPS..."
ssh "${VPS_USER}@${VPS_HOST}" "cd ${APP_DIR} && git pull && docker compose up -d --build"

echo "==> Done"
