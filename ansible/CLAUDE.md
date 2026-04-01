# ansible/

## Rôle
Provisionne le VPS Hostinger pour faire tourner Airflow via Docker Compose.
Idempotent : peut être relancé sans risque.

## VPS

| Paramètre | Valeur |
|:---|:---|
| IP | voir `.env` → `VPS_HOST` |
| User de connexion initial | root |
| User créé par Ansible | deploy (groupe docker) |
| Répertoire app | /home/deploy/marketdata-lakehouse |

## Fichiers

| Fichier | Rôle |
|:---|:---|
| `inventory.ini` | IP + user + clé SSH |
| `ansible.cfg` | roles_path, inventory par défaut |
| `playbooks/setup_vps.yml` | Playbook principal |
| `roles/airflow/tasks/main.yml` | Toutes les tâches d'installation |

## Ce que fait le playbook

1. Installe Docker CE + Docker Compose plugin
2. Crée le user `deploy` (groupe `docker`)
3. Copie la clé SSH locale → `deploy`
4. Clone le repo GitHub
5. Copie le `.env` local → VPS (mode 0600)
6. Lance `docker compose up -d`

## Commandes

```bash
cd ansible

# Tester la connexion
# Copier l'exemple et renseigner l'IP
cp inventory.ini.example inventory.ini

# Tester la connexion
ansible vps -i inventory.ini -m ping

# Provisionner le VPS
ansible-playbook -i inventory.ini playbooks/setup_vps.yml
```

## Notes

- Le `.env` est copié depuis la racine locale — il ne doit jamais être dans le repo.
- Pour re-déployer du code (sans re-provisionner), utiliser `./scripts/deploy.sh`.
