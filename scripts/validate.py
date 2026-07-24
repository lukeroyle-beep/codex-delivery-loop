#!/usr/bin/env python3
"""Validate the GitHub Delivery Loop skill or an issue contract."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_REFERENCES = {
    "references/issue-contract.md",
    "references/state-model.md",
    "references/review-policy.md",
}
PRIMARY_LABELS = {
    "loop:spec",
    "loop:ready",
    "loop:building",
    "loop:review",
    "loop:changes",
    "loop:approved",
    "loop:blocked",
    "loop:human-review",
    "loop:done",
}
ISSUE_HEADINGS = [
    "## Problem",
    "## Acceptance criteria",
    "## Non-goals",
    "## Relevant files",
    "## Verification",
    "## Risk",
    "## Dependencies",
]


def fail(message: str) -> None:
    raise ValueError(message)


def validate_package(root: Path) -> None:
    skill = root / "SKILL.md"
    if not skill.is_file():
        fail(f"Missing {skill}")

    text = skill.read_text(encoding="utf-8")
    frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not frontmatter:
        fail("SKILL.md is missing YAML frontmatter")

    fields = [
        line.split(":", 1)[0].strip()
        for line in frontmatter.group(1).splitlines()
        if line.strip()
    ]
    if fields != ["name", "description"]:
        fail("SKILL.md frontmatter must contain only name and description")
    if "name: github-delivery-loop" not in frontmatter.group(1):
        fail("Skill name must be github-delivery-loop")

    for relative in sorted(REQUIRED_REFERENCES):
        if not (root / relative).is_file():
            fail(f"Missing {relative}")
        if relative not in text:
            fail(f"SKILL.md does not route to {relative}")

    state_text = (root / "references/state-model.md").read_text(encoding="utf-8")
    absent = sorted(label for label in PRIMARY_LABELS if label not in state_text)
    if absent:
        fail(f"State model is missing labels: {', '.join(absent)}")

    required_controls = [
        "Never merge",
        "fresh\nreviewer context",
        "maximum three completed work units",
        "maximum 45 minutes",
        "maximum two repair rounds",
        "re-fetch the head commit",
        "atomic",
    ]
    normalised = text.replace("\r\n", "\n")
    for control in required_controls:
        if control not in normalised:
            fail(f"SKILL.md is missing safety control: {control!r}")


def defined_ids(text: str, prefix: str) -> list[int]:
    if prefix == "AC":
        pattern = r"(?m)^- \[(?: |x|X)\] AC-(\d+):"
    else:
        pattern = r"(?m)^- NG-(\d+):"
    return [int(number) for number in re.findall(pattern, text)]


def validate_contract(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    positions = []
    for heading in ISSUE_HEADINGS:
        position = text.find(heading)
        if position < 0:
            fail(f"Missing heading: {heading}")
        positions.append(position)
    if positions != sorted(positions):
        fail("Issue contract headings are out of order")

    for prefix in ("AC", "NG"):
        ids = defined_ids(text, prefix)
        unique = sorted(set(ids))
        if not unique:
            fail(f"No {prefix}-N identifiers found")
        if unique != list(range(1, max(unique) + 1)):
            fail(f"{prefix}-N identifiers must be sequential from 1")
        if len(ids) != len(unique):
            fail(f"{prefix}-N identifiers must be unique in the contract")


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    package = subparsers.add_parser("package")
    package.add_argument("root", type=Path, nargs="?", default=Path(__file__).parents[1])
    contract = subparsers.add_parser("contract")
    contract.add_argument("path", type=Path)
    args = parser.parse_args()

    try:
        if args.command == "package":
            validate_package(args.root.resolve())
            print("GitHub Delivery Loop package is valid.")
        else:
            validate_contract(args.path.resolve())
            print("Issue contract is valid.")
    except (OSError, ValueError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
