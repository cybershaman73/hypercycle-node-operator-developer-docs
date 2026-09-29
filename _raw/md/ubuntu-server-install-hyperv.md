> For the complete documentation index, see [llms.txt](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/ubuntu-server-install-hyperv.md).

# Ubuntu Server Install - HyperV

For Windows 10/11 HyperV (no GPU support)

### <mark style="color:purple;">Download install ISO media to HyperV Host</mark>

[https://releases.ubuntu.com/22.04.5/ubuntu-22.04.5-live-server-amd64.iso](https://www.google.com/url?q=https://releases.ubuntu.com/22.04.5/ubuntu-22.04.5-live-server-amd64.iso\&sa=D\&source=editors\&ust=1757637900704716\&usg=AOvVaw1hzLtxjLlzkYUEx1YpVr5A)

### <mark style="color:purple;">Create new VM</mark>

#### Disk size min = 56GB (256GB better), 4-8 CPU cores, 16GB RAM min (32GB or more better), Accept defaults, download latest installer, username = hyperai, pass=(yours), no LVM group for disk, no Ubuntu Pro.

### <mark style="color:purple;">Access VM via terminal</mark>

Create a terminal window using PuTTy or similar to allow copy/paste commands. Acquire VM IP via HyperV Connect window, login using hyperai credentials:

```
ip a 
```

(usually a 172.x.x.x/20)

4. Update OS packages

```
sudo apt update && sudo apt upgrade -y
```

#### <mark style="color:yellow;">Shutdown VM</mark>

### <mark style="color:purple;">Set VM IP to static on LAN</mark>

1. Open Hyper-V Manager > right-click your host > Virtual Switch Manager.
2. Create a New Virtual Network Switch > choose External.
3. Pick the physical NIC that connects your host to the LAN.
4. Check “Allow management operating system to share this network adapter” if you want the host to keep using it.
5. Assign this new External Switch to your Ubuntu VM’s network adapter. If you get a binding error, make sure the adapter assigned doesn’t have ICS enabled.
6. Start VM

### <mark style="color:purple;">Assign static IP in Ubuntu</mark>

1. Login via terminal to IP obtained from previous step.
2. Disable cloud-init network control:

```
sudo nano /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
```

Add:

```
network: {config: disabled}
```

<mark style="color:yellow;">save it, Ctrl-x, y</mark>

3. Create your own netplan file:

```
sudo nano /etc/netplan/01-netcfg.yaml
```

Add: (choose IP outside of LAN DHCP range, replace 192.168.1.x values with your own LAN network):

```
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: false
      addresses:
        - 192.168.1.50/24
      routes:
        - to: default
          via: 192.168.1.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 1.1.1.1
```

<mark style="color:yellow;">save it, Ctrl-x, y</mark>

4. Lock down permissions and apply:

```
sudo chmod 600 /etc/netplan/01-netcfg.yaml
```

```
sudo netplan apply
```

5. Test network with these commands:

```
ip a
```

```
ip route
```

```
ping 8.8.8.8
```

```
ping google.com
```

### <mark style="color:yellow;">Reboot VM and test connection with new static IP via terminal.</mark>

#### <mark style="color:$success;">**Obtain WAN\_IP for later use in Node Install sequence (take note):**</mark>

```
curl -s ifconfig.me
```

### [<mark style="color:purple;">Proceed to Node Install</mark>](/hypercycle-cbno/u57KauJomd55OVuTYz6e/hypercycle-node-install.md)
