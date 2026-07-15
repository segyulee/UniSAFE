from pathlib import Path

import pytest
from PIL import Image

from unisafe.schema import Prediction


def test_text_prediction_is_valid():
    prediction = Prediction.from_mapping(
        {
            "id": "case-1",
            "scenario_type": "tt",
            "model": "example/model",
            "output_text": "A safe answer.",
        }
    )
    assert prediction.scenario_type == "TT"


def test_multiturn_requires_four_images(tmp_path: Path):
    paths = []
    for index in range(4):
        path = tmp_path / f"turn-{index}.png"
        Image.new("RGB", (4, 4)).save(path)
        paths.append(str(path))
    prediction = Prediction.from_mapping(
        {
            "id": "case-2",
            "scenario_type": "MT",
            "model": "example/model",
            "output_images": paths,
        }
    )
    prediction.validate(check_files=True)

    with pytest.raises(ValueError, match="four ordered"):
        Prediction.from_mapping(
            {
                "id": "case-2",
                "scenario_type": "MT",
                "model": "example/model",
                "output_images": paths[:3],
            }
        )
