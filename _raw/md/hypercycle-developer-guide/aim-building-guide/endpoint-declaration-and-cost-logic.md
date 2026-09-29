> For the complete documentation index, see [llms.txt](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/hypercycle-developer-guide/aim-building-guide/endpoint-declaration-and-cost-logic.md).

# Endpoint Declaration & Cost Logic

This section explains how AIM endpoints are declared, how cost estimation is handled, and how usage is reported to the Node Manager.

All examples on this page are based on **existing AIM patterns** used in the tutorial and in the **Tortoise TTS AIM**. No schema or behavior is introduced that does not already exist.

***

### <mark style="color:blue;">Conceptual Flow</mark>

<figure><img src="https://3020620922-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FHIm70m3Kmltf5bJkSI4I%2Fuploads%2FgqGWvQohD5GbNiTwkjZn%2FCost_only-flow2.png?alt=media&amp;token=68913ef4-3cb1-4e80-ba13-406426ef8dad" alt=""><figcaption></figcaption></figure>

This diagram reflects the **actual control flow** used by production AIMs:

* Cost estimation and execution are mutually exclusive
* Execution never occurs during `cost_only`
* Usage is reported only after execution

***

### <mark style="color:blue;">Endpoint Declaration with</mark> <mark style="color:blue;"></mark><mark style="color:blue;">`@aim_uri`</mark>

AIM endpoints are declared using the `@aim_uri` decorator via main.py

This decorator serves multiple purposes:

* Declares an HTTP endpoint
* Describes inputs and outputs
* Declares pricing and usage behavior
* Allows the Node Manager to reason about cost before execution

Endpoints declared with `@aim_uri` are discoverable and metered by the Node Manager.

#### <mark style="color:yellow;">Example:</mark> <mark style="color:yellow;"></mark><mark style="color:yellow;">`/speak`</mark> <mark style="color:yellow;"></mark><mark style="color:yellow;">(Tortoise TTS AIM)</mark>

The Tortoise TTS AIM exposes a `/speak` endpoint that converts text into synthesized speech.

```python
    @aim_uri(
        uri="/speak",
        methods=["POST"],
        endpoint_manifest={
            "input_query": "",
            "input_headers": {},
            "input_body": {"text": "<String>", "voice": "<Voice>"},
            "output_body": {"file": "<File:Audio>"},
            # "currency": "HYPC",
            "documentation": "",
            "price_per_call": {"estimated_cost": 0, "min": 0, "max": 500},
            "example_calls": [
                {
                    "body": {
                        "text": "Hello there, Hypercycle. This is a demo of the Tortoise AIM."
                    },
                    "method": "POST",
                    "query": "",
                    "headers": "",
                }
            ],
        },
    )
```

Key points:

* Endpoints are **execution-oriented**, not CRUD resources
* Pricing metadata is declared at the endpoint level
* The decorator does not enforce pricing — it declares intent

***

### <mark style="color:blue;">Cost Estimation (</mark><mark style="color:blue;">`cost_only`</mark><mark style="color:blue;">)</mark>

All AIM endpoints must support cost estimation.

When a request includes the `cost_only` header:

* The AIM **must not perform full execution**
* The AIM returns an estimated cost
* No expensive resources are allocated

#### <mark style="color:yellow;">Example: Cost Estimation in</mark> <mark style="color:yellow;"></mark><mark style="color:yellow;">`/speak`</mark>

```python
if request.headers.get("cost_only"):
    return JSONResponseCORS({"costs": self.estimate(body["text"])})
```

***

### <mark style="color:blue;">Execution Requests</mark>

When `cost_only` is **not** present, the AIM performs full execution.

#### <mark style="color:yellow;">Example: Execution Path in</mark> <mark style="color:yellow;"></mark><mark style="color:yellow;">`/speak`</mark>

```python
spoken, duration = self.orate(text, voice)
return JSONResponseCORS(
    {"file": spoken}, costs=self.estimate(body["text"], used=True)
)
```

Execution behavior:

