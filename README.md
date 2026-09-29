# HyperCycle CBNO and Developer Guides (archive)

Archived copy of <https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/>, captured 2026-09-29T20:54:43+00:00.

Pages are in `docs/`, images in `assets/`, and untouched originals in `_raw/`.
`SOURCES.json` records each file's source URL and checksum.


## CBNO-V1

- [HyperCycle Community Beta Node Operator Program (CBNO)](docs/hypercycle-community-beta-node-operator-program-cbno.md)
- [Ubuntu Server install - Windows 11 WSL w/GPU Support](docs/ubuntu-server-install-windows-11-wsl-w-gpu-support.md)
  - [Remove WSL (Windows Subsystem for Linux)](docs/ubuntu-server-install-windows-11-wsl-w-gpu-support/remove-wsl-windows-subsystem-for-linux.md): For troubleshooting and other cases where you want a fresh install, follow these steps to remove WSL from your system.
  - [Ubuntu 22.04 → 24.04 In-Place Upgrade Guide](docs/ubuntu-server-install-windows-11-wsl-w-gpu-support/ubuntu-22.04-24.04-in-place-upgrade-guide.md): Platform: Windows 11 | WSL 2 | Docker Desktop
- [Ubuntu Server Install - HyperV](docs/ubuntu-server-install-hyperv.md): For Windows 10/11 HyperV (no GPU support)
- [HyperCycle Node Install](docs/hypercycle-node-install.md)
  - [Upgrade Node](docs/hypercycle-node-install/upgrade-node.md)
- [Activating your Node Manager with Node Factory](docs/activating-your-node-manager-with-node-factory.md)
- [Activating your Node Manager with ANFE](docs/activating-your-node-manager-with-anfe.md)
- [HyperCycle AIM Deployment](docs/hypercycle-aim-deployment.md)
  - [Deploy Boinc AIM and register with Einstein@Home](docs/hypercycle-aim-deployment/deploy-boinc-aim-and-register-with-einstein-home.md): Pre-requisites: CPU ok, NVIDIA GPU for more compute credits
  - [Deploy Tortoise Text-to-Speech AIM w/Voiceboard UI & USDC Payments](docs/hypercycle-aim-deployment/deploy-tortoise-text-to-speech-aim-w-voiceboard-ui-and-usdc-payments.md): Pre-requisites: NVIDIA GPU with 10GB VRAM.
  - [Deploy Ollama AIM w/UI & USDC Payments](docs/hypercycle-aim-deployment/deploy-ollama-aim-w-ui-and-usdc-payments.md): Pre-requisites: CPU ok for smaller models, NVIDIA GPU recommended.
  - [Deploy Litellm AIM w/UI & USDC Payments](docs/hypercycle-aim-deployment/deploy-litellm-aim-w-ui-and-usdc-payments.md): Compatibility: Can be run on AMD64 & ARM64 architectures and HyperAI Boxes.

## HyperCycle Developer Guide

- [Developer Build Guide](docs/hypercycle-developer-guide/developer-build-guide.md): Architecture, APIs, and AIM Building Guide
- [HyperCycle APIs](docs/hypercycle-developer-guide/hypercycle-apis.md)
- [AIM Building Guide](docs/hypercycle-developer-guide/aim-building-guide.md)
  - [AIM Structure & Files](docs/hypercycle-developer-guide/aim-building-guide/aim-structure-and-files.md)
    - [AIM Dockerfile](docs/hypercycle-developer-guide/aim-building-guide/aim-structure-and-files/aim-dockerfile.md): Additional details and labels
    - [AIM manifest.json](docs/hypercycle-developer-guide/aim-building-guide/aim-structure-and-files/aim-manifest-json.md): Comprehensive walkthrough on how to document your REST APIs in a manifest.json style. Examples used in this walkthrough do NOT pertain to the Tortoise TTS AIM used elsewhere in this guide.
    - [AIM main.py](docs/hypercycle-developer-guide/aim-building-guide/aim-structure-and-files/aim-main.py.md): Tortoise TTS AIM main.py
    - [AIM Health Check](docs/hypercycle-developer-guide/aim-building-guide/aim-structure-and-files/aim-health-check.md)
  - [Endpoint Declaration & Cost Logic](docs/hypercycle-developer-guide/aim-building-guide/endpoint-declaration-and-cost-logic.md)
  - [Concurrency & Queues](docs/hypercycle-developer-guide/aim-building-guide/concurrency-and-queues.md)
  - [Persistence & Storage](docs/hypercycle-developer-guide/aim-building-guide/persistence-and-storage.md)
    - [Example CDN AIM](docs/hypercycle-developer-guide/aim-building-guide/persistence-and-storage/example-cdn-aim.md): Content Delivery Network (CDN) AIM example
      - [CDN AIM main.py](docs/hypercycle-developer-guide/aim-building-guide/persistence-and-storage/example-cdn-aim/cdn-aim-main.py.md): Content Delivery Network (CDN) AIM main.py example used to demonstrate SubscriptionManager, DiskSpaceManager and StorageManager services within the Node Manager.
  - [Subscriptions & Pricing Models](docs/hypercycle-developer-guide/aim-building-guide/subscriptions-and-pricing-models.md)
  - [External Ports & Secure Access](docs/hypercycle-developer-guide/aim-building-guide/external-ports-and-secure-access.md)
    - [Secure Access with SSH Port Forwarding](docs/hypercycle-developer-guide/aim-building-guide/external-ports-and-secure-access/secure-access-with-ssh-port-forwarding.md)
- [Security Layers (Conceptual Overview)](docs/hypercycle-developer-guide/security-layers-conceptual-overview.md)
- [Reference](docs/hypercycle-developer-guide/reference.md)
  - [pyhypercycle-aim Library Usage](docs/hypercycle-developer-guide/reference/pyhypercycle-aim-library-usage.md): HyperCycle python library simplifies building the AIM's HTTP server.
  - [Session Creation Workflow](docs/hypercycle-developer-guide/reference/session-creation-workflow.md)
