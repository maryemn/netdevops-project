# network-cicd-infra
# 🌐 Network CI/CD Infrastructure

> Pipeline CI/CD complète pour une infrastructure réseau multi-sites automatisée —
> topologie BGP/OSPF, tests réseau automatisés, déploiement reproductible en une commande.

[![CI](https://github.com/AhmedAboutahir/network-cicd-infra/actions/workflows/ci.yml/badge.svg)](https://github.com/AhmedAboutahir/network-cicd-infra/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![FRRouting](https://img.shields.io/badge/Routing-FRRouting-orange)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)
![Ansible](https://img.shields.io/badge/IaC-Ansible-EE0000?logo=ansible&logoColor=white)
![Python](https://img.shields.io/badge/Tests-pytest-3776AB?logo=python&logoColor=white)

---

## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Architecture](#-architecture)
- [Stack technologique](#-stack-technologique)
- [Démarrage rapide](#-démarrage-rapide)
- [Structure du projet](#-structure-du-projet)
- [Pipeline CI/CD](#-pipeline-cicd)
- [Tests automatisés](#-tests-automatisés)
- [Roadmap](#-roadmap)
- [Auteur](#-auteur)

---

## 🎯 Vue d'ensemble

Ce projet reproduit une infrastructure réseau d'entreprise multi-sites entièrement pilotée par une pipeline CI/CD. Chaque modification du code (topologie, config routage, règles firewall) déclenche automatiquement des tests et un déploiement.

**Ce que fait ce projet :**
- Simule deux sites distants interconnectés via BGP eBGP et OSPF
- Déploie toute l'infrastructure en code (IaC) — reproductible en une seule commande
- Exécute une suite de tests réseau automatisés (connectivité, routage, DNS, sécurité)
- Génère un rapport de test HTML accessible depuis GitHub Actions

**Cas d'usage réel :** Ce projet reproduit ce que font des équipes NetDevOps avec des outils comme Batfish, NetBox ou AWX — mais avec une stack 100% open-source, accessible sur un laptop étudiant.

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        GitHub Repository                        │
│                    (Source unique de vérité)                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │ git push
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GitHub Actions Pipeline                       │
│   [lint] → [build] → [deploy topo] → [tests] → [rapport]       │
└──────────────────────────┬──────────────────────────────────────┘
                           │ docker compose up
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                     Infrastructure Docker                        │
│                                                                  │
│  ┌─────────────────┐   172.20.0.0/27   ┌─────────────────┐     │
│  │    Router-A      │◄─────────────────►│    Router-B      │     │
│  │  AS 65001        │    WAN (Transit)   │  AS 65002        │     │
│  │  OSPF + BGP      │                   │  OSPF + BGP      │     │
│  └────────┬─────────┘                   └────────┬─────────┘     │
│           │ 10.10.1.0/24                         │ 10.10.2.0/24  │
│           ▼                                      ▼               │
│      Site A (HQ)                           Site B (Branch)       │
│                                                                  │
│                   ┌──────────────────┐                          │
│                   │  Services (DMZ)   │                          │
│                   │  CoreDNS + Nginx  │                          │
│                   └──────────────────┘                          │
└──────────────────────────────────────────────────────────────────┘
```

| Couche | Composant | Technologie |
|--------|-----------|-------------|
| VCS / GitOps | Repository | GitHub |
| CI/CD | Pipeline | GitHub Actions |
| IaC Réseau | Topologie | Docker Compose + FRRouting |
| IaC Config | Automatisation | Ansible |
| Tests | Validation | pytest + docker SDK |
| DNS / Web | Services | CoreDNS + Nginx |
| Monitoring | Observabilité | Prometheus + Grafana |

---

## 🛠 Stack technologique

| Outil | Usage |
|-------|-------|
| **Docker / Compose** | Conteneurisation de toute l'infrastructure réseau |
| **FRRouting** | Démon de routage open-source — BGP eBGP, OSPF |
| **GitHub Actions** | Orchestration CI/CD — lint, build, test, deploy |
| **Ansible** | Configuration automatisée post-déploiement |
| **pytest + docker SDK** | Tests de connectivité, routage, DNS, sécurité |
| **CoreDNS** | Résolution DNS interne |
| **Nginx** | Serveur web de la DMZ |
| **Prometheus + Grafana** | Monitoring des sessions BGP et métriques réseau |

---

## 🚀 Démarrage rapide

### Prérequis

- Docker Engine 24+ et Docker Compose v2
- Python 3.10+ avec pip
- make (`sudo apt install make`)
- Git

### Installation

```bash
# 1. Cloner le repository
git clone https://github.com/AhmedAboutahir/network-cicd-infra.git
cd network-cicd-infra

# 2. Installer les dépendances Python
pip install -r requirements.txt

# 3. Déployer l'infrastructure
make up

# 4. Lancer les tests
make test

# 5. Arrêter l'infrastructure
make down
```

### Commandes disponibles

```bash
make up        # Démarrer toute l'infrastructure
make down      # Arrêter et nettoyer
make test      # Lancer la suite de tests réseau
make lint      # Valider les fichiers YAML et configs
make ansible   # Appliquer les playbooks Ansible
```

### Vérification manuelle

```bash
# Vérifier la connectivité WAN entre les deux routeurs
docker exec router-a ping -c 3 172.20.0.2
docker exec router-b ping -c 3 172.20.0.5

# Vérifier les tables de routage
docker exec router-a ip route show
docker exec router-b vtysh -c 'show bgp summary'

# Vérifier la résolution DNS
docker exec host-a nslookup web.infra.local
```

---

## 📁 Structure du projet

```
network-cicd-infra/
├── .github/
│   └── workflows/
│       ├── ci.yml          # Pipeline CI principale (lint + build + test)
│       └── deploy.yml      # Pipeline de déploiement (manuel ou on merge)
├── infra/
│   ├── docker-compose.yml  # Topologie réseau complète
│   └── routers/
│       ├── router-a/       # Dockerfile + frr.conf (OSPF + BGP AS65001)
│       └── router-b/       # Dockerfile + frr.conf (OSPF + BGP AS65002)
│   └── services/
│       ├── dns/            # CoreDNS + Corefile
│       └── web/            # Nginx + index.html
├── ansible/
│   ├── inventory.yml       # Inventaire des containers
│   └── playbooks/          # deploy-infra.yml, configure-services.yml
├── tests/
│   ├── conftest.py         # Fixtures pytest
│   ├── test_connectivity.py # Tests ping inter-sites
│   ├── test_routing.py     # Tests BGP/OSPF
│   ├── test_services.py    # Tests DNS + HTTP
│   └── test_security.py    # Tests règles firewall
├── monitoring/
│   ├── prometheus.yml
│   └── grafana/dashboards/
├── docs/
│   ├── architecture.md
│   └── runbook.md
├── scripts/
│   ├── setup.sh
│   └── run-tests.sh
├── Makefile
├── requirements.txt
└── README.md
```

---

## ⚙️ Pipeline CI/CD

La pipeline se déclenche automatiquement sur chaque `push` vers `main` ou `develop` et sur chaque Pull Request.

```
git push
    │
    ▼
┌─────────┐    ┌─────────┐    ┌──────────────┐    ┌────────┐    ┌──────────┐
│  LINT   │───►│  BUILD  │───►│    DEPLOY    │───►│  TEST  │───►│  REPORT  │
│  YAML   │    │ Docker  │    │ docker-compose│    │ pytest │    │ Artifact │
│hadolint │    │ images  │    │    up -d     │    │ réseau │    │  GitHub  │
└─────────┘    └─────────┘    └──────────────┘    └────────┘    └──────────┘
                                                                      │
                                                               always: make down
```

| Étape | Description |
|-------|-------------|
| **Lint** | Validation YAML (yamllint), Dockerfile (hadolint), configs réseau |
| **Build** | `docker compose build` — détecte les erreurs de build |
| **Deploy** | `docker compose up -d` + attente convergence BGP (30s) |
| **Test** | `pytest tests/` — suite réseau complète, rapport HTML généré |
| **Report** | Upload artifact GitHub — rapport accessible dans l'onglet Actions |
| **Teardown** | `docker compose down --volumes` — nettoyage systématique (`if: always()`) |

---

## 🧪 Tests automatisés

La suite de tests valide chaque couche de l'infrastructure :

| Fichier | Couverture | Outils |
|---------|-----------|--------|
| `test_connectivity.py` | Ping inter-sites, latence < 5ms, perte de paquets | subprocess, docker SDK |
| `test_routing.py` | BGP Established, OSPF neighbors, tables de routes | vtysh via docker exec |
| `test_services.py` | DNS nslookup, HTTP 200, résolution interne | requests, subprocess |
| `test_security.py` | Ports fermés, règles iptables, trafic interdit rejeté | scapy, subprocess |
| `test_failover.py` | Convergence BGP < 30s après panne d'un routeur | docker stop, pytest |

Exemple d'exécution :

```bash
$ make test

tests/test_connectivity.py::TestConnectivity::test_site_a_to_wan       PASSED
tests/test_connectivity.py::TestConnectivity::test_site_a_to_site_b    PASSED
tests/test_connectivity.py::TestConnectivity::test_latency_acceptable  PASSED
tests/test_routing.py::TestRouting::test_bgp_established               PASSED
tests/test_routing.py::TestRouting::test_ospf_neighbors                PASSED
tests/test_services.py::TestServices::test_dns_resolution              PASSED
tests/test_services.py::TestServices::test_http_200                    PASSED

7 passed in 12.4s — rapport HTML généré dans reports/
```

---

## 🗺 Roadmap

| Phase | Description | Statut |
|-------|-------------|--------|
| **Phase 1** | Fondations — Docker, FRRouting, topologie WAN, connectivité de base | ✅ En cours |
| **Phase 2** | IaC complète — BGP eBGP, CoreDNS, Nginx, Ansible, variables centralisées | 🔜 À venir |
| **Phase 3** | Pipeline CI/CD — GitHub Actions, lint, build, deploy, rapport de test | 🔜 À venir |
| **Phase 4** | Tests automatisés — connectivité, routage, DNS, sécurité, failover | 🔜 À venir |
| **Phase 5** | Finalisation — README pro, runbook, démo GIF, documentation technique | 🔜 À venir |
| **Bonus** | Monitoring Prometheus/Grafana, Trivy image scanning, Terraform | ⏳ Optionnel |

---

## 👤 Auteur

**Ahmed Aboutahir**
Étudiant ingénieur — Réseaux & DevOps

[![GitHub](https://img.shields.io/badge/GitHub-AhmedAboutahir-181717?logo=github)](https://github.com/AhmedAboutahir)

---

> *Ce projet est conçu pour démontrer des compétences NetDevOps concrètes : IaC, CI/CD, tests réseau automatisés, routage dynamique BGP/OSPF — reproductible en une commande sur n'importe quelle machine.*