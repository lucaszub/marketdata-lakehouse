---
description: Déployer le code sur le VPS Hostinger (git push + docker compose up --build)
allowed-tools: Bash
---

Lancer le déploiement sur le VPS :

```bash
./scripts/deploy.sh
```

Vérifier que les containers tournent après le déploiement :

```bash
source .env && ssh "${VPS_USER}@${VPS_HOST}" "cd marketdata-lakehouse && docker compose ps"
```
