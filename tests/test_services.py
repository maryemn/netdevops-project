"""Vérifie que les services de l'infra tournent : conteneurs actifs
et résolution DNS via CoreDNS (interne + forward externe).

Les noms de conteneurs et IP sont dérivés de network.yml.

Note : le suffixe '.infra.local' est défini en dur dans le Corefile
(infra/services/dns/Corefile), pas dans network.yml — donc il reste
codé en dur ici aussi, faute de source de vérité commune pour le
moment (amélioration prévue : templater le Corefile)."""
import pytest
from conftest import docker_exec

DOMAIN_SUFFIX = "infra.local"


@pytest.fixture(scope="session")
def expected_containers(routers_by_name, lab_hosts_by_name, services_by_name):
    return (
        list(routers_by_name.keys())
        + list(lab_hosts_by_name.keys())
        + list(services_by_name.keys())
    )


def test_all_expected_containers_running(running_containers, expected_containers):
    for container in expected_containers:
        assert container in running_containers, (
            f"Le conteneur '{container}' n'est pas démarré. "
            f"Conteneurs actifs : {running_containers}"
        )


def test_internal_dns_resolution(services_by_name):
    web = services_by_name["web"]
    dns_server = services_by_name["dns"]["ip"]
    fqdn = f"{web['name']}.{DOMAIN_SUFFIX}"
    result = docker_exec("host-a", f"nslookup {fqdn} {dns_server}")
    assert web["ip"] in result.stdout, (
        f"La résolution interne de {fqdn} a échoué.\n"
        f"Sortie obtenue :\n{result.stdout}"
    )


def test_external_dns_forward(services_by_name):
    dns_server = services_by_name["dns"]["ip"]
    result = docker_exec("host-a", f"nslookup google.com {dns_server}")
    assert "Non-authoritative answer" in result.stdout or "Address" in result.stdout, (
        f"Le forward DNS externe semble ne pas fonctionner.\n"
        f"Sortie obtenue :\n{result.stdout}"
    )
