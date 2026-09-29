> For the complete documentation index, see [llms.txt](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/hypercycle-developer-guide/aim-building-guide/aim-structure-and-files/aim-manifest-json.md).

# AIM manifest.json

Comprehensive walkthrough on how to document your REST APIs in a manifest.json style. Examples used in this walkthrough do NOT pertain to the Tortoise TTS AIM used elsewhere in this guide.

### <mark style="color:blue;">Top-Level Manifest Structure</mark>

The `manifest.json` format starts with these fields:

* **`name`**: The API's name (e.g., `"User Management API"`).
* **`short_name`**: A short identifier for the API (e.g., `"user_api"`).
* **`version`**: API version (e.g., `"1.0"`).
* **`documentation_url`**: Link to detailed API documentation.
* **`license`**: License type (e.g., `"MIT"`).
* **`terms_of_service`**: Link to terms of service.
* **`author`**: Author or owner name.
* **`endpoints`**: Array of endpoint objects.

***

### <mark style="color:blue;">Endpoint Structure</mark>

Each endpoint in the `endpoints` array must include the following fields:

#### 1. <mark style="color:yellow;">`uri`</mark>

* **Description**: The endpoint path.
* **Example**: `"/users/{id}"`

#### 2. <mark style="color:yellow;">`methods`</mark>

* **Description**: Supported HTTP methods.
* **Example**: `["GET", "POST"]`

#### 3. <mark style="color:yellow;">`input_query`</mark>

* **Description**: Query parameters accepted by the endpoint.
* **Example**:

  ```json
  {
      "id": {
          "description": "The ID of the user",
          "required": true,
          "example": "12345"
      }
  }
  ```

#### 4. <mark style="color:yellow;">`input_headers`</mark>

* **Description**: Headers required by the endpoint.
* **Example**:

  ```json
  {
      "Authorization": {
          "description": "Bearer token for authentication",
          "example": "Bearer <token>"
      }
  }
  ```

#### 5. <mark style="color:yellow;">`input_body`</mark>

* **Description**: Request body for POST/PUT methods.
* **Example**:

  ```json
  {
      "username": {
          "description": "The user's username",
          "type": "string",
          "required": true,
          "example": "johndoe"
      },
      "password": {
          "description": "The user's password",
          "type": "string",
          "required": true,
          "example": "password123"
      }
  }
  ```

#### 6. <mark style="color:yellow;">`output`</mark>

* **Description**: Response structure.
* **Example**:

  ```json
  {
      "id": {
          "description": "User ID",
          "type": "string",
          "example": "12345"
      },
      "name": {
          "description": "User's name",
          "type": "string",
          "example": "John Doe"
      }
  }
  ```

#### 7. <mark style="color:yellow;">`currency`</mark>

* **Description**: Currency for pricing.
* **Example**: `"USD"`

#### 8. <mark style="color:yellow;">`price_per_call`</mark>

* **Description**: Pricing per API call.
* **Example**:

  ```json
  {
      "estimated_cost": 0.01,
      "min": 0,
      "max": 0.1
  }
  ```

#### 9. <mark style="color:yellow;">`price_per_mb`</mark>

* **Description**: Pricing per MB of data transferred.
* **Example**:

  ```json
  {
      "estimated_cost": 0.01,
      "min": 0,
      "max": 0.1
  }
  ```

#### 10. <mark style="color:yellow;">`documentation`</mark>

* **Description**: A short explanation of the endpoint.
* **Example**: `"Retrieve user information by ID."`

#### 11. <mark style="color:yellow;">`example_calls`</mark>

* **Description**: Examples of how to use the endpoint.
* **Example**:

  ```json
  [
      {
          "method": "GET",
          "query": {
              "id": "12345"
          },
          "headers": {
              "Authorization": "Bearer <token>"
          },
          "body": {},
          "output": {
              "id": "12345",
              "name": "John Doe"
          }
      }
  ]
  ```

***

### <mark style="color:yellow;">Example manifest.json</mark>

```json
{
    "name": "LLM Inference API",
    "short_name": "llm_api",
    "version": "1.0",
    "documentation_url": "https://example.com/docs",
    "license": "Proprietary",
    "terms_of_service": "https://example.com/terms",
    "author": "AI Company",
    "endpoints": [
        {
            "uri": "/v1/completions",
            "methods": ["POST"],
            "input_query": {},
            "input_headers": {
                "Authorization": {
                    "description": "Bearer token for authentication",
                    "example": "Bearer <token>"
                }
            },
            "input_body": {
                "model": {
                    "description": "The model to use for inference (e.g., gpt-4)",
                    "type": "string",
                    "required": true,
                    "example": "gpt-4"
                },
                "prompt": {
                    "description": "The input prompt for the model",
                    "type": "string",
                    "required": true,
                    "example": "Write a short poem about the moon."
                },
                "max_tokens": {
                    "description": "The maximum number of tokens to generate",
                    "type": "integer",
                    "required": false,
                    "example": 150
                },
                "temperature": {
                    "description": "Sampling temperature",
                    "type": "number",
                    "required": false,
                    "example": 0.7
                }
            },
            "output": {
                "id": {
                    "description": "Unique ID for the request",
                    "type": "string",
                    "example": "cmpl-12345"
                },
                "choices": [
                    {
                        "text": {
                            "description": "The generated text from the model",
                            "type": "string",
                            "example": "The moon shines brightly in the night sky..."
                        },
                        "finish_reason": {
                            "description": "Reason for stopping (e.g., max_tokens)",
                            "type": "string",
                            "example": "stop"
                        }
                    }
                ]
            },
            "currency": "USD",
            "price_per_call": {
                "estimated_cost": 0.02,
                "min": 0,
                "max": 0.1
            },
            "price_per_mb": {
                "estimated_cost": 0.01,
                "min": 0,
                "max": 0.05
            },
            "documentation": "Generate text completions based on a prompt using the specified model.",
            "example_calls": [
                {
                    "method": "POST",
                    "query": {},
                    "headers": {
                        "Authorization": "Bearer <token>"
                    },
                    "body": {
                        "model": "gpt-4",
                        "prompt": "Write a short poem about the moon.",
                        "max_tokens": 150,
                        "temperature": 0.7
                    },
                    "output": {
                        "id": "cmpl-12345",
                        "choices": [
                            {
                                "text": "The moon shines brightly in the night sky...",
                                "finish_reason": "stop"
                            }
                        ]
                    }
                }
            ]
        }
    ]
}
```

***

### <mark style="color:blue;">Best Practices</mark>

1. Use descriptive `documentation` fields for each endpoint.
2. Include detailed `example_calls` to demonstrate real usage.
3. Regularly update the `manifest.json` to reflect API changes.
4. Ensure the `example_calls` include realistic values for easy testing.
5. The price per call and price per mb should be set to the minimum value for the API and there not both required only one is required.
