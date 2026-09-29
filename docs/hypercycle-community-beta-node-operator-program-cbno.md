# HyperCycle Community Beta Node Operator Program (CBNO)

#### Welcome to CBNO. This guide covers most installation scenarios for getting your node running. There are four primary execution environments:

* <mark style="color:$success;">**Bare metal:**</mark> This is the most ideal environment for dedicating all available resources to the node. There is no guide for installing the base OS on Bare metal, we expect you to have a working Ubuntu Server 24.04 LTS command line environment ready for node install.
* <mark style="color:$success;">**Windows WSL:**</mark> Ideal for those who can’t dedicate a whole bare machine to the node. WSL also allows GPU access.
* <mark style="color:$success;">**HyperV:**</mark> Ideal for those familiar with virtual machines that don’t need GPU access. Also suitable for multiple granular test node installations running simultaneously.
* <mark style="color:$success;">**Cloud based:**</mark> Ideal for those familiar with virtual machines who do not have available hardware resources. There is no guide for installing the base OS on Cloud, we expect you to have a working Ubuntu Server 24.04 LTS command line environment ready for node install. Depending on cloud provider and pricing, GPU may be available at your discretion.

<mark style="color:orange;">**Important note:**</mark> The Node Install process will take care of all the essential base OS libraries and dependencies necessary for optimal performance. There’s no need to pre-install those.

### **Minimum Hardware/VM specs:**

* <mark style="color:green;">**amd64/arm64 chipset, 4 CPU, 16GB RAM, 54GB SSD**</mark>

### **Recommended Hardware/VM specs:**

* <mark style="color:green;">**amd64/arm64 chipset, 8 CPU, 32GB RAM, 256GB SSD + NVIDIA GPU 10GB+**</mark>

## <mark style="color:yellow;">Goals checklist for CBNO</mark>

* [ ] Install Node Manager 0.5.0 (or latest)
* [ ] Activate NM with NF or ANFE
* [ ] Deploy AIMs, Web UIs & USDC Payments
* [ ] Upgrade Node Manager to latest version when available

### <mark style="color:yellow;">**Guide links:**</mark>

* Ubuntu Server OS install
  * [<mark style="color:$primary;">Windows WSL with GPU support</mark>](ubuntu-server-install-windows-11-wsl-w-gpu-support.md)
  * [<mark style="color:$primary;">Windows HyperV without GPU</mark>](ubuntu-server-install-hyperv.md)
* [<mark style="color:$primary;">HyperCycle Node install</mark>](hypercycle-node-install.md)
* [Activate Node Manager with NF](activating-your-node-manager-with-node-factory.md)
* [Activate Node Manager with ANFE](activating-your-node-manager-with-anfe.md)
* [HyperCycle AIM Deployment](hypercycle-aim-deployment.md)
