# Remove WSL (Windows Subsystem for Linux)

For troubleshooting and other cases where you want a fresh install, follow these steps to remove WSL from your system.

#### List installed distributions via PowerShell in admin mode:

```
wsl --list --verbose
```

Example output:

<mark style="color:green;">NAME                    STATE    VERSION</mark>

<mark style="color:green;">Ubuntu-24.04     Stopped         2</mark> &#x20;

#### Unregister (delete) each distro including docker-desktop:

```
wsl --unregister Ubuntu-24.04
```

```
wsl --unregister docker-desktop
```

<mark style="color:red;">**This deletes the Linux filesystem and all data inside it!**</mark>

#### **Uninstall WSL and Docker Desktop apps**

* Open Start > Installed Apps (or Settings > Apps > Installed apps)
* Search for **Windows Subsystem for Linux** **Update** and **Ubuntu 24.04.4 LTS**
* Click **Uninstall for each**
* Search for **Docker Desktop**, click **Uninstall**

#### **Disable Windows features**

Open PowerShell as Administrator and run:

```
dism.exe /online /disable-feature /featurename:VirtualMachinePlatform /norestart
```

```
dism.exe /online /disable-feature /featurename:Microsoft-Windows-Subsystem-Linux /norestart
```

<mark style="color:yellow;">**Reboot PC.**</mark>
