> For the complete documentation index, see [llms.txt](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/hypercycle-developer-guide/aim-building-guide/persistence-and-storage.md).

# Persistence & Storage

This section explains how AIMs use persistent storage **correctly and safely**, and how storage and bandwidth usage can be **tracked and accounted for** using the StorageManager.

Persistence in HyperCycle is **opt-in** and **explicit**. Storage is treated as a **metered resource**, not an implicit capability.

***

### <mark style="color:blue;">Stateless by Default</mark>

By default, AIMs are stateless.

Unless persistence is explicitly enabled:

* Containers may be restarted at any time
* Local filesystem state may be lost
* Execution must be repeatable and idempotent
* No disk writes may be assumed to persist

This is the baseline execution model used by AIMs such as **Tortoise TTS**, where:

* Each request is independent
* All results are returned directly
* No state is carried between calls

***

### <mark style="color:blue;">When Persistence Is Required</mark>

Some AIMs require persistence to function correctly, including:

* Subscription-based services
* AIMs that store user artifacts
* AIMs that download and cache large assets
* AIMs that expose file listings or retrieval endpoints
* AIMs that meter storage or bandwidth usage over time

In these cases, persistence must be **explicitly declared** and **accounted for**.

***

### <mark style="color:blue;">Persistent Volumes (</mark><mark style="color:blue;">`/container_mount`</mark><mark style="color:blue;">)</mark>

When defined within the AIM's Dockerfile as label:

```
LABEL PERSIST_VOLUME=1
```

the Node Manager mounts a persistent volume into the AIM container at:

```
/container_mount
```

This directory:

* Persists across container restarts
* Is managed by the Node Manager
* Is the **only** location intended for durable storage

AIM authors must:

* Write persistent data only inside `/container_mount`
* Treat all other filesystem paths as ephemeral
* Remain functional if persistence is unavailable

***

### <mark style="color:blue;">StorageManager: Accounting for Storage and Bandwidth</mark>

This guide introduces the **StorageManager** abstraction to support AIMs that need to:

* Track stored data size
* Track bandwidth usage
* Associate usage with a specific user or license
* Report usage back to the Node Manager for accounting

This allows storage to participate in the same **metered resource model** as execution.

***

### <mark style="color:yellow;">Conceptual Storage & Accounting Flow</mark>

{% @mermaid/diagram content="flowchart TD
NM\[Node Manager]

```
subgraph AIM["AIM Container"]
    E[Endpoint Execution]
    SM[StorageManager]
    FS[/container_mount/]
end

NM --> E
E --> SM
SM --> FS
SM -->|usage metrics| E
E -->|usage report| NM
```

" %}

Key properties:

* Storage access flows through StorageManager
* Storage usage is measured, not assumed
* Bandwidth and disk usage can be reported alongside execution cost

***

### <mark style="color:blue;">What StorageManager Tracks</mark>

Using StorageManager, an AIM can track:

* Bytes written
* Bytes read
* Total storage consumed
* Bandwidth usage over time

This enables:

* Fair pricing for storage-heavy AIMs
* Subscription models that include quotas
* Enforcement by the Node Manager without AIM-side billing logic

The AIM **reports usage** — it does not deduct balances.

***

### <mark style="color:blue;">Persistence and Cost Semantics</mark>

Storage and bandwidth usage follow the same rules as execution cost:

* `cost_only` requests must never write to storage
* Cost estimation must not depend on stored state
* Usage is reported after execution
* Pricing remains deterministic from inputs + measured usage

Caching may improve performance, but must never:

* Affect cost estimation
* Introduce hidden state
* Leak data across users

***

### <mark style="color:blue;">Persistence in Subscription-Based AIMs</mark>

Subscription-based AIMs commonly rely on persistence to:

* Store user artifacts
* Track subscription-scoped data
* Enforce quotas (storage, bandwidth, usage limits)

In this model:

* Persistence is part of the **service contract**
* Storage usage contributes to ongoing cost
* The Node Manager enforces limits using reported usage

AIMs must document:

* What data is stored
* How long it persists
* How usage is measured

***

### <mark style="color:blue;">Safety and Isolation</mark>

AIM authors must ensure:

* User data is logically isolated
* Stored artifacts are scoped correctly
* No cross-user leakage occurs
* Storage paths are predictable and controlled

Persistence increases responsibility and must be used deliberately.

***

### <mark style="color:blue;">Tortoise TTS and Storage (Baseline)</mark>

The Tortoise TTS AIM does **not** use persistence:

* Audio output is generated in memory
* Temporary files are discarded
* No data is written to `/container_mount`

This makes it a good baseline before introducing stateful AIM patterns.

***

### <mark style="color:blue;">Summary</mark>

Persistence in HyperCycle is:

* Explicit, not implicit
* Metered, not free
* Accounted for using StorageManager
* Enforced by the Node Manager

Key takeaways:

* Stateless is the default
* `/container_mount` is the only durable path
* Storage and bandwidth are first-class resources
* AIMs report usage, never enforce billing

***

### <mark style="color:blue;">What’s Next</mark>

The next section builds on persistence to explain **long-lived economic relationships**:

[<mark style="color:yellow;">**Subscriptions & Pricing Models**</mark>](/hypercycle-cbno/u57KauJomd55OVuTYz6e/hypercycle-developer-guide/aim-building-guide/subscriptions-and-pricing-models.md)

That section covers:

* Per-call vs subscription services
* How storage and bandwidth fit into subscriptions
* How AIMs participate without enforcing payments
