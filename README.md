# Network Automation Lab

NetDevOps project implementing automated deployment, configuration, and testing of a containerized network infrastructure using Infrastructure as Code (IaC), CI/CD, and automated testing.

![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![FRRouting](https://img.shields.io/badge/Networking-FRRouting-orange)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?logo=githubactions&logoColor=white)
![Ansible](https://img.shields.io/badge/Automation-Ansible-EE0000?logo=ansible&logoColor=white)
![Python](https://img.shields.io/badge/Testing-pytest-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Installation](#installation)
- [Running the infrastructure](#running-the-infrastructure)
- [Ansible automation](#ansible-automation)
- [CI/CD pipeline](#cicd-pipeline)
- [Automated tests](#automated-tests)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## Overview

Network Automation Lab is a NetDevOps experimentation project that automates the deployment, configuration, and validation of a network infrastructure.

Goals:

- Manage infrastructure as code (IaC)
- Automate network configuration
- Validate changes through CI/CD pipelines
- Run automated tests before deployment

The environment reproduces a multi-site network architecture with virtual routers, dynamic routing (OSPF/BGP), and a continuous integration chain.

## Architecture

```
GitHub Repository
        |
        | git push
        v
GitHub Actions Pipeline
        |
   +----+----------+
   |    |          |
  Lint Build      Tests
   |    |          |
   +----+----------+
        |
        v
Docker Network Environment

+---------------------------------------------+
|                                               |
|   Router A  (AS 65001)                       |
|        |  OSPF + BGP                         |
|        |                                     |
|     WAN Transit                              |
|        |                                     |
|        |  OSPF + BGP                         |
|   Router B  (AS 65002)                       |
|                                               |
+---------------------------------------------+
```

## Tech stack

| Area | Technologies |
|---|---|
| Containerization | Docker, Docker Compose |
| Network routing | FRRouting, OSPF, BGP |
| Automation | Ansible |
| CI/CD | GitHub Actions |
| Testing | Python, pytest |
| Version control | Git, GitHub |
| Monitoring (planned) | Prometheus, Grafana |

## Project structure

```
network-automation-lab/
├── .github/
│   └── workflows/
│       └── ci.yml                 # CI/CD pipeline
│
├── infra/
│   ├── docker-compose.yml         # Network topology
│   └── routers/
│       ├── router-a/              # Router A configuration
│       └── router-b/              # Router B configuration
│
├── ansible/
│   ├── inventory.yml              # Network inventory
│   └── playbooks/                 # Configuration automation
│
├── tests/
│   └── test_network.py            # Automated tests
│
├── monitoring/
│   └── prometheus/                # Monitoring (planned)
│
├── docs/
│   └── architecture.md            # Technical documentation
│
├── requirements.txt
└── README.md
```

## Installation

### Requirements

- Docker Engine
- Docker Compose
- Python 3.10+
- Ansible
- Git

### Clone the repository

```bash
git clone https://github.com/maryemn/network-automation-lab.git
cd network-automation-lab
```

### Install Python dependencies

```bash
pip install -r requirements.txt
```

## Running the infrastructure

Start the network environment:

```bash
docker compose up -d
```

Check running containers:

```bash
docker ps
```

Stop the environment:

```bash
docker compose down
```

## Ansible automation

Ansible playbooks automate network configuration (interfaces, routing protocols, BGP policies, etc.).

Example run:

```bash
ansible-playbook -i ansible/inventory.yml ansible/playbooks/deploy.yml
```

## CI/CD pipeline

On every push, the GitHub Actions pipeline runs automatically:

```
git push
   |
   v
GitHub Actions
   |
   +-- Lint   -> YAML file validation
   +-- Build  -> Docker build verification
   +-- Tests  -> deployment + network tests
   |
   v
Final validation
```

Checks performed:

- YAML file validation
- Docker build verification
- Test environment deployment
- Automated network test execution

## Automated tests

Tests validate:

- Connectivity between devices
- Dynamic routing state (OSPF/BGP)
- Network service availability
- Configuration consistency

### Run

```bash
pytest tests/
```

### Example output

```
tests/test_connectivity.py  PASSED
tests/test_routing.py       PASSED
tests/test_services.py      PASSED
```

## Roadmap

| Feature | Status |
|---|---|
| Docker network environment | Done |
| Dynamic routing (OSPF/BGP) | In progress |
| Ansible automation | In progress |
| GitHub Actions pipeline | In progress |
| Automated network tests | Planned |
| Prometheus/Grafana monitoring | Planned |
| Cloud deployment | Planned |

## Contributing

1. Fork the repository
2. Create a branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push the branch (`git push origin feature/my-feature`)
5. Open a pull request

## License

This project is distributed under the MIT License. See the `LICENSE` file for details.

## Author

**Maryem Nasseur**
Engineering student — Networks & DevOps

GitHub: [@maryemn](https://github.com/maryemn)