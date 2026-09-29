> For the complete documentation index, see [llms.txt](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/hypercycle-developer-guide/hypercycle-apis.md).

# HyperCycle APIs

This section describes the API surfaces available in the HyperCycle ecosystem, how they are categorized, and how developers are expected to use them.

HyperCycle does not expose a single monolithic API. Instead, it exposes multiple **HTTP-based API planes** that follow **REST-style conventions**, while extending them with execution, pricing, and metering semantics required for decentralized AI services.

***

### <mark style="color:blue;">API Planes</mark>

HyperCycle APIs fall into four categories:

* **Network & Observability APIs**
* **AIM Registry API**
* **Node Manager APIs**
* **AIM Service APIs**

Each plane serves a different purpose and audience.

***

{% tabs %}
{% tab title="Network APIs" %}

#### <mark style="color:blue;">Network & Observability APIs</mark>

These APIs provide **read-only visibility** into the HyperCycle network.

Typical use cases include:

* Dashboards and license/block explorers
* Monitoring and reporting
* Auditing and analytics

These APIs have no execution side effects and do not interact with AIMs directly.

#### <mark style="color:yellow;">Example: License Uptime / Activity Report</mark>

Look up historical tilling or uptime data for a license:

* ***JSON:***

{% embed url="<http://18.216.251.149:8003/uptime_report?license=4503874505352761>" %}

* ***Web-UI:***

{% embed url="<https://explorer.hypercycle.ai/license/4503874505352761>" %}

#### <mark style="color:yellow;">Example: License Status (Delegation in Block)</mark>

{% embed url="<https://explorer.hypercycle.ai:3000/v1/licenses/status?license=581194974499375&network=main>" %}

#### <mark style="color:yellow;">Example: Block Content (signatures, computations, licenses, nodes)</mark>

{% embed url="<https://explorer.hypercycle.ai:3000/v1/blocks/631546?network=main&page=1&pageSize=20>" %}

#### <mark style="color:yellow;">Example: Active Licenses (HMS)</mark>

* ***Base / ANFE network:***

{% embed url="<https://activation-service.hyperpg.site/hms_api/license_register>" %}

* ***Ethereum / Node Factory network:***

{% embed url="<https://hms.hyperpg.site/hms_api/license_register>" %}

* ***Pagination:***

{% embed url="<https://hms.hyperpg.site/hms_api/license_register?page=2&page_size=50>" %}

***

{% endtab %}

{% tab title="AIM Registry APIs" %}

#### <mark style="color:blue;">AIM Registry APIs</mark>

AIM Registry APIs are used to **discover AIMs available for deployment**.

Typical uses:

* Filtering AIMs by architecture or metadata
* Supporting developer tooling and marketplaces
* Assisting Node Managers in deployment selection

#### Important

> <mark style="color:$success;">The AIM Registry does</mark> <mark style="color:$success;"></mark><mark style="color:$success;">**not**</mark> <mark style="color:$success;"></mark><mark style="color:$success;">indicate whether an AIM is deployed or currently running.</mark>

#### <mark style="color:yellow;">Example: List AIMs</mark>

{% embed url="<https://appdemos.hyperpg.site/aims?page_size=100&page=1>" %}

Filter by Architecture

{% embed url="<https://appdemos.hyperpg.site/aims?arch=arm64>" %}

Retrieve AIM Metadata

{% embed url="<https://appdemos.hyperpg.site/aim?aim_name=hypercycle/boinc-aim>" %}

***

{% endtab %}

{% tab title="Node Manager APIs" %}

#### <mark style="color:blue;">The</mark> <mark style="color:blue;"></mark><mark style="color:blue;">**Node Manager API**</mark> <mark style="color:blue;"></mark><mark style="color:blue;">is the operational interface of a HyperCycle node.</mark>

It is the only API plane responsible for:

* Authenticating requests
* Managing balances and payments
* Routing execution to AIM containers
* Advertising node capabilities and running services

<mark style="color:green;">All paid or metered interaction with AIMs flows through the Node Manager.</mark>

***

#### <mark style="color:blue;">Execution Flow</mark>

The Node Manager enforces execution and payment through a **two-phase interaction model:**

<figure><img src="https://3020620922-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FHIm70m3Kmltf5bJkSI4I%2Fuploads%2FTkhaba6MEP1pERdykpbx%2FNM-Execution-Flow.png?alt=media&amp;token=ef449519-fc75-497e-83c7-98ee14d3f220" alt=""><figcaption></figcaption></figure>

#### <mark style="color:blue;">Role of the Node Manager</mark>

The Node Manager sits between **clients** and **AIM containers** and enforces the core HyperCycle execution contract.

At a high level, it:

* Verifies signed requests
* Ensures sufficient balance or subscription status
* Routes requests to the correct AIM
* Collects usage and deducts payment
* Returns results to the client

AIM containers are not exposed directly for paid execution.

***

#### <mark style="color:blue;">Common Node Manager Endpoints</mark>

> The exact set of endpoints may vary by node configuration and version.

#### <mark style="color:yellow;">Example: Node Information (</mark><mark style="color:yellow;">`/info`</mark><mark style="color:yellow;">)</mark>

http\://\<node-address>:8000:/info

(alternatively from command line)

```
curl http://localhost:8000/info
```

Typical data includes:

* Node identity
* Active licenses
* Running AIMs
* Exposed service endpoints
* Sample JSON reply from /info endpoint:

```json
{
  "status": "alive",
  "name": "Monkey Brains Node (2)",
  "address": "207.53.252.108:8010",
  "node_version": "0.4.15",
  "node_id": "562928bc42cea196",
  "protocol_version": "2",
  "network": "mainnet",
  "tm": {
    "network": "mainnet",
    "driver": "ethereum",
    "version": "0.1.0",
    "address": "0x2c64...C4b7"
  },
  "vm": {
    "version": "0.0.1"
  },
  "aim": {
    "interface_version": "0.0.1",
    "aims": [
      {
        "image_id": "23d3b12aa75c5b020e29de5490684632864e17a8882b7ab188f0c1e464f49147",
        "image_name": "ollama-alternative-aim",
        "image_tag": "latest",
        "status": "running",
        "network_mode": "host",
        "whitelisted": true,
        "tries": 0,
        "labels": {
          "ENV_VARS": "PORT=4000;PORT_STREAM=4001;OLLAMA_MODEL=gemma3:1b;",
          "EXTRA_PORT_ENV": "PORT_STREAM,",
          "GPUS": "0+",
          "GPU_MEMORY": "0",
          "org.opencontainers.image.ref.name": "ubuntu",
          "org.opencontainers.image.version": "24.04"
        },
        "container_id": "6d6b8867bd08",
        "uri_cost": {
          "default": {
            "HyPC": {
              "currency": "HyPC",
              "fixed": 0
            },
            "USDC": {
              "currency": "USDC",
              "fixed": 10000
            }
          }
        },
        "slot": 0,
        "port": 9100
      }
    ]
  },
  "platform": "x86_64",
  "hardware": {
    "memory": 135027404800,
    "cpu_count": 72,
    "cpu_freq": [1200.03004166667, 1200, 3600],
    "disk_space": 943441317888,
    "disk_space_free": 252298969088,
    "gpu": {
      "gpu_count": 1,
      "gpus": [
        {
          "id": "0",
          "uuid": "GPU-9b60e257-bd52-eb4b-87c2-e44771d8785c",
          "memory": 15360,
          "name": "Tesla T4",
          "driver": "575.57.08",
          "serial": "1561220010039"
        }
      ]
    }
  },
  "priority": 0,
  "license": "4649559795957782",
  "hypervm": {
    "version": "0.0.1"
  },
  "geo_ip": "161.115.58.252",
  "accepting_currencies": [
    "HyPC",
    "USDC"
  ],
  "license_freelancing": {
    "contact": "",
    "enabled": true,
    "expected_APR": 0,
    "grace_period_blocks": 30,
    "revenue_split": 0.4
  },
  "license_freelancing_active": false,
  "cold_wallet_address": "0x05...E89",
  "uptime_summary": {
    "total_time": 16345212.6972406,
    "up_time": 14455006.3750339,
    "down_time": 1890206.32220674,
    "percent_up": 0.884357184843391,
    "heartbeats": 29992
  }
}
```

This endpoint is foundational for:

* Discovering deployed AIMs
* Community network scanners
* Monitoring and observability tools

***

#### <mark style="color:yellow;">Example: Node Admin Web-UI</mark>

http\://\<node-address>:8006

<figure><img src="https://3020620922-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FHIm70m3Kmltf5bJkSI4I%2Fuploads%2FhcuqnBexALeboHwTWgkO%2FNM-0.4.16.png?alt=media&amp;token=3d697080-c339-498d-9ec6-df0006993e0f" alt=""><figcaption></figcaption></figure>

***

{% endtab %}

{% tab title="AIM Service APIs" %}

#### <mark style="color:blue;">**AIM Service APIs**</mark> <mark style="color:blue;"></mark><mark style="color:blue;">define the service interface exposed by an individual AIM (AI Machine).</mark>

AIM Service APIs are responsible for:

* Executing AI or compute logic
* Validating service-level inputs
* Producing service outputs
* Declaring cost and usage for execution