* Full TTS inference is performed
* Output is generated and returned
* Actual usage is reported alongside the result

The AIM does **not**:

* Identify the end user
* Deduct payment
* Know whether the request is prepaid or subscription-based

***

### <mark style="color:blue;">Returning Cost and Usage</mark>

AIMs return cost and usage information as part of the response payload.

#### <mark style="color:yellow;">Example: Cost Structure Returned by Tortoise TTS</mark>

```python
def estimate(self, text, used=False):
    word_count = len(text.split())
    costs = [
        {
            "currency": "ProcessingUnits",
            "min": 0,
            "max": 100000,
            "estimated_cost": word_count,
        },
        {
            "currency": "USDC",
            "min": 0,
            "max": 100000,
            "estimated_cost": math.ceil(word_count / 10) * 10000,
        }
    ]
    if used:
        for cost in costs:
            cost["used"] = cost["estimated_cost"]
    return costs
```

Key characteristics:

* Costs are derived from input parameters only
* Both estimated and used costs share the same structure
* Usage is only populated during execution

The Node Manager consumes this information to perform deduction and accounting.

***

### <mark style="color:blue;">Deterministic Cost Logic</mark>

Cost estimation must be:

* Deterministic
* Derived solely from request inputs
* Independent of execution side effects

#### <mark style="color:yellow;">Example: Deterministic Cost Basis</mark>

```python
word_count = len(text.split())
```

For the Tortoise TTS AIM:

* Cost scales with input text length
* The same input always produces the same estimate
* Execution duration does not influence cost estimation

This guarantees predictable pricing behavior.

***

### <mark style="color:blue;">Error Handling and Safety</mark>

AIM endpoints should validate inputs and fail fast on invalid requests.

#### <mark style="color:yellow;">Example: Input Validation in</mark> <mark style="color:yellow;"></mark><mark style="color:yellow;">`/speak`</mark>

```python
if voice not in set(self.available_voices):
    return JSONResponseCORS({"error": "voice not found"}, status_code=400)
```

Error handling principles:

* Errors are returned as normal HTTP responses
* Partial execution is avoided
* No cost or usage is reported on failure

The AIM does not attempt to interpret authorization or payment state.

***

### <mark style="color:blue;">Supporting Endpoints</mark>

The Tortoise TTS AIM also exposes non-executing endpoints, such as `/list-voices`.

#### <mark style="color:yellow;">Example: Read-Only Endpoint with Cost Handling</mark>

```python
@aim_uri(
    uri="/list-voices",
    methods=["GET"],
    endpoint_manifest={...},
)
def list_voices(self, request):
    costs = [
        {"currency": "ProcessingUnits", "min": 0, "max": 0, "estimated_cost": 0},
        {"currency": "HyPC", "min": 0, "max": 0, "estimated_cost": 0},
    ]
    if request.headers.get("cost_only"):
        return JSONResponseCORS({"costs": costs})
    costs[0]["used"] = 0
    return JSONResponseCORS(
        {"available_voices": self.available_voices}, costs=costs
    )
```

This shows that:

* Even non-executing endpoints participate in the cost model
* `cost_only` is handled consistently across endpoints

***

#### <mark style="color:yellow;">Bonus reference:</mark>&#x20;

See how endpoint definitions and cost logic are implemented using the core classes and decorators provided by the [`pyhypercycle-aim` Python library.](/hypercycle-cbno/u57KauJomd55OVuTYz6e/hypercycle-developer-guide/reference/pyhypercycle-aim-library-usage.md)&#x20;

***

### <mark style="color:blue;">What’s Next</mark>

The next section extends endpoint logic to protect hardware resources:

[<mark style="color:yellow;">**Concurrency & Queues**</mark>](/hypercycle-cbno/u57KauJomd55OVuTYz6e/hypercycle-developer-guide/aim-building-guide/concurrency-and-queues.md)

That section introduces:

* `SimpleQueue`
* `AsyncQueue`
* Safe handling of GPU-bound workloads
