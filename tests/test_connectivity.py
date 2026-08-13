"""Vérifie la connectivité IP bout-en-bout entre les deux LAN,
qui ne peut fonctionner que si le routage est opérationnel.

Toutes les IP sont dérivées de ansible/vars/network.yml (source de
vérité), jamais codées en dur, pour que les tests restent valides
si la topologie change."""
from conftest import docker_exec


def test_ping_cross_lan(lab_hosts_by_name):
    names = list(lab_hosts_by_name.keys())
    assert len(names) == 2, "Ce test suppose exactement 2 lab_hosts"
    a, b = names
    pairs = [
        (a, lab_hosts_by_name[b]["ip"]),
        (b, lab_hosts_by_name[a]["ip"]),
    ]
    for source, destination_ip in pairs:
        result = docker_exec(source, f"ping -c 3 -W 2 {destination_ip}")
        assert "0% packet loss" in result.stdout, (
            f"Le ping de {source} vers {destination_ip} a échoué ou a "
            f"subi des pertes.\nSortie obtenue :\n{result.stdout}"
        )


def test_ping_wan_link(routers_by_name):
    names = list(routers_by_name.keys())
    assert len(names) == 2, "Ce test suppose exactement 2 routeurs"
    a, b = names
    pairs = [
        (a, routers_by_name[b]["wan_ip"]),
        (b, routers_by_name[a]["wan_ip"]),
    ]
    for source, destination_ip in pairs:
        result = docker_exec(source, f"ping -c 3 -W 2 {destination_ip}")
        assert "0% packet loss" in result.stdout, (
            f"Le lien WAN entre routeurs est down : ping {source} -> "
            f"{destination_ip} a échoué.\nSortie obtenue :\n{result.stdout}"
        )
