# AIM Health Check

The AIM health check mechanism allows the Node Manager to verify that an AIM container is ready to serve requests after startup. This is crucial for AIMs that need time to initialize or download dependencies.

### <mark style="color:blue;">**Mechanism**</mark>

* Configuration is provided via Docker image labels (`HEALTH_*`).

### <mark style="color:blue;">**Process**</mark>

* The Node Manager periodically calls the HTTP endpoint specified by the `HEALTH_URI` label within the AIM container.
* A successful `HTTP 200 OK` response indicates the AIM is healthy and ready.
* Any other HTTP status code or a failure to respond within the `HEALTH_TIMEOUT` period is considered an unhealthy attempt.

### <mark style="color:blue;">**Labels**</mark>

* `HEALTH_URI` (Required for check): The endpoint path within the AIM for the health check (e.g., `"/health"`). This endpoint should be lightweight and perform essential checks (e.g., model loaded, dependencies available).
* `HEALTH_RETRIES` (Optional): The number of consecutive failures allowed before the Node Manager marks the AIM as definitively unhealthy (Default: `1` if not specified, meaning a single failure marks it unhealthy).
* `HEALTH_TIMEOUT` (Optional): Maximum time in milliseconds the Node Manager will wait for a response from the `HEALTH_URI` endpoint (e.g., `"5000"` for 5 seconds). Default depends on Node Manager implementation.
* `HEALTH_INTERVAL` (Optional): Time in milliseconds the Node Manager waits between health check attempts *after* a failure, before retrying (up to `HEALTH_RETRIES` times). Default depends on Node Manager implementation.
* **Backward Compatibility:** If no `HEALTH_URI` label is present in the Docker image, the Node Manager assumes the AIM is healthy immediately after the container starts.

#### <mark style="color:yellow;">**Example Health Check Endpoint (Conceptual):**</mark>

```python
# In your AIM's server code (e.g., using pyhypercycle-aim)

from starlette.responses import JSONResponse

@aim_uri(uri="/health", methods=["GET"], endpoint_manifest={...}, is_public=True)
async def health_check(self, request):
    try:
        # Perform checks: Is the model loaded? Can dependencies be reached?
        if self.model is None:
             raise RuntimeError("Model not loaded")
        # Add other essential checks...

        # If all checks pass
        return JSONResponse({"status": "healthy"}, status_code=200)
    except Exception as e:
        # Log the error for debugging
        print(f"Health check failed: {e}")
        return JSONResponse({"status": "unhealthy", "reason": str(e)}, status_code=503) # 503 Service Unavailable
```
