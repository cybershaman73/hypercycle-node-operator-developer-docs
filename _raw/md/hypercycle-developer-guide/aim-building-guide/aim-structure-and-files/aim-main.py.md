> For the complete documentation index, see [llms.txt](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/hypercycle-developer-guide/aim-building-guide/aim-structure-and-files/aim-main.py.md).

# AIM main.py

Tortoise TTS AIM main.py

#### &#x20;<mark style="color:yellow;">Example: python imports, manifest, and endpoints</mark>

```python
import base64
import math
import os
import subprocess
import tempfile

import torchaudio
from pyhypercycle_aim import JSONResponseCORS, SimpleQueue, aim_uri
from tortoise.api import TextToSpeech
from tortoise.utils.audio import get_voices, load_voices

PORT = int(os.environ.get("PORT", "4000"))
EXTRA_VOICES = [
    v
    for v in [
        f"{os.path.dirname(__file__)}/extra-voices/",
        os.path.abspath(f"{os.path.dirname(__file__)}/../extra-voices"),
    ]
    if os.path.isdir(v)
]


class TortoiseAim(SimpleQueue):
    manifest = {
        "name": "TortoiseTTS",
        "short_name": "tortoise",
        "costs": "Returns costs based on number of words in input, or length of output (whichever is greater).",
        "version": "0.1.0",
        "license": "Open",
        "terms-of-service": "https://hypercycle.ai/tos",
        "author": "inaimathi<leo.zovic@gmail.com>",
    }

    def __init__(self):
        self.model = TextToSpeech(kv_cache=True, half=True)
        self.available_voices = list(get_voices(EXTRA_VOICES).keys())

    @aim_uri(
        uri="/list-voices",
        methods=["GET"],
        endpoint_manifest={
            "input_query": "",
            "input_headers": {},
            "input_body": {},
            "output_body": {"available_voices": ["<Voice>"]},
            # "currency": "HYPC",
            "documentation": "",
            # "price_per_call": {"estimated_cost": 0, "min": 0, "max": 0.1},
            # "price_per_mb": {"estimated_cost": 0, "min": 0, "max": 0.1},
            "example_calls": [
                {
                    "method": "GET",
                    "query": "",
                    "headers": "",
                }
            ],
        },
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

    @aim_uri(
        uri="/speak",
        methods=["OPTIONS"],
        endpoint_manifest={
            "input_query": "",
            "input_headers": {},
            "input_body": {},
            "output_body": {"available_voices": ["<Voice>"]},
            # "currency": "HYPC",
            "documentation": "",
            "example_calls": [
                {
                    "body": {},
                    "method": "OPTIONS",
                    "query": "",
                    "headers": "",
                }
            ],
        },
    )
    async def options(self, request):
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
    async def post(self, request):
        body = await request.json()
        text = body["text"]
        voice = body.get("voice", "daniel")
        if voice not in set(self.available_voices):
            return JSONResponseCORS({"error": "voice not found"}, status_code=400)
        if request.headers.get("cost_only"):
            return JSONResponseCORS({"costs": self.estimate(body["text"])})
        spoken, duration = self.orate(text, voice)
        return JSONResponseCORS(
            {"file": spoken}, costs=self.estimate(body["text"], used=True)
        )

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

    def orate(self, text, voice):
        arr = self.model.tts_with_preset(
            text, voice_samples=load_voices([voice], EXTRA_VOICES)[0]
        )
        with tempfile.NamedTemporaryFile(suffix=".wav") as f:
            torchaudio.save(f.name, arr.squeeze(0).cpu(), 24000)
            duration = float(subprocess.check_output(["soxi", "-D", f.name]))
            return base64.b64encode(f.read()).decode("utf-8"), duration


def main():
    app = TortoiseAim()
    app.run(uvicorn_kwargs={"port": PORT, "host": "0.0.0.0"})


if __name__ == "__main__":
    main()
```
