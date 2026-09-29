> For the complete documentation index, see [llms.txt](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/ubuntu-server-install-windows-11-wsl-w-gpu-support/ubuntu-22.04-24.04-in-place-upgrade-guide.md).

# Ubuntu 22.04 → 24.04 In-Place Upgrade Guide

Platform: Windows 11 | WSL 2 | Docker Desktop

***

### Overview

This guide covers an in-place upgrade of Ubuntu 22.04 LTS (Jammy) to Ubuntu 24.04 LTS (Noble) running under WSL 2 on Windows 11, and the required Docker Desktop steps to restore full functionality afterward.&#x20;

This is a mandatory upgrade for HyperCycle Node Manager V0.5.1 and above. You may use the OS upgrade steps for any installation of Ubuntu, WSL or otherwise. The Docker Desktop steps are WSL specific.&#x20;

> **Note:** An in-place upgrade does **not** rename the WSL distro. It remains `Ubuntu`, not `Ubuntu-24.04`. This matters when re-enabling Docker Desktop's WSL integration later.

***

### 1. Pre-Upgrade Checklist

Run the following inside your Ubuntu WSL terminal before starting:

```bash
# Stop HyperCycle service
sudo systemctl stop hypercycle

# Check current Ubuntu version
lsb_release -a

# Fully update the system
sudo apt update
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoremove -y
```

> **Note:** `apt dist-upgrade` is important before a major version jump — unlike `apt upgrade` it handles dependency changes across packages.

Then reboot before proceeding:

```bash
sudo reboot
```

Once back in Ubuntu, install the upgrade tool and verify the upgrade config:

```bash
# Install the upgrade tool if not present
sudo apt install update-manager-core -y

# Check the release upgrade config
sudo nano /etc/update-manager/release-upgrades
```

Make sure the file contains:

```
Prompt=lts
```

> **Important:** If `Prompt` is set to `never` or `normal`, `do-release-upgrade` will not find the 24.04 path. It must be set to `lts` before continuing.

Finally, confirm the upgrade path is available:

```bash
sudo do-release-upgrade --check-dist-upgrade-only
```

***

### 2. Performing the In-Place Upgrade

#### 2.1 Run the Upgrade

```bash
sudo do-release-upgrade
```

The upgrade tool will walk through several interactive prompts. Expect the following:

* It will ask you to confirm the upgrade from 22.04 to 24.04.
* It may ask how to handle modified configuration files — keeping your existing config is generally safe.
* The process takes 20–40 minutes depending on your connection and system speed.
* At the end we recommend you restart the machine to avoid hangs.

#### 2.2 Verify the Upgrade

Inside the Ubuntu terminal:

```bash
lsb_release -a
# Expected: Ubuntu 24.04 LTS (Noble Numbat)

uname -r
# Verify kernel version
```

***

### 3. Docker Desktop — Reinstall Required

The in-place upgrade has been known to break Docker Desktop's WSL 2 integration. The most reliable fix is a clean uninstall and reinstall.

#### 3.1 (Optional) Export Images and Volumes

If you have Docker images or volumes you want to preserve across the reinstall, export them before uninstalling.&#x20;

**NOTE: Uninstalling Docker Desktop will permanently delete all local images, containers, and volumes.**

```bash
# List all images
docker images

# Save an image to a tar file
docker save -o my-image-backup.tar my-image-name:tag

# List all named volumes
docker volume ls

# Back up a named volume (example using a temp container)
docker run --rm -v my-volume:/data -v $(pwd):/backup ubuntu \
  tar czf /backup/my-volume-backup.tar.gz -C /data .
```

Store the exported `.tar` files somewhere outside of Docker Desktop — your Windows filesystem or a network share.

#### 3.2 Uninstall Docker Desktop

1. Open **Windows Settings → Apps → Installed Apps**
2. Search for **Docker Desktop** and select **Uninstall**
3. Follow the prompts to completion

> **Warning:** Uninstalling Docker Desktop **permanently removes** all images, containers, and volumes stored in its internal VM. Only proceed once you have exported anything you need to keep.

Clean up Docker Desktop's internal WSL distros for a fully fresh slate. From **PowerShell (Administrator)**:

```powershell
wsl --unregister docker-desktop
wsl --unregister docker-desktop-data
```

> **Note:** This does not affect your Ubuntu distro — it only removes Docker Desktop's own internal helper distros.

#### 3.3 Download and Reinstall

Download the latest Docker Desktop installer from Docker's official page:

* **Direct installer link:** `https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe`
* **Official install docs:** `https://docs.docker.com/desktop/setup/install/windows-install/`

During installation, ensure **"Use WSL 2 instead of Hyper-V"** is selected on the configuration page.

#### 3.4 Re-enable WSL Integration

Once Docker Desktop has fully launched:

1. Open **Settings → Resources → WSL Integration**
2. Enable the toggle for **Ubuntu**
3. Click **Apply & Restart** and wait for Docker Desktop to fully reload
4. Verify inside your Ubuntu terminal:

```bash
docker --version
docker run hello-world
```

NOTE: If the terminal hangs or takes too long to open, restart the machine.

#### 3.5 (Optional) Restore Images and Volumes

If you exported images and volumes in step 3.1, restore them now:

```bash
# Restore an image from a tar file
docker load -i my-image-backup.tar

# Recreate a volume and restore its data
docker volume create my-volume
docker run --rm -v my-volume:/data -v $(pwd):/backup ubuntu \
  tar xzf /backup/my-volume-backup.tar.gz -C /data
```

***

### 4. Quick Reference — All Commands

#### Inside Ubuntu WSL

```bash
sudo apt update
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoremove -y
sudo reboot                               # reboot before upgrading
sudo apt install update-manager-core -y
# verify /etc/update-manager/release-upgrades has Prompt=lts
sudo do-release-upgrade
lsb_release -a                            # verify version post-upgrade
docker --version && docker run hello-world  # final verification
```

#### From PowerShell (Administrator)

```powershell
wsl --list --verbose                      # check distro names and state
wsl --shutdown                            # stop all WSL distros
wsl --terminate Ubuntu                    # stop only Ubuntu
wsl -d Ubuntu                             # relaunch Ubuntu

# Clean up Docker Desktop's internal WSL distros (optional):
wsl --unregister docker-desktop
wsl --unregister docker-desktop-data
```
