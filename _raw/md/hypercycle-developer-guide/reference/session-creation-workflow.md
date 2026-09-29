> For the complete documentation index, see [llms.txt](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/hypercycle-developer-guide/reference/session-creation-workflow.md).

# Session Creation Workflow

This documentation describes the session creation process that enables authenticated interactions with AIMs without requiring wallet signatures for each request. Sessions improve user experience by maintaining authentication state for a configurable duration.

### Prerequisites <a href="#prerequisites" id="prerequisites"></a>

* Valid wallet address (e.g., `0x742d35Cc6634C0532925a3b844Bc454e4438f44e`)
* Web3 library installed (ethers.js, viem, or equivalent)
* Server endpoint access

### <mark style="color:$success;">Process Overview</mark> <a href="#process-overview" id="process-overview"></a>

1. Generate cryptographic key pair
2. Request session UUID via GET
3. Sign session parameters
4. Register session via POST
5. Use session for authenticated requests

### <mark style="color:orange;">Step-by-Step Implementation</mark> <a href="#step-by-step-implementation" id="step-by-step-implementation"></a>

#### <mark style="color:blue;">1. Generate Key Pair</mark> <a href="#id-1-generate-key-pair" id="id-1-generate-key-pair"></a>

Using a web3 library, create a cryptographic key pair:

```
// ethers.js example
import { ethers } from "ethers";

const wallet = ethers.Wallet.createRandom();
const publicKey = wallet.publicKey;  // "0x04a1b...2c3d4"
const privateKey = wallet.privateKey; // Securely store
```

#### <mark style="color:blue;">2. Request Session UUID</mark> <a href="#id-2-request-session-uuid" id="id-2-request-session-uuid"></a>

Initiate session creation with a GET request:

**Endpoint: `GET /create_session`**

**Parameters:**

| **Name**       | **Required** | **Type** | **Description**             | **Constraints**                                                                            |
| -------------- | ------------ | -------- | --------------------------- | ------------------------------------------------------------------------------------------ |
| `user_address` | Yes          | String   | Wallet address              | Valid address                                                                              |
| `duration`     | No           | Integer  | Session lifetime in seconds | <p><em>Default</em>: <code>21600</code> (6h)<br><em>Max</em>: <code>86400</code> (24h)</p> |

**Example Request:**

```
curl -X GET "http://api.example.com/create_session?user_address=0x742d35Cc6634C0532925a3b844Bc454e4438f44e&duration=36000"
```

**Response:**

```
{
  "data": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

#### <mark style="color:blue;">3. Create Session Signature</mark> <a href="#id-3-create-session-signature" id="id-3-create-session-signature"></a>

Construct and sign the verification message:

**Message Format:** `<public_key>_<session_key>`

**Example:**

```
0x04a1b...2c3d4_f47ac10b-58cc-4372-a567-0e02b2c3d479
```

**Signing Process:**

```
const message = `${publicKey}_${sessionKey}`;
const signature = await wallet.signMessage(message); 
// "0x3045022100e0ac..."
```

#### <mark style="color:blue;">4. Register Session</mark> <a href="#id-4-register-session" id="id-4-register-session"></a>

Submit signed parameters to activate the session:

**Endpoint: `POST /create_session`**\
**Content-Type: `application/json`**

**Request Body:**

```
{
  "signer_address": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "public_key": "0x04a1b...2c3d4",
  "session_key": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "signature": "0x3045022100e0ac..."
}
```

**Success Response:**

```
{
  "status": "ok"
}
```

#### <mark style="color:blue;">5. Use Session Authentication</mark> <a href="#id-5-use-session-authentication" id="id-5-use-session-authentication"></a>

For subsequent AIM requests:

1. Sign the nonce using the private key
2. Include session in headers
3. Omit wallet signatures

**Example Request**

```
# NOTE: Other needed headers are not included on this example...
curl --location 'localhost:8000/aim/0/create' \
--header 'tx-session-key: f47ac10b-58cc-4372-a567-0e02b2c3d479' \
--header 'tx-sender: 0x742d35Cc6634C0532925a3b844Bc454e4438f44e' \
--header 'tx-nonce: 659492e8a529939ed35ce0480844f9499bc09f8aee63f79d06cbbf377a91f110' \
--header 'tx-signature: 0xe15a9ecee539...' \
--header 'Content-Type: application/json' \
--data '{}'
```
