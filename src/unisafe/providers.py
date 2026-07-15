from __future__ import annotations

import base64
import os
from io import BytesIO
from typing import Any, Protocol, Sequence

from PIL import Image


JUDGMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "Reasoning": {"type": "string"},
        "Judgment Result": {"type": "integer", "enum": [0, 1]},
        "Risk Rating": {"type": "integer", "minimum": 1, "maximum": 3},
    },
    "required": ["Reasoning", "Judgment Result", "Risk Rating"],
    "additionalProperties": False,
}


class Judge(Protocol):
    model: str

    def generate(self, prompt: str, images: Sequence[Image.Image]) -> str: ...


def _data_url(image: Image.Image) -> str:
    buffer = BytesIO()
    image.convert("RGB").save(buffer, format="JPEG", quality=95)
    payload = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{payload}"


class OpenAIJudge:
    def __init__(self, model: str):
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "Install the OpenAI extra: pip install -e '.[openai]'"
            ) from exc
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate(self, prompt: str, images: Sequence[Image.Image]) -> str:
        content: list[dict[str, Any]] = [{"type": "input_text", "text": prompt}]
        content.extend(
            {"type": "input_image", "image_url": _data_url(image)} for image in images
        )
        response = self.client.responses.create(
            model=self.model,
            input=[{"role": "user", "content": content}],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "unisafe_judgment",
                    "schema": JUDGMENT_SCHEMA,
                    "strict": True,
                }
            },
        )
        return response.output_text


class CompatibleJudge:
    def __init__(self, model: str, base_url: str | None):
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "Install the OpenAI extra: pip install -e '.[openai]'"
            ) from exc
        self.model = model
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=base_url or os.getenv("OPENAI_BASE_URL"),
        )

    def generate(self, prompt: str, images: Sequence[Image.Image]) -> str:
        content: list[dict[str, Any]] = [{"type": "text", "text": prompt}]
        content.extend(
            {"type": "image_url", "image_url": {"url": _data_url(image)}}
            for image in images
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": content}],
            response_format={"type": "json_object"},
            temperature=0,
        )
        return response.choices[0].message.content or ""


class GoogleJudge:
    def __init__(self, model: str):
        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:
            raise RuntimeError(
                "Install the Google extra: pip install -e '.[google]'"
            ) from exc
        self.model = model
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.types = types

    def generate(self, prompt: str, images: Sequence[Image.Image]) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=[prompt, *images],
            config=self.types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json",
                response_schema=JUDGMENT_SCHEMA,
            ),
        )
        return response.text or ""


def create_judge(backend: str, model: str, base_url: str | None = None) -> Judge:
    if backend == "google":
        return GoogleJudge(model)
    if backend == "openai":
        return OpenAIJudge(model)
    if backend == "openai-compatible":
        return CompatibleJudge(model, base_url)
    raise ValueError(f"Unsupported backend: {backend}")
