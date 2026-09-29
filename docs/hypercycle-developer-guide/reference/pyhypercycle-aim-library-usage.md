# pyhypercycle-aim Library Usage

HyperCycle python library simplifies building the AIM's HTTP server.

This section introduces the core building blocks of the pyhypercycle-aim Python library used to implement AIMs. It explains how server classes, decorators, and helper utilities work together to turn endpoint definitions into a running service, before extending those patterns with queues and concurrency.

### <mark style="color:blue;">Key Classes</mark> <a href="#key-classes" id="key-classes"></a>

* **`BaseServer`**: Provides basic server functionalities.
* **`SimpleServer`**: A helper class to run a basic server. It collects routes defined using the `aim_uri` decorator and runs using `uvicorn`. Does not handle job queues.
* **`SimpleQueue`**: Extends `SimpleServer` to manage a *synchronous* job queue (e.g., for model inference). Processes jobs sequentially in a loop. Provides an `add_job` method and a `/queue` endpoint.
* **`AsyncQueue`**: Extends `SimpleQueue` to manage an *asynchronous* job queue (e.g., for model training). Processes jobs concurrently. The `add_job` method accepts a callback. Provides a `/queue` endpoint.

### <mark style="color:blue;">`aim_uri`</mark> <mark style="color:blue;"></mark><mark style="color:blue;">Decorator</mark> <a href="#aim_uri-decorator" id="aim_uri-decorator"></a>

Used to define HTTP endpoints within server classes.

* **Mandatory Parameters:**
  * `uri` (str): The endpoint path (e.g., `"/predict"`).
  * `methods` (list): Allowed HTTP methods (e.g., `["POST"]`).
  * `endpoint_manifest` (dict): Metadata matching the structure required in the main `/manifest.json` for this specific endpoint (input/output formats, documentation, etc.).
* **Functionality:** Adds metadata attributes to the decorated function (`_uri`, `_methods`, etc.) which are collected by the server's `run` method to configure the Starlette/Uvicorn application. Works with both `async def` and `def` functions.

#### <mark style="color:yellow;">**Example using**</mark><mark style="color:yellow;">**&#x20;**</mark><mark style="color:yellow;">**`SimpleServer`**</mark><mark style="color:yellow;">**&#x20;**</mark><mark style="color:yellow;">**and**</mark><mark style="color:yellow;">**&#x20;**</mark><mark style="color:yellow;">**`aim_uri`**</mark><mark style="color:yellow;">**:**</mark>

```python
from pyhypercycle_aim import SimpleServer, aim_uri, JSONResponseCORS

class MyAIMServer(SimpleServer):
    # Corresponds to the top-level fields in /manifest.json
    manifest = {
        "name": "MyAIM",
        "short_name": "myaim",
        "version": "0.1.0",
        "documentation_url": "...",
        "license": "MIT",
        "terms_of_service": "",
        "author": "Me"
    }

    @aim_uri(
        uri="/greet",
        methods=["GET"],
        endpoint_manifest={
            "input_query": {"name": "<string>"},
            "input_body": {},
            "output": {"message": "<string>"},
            "documentation": "Returns a personalized greeting.",
            "example_calls": [{
                "method": "GET",
                "query": "?name=World",
                "output": {"message": "Hello, World!"}
            }],
            "is_public": True # Assuming this is a free endpoint
        }
    )
    async def greet_endpoint(self, request):
        name = request.query_params.get("name", "stranger")
        return JSONResponseCORS({"message": f"Hello, {name}!"})

    # --- Add other endpoints here ---
    # Including the mandatory /manifest.json endpoint which can often
    # be generated automatically by the base server classes based on
    # the self.manifest and collected endpoint_manifests. Check library specifics.

if __name__ == '__main__':
    server = MyAIMServer()
    # Default port is often handled by PORT env var when run by Node Manager
    # For local testing, specify port/host:
    server.run(uvicorn_kwargs={"port": 8000, "host": "0.0.0.0"})
```

### <mark style="color:blue;">`util.py`</mark> <mark style="color:blue;"></mark><mark style="color:blue;">Module</mark> <a href="#utilpy-module" id="utilpy-module"></a>

Provides helper functions:

* `to_async`: Converts sync functions to async using a thread pool.
* `JSONResponseCORS`, `HTMLResponseCORS`: Create responses with appropriate CORS headers.
* `handle_interrupt`: Graceful shutdown signal handling.
* `not_found`, `server_error`: Default 404/500 error handlers.
* `default_exception_handlers`: Dictionary of default handlers.
