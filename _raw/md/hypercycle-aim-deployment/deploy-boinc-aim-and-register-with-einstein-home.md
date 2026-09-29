> For the complete documentation index, see [llms.txt](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/hypercycle-aim-deployment/deploy-boinc-aim-and-register-with-einstein-home.md).

# Deploy Boinc AIM and register with Einstein\@Home

Pre-requisites: CPU ok, NVIDIA GPU for more compute credits

Here we test deployment of an AIM with optional use of GPU. The “<mark style="color:yellow;">boinc-aim</mark>” client application provides computational services for a number of compute projects around the world.

* In this exercise, we’ll be providing computation for <mark style="color:yellow;">Einstein\@Home</mark>. This project searches for weak astrophysical signals from spinning neutron stars (often called pulsars) using data from the LIGO gravitational-wave detectors, the MeerKAT radio telescope, the Fermi gamma-ray satellite, as well as archival data from the Arecibo radio telescope.
* Einstein\@Home also allows us to define how much of our node resources (CPU, RAM) are used for computation.

### <mark style="color:purple;">**1. Open your Ubuntu 22.04.5 LTS app**</mark> and run <mark style="color:yellow;">htop</mark> for a baseline resource utilization check:

```
htop
```

&#x20;(Take note i.e, Tasks=48, Mem=1.33GB, CPUs mostly idle)

### <mark style="color:purple;">**2. Deploy AIM**</mark>

* Goto local PC web browser and open:

<mark style="color:yellow;"><http://LAN-IP:8006/aims></mark>

* Use search box, type *<mark style="color:yellow;">**boinc**</mark>* to display the “boinc-aim”.
* Click on *<mark style="color:blue;">**View**</mark>*
* This will provide AIM Details. Under <mark style="color:yellow;">**Select tag**</mark>, choose version <mark style="color:yellow;">**0.1.0**</mark>
* The node has a range of ports available for aim deployments. Starting with 9000 and going to 9100. The first aim will take port 9000, the second 9001, and so on. The aim slot number is the last number of the port, i.e. port 9000, slot = 0.
* Click on *<mark style="color:green;">**Deploy**</mark>*
* This will initiate downloading the aim image and starting up the aim. Depending on their size (listed under AIM Details), some aim images take a while to download. You can click on the **Back** button to view the deployed machines and their status.&#x20;
  * If you get a "download failed" message, go back to the main AIMs page and click "Retry" under the deployed machines list.&#x20;

<mark style="color:orange;">Alternate command line AIM deploy method</mark>

{% code overflow="wrap" %}

```
curl http://localhost:8005/add_aim -d '{"name": "boinc-aim", "tag": "0.1.0", "port": 9000}'
```

{% endcode %}

### <mark style="color:purple;">**3. Create a new Einstein account**</mark>

<https://einsteinathome.org/>

* After account creation, under this URL:

<https://einsteinathome.org/account/info/edit>

* Find your Weak account key, take note:

i.e. <mark style="color:yellow;">Weak account key</mark> “1054533\_\*\*\*\*\*\*\*\*”

### <mark style="color:purple;">**4. Register your Boinc AIM with Einstein Project URL**</mark>

* Via command line issue the following (make sure you insert your own Weak Account key into the "WEAK\_ACCOUNT\_KEY" field in the command, keep the quotes):

{% code overflow="wrap" %}

```
curl -XPOST http://localhost:8005/aim/0/update_default -d '{"authenticator": "WEAK_ACCOUNT_KEY", "project_url": "https://einsteinathome.org"}'
```

{% endcode %}

* <mark style="color:orange;">Important note</mark>, the aim slot is included in the command. If you chose port 9000 for your aim deployment, then slot = 0, and is found in the command here: localhost:8005/aim/0
* For checking weak authenticator and project on running aim:

```
curl localhost:9000/get_default_task
```

### <mark style="color:purple;">**5. Check Einstein status of Boinc AIM**</mark>

<https://einsteinathome.org/account/dashboard>

* Under **Computers**, the name equals the AIMs container ID via:

```
docker ps
```

* Important note, there’s a lot of good info under Computer details, including a link to its running tasks, those validated, credited, specs of your machine, etc.
* **To change preferences for your AIM, including CPU and RAM usage:**

<https://einsteinathome.org/account/prefs>

Goto <mark style="color:yellow;">Advanced Settings</mark>

(changes take effect next time AIM checks in with account)

### GPU Usage Control

<mark style="color:$danger;">Important note:</mark> GPU usage for Boinc AIM is not controlled via Einstein Advanced Settings (outside of excluding its use under certain  idle user and CPU conditions).  For this reason, the AIM will take 100% of the GPU power. In some cases this can cause overheating or excessive power use. The most reliable way to reduce overall % usage of the GPU is to cap power utilization.

<mark style="color:yellow;">The following commands will only work for bare metal installations. For those of you running WSL, the same commands can be applied via Windows PowerShell as administrator.</mark>

You can check your power limits and range via terminal:

```
nvidia-smi -q -d POWER
```

Then if the default power limit is 250W for example, you can set the power limit to 50% or 125W like this:

```
nvidia-smi -pl 125
```

We can also if desired, have more granular control of GPU clock. Check your GPU clock ranges:

```
nvidia-smi -q -d SUPPORTED_CLOCKS
```

Locking Clocks is optional for finer control. You can fix GPU core/memory clocks to lower values (values given are examples):

```
nvidia-smi --lock-gpu-clocks=900,1200
nvidia-smi --lock-memory-clocks=5000,5000
```
