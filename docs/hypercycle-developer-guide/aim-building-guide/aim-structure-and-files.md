# AIM Structure & Files

This section describes the **required file structure** of an AIM, how each file participates in runtime behavior, and how Node Managers and tooling interact with these artifacts.

All subsequent AIM Building sections reference the **same canonical AIM** unless explicitly stated otherwise.

### <mark style="color:blue;">Canonical AIM Example: Tortoise TTS AIM</mark>

Throughout this guide, we use the following canonical example:

> **Tortoise TTS AIM**\
> A GPU-backed, per-call, stateless text-to-speech service built on the Tortoise TTS model.

This AIM was chosen because it represents a **realistic production deployment**:

* Requires GPU acceleration
* Uses external model assets (voices)
* Implements `cost_only`
* Returns usage metrics
* Does **not** require persistence or subscriptions

It sits at the midpoint between “hello world” and advanced infrastructure AIMs.

> ⚠️ When a feature requires additional structure (subscriptions, persistence, external ports, SSH), the guide will introduce a **specialized example** and clearly label it.

***

### <mark style="color:blue;">Minimal AIM Directory Layout</mark>

The Tortoise TTS AIM follows the standard AIM layout:

```
aim/
├── Dockerfile
├── requirements.txt
├── manifest.json
├── app/
│   └── main.py
└── extra-voices/
    └── ...
```

### <mark style="color:blue;">Dockerfile</mark>

The `Dockerfile` defines the AIM’s **runtime environment**, hardware requirements, and startup behavior.

#### <mark style="color:yellow;">Example: Tortoise TTS Dockerfile (Canonical)</mark>

```
FROM nvidia/cuda:12.6.2-base-ubuntu22.04

ENV DEBIAN_FRONTEND=1

LABEL GPUS=1
LABEL GPU_MEMORY=8GB
LABEL description="Tortoise TTS-based text-to-speech."

WORKDIR /opt

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev \
    build-essential \
    cmake \
    git \
    curl \
    ffmpeg \
    sox \
    ca-certificates \
    libjpeg-dev \
    libpng-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./app .
COPY ./extra-voices ./extra-voices

EXPOSE 4000/tcp

CMD ["python3", "main.py"]

```

Additional Dockerfile considerations and labels covered in [this subpage.](../../hypercycle-developer-guide/aim-building-guide/aim-structure-and-files/aim-dockerfile.md)

***

### <mark style="color:blue;">requirements.txt</mark>

`requirements.txt` defines the Python dependencies required by the AIM.

<mark style="color:yellow;">Example:</mark>

```
torch
torchaudio
fastapi
uvicorn
```

Best practices:

* Keep dependencies explicit
* Avoid unnecessary system packages
* Pin versions when stability is required

***

### <mark style="color:blue;">manifest.json</mark>

`manifest.json` declares **what the AIM is**, not how it runs.

It is consumed by:

* Node Managers
* AIM Registry
* Marketplaces
* Developer tools

Typical contents include:

* AIM name, version, and description
* Supported architectures
* Endpoint metadata
* Pricing declarations
* Configuration hints

The full schema and examples are covered in [this subpage.](../../hypercycle-developer-guide/aim-building-guide/aim-structure-and-files/aim-manifest-json.md)

***

### <mark style="color:blue;">main.py</mark>

`main.py` implements the AIM’s **application server**.

#### Responsibilities

* Start an HTTP server (default port `4000`)
* Declare AIM endpoints (e.g. `/speak`)
* Implement TTS inference logic
* Handle `cost_only` requests
* Report cost and usage metrics

Key characteristics:

* The AIM assumes all requests are authorized
* The AIM never verifies signatures
* The AIM never deducts payment
* The AIM never identifies the end user

<mark style="color:yellow;">Full main.py example for Tortoise TTS AIM covered in</mark> [<mark style="color:yellow;">this subpage.</mark>](../../hypercycle-developer-guide/aim-building-guide/aim-structure-and-files/aim-main.py.md)

Endpoint declaration and cost logic are covered in [this subpage.](../../hypercycle-developer-guide/aim-building-guide/endpoint-declaration-and-cost-logic.md)

***

### <mark style="color:blue;">Stateless by Default (Reinforced)</mark>

The Tortoise TTS AIM is **stateless by default**:

* No files are written during execution
* No state survives container restarts
* Execution is idempotent

This is intentional.

Persistence is introduced later using:

* Explicit container labels
* Mounted volumes (`/container_mount`)
* Purpose-built managers (e.g. `SubscriptionManager`)

***

### <mark style="color:blue;">Container Responsibility Boundary</mark>

Inside the container, the AIM is responsible for:

* Exposing HTTP endpoints
* Executing compute logic
* Estimating cost and reporting usage
* Returning results

Outside the container, the Node Manager handles:

* Authentication and signature verification
* Payment enforcement
* Balance tracking
* Request routing

This separation is fundamental to HyperCycle’s architecture.

***

### <mark style="color:blue;">When Specialized Examples Are Introduced</mark>

Some capabilities require additional structure and **cannot be demonstrated cleanly** using the Tortoise TTS AIM.

These include:

| Capability              | Example Type            |
| ----------------------- | ----------------------- |
| Persistence & Volumes   | Subscription-backed AIM |
| Subscriptions           | Time-based access AIM   |
| External Ports          | Streaming / TCP AIM     |
| Secure Access           | SSH-enabled AIM         |
| Infrastructure Services | Storage / CDN AIM       |

When these appear, the guide will:

* Clearly label them as specialized examples
* Explain how they extend the canonical model
* Avoid mixing concerns on a single page

***

### <mark style="color:blue;">What’s Next</mark>

Following the AIM Structure & Files subpage examples, the next section guides:

[<mark style="color:yellow;">**Endpoint Declaration & Cost Logic**</mark>](../../hypercycle-developer-guide/aim-building-guide/endpoint-declaration-and-cost-logic.md)

This is where:

* `@aim_uri` decorators are introduced via main.py
* `cost_only` behavior is formalized via main.py
* Usage and pricing schemas are explained
