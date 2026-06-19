#!/usr/bin/env python3
"""Install the repository Codex skill into CODEX_HOME."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


def default_codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("skills/msl-ai-intelligence"),
        help="Skill source directory.",
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=default_codex_home(),
        help="Codex home directory.",
    )
    args = parser.parse_args()

    source = args.source.resolve()
    if not source.exists():
        raise SystemExit(f"Skill source does not exist: {source}")

    destination_root = args.codex_home.expanduser().resolve() / "skills"
    destination_root.mkdir(parents=True, exist_ok=True)
    destination = destination_root / source.name
    shutil.copytree(source, destination, dirs_exist_ok=True)
    print(f"Installed {source.name} to {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
