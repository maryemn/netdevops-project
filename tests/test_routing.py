"""Vérifie que le peering eBGP est établi et que chaque routeur a
appris le préfixe LAN de son voisin.

Les noms de routeurs et préfixes sont dérivés de network.yml,
jamais codés en dur."""
import time
from conftest import docker_exec

MAX_RETRIES = 6
RETRY_DELAY_SECONDS = 10


def _bgp_summary(router: str) -> str:
    return docker_exec(router, 'vtysh -c "show ip bgp summary"').stdout


DOWN_STATES = {"Idle", "Active", "Connect", "OpenSent", "OpenConfirm", "never"}


def _is_established(bgp_summary_output: str) -> bool:
    """Une session BGP est Established si la ligne du neighbor NE contient
    PAS un état textuel de session down (Idle/Active/...). FRR remplace
    la colonne State/PfxRcd par le nombre de préfixes reçus une fois la
    session up — il n'affiche jamais littéralement le mot 'Established'."""
    for line in bgp_summary_output.splitlines():
        line = line.strip()
        if not line or line.startswith(("Neighbor", "IPv4", "BGP", "RIB", "Peers", "Total")):
            continue
        if any(state in line for state in DOWN_STATES):
            return False
        # Ligne neighbor présente, sans état "down" détecté -> Established
        if line[0].isdigit():
            return True
    return False


def _wait_for_established(router: str) -> str:
    last_output = ""
    for _ in range(MAX_RETRIES):
        last_output = _bgp_summary(router)
        if _is_established(last_output):
            return last_output
        time.sleep(RETRY_DELAY_SECONDS)
    return last_output


def test_bgp_session_established(routers_by_name):
    for router in routers_by_name:
        output = _wait_for_established(router)
        assert _is_established(output), (
            f"La session BGP sur {router} n'est pas Established après "
            f"{MAX_RETRIES * RETRY_DELAY_SECONDS}s d'attente.\n"
            f"Sortie obtenue :\n{output}"
        )


def test_bgp_route_learned(routers_by_name):
    names = list(routers_by_name.keys())
    assert len(names) == 2, "Ce test suppose exactement 2 routeurs"
    a, b = names
    # Chaque routeur doit apprendre le préfixe LAN de son voisin via BGP
    pairs = [
        (a, routers_by_name[b]["prefix"]),
        (b, routers_by_name[a]["prefix"]),
    ]
    for router, expected_prefix in pairs:
        result = docker_exec(router, 'vtysh -c "show ip route bgp"')
        assert expected_prefix in result.stdout, (
            f"La route BGP {expected_prefix} n'apparaît pas dans la "
            f"table de routage de {router}.\n"
            f"Sortie obtenue :\n{result.stdout}"
        )
