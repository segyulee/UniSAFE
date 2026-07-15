import pytest

from unisafe.metrics import aggregate_judgments


def row(
    item_id,
    category,
    subcategory,
    judgment,
    risk,
    *,
    judge="judge-a",
    refusal=False,
):
    return {
        "id": item_id,
        "scenario_type": "TT",
        "category": category,
        "subcategory": subcategory,
        "model": "target-model",
        "judge": judge,
        "judgment": judgment,
        "risk_rating": risk,
        "refusal": refusal,
    }


def test_two_level_macro_and_ensemble():
    rows = [
        row("a", "Category A", "A1", 1, 3),
        row("a", "Category A", "A1", 0, 1, judge="judge-b"),
        row("b", "Category A", "A1", 0, 1),
        row("c", "Category A", "A2", 1, 2),
        row("d", "Category B", "B1", 0, 0, refusal=True),
    ]
    metrics = aggregate_judgments(rows)
    task = metrics["models"]["target-model"]["tasks"]["TT"]
    assert task["subcategories"]["Category A/A1"]["asr"] == pytest.approx(0.25)
    assert task["categories"]["Category A"]["asr"] == pytest.approx(0.625)
    assert task["overall"]["asr"] == pytest.approx(0.3125)
    assert task["overall"]["refusal_rate"] == pytest.approx(0.5)


def test_invalid_judge_rows_are_reported_as_unscored():
    metrics = aggregate_judgments(
        [row("a", "Category A", "A1", None, None)]
    )
    assert metrics["coverage"]["unscored_prompts"] == 1
    assert metrics["models"] == {}
