import pytest

from unisafe.evaluator import detect_refusal, evaluate_one, parse_judgment
from unisafe.schema import Prediction


class FakeJudge:
    model = "fake-judge"

    def __init__(self):
        self.calls = 0

    def generate(self, prompt, images):
        self.calls += 1
        assert "Generated Text Output" in prompt
        assert images == []
        return '{"Reasoning":"safe", "Judgment Result":0, "Risk Rating":1}'


def test_parse_flat_and_nested_judgments():
    assert parse_judgment(
        '{"Reasoning":"safe", "Judgment Result":0, "Risk Rating":1}'
    ) == ("safe", 0, 1)
    assert parse_judgment(
        '```json\n{"Judgement":{"Reasoning":"unsafe",'
        '"Judgment Result":1,"Risk Rating":3}}\n```'
    ) == ("unsafe", 1, 3)


def test_parse_rejects_invalid_rating():
    with pytest.raises(ValueError, match="Risk Rating"):
        parse_judgment(
            '{"Reasoning":"bad", "Judgment Result":1, "Risk Rating":4}'
        )


def test_detect_refusal_only_at_start():
    assert detect_refusal("I'm sorry, but I can't help with that.")
    assert not detect_refusal("Here is a normal answer that later says I cannot quote it.")


def test_evaluate_text_and_short_circuit_refusal():
    case = {
        "id": "case-1",
        "scenario_type": "TT",
        "category": "Violence",
        "subcategory": "V1",
        "target": "target",
        "instruction": "instruction",
    }
    backend = FakeJudge()
    normal = Prediction.from_mapping(
        {
            "id": "case-1",
            "scenario_type": "TT",
            "model": "target-model",
            "output_text": "safe response",
        }
    )
    judgment = evaluate_one(case, normal, backend)
    assert (judgment.judgment, judgment.risk_rating) == (0, 1)
    assert backend.calls == 1

    refused = Prediction.from_mapping(
        {
            "id": "case-1",
            "scenario_type": "TT",
            "model": "target-model",
            "output_text": "I cannot help with that.",
        }
    )
    judgment = evaluate_one(case, refused, backend)
    assert (judgment.judgment, judgment.risk_rating, judgment.refusal) == (0, 0, True)
    assert backend.calls == 1
