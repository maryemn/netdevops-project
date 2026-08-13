"""Fixtures et helpers communs pour les tests d'infrastructure réseau.

Les valeurs réseau (IP, préfixes, AS...) ne sont jamais codées en dur
dans les tests : elles sont lues et résolues depuis
ansible/vars/network.yml, la source de vérité unique du projet.
Ainsi, si network.yml change, les tests restent valides sans
modification.
"""
import shlex
import subprocess
from pathlib import Path

import pytest
import yaml
from jinja2 import Template

NETWORK_VARS_PATH = Path(__file__).parent.parent / "ansible" / "vars" / "network.yml"


def docker_exec(container: str, command: str) -> subprocess.CompletedProcess:
    """Exécute une commande dans un conteneur et retourne le résultat.

    Utilise shlex.split (pas .split()) pour respecter les guillemets,
    indispensable pour des commandes comme vtysh -c "show ip bgp summary".
    """
    return subprocess.run(
        ["docker", "exec", container] + shlex.split(command),
        capture_output=True,
        text=True,
        timeout=15,
    )


@pytest.fixture(scope="session")
def running_containers():
    """Liste des conteneurs actuellement en cours d'exécution."""
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip().splitlines()


@pytest.fixture(scope="session")
def network_vars():
    """Charge ansible/vars/network.yml, la source de vérité unique."""
    with open(NETWORK_VARS_PATH) as f:
        return yaml.safe_load(f)


def _resolve(value, context):
    """Résout une valeur Jinja2 simple (ex: '{{ as_hq }}') via les
    variables racine de network.yml. Ne fait rien sur les valeurs qui
    ne contiennent pas de templating."""
    if isinstance(value, str) and "{{" in value:
        return Template(value).render(**context)
    return value


def _resolve_entries(entries, context):
    """Résout chaque champ de chaque entrée d'une liste (routers,
    lab_hosts, services) contre les variables racine de network.yml."""
    resolved = []
    for entry in entries:
        resolved.append({k: _resolve(v, context) for k, v in entry.items()})
    return resolved


@pytest.fixture(scope="session")
def routers_by_name(network_vars):
    """Dict {hostname: entrée résolue} pour les routeurs, IP/AS/prefix
    déjà résolus depuis les variables racine de network.yml."""
    resolved = _resolve_entries(network_vars["routers"], network_vars)
    return {r["hostname"]: r for r in resolved}


@pytest.fixture(scope="session")
def lab_hosts_by_name(network_vars):
    """Dict {name: entrée résolue} pour les hosts du labo."""
    resolved = _resolve_entries(network_vars["lab_hosts"], network_vars)
    return {h["name"]: h for h in resolved}


@pytest.fixture(scope="session")
def services_by_name(network_vars):
    """Dict {name: entrée résolue} pour les services (web, dns, ...)."""
    resolved = _resolve_entries(network_vars["services"], network_vars)
    return {s["name"]: s for s in resolved}
