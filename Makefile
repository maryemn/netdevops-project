.PHONY: up down test clean logs status

# Déploie toute l'infrastructure via Ansible (génération configs + docker compose up)
# Nécessite un sudo NOPASSWD pour iptables (voir README) — obligatoire pour tourner en CI
up:
	ansible-playbook ansible/playbooks/deploy-infra.yml

# Détruit complètement l'infrastructure (conteneurs + volumes + réseaux)
down:
	docker compose -f infra/docker-compose.yml down --volumes --remove-orphans

# Lance la suite de tests réseau (pytest)
test:
	mkdir -p reports
	pytest tests/ --html=reports/report.html --junitxml=reports/junit.xml --self-contained-html

# Affiche l'état des conteneurs de l'infra
status:
	docker compose -f infra/docker-compose.yml ps

# Affiche les logs de tous les conteneurs
logs:
	docker compose -f infra/docker-compose.yml logs --tail=100

# Nettoyage complet : infra + images buildées localement
clean: down
	docker compose -f infra/docker-compose.yml down --rmi local
