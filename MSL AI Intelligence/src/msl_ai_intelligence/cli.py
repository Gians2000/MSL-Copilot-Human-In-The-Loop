"""Command line interface for MSL AI Intelligence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .example_data import EXAMPLE_OPPORTUNITY
from .scoring import score_opportunity
from .templates import render_opportunity_brief


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_or_print(text: str, output: Path | None) -> None:
    if output:
        output.write_text(text, encoding="utf-8")
    else:
        print(text)


def init_command(args: argparse.Namespace) -> int:
    args.output.write_text(
        json.dumps(EXAMPLE_OPPORTUNITY, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return 0


def score_command(args: argparse.Namespace) -> int:
    data = _read_json(args.input)
    report = score_opportunity(data.get("scores", {}))

    if args.format == "json":
        payload = {
            "weighted_score": report.weighted_score,
            "priority_band": report.priority_band,
            "missing_dimensions": list(report.missing_dimensions),
            "dimension_scores": report.dimension_scores,
        }
        _write_or_print(json.dumps(payload, indent=2) + "\n", args.output)
        return 0

    missing = "None" if not report.missing_dimensions else ", ".join(report.missing_dimensions)
    markdown = "\n".join(
        [
            f"- Weighted score: {report.weighted_score}/100",
            f"- Priority band: {report.priority_band}",
            f"- Missing scoring dimensions: {missing}",
        ]
    )
    _write_or_print(markdown + "\n", args.output)
    return 0


def render_command(args: argparse.Namespace) -> int:
    data = _read_json(args.input)
    _write_or_print(render_opportunity_brief(data), args.output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="msl-intel")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Write an example opportunity JSON file.")
    init_parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("msl_opportunity_input.json"),
    )
    init_parser.set_defaults(func=init_command)

    score_parser = subparsers.add_parser("score", help="Score a trial opportunity JSON file.")
    score_parser.add_argument("input", type=Path)
    score_parser.add_argument("--output", "-o", type=Path)
    score_parser.add_argument("--format", choices=("json", "markdown"), default="json")
    score_parser.set_defaults(func=score_command)

    render_parser = subparsers.add_parser("render", help="Render a trial opportunity brief.")
    render_parser.add_argument("input", type=Path)
    render_parser.add_argument("--output", "-o", type=Path)
    render_parser.set_defaults(func=render_command)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
