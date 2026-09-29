> For the complete documentation index, see [llms.txt](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/hypercycle-developer-guide/aim-building-guide/external-ports-and-secure-access.md).

# External Ports & Secure Access

This section explains how AIMs can expose external ports and provide secure, long-lived access outside of standard HTTP endpoint execution.

External ports are an **advanced capability** and are not part of the default AIM execution model.

***

### <mark style="color:blue;">Default Access Model</mark>

By default, all interaction with an AIM occurs through:

* HTTP endpoints declared with `@aim_uri`
* Requests routed through the Node Manager
* Signed authorization and metered execution
* Cost estimation and usage reporting

This model is:

* Stateless
* Auditable
* Metered
* Secure by default

External ports deliberately step **outside** this model.

***

### <mark style="color:blue;">Why External Ports Exist</mark>

Some AIMs provide services that are not well suited to per-request HTTP execution, such as:

* Interactive dashboards
* Long-running terminals
* Streaming interfaces
* Management UIs
* Protocols that require persistent connections

In these cases, exposing an external port may be appropriate.

***

### <mark style="color:blue;">External Ports Are Not Metered Per Call</mark>

When an AIM exposes an external port:

* Traffic does **not** flow through endpoint execution
* Requests are **not** individually metered
* `cost_only` does not apply
* Execution is not mediated by the Node Manager per request

Because of this, external ports are typically paired with:

* Subscription-based access
* Time-based access windows
* Operator-defined policies

***

### <mark style="color:blue;">Responsibility Shift</mark>

When using external ports, responsibility shifts as follows:

#### AIM Responsibilities

* Expose the service on the declared port
* Enforce any internal access rules
* Handle authentication inside the service (if required)
* Remain stable under long-lived connections

#### Node Operator Responsibilities

* Decide whether external access is allowed
* Control port exposure
* Gate access behind subscriptions or operator policy
* Monitor and manage resource usage

The Node Manager does **not** enforce per-request economics for external ports.

***

### <mark style="color:blue;">Declaring External Ports</mark>

External ports are declared via container configuration and metadata (not endpoint decorators).

Common patterns include:

* Declaring exposed ports in the Dockerfile

#### <mark style="color:yellow;">Example: Exposing SSH and an Additional Service Port</mark>

```dockerfile
ENV ENV_VARS="SSH_PORT=2222;DASHBOARD_PORT=5000"
ENV EXTRA_PORT_ENV="SSH_PORT,DASHBOARD_PORT"
```

In this example:

* Port `2222` (from `SSH_PORT`) will be exposed
* Port `5000` (from `DASHBOARD_PORT`) will be exposed
* The Node Manager can detect and map these ports safely

AIM authors must document:

* What service runs on the port
* Whether authentication is required
* How access is intended to be controlled

***

### <mark style="color:blue;">Secure Access Patterns</mark>

Because external ports bypass per-call enforcement, secure access becomes critical.

Common patterns include:

* Subscription-gated access (active subscription required)
* Network-level restrictions
* Operator-managed credentials
* Time-limited access

External services should never assume:

* Anonymous public access is acceptable
* The Node Manager will enforce access automatically
* Usage will be metered implicitly

***

### <mark style="color:blue;">Example Use Cases</mark>

External ports are appropriate for:

* Node dashboards and monitoring tools
* Interactive terminals
* Long-running control planes
* Visualization UIs tied to an active subscription

They are **not** appropriate for:

* Stateless inference
* Metered execution
* High-volume request handling
* Unbounded public access

***

### <mark style="color:blue;">Relationship to Subscriptions</mark>

In practice, external ports are almost always paired with subscriptions:

* The subscription grants access
* The port provides the interface
* Enforcement happens at a higher level than per request

This aligns with HyperCycle’s design:

* Execution endpoints remain metered and auditable
* External services are opt-in and explicitly managed

***

### <mark style="color:blue;">Summary</mark>

Key points to remember:

* External ports are an advanced feature
* They bypass per-request metering
* They shift responsibility to the AIM author and node operator
* They should be used sparingly and deliberately
* Subscriptions are the primary access control mechanism

External access trades fine-grained enforcement for flexibility and long-lived interaction.
