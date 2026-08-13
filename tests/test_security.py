"""Vérifie l'absence de règles réseau parasites pouvant bloquer le trafic
(cf. bug historique : règles iptables 'raw' résiduelles empêchant la
convergence BGP entre router-a et router-b)."""
import subprocess


def test_no_stale_iptables_raw_rules():
    result = subprocess.run(
        ["sudo", "iptables", "-t", "raw", "-L", "-n"],
        capture_output=True,
        text=True,
    )
    # On s'attend à seulement les chaînes par défaut (PREROUTING, OUTPUT),
    # sans règle DROP/NOTRACK résiduelle qui bloquerait le trafic BGP.
    suspicious_lines = [
        line for line in result.stdout.splitlines()
        if line and not line.startswith("Chain") and not line.startswith("target")
    ]
    assert not suspicious_lines, (
        f"Des règles iptables 'raw' résiduelles ont été détectées, "
        f"elles peuvent bloquer le trafic (BGP notamment) :\n"
        f"{suspicious_lines}"
    )
