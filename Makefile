# Makefile
up:
	ansible-playbook ansible/playbooks/deploy-infra.yml

down:
	docker compose -f infra/docker-compose.yml down -v

test:
	pytest tests/