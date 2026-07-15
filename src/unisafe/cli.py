from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Iterable

from tqdm import tqdm

from .data import DEFAULT_DATASET, load_cases
from .evaluator import evaluate
from .io import read_jsonl, write_jsonl
from .providers import create_judge
from .schema import Judgment, Prediction, case_key


def _predictions(path: Path) -> list[Prediction]:
    rows: list[Prediction] = []
    seen: set[tuple[str, str, str]] = set()
    for value in read_jsonl(path):
        prediction = Prediction.from_mapping(value)
        if prediction.output_image:
            prediction.output_image = _absolute(path.parent, prediction.output_image)
        prediction.output_images = [
            _absolute(path.parent, image) for image in prediction.output_images
        ]
        key = (prediction.model, prediction.id, prediction.scenario_type)
        if key in seen:
            raise ValueError(f"Duplicate prediction: {key}")
        seen.add(key)
        rows.append(prediction)
    return rows


def _absolute(base: Path, value: str) -> str:
    path = Path(value)
    return str(path if path.is_absolute() else (base / path).resolve())


def _resolve_case_images(cases: list[dict[str, Any]], source: Path | None) -> None:
    if source is None:
        return
    for case in cases:
        for field in ("input_image", "input_image_b"):
            if isinstance(case.get(field), str) and case[field]:
                case[field] = _absolute(source.parent, case[field])


def _pairs(
    cases: list[dict[str, Any]],
    predictions: list[Prediction],
    tasks: set[str],
) -> list[tuple[dict[str, Any], Prediction]]:
    case_index = {case_key(case): case for case in cases}
    pairs: list[tuple[dict[str, Any], Prediction]] = []
    for prediction in predictions:
        if tasks and prediction.scenario_type not in tasks:
            continue
        key = (prediction.id, prediction.scenario_type)
        if key not in case_index:
            raise ValueError(f"Prediction has no matching benchmark case: {key}")
        pairs.append((case_index[key], prediction))
    return pairs


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="unisafe-eval",
        description="Evaluate UniSAFE model outputs with an automated judge.",
    )
    parser.add_argument("--split", required=True, choices=("image", "text"))
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--dataset", default=DEFAULT_DATASET)
    parser.add_argument("--cases-file", type=Path)
    parser.add_argument(
        "--backend",
        required=True,
        choices=("google", "openai", "openai-compatible"),
    )
    parser.add_argument("--judge-model", required=True)
    parser.add_argument("--base-url")
    parser.add_argument(
        "--task",
        action="append",
        choices=("TI", "IE", "IC", "MT", "TT", "IT", "MU"),
    )
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--resume", action="store_true")
    return parser


def run(args: argparse.Namespace) -> None:
    cases = load_cases(
        split=args.split,
        dataset=args.dataset,
        cases_file=args.cases_file,
    )
    _resolve_case_images(cases, args.cases_file)
    pairs = _pairs(cases, _predictions(args.predictions), set(args.task or []))
    if args.limit is not None:
        pairs = pairs[: args.limit]
    if not pairs:
        raise ValueError("No predictions selected")

    completed: list[Judgment] = []
    completed_keys: set[tuple[str, str, str, str]] = set()
    if args.resume and args.output.exists():
        completed = [Judgment.from_mapping(row) for row in read_jsonl(args.output)]
        completed_keys = {
            (row.model, row.id, row.scenario_type, row.judge) for row in completed
        }
    pending = [
        pair
        for pair in pairs
        if (pair[1].model, pair[1].id, pair[1].scenario_type, args.judge_model)
        not in completed_keys
    ]
    if not pending:
        print(f"Nothing to evaluate; {len(completed)} judgments already exist.")
        return

    judge = create_judge(args.backend, args.judge_model, args.base_url)
    results = evaluate(
        pending,
        judge,
        workers=args.workers,
        max_attempts=args.max_attempts,
    )
    for index, judgment in enumerate(
        tqdm(results, total=len(pending), desc="Evaluating"), start=1
    ):
        completed.append(judgment)
        if index % 10 == 0:
            write_jsonl(args.output, (row.to_dict() for row in completed))
    write_jsonl(args.output, (row.to_dict() for row in completed))

    errors = sum(row.error is not None for row in completed)
    print(f"Saved {len(completed)} judgments to {args.output} ({errors} errors).")


def main(argv: Iterable[str] | None = None) -> int:
    parser = _parser()
    try:
        run(parser.parse_args(argv))
    except (OSError, RuntimeError, ValueError) as exc:
        parser.error(str(exc))
    return 0
