# Upgrade Node

### **Upgrade node version**

<mark style="color:red;">**Wait for release instructions before following these steps.**</mark>&#x20;

* There are two ways to upgrade, via node manager admin panel and command line:

#### <mark style="color:purple;">VIa Node Manager Admin Panel</mark>

* Access via <mark style="color:yellow;"><http://LAN-IP:8006></mark>
* Goto Settings page and look for the Version block lower left side of page.&#x20;
* Click on upgrade. The process is silent. You'll see the page refresh after a few minutes and the new node version display on the home page.

#### <mark style="color:purple;">Via Command Line</mark>

Login as hypercycle user, obtain desired version from release bucket (change tar file version to match latest):

```
sudo su hypercycle
```

<mark style="color:yellow;">Note: Always confirm your file versions before copy/pasting commands, these are non-working examples.</mark>

```
cd /home/hypercycle/

wget https://hypercycle-release.s3.us-east-2.amazonaws.com/hypercycle-0.5.1-x86.tar
```

Change directory to current node manager folder (yours may differ from example below):

```
cd /home/hypercycle/hypercycle-manager-0.5.0
```

Run upgrade script with current version and desired upgrade version:

```
sudo ./upgrade.sh 0.5.0 0.5.1-x86
```

After the upgrade runs, check version:

{% code overflow="wrap" %}

```
curl -s http://localhost:8000/info | awk -F'"node_version":"' '{print $2}' | awk -F'"' '{print $1}'
```

{% endcode %}

Clear out old manager versions that may still be running:

```
sudo systemctl stop hypercycle
```

```
sudo pkill -9 -f python3
```

```
sudo systemctl start hypercycle
```