> **Important**\
> They do **not** handle authentication, payment enforcement, or client identity.\
> All enforcement is handled by the Node Manager. AIMs assume all incoming requests have already been authenticated and authorized by the Node Manager.

***

#### <mark style="color:blue;">AIM Endpoints</mark>

Each AIM defines its endpoints as part of its implementation and manifest.

Typical AIM endpoints include:

* Inference or generation endpoints
* Metadata or capability endpoints
* Health or readiness checks
* Subscription or job-based endpoints

The shape of these endpoints is **AIM-specific**.

#### <mark style="color:yellow;">Example: Node AIM Health Endpoint</mark>

http\://\<node-address>:8006/api/aim/0/health

```
{"status":"ok"}
```

* Where ".../api/aim/0..." defines the slot of the AIM, starting with slot 0 for port 9000, slot 1 for port 9001, etc. Multiple AIMs can be deployed by the node manager at any given time, each with their own slot.

#### <mark style="color:yellow;">Example: Node AIM Manifest Endpoint</mark>

http\://\<node-address>:8006/api/aim/0/manifest.json

```
{
  "name": "cog-videox",
  "short_name": "cogvid",
  "version": "0.1",
  "documentation_url": "https://huggingface.co/zai-org/CogVideoX-2b",
  "license": "",
  "terms_of_service": "",
  "author": "Ray Mata",
  "description": "Text to Video Generator, 6sec, 49 frames, 8fps",
  "endpoints": [
    {
      "documentation": "Download a generated file",
      "price_per_call": [
        {
          "estimated_cost": 0,
          "min": 0,
          "max": null,
          "currency": "ProcessingUnits"
        }
      ],
      "is_public": true,
      "uri": "/download",
      "input_methods": [
        "GET"
      ]
    },
    {
      "documentation": "Run inference",
      "input_body": {
        "text": "\u003Cstring\u003E"
      },
      "output": {
        "result": "\u003Cstring\u003E"
      },
      "example_calls": [],
      "costs": [
        {
          "currency": "USDC",
          "min": 10000,
          "max": 10000,
          "estimated": 10000
        }
      ],
      "uri": "/generate",
      "input_methods": [
        "POST"
      ]
    },
    {
      "documentation": "Health check endpoint",
      "price_per_call": [
        {
          "estimated_cost": 0,
          "min": 0,
          "max": null,
          "currency": "ProcessingUnits"
        }
      ],
      "output": {
        "status": "\u003Cstring\u003E"
      },
      "example_calls": [],
      "is_public": true,
      "uri": "/health",
      "input_methods": [
        "GET"
      ]
    }
  ],
  "royalties": {
    "address": "0xB84...C651",
    "fee_percent": "5"
  }
}
```

#### <mark style="color:yellow;">Example: Cost Estimation vs Execution</mark> *(Text-to-Audio Generation)*

This example demonstrates how an AIM endpoint handles **cost estimation** and **execution** using a Text-to-Speech service (`/speak`).

The AIM is responsible only for:

* Estimating cost
* Executing computation
* Reporting usage

<figure><img src="https://3020620922-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FHIm70m3Kmltf5bJkSI4I%2Fuploads%2F3MfHkKBfM9oizuRXSefK%2FCost_only-flow.png?alt=media&amp;token=226ce66a-60fa-4641-9390-2be5dcb6c51a" alt=""><figcaption></figcaption></figure>

***

#### <mark style="color:blue;">Direct Port Access (Operator Discretion)</mark>

> **Exception**

Node operators may expose AIM endpoints directly via ports:

* Without Node Manager mediation
* Without per-call or subscription pricing
* Typically for trusted, internal, or experimental use

When direct access is enabled:

* The AIM may receive unauthenticated requests
* Payment enforcement is the operator’s responsibility

AIMs must remain correct and safe under both mediated and direct access.

***

{% endtab %}
{% endtabs %}

### <mark style="color:blue;">Discovery vs Availability</mark>

A common source of confusion is the difference between **AIM discovery** and **service availability**.

* The **AIM Registry** lists AIMs that *can* be deployed
* It does **not** list AIMs that are currently running

At this time, prior to more advanced network features such as **Swarm AI** and autonomous AI-to-AI agent interaction, deployed AIMs must be discovered by querying active nodes.

To find running AIMs, clients typically:

* Discover active nodes via network scanners or monitors
* Query node `/info` endpoints
* Parse advertised running services

This process is decentralized and commonly implemented by community scanners, monitors, and marketplaces.

***

### <mark style="color:blue;">What’s Next</mark>

Next, we’ll move into <mark style="color:yellow;">**AIM Building Guide**</mark>:

* AIM structure and manifests
* Container expectations
* Lifecycle and deployment
* Common AIM patterns

This is where AIM authors go from concept to running service.
