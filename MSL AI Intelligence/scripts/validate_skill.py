#!/usr/bin/env python3
"""Small validation helper for repository skills.

This is intentionally dependency-free so CI and fresh clones can run it before
installing any package extras.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter.")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter must be closed with ---.")
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        return [f"Missing {skill_md}"]

    text = skill_md.read_text(encoding="utf-8")
    try:
        fields = _frontmatter(text)
    except ValueError as exc:
        return [str(exc)]

    name = fields.get("name", "")
    description = fields.get("description", "")
    if name != path.name:
        errors.append(f"Skill name '{name}' must match directory '{path.name}'.")
    if not re.fullmatch(r"[a-z0-9-]{1,63}", name):
        errors.append("Skill name must use lowercase letters, digits, and hyphens only.")
    if not description or "TODO" in description:
        errors.append("Skill description must be complete and non-empty.")

    openai_yaml = path / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        errors.append("Missing agents/openai.yaml.")
    else:
        yaml_text = openai_yaml.read_text(encoding="utf-8")
        if "$msl-ai-intelligence" not in yaml_text:
            errors.append("agents/openai.yaml default prompt should mention $msl-ai-intelligence.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    errors = validate(args.path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
