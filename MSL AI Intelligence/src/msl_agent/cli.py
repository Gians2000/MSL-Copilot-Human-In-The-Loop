"""Command line interface for the MSL Agent PoC."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .agents import TrialOpportunityRequest, run_trial_opportunity_pipeline
from .demo import run_nsclc_demo


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    parser = argparse.ArgumentParser(prog="msl-agent")
    parser.add_argument("--version", action="store_true", help="Print package version and exit.")
    subparsers = parser.add_subparsers(dest="command")

    demo_parser = subparsers.add_parser("demo", help="Generate the minimal NSCLC demo artifacts.")
    demo_parser.add_argument(
        "--output",
        type=Path,
        default=Path("examples/nsclc_trial_opportunity_brief.md"),
    )
    demo_parser.add_argument(
        "--ledger-output",
        type=Path,
        default=Path("examples/evidence_ledger_sample.json"),
    )

    brief_parser = subparsers.add_parser("brief", help="Generate a brief from a TrialOpportunityRequest JSON file.")
    brief_parser.add_argument("input", type=Path)
    brief_parser.add_argument("--output", "-o", type=Path, required=True)
    brief_parser.add_argument("--ledger-output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command-line interface."""

    parser = build_parser()
    args = parser.parse_args(argv)
    if args.version:
        from . import __version__

        print(__version__)
        return 0
    if args.command == "demo":
        run_nsclc_demo(output=args.output, ledger_output=args.ledger_output)
        return 0
    if args.command == "brief":
        request = TrialOpportunityRequest.model_validate_json(args.input.read_text(encoding="utf-8"))
        result = run_trial_opportunity_pipeline(request)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result.final_report.markdown, encoding="utf-8")
        if args.ledger_output:
            args.ledger_output.parent.mkdir(parents=True, exist_ok=True)
            args.ledger_output.write_text(
                json.dumps(result.final_report.ledger.model_dump(mode="json"), indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        return 0
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
