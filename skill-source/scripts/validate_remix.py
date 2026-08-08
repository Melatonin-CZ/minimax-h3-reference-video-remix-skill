#!/usr/bin/env python3
"""Validate a finished remix prompt against its remix-contract.json.

Adapted from penposs/remix-reference-video-prompt (scripts/validate_remix.py);
see this skill's SKILL.md for attribution. Two changes from the source
version, both needed because this skill's output is MiniMax H3 English-
syntax prompts rather than free-text Chinese prompts:

1. Timeline extraction looks for this system's own shot-timestamp marker
   ("[Shot N] At MM:SS.mmm") from VIDEO_PROMPT_WRITING_GUIDE_ref_en.md,
   instead of a "X-Y秒" range pattern.
2. META_PATTERNS matches English process-narration phrasing (the kind of
   language Stage 5 of certification_checklist.md bans), instead of the
   original Chinese phrase list.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SHOT_TIME_RE = re.compile(r"\[Shot\s+\d+\]\s+At\s+(\d{2}):(\d{2})\.(\d{3})")

# Process/meta-commentary phrasing that should never appear in a finished
# generation prompt (Stage 5 of certification_checklist.md). These describe
# the *remix operation itself* rather than final renderable content.
META_PATTERNS = [
    r"\breplac(?:e|ed|ing)\s+the\s+(?:original|source)\b",
    r"\boriginal(?:ly)?\s+(?:subject|character|person|costume|wardrobe|scene|setting|prop|background)s?\s+(?:is|are|was|were)?\s*(?:replaced|changed|swapped)",
    r"\bif\s+(?:this|it)\s+conflicts?\s+with\s+the\s+reference\s+video\b",
    r"\bchanged\s+from\s+the\s+original\b",
    r"\binstead\s+of\s+the\s+original\b",
    r"\bonly\s+(?:allowed|permitted)\s+to\s+replace\b",
    r"\bbased\s+on\s+the\s+reference\s+video\b",
    r"\bthe\s+deconstruction\s+(?:shows|found|identified)\b",
    r"\bper\s+the\s+layer\s+contract\b",
]


def read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def extract_shot_times(text: str) -> list[float]:
    times = []
    for match in SHOT_TIME_RE.finditer(text):
        minutes, seconds, millis = match.groups()
        total = int(minutes) * 60 + int(seconds) + int(millis) / 1000
        times.append(round(total, 3))
    return times


def check_timeline(prompt_text: str, locked: dict, errors: list[str]) -> None:
    expected = locked.get("timeline")
    if not expected:
        return
    found = extract_shot_times(prompt_text)
    if len(found) < len(expected) - 1:
        # timeline entries describe shot spans; cut markers = spans - 1
        errors.append(
            f"Expected at least {len(expected) - 1} shot-cut timestamp(s) "
            f"('[Shot N] At MM:SS.mmm'), found {len(found)}."
        )


def check_required_phrases(prompt_text: str, locked: dict, errors: list[str]) -> None:
    lowered = prompt_text.lower()
    for phrase in locked.get("required_phrases", []):
        if phrase.lower() not in lowered:
            errors.append(f"Required phrase missing from prompt: {phrase!r}")


def check_meta_patterns(prompt_text: str, errors: list[str]) -> None:
    lowered = prompt_text.lower()
    for pattern in META_PATTERNS:
        if re.search(pattern, lowered):
            errors.append(f"Prompt contains process/meta-commentary matching: {pattern!r}")


def check_char_limit(prompt_text: str, limits: dict, errors: list[str]) -> None:
    max_chars = limits.get("max_chars")
    if max_chars and len(prompt_text) > max_chars:
        errors.append(f"Prompt is {len(prompt_text)} chars, exceeds max_chars={max_chars}.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a finished remix prompt against its remix-contract.json."
    )
    parser.add_argument("--contract", required=True, help="Path to remix-contract.json")
    parser.add_argument(
        "--prompt", required=True, help="Path to the finished prompt text, or - for stdin"
    )
    args = parser.parse_args()

    try:
        contract = json.loads(Path(args.contract).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: Cannot read valid contract JSON: {exc}")
        return 1

    try:
        prompt_text = read_text(args.prompt)
    except OSError as exc:
        print(f"ERROR: Cannot read prompt: {exc}")
        return 1

    errors: list[str] = []
    locked = contract.get("locked", {})
    validation = contract.get("validation", {})
    limits = contract.get("limits", {})

    if validation.get("preserve_timeline"):
        check_timeline(prompt_text, locked, errors)

    check_required_phrases(prompt_text, locked, errors)
    check_meta_patterns(prompt_text, errors)
    check_char_limit(prompt_text, limits, errors)

    if validation.get("direct_result_only") and re.search(
        r"\b(?:deconstruction|remix[- ]contract|layer\s+policy)\b", prompt_text.lower()
    ):
        errors.append(
            "Prompt references internal working artifacts (deconstruction/contract/"
            "layer policy) instead of describing final renderable content only."
        )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"REMIX_PROMPT_OK chars={len(prompt_text)} shots={len(extract_shot_times(prompt_text)) + 1}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
