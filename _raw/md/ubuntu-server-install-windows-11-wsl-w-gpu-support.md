> For the complete documentation index, see [llms.txt](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/ubuntu-server-install-windows-11-wsl-w-gpu-support.md).

# Ubuntu Server install - Windows 11 WSL w/GPU Support

Pre-requisites:&#x20;

* Windows 11 with latest security and OS updates.&#x20;
* 20GB free disk space.&#x20;
* Optional: NVIDIA GPU.

#### <mark style="color:$success;">Estimated time to complete: 15-30min</mark>

### <mark style="color:purple;">1.</mark> <mark style="color:purple;"></mark><mark style="color:purple;">**Enable NVIDIA GPU Passthrough**</mark> <a href="#r5pjkuf1oqni" id="r5pjkuf1oqni"></a>

If you have an NVIDIA GPU in your system, make sure Windows NVIDIA drivers are installed (latest Game Ready or Studio driver).\
👉 Download:[ https://www.nvidia.com/Download<br>](https://www.nvidia.com/Download)This also installs CUDA WSL components if available.

### <mark style="color:purple;">**2. Enable Required Windows Features**</mark> <a href="#aqeiiyfor70u" id="aqeiiyfor70u"></a>

Open **PowerShell** as Administrator and run:

{% code overflow="wrap" fullWidth="false" %}

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

{% endcode %}

{% code overflow="wrap" %}

```powershell
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

{% endcode %}

#### <mark style="color:yellow;">R</mark><mark style="color:yellow;">**eboot**</mark> <mark style="color:yellow;"></mark><mark style="color:yellow;">your PC.</mark>

### <mark style="color:purple;">**3. Install WSL & Ubuntu 24.04**</mark> <a href="#w7y976thhqjn" id="w7y976thhqjn"></a>

Open **PowerShell** as Administrator and run:

```
wsl --set-default-version 2
```

```
wsl --install -d Ubuntu-24.04
```

NOTE: This step may require a reboot mid-process, make sure to save all work before running it. It is recommended that nothing else is running while performing this installation.

<mark style="color:green;">Enter new UNIX username:</mark> <mark style="color:yellow;">hyperai</mark>

<mark style="color:green;">New password:</mark> \[enter your own] (confirm)

Type <mark style="color:yellow;">exit</mark> to leave the Ubuntu shell and go back to PowerShell.

```
wsl --set-default Ubuntu-24.04
```

Check version:

```
wsl --version
```

Make sure ‘WSL version 2.5’ or higher is shown. If not:

```
wsl --set-default-version 2
```

### <mark style="color:purple;">**4. Update Ubuntu, Network & Basic Tools**</mark> <a href="#ygtx1tpqnhpd" id="ygtx1tpqnhpd"></a>

* In Windows search for <mark style="color:yellow;">Ubuntu 24.04</mark> and pin the startup icon to your taskbar and launch.

#### Enable nvidia-smi in WSL via symbolic link

```
sudo ln -s /usr/lib/wsl/lib/nvidia-smi /usr/bin/nvidia-smi
```

Test NVIDIA GPU passthrough (you'll see  table with driver version, model, temp, usage, etc):

```
nvidia-smi
```

#### Disable IPv6:

```
sudo nano /etc/sysctl.conf
```

Add these lines at the end and save, Ctrl-x, y:

```
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
```

Apply changes:

```
sudo sysctl -p
```

Verify:

```
cat /proc/sys/net/ipv6/conf/all/disable_ipv6
```

Should show <mark style="color:yellow;">1</mark>

#### Update DNS to stop WSL from auto-generating the resolver:

```
sudo nano /etc/wsl.conf
```

Add to this file these two lines and save, Ctrl-x, y:

```
[network]
generateResolvConf = false
```

Replace resolv.conf:

```
sudo rm /etc/resolv.conf
```

```
sudo nano /etc/resolv.conf
```

Add these two lines and save, Ctrl-x, y:

```
nameserver 1.1.1.1
nameserver 8.8.8.8
```

Shutdown WSL via PowerShell:

```
wsl --shutdown
```

Relaunch Ubuntu via startup icon.

#### Update system:

```
sudo apt update && sudo apt upgrade -y
```

#### Check Ubuntu version:

```
lsb_release -a
```

Should have output:

<mark style="color:green;">Distributor ID: Ubuntu</mark>

<mark style="color:green;">Description: Ubuntu 24.04.4 LTS</mark>

<mark style="color:green;">Release: 24.04</mark>

<mark style="color:green;">Codename: noble</mark>

### <mark style="color:purple;">**5. Install Docker Desktop (Windows)**</mark> <a href="#dnhsm9gxc3c0" id="dnhsm9gxc3c0"></a>

1. Download & install from[ https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. During setup:
   * Use WSL2 is checked
3. After install, open Docker Desktop
   * Accept License, Skip Personal setup
   * Goto > Settings > General:
     * Enable Start Docker Desktop when you sign in
     * Disable Open Docker Dashboard
4. Under Settings > Resources > WSL integration:
   * Enable integration with my default WSL distro
   * Click Apply, exit

### <mark style="color:purple;">**6. Auto-start Fix (WSL waits for Docker)**</mark> <a href="#gh2z16vybm6e" id="gh2z16vybm6e"></a>

Sometimes WSL starts before Docker Desktop. Edit bash shell:

```
sudo nano ~/.bashrc
```

Add this to the end your Ubuntu shell config and save Ctrl-x, y:

```
# Ensure Docker is running before using it
if ! docker info >/dev/null 2>&1; then
  echo "⏳ Waiting for Docker Desktop to start..."
  while ! docker info >/dev/null 2>&1; do
    sleep 1
  done
  echo "✅ Docker is now available."
fi
```

#### <mark style="color:$success;">**Obtain WAN\_IP for later use in Node Install sequence (take note):**</mark>

```
curl -s ifconfig.me
```

#### <mark style="color:yellow;">**Reboot PC.**</mark>

#### [<mark style="color:purple;">**Proceed to Node Install**</mark>](/hypercycle-cbno/u57KauJomd55OVuTYz6e/hypercycle-node-install.md)

### <mark style="color:$info;">Optional: Customize WSL resource usage & limits</mark>

By default WSL will use up to 80% of available RAM and CPU resources. Storage is assigned dynamically with no hard limit on how much of the storage it can use. If you want to have more control over these variables, create a file with Notepad called <mark style="color:yellow;">.wslconfig</mark> (no file extension) and save it to your Windows user profile folder, usually C:\Users\\%UserProfile%

Here's an example <mark style="color:yellow;">.wslconfig</mark> file you can modify as desired:

```
[wsl2]
# Limit WSL memory to 8 GB (adjust if you have more/less system RAM)
memory=32GB  

# Set how many CPU cores WSL can use (or omit to allow all)
processors=8  

# Enable/disable swap and size (helps prevent OOM in heavy workloads)
swap=8GB  

# Location of swap file (optional, defaults inside AppData\Local\Temp)
# swapfile=C:\\Users\\<YourUser>\\wsl-swap.vhdx  

# Disable page reporting for a small perf boost
# pageReporting=false  

# Ensure GPU compute (CUDA, DirectML) is available to WSL2
gpu=true  

# Allow WSL to grow its virtual disk dynamically up to a limit
# (default is no hard limit, but you can cap it here)
# For example, cap at 100GB:
disk=108GB

```

After creating this file, shutdown and restart your Ubuntu 24.04 session. To shutdown, open Powershell as Administrator:

```
wsl --shutdown
```
