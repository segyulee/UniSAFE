from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

from tqdm import tqdm

from .data import DEFAULT_DATASET, load_cases, summarize_cases
from .io import read_jsonl, write_json, write_jsonl
from .judging import create_backend, evaluate_many
from .metrics import aggregate_judgments
from .schema import Judgment, Prediction, case_key


def _add_source_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--split", required=True, choices=("image", "text"))
    parser.add_argument("--dataset", default=DEFAULT_DATASET)
    parser.add_argument(
        "--cases-file",
        type=Path,
        help="Use a local JSONL export instead of loading from Hugging Face.",
    )


def _load_predictions(path: Path, *, check_files: bool = False) -> list[Prediction]:
    predictions: list[Prediction] = []
    seen: set[tuple[str, str, str]] = set()
    for row in read_jsonl(path):
        prediction = Prediction.from_mapping(row)
        if prediction.output_image:
            image = Path(prediction.output_image)
            if not image.is_absolute():
                prediction.output_image = str((path.parent / image).resolve())
        prediction.output_images = [
            str((path.parent / image).resolve()) if not Path(image).is_absolute() else image
            for image in prediction.output_images
        ]
        prediction.validate(check_files=check_files)
        key = (prediction.model, prediction.id, prediction.scenario_type)
        if key in seen:
            raise ValueError(f"duplicate prediction: {key}")
        seen.add(key)
        predictions.append(prediction)
    return predictions


def _resolve_case_paths(cases: list[dict[str, Any]], cases_file: Path | None) -> None:
    if cases_file is None:
        return
    base = cases_file.parent.resolve()
    for case in cases:
        for field in ("input_image", "input_image_b"):
            value = case.get(field)
            if isinstance(value, str) and value and not Path(value).is_absolute():
                case[field] = str((base / value).resolve())


def _load_source(args: argparse.Namespace) -> list[dict[str, Any]]:
    cases = load_cases(
        split=args.split,
        dataset=args.dataset,
        cases_file=args.cases_file,
    )
    _resolve_case_paths(cases, args.cases_file)
    return cases


def command_info(args: argparse.Namespace) -> int:
    summary = summarize_cases(_load_source(args))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def command_validate(args: argparse.Namespace) -> int:
    predictions = _load_predictions(args.predictions, check_files=args.check_files)
    models = sorted({prediction.model for prediction in predictions})
    tasks: dict[str, int] = {}
    for prediction in predictions:
        tasks[prediction.scenario_type] = tasks.get(prediction.scenario_type, 0) + 1
    print(
        json.dumps(
            {"valid": len(predictions), "models": models, "tasks": dict(sorted(tasks.items()))},
            indent=2,
        )
    )
    return 0


def command_evaluate(args: argparse.Namespace) -> int:
    cases = _load_source(args)
    case_index = {case_key(case): case for case in cases}
    predictions = _load_predictions(args.predictions)

    selected: list[tuple[dict[str, Any], Prediction]] = []
    missing_cases: list[tuple[str, str]] = []
    tasks = set(args.task or [])
    for prediction in predictions:
        if tasks and prediction.scenario_type not in tasks:
            continue
        case = case_index.get((prediction.id, prediction.scenario_type))
        if case is None:
            missing_cases.append((prediction.id, prediction.scenario_type))
            continue
        selected.append((case, prediction))
    if missing_cases:
        example = missing_cases[0]
        raise ValueError(
            f"{len(missing_cases)} predictions have no matching case; first: {example}"
        )
    if args.limit is not None:
        selected = selected[: args.limit]
    if not selected:
        raise ValueError("no predictions selected for evaluation")

    completed: list[Judgment] = []
    completed_keys: set[tuple[str, str, str, str]] = set()
    if args.resume and args.output.exists():
        completed = [Judgment.from_mapping(row) for row in read_jsonl(args.output)]
        completed_keys = {
            (row.model, row.id, row.scenario_type, row.judge) for row in completed
        }

    pending = [
        pair
        for pair in selected
        if (pair[1].model, pair[1].id, pair[1].scenario_type, args.judge_model)
        not in completed_keys
    ]
    backend = create_backend(
        args.backend,
        args.judge_model,
        base_url=args.base_url,
    )
    generated = evaluate_many(
        pending,
        backend,
        workers=args.workers,
        detect_text_refusals=args.detect_text_refusals,
        max_attempts=args.max_attempts,
    )
    for index, judgment in enumerate(
        tqdm(generated, total=len(pending), desc="Judging"), start=1
    ):
        completed.append(judgment)
        if index % args.checkpoint_every == 0:
            write_jsonl(args.output, (row.to_dict() for row in completed))
    write_jsonl(args.output, (row.to_dict() for row in completed))
    errors = sum(row.error is not None for row in completed)
    print(f"Wrote {len(completed)} judgments to {args.output} ({errors} errors).")
    return 0


def command_aggregate(args: argparse.Namespace) -> int:
    rows: list[dict[str, Any]] = []
    for path in args.judgments:
        rows.extend(read_jsonl(path))
    result = aggregate_judgments(rows)
    write_json(args.output, result)
    print(f"Wrote metrics to {args.output}.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="unisafe", description="UniSAFE benchmark evaluation toolkit"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    info = subparsers.add_parser("info", help="Summarize a benchmark split.")
    _add_source_arguments(info)
    info.set_defaults(func=command_info)

    validate = subparsers.add_parser(
        "validate", help="Validate a model predictions JSONL file."
    )
    validate.add_argument("--predictions", type=Path, required=True)
    validate.add_argument("--check-files", action="store_true")
    validate.set_defaults(func=command_validate)

    evaluate = subparsers.add_parser(
        "evaluate", help="Evaluate model predictions with an automated judge."
    )
    _add_source_arguments(evaluate)
    evaluate.add_argument("--predictions", type=Path, required=True)
    evaluate.add_argument("--output", type=Path, required=True)
    evaluate.add_argument(
        "--backend", required=True, choices=("google", "openai", "openai-compatible")
    )
    evaluate.add_argument("--judge-model", required=True)
    evaluate.add_argument("--base-url")
    evaluate.add_argument("--task", action="append", choices=("TI", "IE", "IC", "MT", "TT", "IT", "MU"))
    evaluate.add_argument("--workers", type=int, default=4)
    evaluate.add_argument("--max-attempts", type=int, default=3)
    evaluate.add_argument("--limit", type=int)
    evaluate.add_argument("--checkpoint-every", type=int, default=10)
    evaluate.add_argument("--resume", action="store_true")
    evaluate.add_argument(
        "--detect-text-refusals",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    evaluate.set_defaults(func=command_evaluate)

    aggregate = subparsers.add_parser(
        "aggregate", help="Aggregate one or more judge JSONL files."
    )
    aggregate.add_argument("--judgments", type=Path, nargs="+", required=True)
    aggregate.add_argument("--output", type=Path, required=True)
    aggregate.set_defaults(func=command_aggregate)
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (OSError, RuntimeError, ValueError) as exc:
        parser.error(str(exc))
    return 2
