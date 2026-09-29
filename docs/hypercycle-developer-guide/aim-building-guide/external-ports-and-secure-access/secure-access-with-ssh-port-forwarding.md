# Secure Access with SSH Port Forwarding

Some AIMs require secure, long-lived access that goes beyond HTTP endpoints. Common use cases include:

* Secure port forwarding to services running inside an AIM
* Administrative or operator shell access
* Debugging or management interfaces
* Controlled access for developers without exposing public ports

To support these patterns safely, HyperCycle provides **SSH-based secure access** via an SSH port management facility.

***

### <mark style="color:blue;">Why SSH Instead of Open Ports</mark>

Directly exposing open ports can introduce risks:

* Unauthenticated access
* Unmetered usage
* Persistent attack surface

Using SSH instead allows:

* Encrypted connections
* Strong key-based authentication
* Fine-grained access control
* Port forwarding without exposing services publicly

This approach is especially useful when paired with **subscription-based access** or **operator-only controls**.

***

### <mark style="color:blue;">SSH Access Model</mark>

A common pattern is to define **multiple SSH user roles**, each with different permissions:

* **Access user**
  * Port forwarding only
  * No shell access
  * Intended for end users or subscribers
* **Manager user**
  * Full shell access
  * Intended for node operators or administrators only

Shell access should be restricted whenever possible, as it grants full control inside the container.

***

### <mark style="color:blue;">SSH Initialization at Startup</mark>

At AIM startup, the SSH manager is initialized and access rules are defined.

#### <mark style="color:yellow;">Example: SSH Setup</mark>

```python
SSHPortManager.init(ssh_port=SSH_PORT)

SSHPortManager.allow_access(
    ports=[4000, 4001, 5000],
    shell=False,
    username="access"
)

SSHPortManager.allow_access(
    ports=None,
    shell=True,
    username="manager"
)
```

This configuration means:

* The **access** user:
  * Can forward ports 4000, 4001, and 5000
  * Cannot open a shell
* The **manager** user:
  * Can open a shell inside the container
  * Has no port restrictions

***

### <mark style="color:blue;">API Endpoints for SSH Key Management</mark>

Rather than managing static SSH keys, AIMs can generate **ephemeral `.pem` keys** on demand using API endpoints.

#### <mark style="color:yellow;">1. Get SSH Key for Port Forwarding</mark>

```python
@aim_uri(uri="/get_access", methods=["POST"])
async def get_access(self, request):
    SSHPortManager.generate_key(username="access")
    return FileResponseCORS(
        data,
        "access.pem",
        "x-pem-file",
        costs=[]
    )
```

This endpoint:

* Generates a private SSH key for the **access** user
* Returns it as a downloadable `.pem` file
* Allows the caller to establish secure port forwarding

**Typical usage:**

```bash
ssh -i access.pem -p <SSH_PORT> -N \
    -L 8080:localhost:4000 access@<aim-host>
```

This forwards local port `8080` to port `4000` inside the AIM.

***

#### <mark style="color:yellow;">2. Get SSH Key for Shell Access (Private)</mark>

```python
@aim_uri(uri="/private_access", methods=["POST"], is_private=True)
async def private_access(self, request):
    pem = SSHPortManager.generate_key(username="manager")
    return FileResponseCORS(
        data,
        "manager.pem",
        "x-pem-file",
        costs=[]
    )
```

This endpoint:

* Generates a key for the **manager** user
* Is marked as private
* Grants full shell access

**Example usage:**

```bash
ssh -i manager.pem -p <SSH_PORT> manager@<aim-host>
```

> ⚠️ Shell access should be enabled only when absolutely necessary, as it provides unrestricted access inside the container.

***

#### <mark style="color:yellow;">3. List Registered SSH Users and Keys</mark>

```python
@aim_uri(uri="/list_users", methods=["GET"], is_private=True)
async def list_users(self, request):
    user_info = SSHPortManager.list_users(["access", "manager"])
    return JSONResponseCORS(user_info, costs=[])
```

Example output:

```json
{
  "access": [
    "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC7...",
    "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC8..."
  ],
  "manager": [
    "ssh-rsa AAAAB3Nza..."
  ]
}
```

This endpoint is useful for:

* Auditing active keys
* Key rotation
* Verifying access state

***

### <mark style="color:blue;">Dockerfile Configuration for External Access</mark>

AIMs that expose external services or require additional ports must declare this explicitly using **container metadata understood by the Node Manager**.

External access is configured **via environment variables**, not custom Docker labels.

***

#### <mark style="color:blue;">Default Port Behavior</mark>

By default, AIMs expose a single HTTP service port:

