# Ansible — VPS Setup

## Prérequis (en local)
```bash
pip install ansible
ansible-galaxy collection install community.docker
```

## Configuration
1. Mettre l'IP du VPS dans `inventory.ini`
2. S'assurer que `~/.ssh/id_rsa.pub` est bien ta clé SSH

## Déploiement
```bash
# Test de connexion
ansible vps -i ansible/inventory.ini -m ping

# Déploiement complet
ansible-playbook -i ansible/inventory.ini ansible/playbooks/setup_vps.yml

# Après le playbook : copier le .env manuellement
scp .env deploy@YOUR_VPS_IP:/home/deploy/marketdata-lakehouse/.env

# Relancer Airflow avec le .env
ssh deploy@YOUR_VPS_IP "cd marketdata-lakehouse && docker compose up -d"
```


