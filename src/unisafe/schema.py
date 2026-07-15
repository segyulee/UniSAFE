from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Mapping


IMAGE_TASKS = frozenset({"TI", "IE", "IC", "MT"})
TEXT_TASKS = frozenset({"TT", "IT", "MU"})
TASKS = IMAGE_TASKS | TEXT_TASKS


def case_key(item: Mapping[str, Any]) -> tuple[str, str]:
    """Return the stable key used to join a case with a prediction."""
    return str(item.get("id", "")), str(item.get("scenario_type", "")).upper()


@dataclass(slots=True)
class Prediction:
    id: str
    scenario_type: str
    model: str
    output_text: str | None = None
    output_image: str | None = None
    output_images: list[str] = field(default_factory=list)
    refusal: bool = False
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "Prediction":
        output_images = value.get("output_images") or []
        if not isinstance(output_images, list):
            raise ValueError("output_images must be a list")
        prediction = cls(
            id=str(value.get("id", "")).strip(),
            scenario_type=str(value.get("scenario_type", "")).upper().strip(),
            model=str(value.get("model", "")).strip(),
            output_text=value.get("output_text"),
            output_image=value.get("output_image"),
            output_images=[str(path) for path in output_images],
            refusal=bool(value.get("refusal", False)),
            error=value.get("error"),
            metadata=dict(value.get("metadata") or {}),
        )
        prediction.validate()
        return prediction

    def validate(self, *, check_files: bool = False) -> None:
        if not self.id:
            raise ValueError("id is required")
        if self.scenario_type not in TASKS:
            raise ValueError(f"scenario_type must be one of {sorted(TASKS)}")
        if not self.model:
            raise ValueError("model is required")
        if self.error or self.refusal:
            return
        if self.scenario_type in TEXT_TASKS:
            if not isinstance(self.output_text, str) or not self.output_text.strip():
                raise ValueError(f"output_text is required for {self.scenario_type}")
            return
        paths = self.output_images if self.scenario_type == "MT" else [self.output_image]
        if self.scenario_type == "MT" and len(paths) != 4:
            raise ValueError("MT predictions require four ordered output_images")
        if any(not isinstance(path, str) or not path for path in paths):
            raise ValueError(f"image output is required for {self.scenario_type}")
        if check_files:
            missing = [path for path in paths if not Path(path).is_file()]
            if missing:
                raise ValueError(f"image output does not exist: {missing[0]}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Judgment:
    id: str
    scenario_type: str
    category: str
    subcategory: str
    model: str
    judge: str
    judgment: int | None
    risk_rating: int | None
    refusal: bool = False
    reasoning: str | None = None
    error: str | None = None
    raw_response: str | None = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "Judgment":
        return cls(
            id=str(value["id"]),
            scenario_type=str(value["scenario_type"]).upper(),
            category=str(value["category"]),
            subcategory=str(value["subcategory"]),
            model=str(value.get("model", "unknown")),
            judge=str(value.get("judge", "unknown")),
            judgment=value.get("judgment"),
            risk_rating=value.get("risk_rating"),
            refusal=bool(value.get("refusal", False)),
            reasoning=value.get("reasoning"),
            error=value.get("error"),
            raw_response=value.get("raw_response"),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
