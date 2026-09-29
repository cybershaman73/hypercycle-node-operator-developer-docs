> For the complete documentation index, see [llms.txt](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/hypercycle-node-install.md).

# HyperCycle Node Install

Pre-requisites:&#x20;

* ***Ubuntu Server 24.04*** LTS with latest updates.&#x20;
* 20GB free disk space, recommend 54GB or more if running AIMs.&#x20;
* Optional: NVIDIA GPU.

#### <mark style="color:$success;">Estimated time to complete: 5-10min</mark>

## <mark style="color:purple;">**Install Node Manager**</mark> (v0.5.1 at time of this guide):

* Follow these steps for all Ubuntu 24.04 LTS ready installations regardless of platform (i.e. WSL, HyperV, Cloud or Bare-metal):

{% code overflow="wrap" %}

```
wget https://hypercycle-release.s3.us-east-2.amazonaws.com/downloader.sh && chmod a+x downloader.sh && sudo ./downloader.sh
```

{% endcode %}

## Installation Prompts

* During installation, you will be prompted for several inputs:

### <mark style="color:purple;">**1. MongoDB Installation**</mark>

* MongoDB is required. Accept the default (y) unless you already have a MongoDB installation. Recommended to install it anyway.

```
Use a system mongo install [y/n]? (Default: y) y
```

### <mark style="color:purple;">**2. NVIDIA Driver Installation**</mark>

* If your machine has a NVIDIA GPU ***AND*** you are *NOT* using Windows WSL or HyperV, choose y. Otherwise, choose n.

```
Install nvidia drivers [y/n]? (Default: y)
```

(if you select yes, it will take a while)

* Towards the end of this step, you may see a prompt for how to handle a <mark style="color:yellow;">/etc/docker/daemon.json</mark> file.  Choose to keep the currently installed version, N.

### <mark style="color:purple;">**3. Node Configuration**</mark>

* You'll be asked to configure basic settings. These can be updated later in the config.yaml file located at <mark style="color:yellow;">/home/hypercycle/config/config.yaml</mark>
* Network: Choose whether the node should connect to the testnet (recommended for development) or mainnet. For CBNO we are connecting to mainnet:

```
Network connecting to (testnet or mainnet): mainnet
```

* Set the externally visible address of your node. Use <mark style="color:yellow;">localhost</mark> if running locally for development and testing. For CBNO and mainnet, use [<mark style="color:$success;">WAN\_IP</mark>](/hypercycle-cbno/u57KauJomd55OVuTYz6e/ubuntu-server-install-windows-11-wsl-w-gpu-support.md#obtain-wan_ip-for-later-use-in-node-install-sequence-take-note) obtained prior to start of node install:

{% code overflow="wrap" %}

```
Externally visible node address (for example: "34.31.18.244" or "node.myserver.com"): WAN_IP
```

{% endcode %}

* Choose a port. <mark style="color:yellow;">Default is 8000</mark>. Save this value for future use:

```
External port used for the node (default 8000): 8000
```

* Set the replica number. Use <mark style="color:yellow;">0</mark> if unsure (this makes it the primary node).

```
Replica Number (0 = primary, 1+ = replicas, default = 0): 0
```

#### <mark style="color:orange;">**After install completes, reboot the PC.**</mark>

### **Test for Node&#x20;**<mark style="color:yellow;">**alive**</mark>**&#x20;status**

```
curl -X GET localhost:8000/info
```

Will look like this:

<mark style="color:$info;">{"status":"alive","name":"Hypercycle Node"......}</mark>

### **Login to Node Manager Admin Panel**

* Locate the node’s LAN IP via command line:

```
ip a
```

(LAN-IP will be commonly listed under interface <mark style="color:yellow;">eth0</mark> on the <mark style="color:yellow;">inet</mark> line, i.e. 172.27.126.244)

* Goto Admin Panel web page

<mark style="color:yellow;"><http://LAN-IP:8006></mark>

#### [***Activate your node with Node Factory***](/hypercycle-cbno/u57KauJomd55OVuTYz6e/activating-your-node-manager-with-node-factory.md)

#### [***Activate your node with ANFE***](/hypercycle-cbno/u57KauJomd55OVuTYz6e/activating-your-node-manager-with-anfe.md)

#### [*<mark style="color:green;">**Setting up Payment Engine**</mark>*](/hypercycle-cbno/u57KauJomd55OVuTYz6e/hypercycle-aim-deployment.md#setting-up-payment-engine-1)
