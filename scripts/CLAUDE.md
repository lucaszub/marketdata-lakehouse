# scripts/

## Rôle
Scripts shell pour les opérations de déploiement.

## Scripts disponibles

### deploy.sh — Déployer sur le VPS

```bash
./scripts/deploy.sh
```

Fait :
1. `git push` vers GitHub
2. SSH sur le VPS → `git pull && docker compose up -d --build`

Utiliser après chaque modification de code ou de configuration.

> **Important :** `--build` est inclus → rebuild automatique de l'image Docker.
> Toujours utiliser ce script pour déployer sur le VPS, jamais de commande manuelle.

### push_to_acr.sh — Déployer Streamlit sur Azure

```bash
./scripts/push_to_acr.sh
```

Fait :
1. Récupère un token ACR via `az acr login --expose-token`
2. Build l'image Docker (Streamlit)
3. Tag et push vers `marketdataregistry.azurecr.io/marketdata-streamlit:latest`
4. Force une nouvelle révision Azure Container Apps (`--revision-suffix $(date +%s)`)

> **Important :** Azure ignore les re-push du même tag `latest` sans nouveau suffix de révision.
> Le script gère ça automatiquement — ne jamais faire `az containerapp update` à la main.

Prérequis : `az` CLI installé et authentifié (`az login`).

## Skill associé

`/deploy` — lance `./scripts/deploy.sh` depuis Claude
