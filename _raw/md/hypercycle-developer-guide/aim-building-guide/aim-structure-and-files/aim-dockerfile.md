> For the complete documentation index, see [llms.txt](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/hypercycle-developer-guide/aim-building-guide/aim-structure-and-files/aim-dockerfile.md).

# AIM Dockerfile

Additional details and labels

### <mark style="color:blue;">Dockerfile Responsibilities</mark>

In the context of an AIM, the Dockerfile is responsible for:

* Selecting the correct base image (python slim, nvidia/cuda, etc)
* Declaring hardware requirements via labels
* Declaring data storage persistence via labels
* Declaring resource and permissions via labels
* Declaring environment configuration variables via labels
* Declaring royalty address and percentage via labels
* Installing system and Python dependencies
* Copying model assets and application code
* Exposing required ports (port 4000 is a default main.py application server port expected by the Node Manager for advertisement of service and cost via manifest.json)
* Defining the container entry point, "main.py"

The Dockerfile **does not**:

* Define pricing
* Declare endpoints
* Handle authentication

***

### <mark style="color:blue;">Dockerfile Labels</mark>

The following labels are used by Node Managers and tooling to determine placement:

| Label              | Purpose                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GPUS=1`           | Indicates GPU is required.                                                                                                                                                                                                                                                                                                                                                                                                |
| `GPU_MEMORY=8GB`   | Minimum GPU memory requirement.                                                                                                                                                                                                                                                                                                                                                                                           |
| `description`      | Human-readable AIM description.                                                                                                                                                                                                                                                                                                                                                                                           |
| `PERSIST_VOLUME=1` | Optional. This enables persistent storage inside the AIM container at `/container_mount`                                                                                                                                                                                                                                                                                                                                  |
| `ENV_VARS=`        | <p></p><p>Default environment variables for the container.</p><ul><li>Format: Semicolon-separated key-value pairs (<code>"VAR1=value1;VAR2=value2"</code>).</li><li>Optional.</li><li>Example: "PORT=4000;FTP\_PORT=1121;FTP\_PASSIVE\_PORT=1120;PROTOCOL=FTPS;MAX\_DISK\_ALLOCATION=;PERSIST\_DIRECTORY=;"</li></ul>                                                                                                     |
| `EXTRA_PORT_ENV=`  | <p></p><p>Specifies environment variables that contain <em>additional</em> port mappings the container needs exposed.</p><ul><li>Format: Comma-separated list of env var names (<code>"PORT\_VAR1,PORT\_VAR2"</code>). The corresponding env vars should hold port numbers.</li><li>Optional. Recommended for services needing ports beyond the default (4000).</li><li>Example: "FTP\_PORT,FTP\_PASSIVE\_PORT"</li></ul> |
| `CAP_ADD=`         | <p></p><p>Additional Linux capabilities to grant.</p><ul><li>Format: Comma-separated list (<code>"SYS\_ADMIN,NET\_ADMIN"</code>).</li><li>Requires the AIM to be whitelisted in the AIM database.</li><li>Optional. Use minimally.</li></ul>                                                                                                                                                                              |
| `PRIVILEGED=1`     | <p></p><p>Flag to run the container in privileged mode.</p><ul><li>If present, grants full host device access. Necessary for some services/models requiring special network/port access. </li><li>Optional. Use with extreme caution due to security implications.</li></ul>                                                                                                                                              |

### <mark style="color:blue;">Health Check Labels</mark> <a href="#health-check-labels" id="health-check-labels"></a>

See [AIM Health Check](/hypercycle-cbno/u57KauJomd55OVuTYz6e/hypercycle-developer-guide/aim-building-guide/aim-structure-and-files/aim-health-check.md) documentation for additional details.

* **`HEALTH_URI`**: Path for the health check endpoint (e.g., `"/health"`).
* **`HEALTH_RETRIES`**: Number of retries (e.g., `"3"`).
* **`HEALTH_TIMEOUT`**: Timeout per attempt in milliseconds (e.g., `"400"`).
* **`HEALTH_INTERVAL`**: Interval between retries in milliseconds (e.g., `"400"`).

### <mark style="color:blue;">Restrictions and Notes</mark> <a href="#restrictions-and-notes" id="restrictions-and-notes"></a>

* **Default Port:** Container port 4000 is automatically mapped.
* **GPU Allocation:** Based on available memory; allocation fails if requirements aren't met.
* **Whitelisting:** Required for certain privileges (`CAP_ADD`, potentially `PRIVILEGED`).
* **Auto-removal:** Containers are run with `auto_remove=True`.
* **Platform Compatibility:** Host/image platform compatibility (amd64/arm64) is checked.
