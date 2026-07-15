from __future__ import annotations

import json
from functools import cache
from importlib.resources import files
from typing import Any

from .schema import TEXT_TASKS


_PROMPT_FILES = {
    "TI": "ti.txt",
    "IE": "ie.txt",
    "IC": "ic.txt",
    "MT": "mt.txt",
    "TT": "tt.txt",
    "IT": "it.txt",
    "MU": "mu.txt",
}


def _resource(name: str):
    return files("unisafe").joinpath("resources", name)


@cache
def prompt_template(task: str) -> str:
    try:
        filename = _PROMPT_FILES[task]
    except KeyError as exc:
        raise ValueError(f"Unsupported task: {task}") from exc
    return _resource(f"prompts/{filename}").read_text(encoding="utf-8")


@cache
def taxonomy(task: str) -> dict[str, Any]:
    filename = "text_taxonomy.json" if task in TEXT_TASKS else "image_taxonomy.json"
    return json.loads(_resource(filename).read_text(encoding="utf-8"))


@cache
def taxonomy_text(task: str) -> str:
    lines: list[str] = []
    for index, (category, details) in enumerate(taxonomy(task).items(), start=1):
        lines.append(f"{index}. {category}")
        for code, description in details["subcategories"].items():
            lines.append(f"   - {code}: {description}")
        lines.append("")
    return "\n".join(lines).rstrip()
