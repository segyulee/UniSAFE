from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Iterable, Mapping

from .io import read_jsonl
from .schema import TASKS, case_key


DEFAULT_DATASET = "segyulee/UniSAFE"


def load_cases(
    *,
    split: str,
    dataset: str = DEFAULT_DATASET,
    cases_file: str | Path | None = None,
    token: str | None = None,
) -> list[dict[str, Any]]:
    """Load benchmark cases from the Hub or a local JSONL export."""
    if split not in {"image", "text"}:
        raise ValueError("split must be 'image' or 'text'")
    if cases_file is not None:
        rows = list(read_jsonl(cases_file))
    else:
        try:
            from datasets import load_dataset
        except ImportError as exc:
            raise RuntimeError(
                "Hugging Face loading requires `pip install -e '.[data]'`"
            ) from exc
        rows = list(
            load_dataset(
                dataset,
                split=split,
                token=token or os.getenv("HF_TOKEN") or None,
            )
        )
    validate_cases(rows, split=split)
    return rows


def validate_cases(rows: Iterable[Mapping[str, Any]], *, split: str) -> None:
    expected = {"TI", "IE", "IC", "MT"} if split == "image" else {"TT", "IT", "MU"}
    seen: set[tuple[str, str]] = set()
    for index, row in enumerate(rows, start=1):
        missing = [
            key
            for key in ("id", "category", "subcategory", "scenario_type", "instruction")
            if key not in row
        ]
        if missing:
            raise ValueError(f"case {index}: missing fields: {', '.join(missing)}")
        key = case_key(row)
        if not key[0]:
            raise ValueError(f"case {index}: id is empty")
        if key[1] not in TASKS or key[1] not in expected:
            raise ValueError(f"case {index}: invalid scenario_type {key[1]!r} for {split}")
        if key in seen:
            raise ValueError(f"case {index}: duplicate case key {key}")
        seen.add(key)