* **Port 4000**
* Typically used for AIM HTTP endpoints (`@aim_uri`)

No additional configuration is required if the AIM only uses this default port.

***

#### <mark style="color:blue;">Declaring Environment Variables (</mark><mark style="color:blue;">`ENV_VARS`</mark><mark style="color:blue;">)</mark>

The `ENV_VARS` field allows AIM authors to declare default environment variables that should be present inside the container.

#### Format

```
ENV_VARS="VAR1=value1;VAR2=value2"
```

* Semicolon-separated `KEY=value` pairs
* Optional
* Used to configure runtime behavior, including port values

#### <mark style="color:yellow;">Example</mark>

```dockerfile
ENV ENV_VARS="SSH_PORT=2222;SERVICE_PORT=5000"
```

This makes the following variables available inside the container:

* `SSH_PORT=2222`
* `SERVICE_PORT=5000`

***

#### <mark style="color:blue;">Exposing Additional Ports (</mark><mark style="color:blue;">`EXTRA_PORT_ENV`</mark><mark style="color:blue;">)</mark>

AIMs that require ports **beyond the default port (4000)** must explicitly declare which environment variables contain additional port numbers.

This is done using the `EXTRA_PORT_ENV` field.

#### Format

```
EXTRA_PORT_ENV="PORT_VAR1,PORT_VAR2"
```

* Comma-separated list of environment variable names
* Each referenced environment variable must contain a port number
* Optional, but **recommended** for AIMs exposing additional services

***

#### <mark style="color:yellow;">Example: Exposing SSH and an Additional Service Port</mark>

```dockerfile
ENV ENV_VARS="SSH_PORT=2222;DASHBOARD_PORT=5000"
ENV EXTRA_PORT_ENV="SSH_PORT,DASHBOARD_PORT"
```

In this example:

* Port `2222` (from `SSH_PORT`) will be exposed
* Port `5000` (from `DASHBOARD_PORT`) will be exposed
* The Node Manager can detect and map these ports safely

***

### <mark style="color:blue;">How This Is Used by AIMs</mark>

Inside the AIM, the application reads the environment variables normally:

```python
SSH_PORT = int(os.environ.get("SSH_PORT", 2222))
```

The AIM itself:

* Does **not** expose ports dynamically
* Does **not** decide which ports are mapped externally
* Simply binds to the ports defined in its environment

The Node Manager:

* Reads `EXTRA_PORT_ENV`
* Resolves the actual port values
* Handles exposure according to operator policy

***

### <mark style="color:blue;">Privileged Access</mark>

Some AIMs require elevated privileges to function correctly (for example, when managing SSH services, mounts, or internal networking).

In those cases, the container must explicitly request privileged execution.

```dockerfile
LABEL PRIVILEGED=1
```

This should be used **only when necessary**, and documented clearly by the AIM author.

***

### <mark style="color:blue;">Security Considerations</mark>

When using SSH-based access:

* Prefer port forwarding over shell access
* Restrict shell access to operators only
* Generate keys dynamically instead of storing static credentials
* Pair access with subscriptions or explicit operator policy
* Document access behavior clearly

External access trades enforcement granularity for flexibility and must be used deliberately.

***

### <mark style="color:blue;">Summary</mark>

Key points:

* Default AIM port is 4000
* Additional ports must be declared via environment variables
* `EXTRA_PORT_ENV` tells the Node Manager which ports to expose
* AIMs read ports from environment variables
* Privileged access is opt-in and explicit

SSH-based secure access enables:

* Encrypted, authenticated access to AIM services
* Controlled port forwarding without public exposure
* Operator-only administrative access when required

Key takeaways:

* External access is an advanced capability
* SSH provides a safer alternative to open ports
* AIMs manage access mechanics; operators manage policy
* Shell access should be rare and restricted

***

### <mark style="color:blue;">Best Practices</mark>

When exposing external ports:

* Use environment variables for all port configuration
* Declare additional ports explicitly using `EXTRA_PORT_ENV`
* Avoid hardcoding port numbers in code
* Prefer port forwarding or subscription-gated access
* Document all exposed services clearly

External access is powerful, but it must remain **intentional and auditable**.

***

### <mark style="color:blue;">What’s Next</mark>

This concludes the AIM Building section.

From here, readers should be able to:

* Understand AIM structure
* Declare endpoints and cost logic
* Manage concurrency and persistence
* Implement subscriptions
* Expose advanced services safely

Future sections may explore:

* Advanced AIM patterns
* Multi-AIM interaction
* Network-level tooling and discovery

[<mark style="color:yellow;">Lastly we provide a conceptual overview of our Security Layers</mark>](../../../hypercycle-developer-guide/security-layers-conceptual-overview.md)
