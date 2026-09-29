# Example CDN AIM

Content Delivery Network (CDN) AIM example

## <mark style="color:yellow;">Example: A Simple CDN AIM</mark>

This example demonstrates a **stateful, subscription-based AIM** that uses persistent storage, bandwidth accounting, and public file serving.

It builds on the persistence concepts introduced earlier and shows how:

* Disk space is allocated per user
* Bandwidth is metered and enforced
* Subscriptions control lifecycle and cleanup
* Storage and bandwidth participate in the cost model

The CDN AIM's complete main.py is [here](../../../hypercycle-developer-guide/aim-building-guide/persistence-and-storage/example-cdn-aim/cdn-aim-main.py.md).

***

### <mark style="color:blue;">Overview</mark>

The CDN AIM exposes the following endpoints:

* **`/allocate`**\
  Allocate disk space and/or bandwidth for a user
* **`/get_subscription`**\
  Query current disk subscriptions and bandwidth usage
* **`/upload_file`**\
  Upload or delete files within an allocated disk
* **`re:/data/(.*)`**\
  Public endpoint for serving stored files and metering bandwidth

Together, these endpoints implement a minimal content delivery service with **persistent state and economic enforcement**.

***

### <mark style="color:blue;">Key Components Used</mark>

This AIM combines several core HyperCycle abstractions:

* **SubscriptionManager**\
  Tracks subscription lifetime and metadata
* **DiskSpaceManager**\
  Creates and removes disk volumes
* **StorageManager**\
  Tracks bandwidth usage as a metered resource

Each component has a distinct responsibility, and no single class enforces everything.

***

### <mark style="color:blue;">Allocating Storage and Bandwidth (</mark><mark style="color:blue;">`/allocate`</mark><mark style="color:blue;">)</mark>

The `/allocate` endpoint allows a user to:

* Create a disk of a given size
* Specify how long the disk should exist
* Allocate bandwidth quota

#### <mark style="color:blue;">Cost Estimation and Execution</mark>

As with all AIM endpoints, `/allocate` supports `cost_only`:

```python
if request.headers.get("cost_only"):
    return JSONResponseCORS({"costs": costs_only})
```

Costs are calculated based on:

* Disk size × subscription duration
* Allocated bandwidth

Execution is skipped entirely during cost estimation.

***

### <mark style="color:blue;">Disk Creation and Subscription Tracking</mark>

When execution proceeds, the AIM:

1. Derives a **subscription key** from the user address and disk name
2. Creates a subscription using `SubscriptionManager`
3. Creates a physical disk using `DiskSpaceManager`

```python
DiskSubscriptionManager.add_subscription(
    key,
    {"address": user_address, "space": space, "name": name, "disk_id": disk_id},
    delete_on_expire=True,
    months=months
)

DiskSpaceManager.add_disk("1K", size // 1024, disk_id)
```

This separation ensures:

* Subscription logic is decoupled from disk management
* Cleanup can occur automatically on expiration

***

### <mark style="color:blue;">Tracking Bandwidth Usage with StorageManager</mark>

Bandwidth usage is tracked independently using `StorageManager`.

When bandwidth is allocated:

```python
value = StorageManager.get(user_address, "bandwidth", 0)
StorageManager.store(user_address, "bandwidth", value + bandwidth)
```

When a file is downloaded, bandwidth is **consumed**:

```python
value = StorageManager.get(user_address, "bandwidth", 0)
if value >= bandwidth:
    StorageManager.store(user_address, "bandwidth", value - bandwidth)
else:
    return HTMLResponse("Resource bandwidth not allocated.", status=402)
```

This makes bandwidth:

* A finite, enforceable resource
* Independent of disk allocation
* Fully metered and auditable

***

### <mark style="color:blue;">File Upload and Management (</mark><mark style="color:blue;">`/upload_file`</mark><mark style="color:blue;">)</mark>

The `/upload_file` endpoint allows users to:

* Upload files into their allocated disk
* Delete files and clean up empty directories

All files are written under:

```
/container_mount/disk_mounts/<disk_id>/
```

This ensures:

* Persistence across container restarts
* Isolation between users
* Predictable storage layout

If a subscription does not exist, the request fails.

***

### <mark style="color:blue;">Public File Serving with Regex Endpoints</mark>

The CDN AIM exposes a public download endpoint using a **regex URI**:

```python
@aim_uri(uri="re:/data/(.*)", methods=["GET"], is_public=True)
```

Important properties:

* `re:` indicates a regex-based route
* The Node Manager matches the URI dynamically
* No authentication is required
* Bandwidth is still enforced per user

Each download:

* Resolves the owning user
* Checks remaining bandwidth
* Deducts usage
* Returns the file or an error

This pattern enables **public content delivery with private billing**.

***

### <mark style="color:blue;">Subscription Expiry and Cleanup</mark>

Unlike simple subscription-gated AIMs, this AIM must **remove state** when a subscription expires.

To accomplish this, it defines a custom `SubscriptionManager` with a removal callback:

```python
class DiskSubscription(SubscriptionManager):
    @classmethod
    def remove_callback(cls, key):
        subscription = cls.get_subscription(key)
        DiskSpaceManager.remove_disk("1K", size // 1024, disk_id)
```

A background loop runs on startup:

```python
async def on_startup(self):
    async def loop():
        while True:
            DiskSubscriptionManager.check_all_subscriptions()
            await asyncio.sleep(20)
    asyncio.create_task(loop())
```

This ensures:

* Expired disks are removed automatically
* Storage does not leak
* Subscription state remains authoritative

***

### <mark style="color:blue;">Dockerfile Requirement: Privileged Mode</mark>

Because this AIM mounts disks inside the container, its Dockerfile must include:

```
LABEL PRIVILEGED=1
```

Without this label:

* DiskSpaceManager cannot mount volumes
* Disk allocation will fail

This requirement must be documented clearly by the AIM author.

***

### <mark style="color:blue;">What This Example Demonstrates</mark>

This CDN AIM shows how to build a **fully stateful, economically enforced service**:

* Persistence is explicit and scoped
* Storage and bandwidth are metered
* Subscriptions control lifecycle
* Cleanup is automated
* Public access does not bypass accounting

It represents the **upper bound of AIM complexity** before introducing distributed or multi-node patterns.

***

### <mark style="color:blue;">Summary</mark>

Key takeaways from this example:

* Persistence is a contract, not an assumption
* StorageManager tracks usage, not files
* SubscriptionManager governs lifecycle
* DiskSpaceManager handles physical resources
* AIMs report usage — Node Managers enforce it

This pattern is suitable for:

* CDN-style services
* Hosting platforms
* Artifact repositories
* Subscription-backed storage AIMs

***

### <mark style="color:blue;">What’s Next</mark>

The next section steps back from storage and focuses on **economic structure**:

[<mark style="color:yellow;">**Subscriptions & Pricing Models**</mark>](../../../hypercycle-developer-guide/aim-building-guide/subscriptions-and-pricing-models.md)

That section explains:

* Per-call vs subscription AIMs
* How pricing integrates with persistence
* How AIMs remain enforcement-free
