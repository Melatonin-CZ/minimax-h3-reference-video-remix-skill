#!/usr/bin/env python3
"""Validate structured reference-video deconstruction JSON.

Adapted with minimal changes from penposs/remix-reference-video-prompt
(scripts/validate_deconstruction.py), reused here under this skill's
attribution note in SKILL.md. Field names match deconstruction_schema.md
in this skill's references/ folder.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


EVIDENCE_TYPES = {"video", "prompt_only", "transcript_only", "mixed"}
POLICY_VALUES = {"preserve", "adapt", "replace", "omit"}
CONFIDENCE_VALUES = {"high", "medium", "low"}
REQUIRED_SHOT_FIELDS = {
    "shot_id",
    "start_seconds",
    "end_seconds",
    "camera",
    "composition",
    "action",
    "transition_effects",
    "audio",
    "narrative_function",
}


def read_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a structured reference-video deconstruction."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Deconstruction JSON path, or - to read standard input",
    )
    args = parser.parse_args()

    try:
        data = json.loads(read_input(args.input))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: Cannot read valid JSON: {exc}")
        return 1

    errors: list[str] = []
    source = data.get("source")
    evidence = source.get("evidence") if isinstance(source, dict) else None
    if evidence not in EVIDENCE_TYPES:
        errors.append(
            "source.evidence must be one of: " + ", ".join(sorted(EVIDENCE_TYPES))
        )

    shots = data.get("shots")
    if not isinstance(shots, list) or not shots:
        errors.append("shots must be a non-empty array.")
        shots = []

    previous_start = -1.0
    seen_ids: set[str] = set()
    for index, shot in enumerate(shots, start=1):
        label = f"shots[{index - 1}]"
        if not isinstance(shot, dict):
            errors.append(f"{label} must be an object.")
            continue

        missing = sorted(REQUIRED_SHOT_FIELDS - set(shot))
        if missing:
            errors.append(f"{label} missing fields: {', '.join(missing)}")

        shot_id = shot.get("shot_id")
        if not isinstance(shot_id, str) or not shot_id.strip():
            errors.append(f"{label}.shot_id must be a non-empty string.")
        elif shot_id in seen_ids:
            errors.append(f"{label}.shot_id is duplicated: {shot_id}")
        else:
            seen_ids.add(shot_id)

        start = shot.get("start_seconds")
        end = shot.get("end_seconds")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
            errors.append(f"{label} start_seconds and end_seconds must be numbers.")
        else:
            if start < previous_start:
                errors.append(f"{label} is out of chronological order.")
            if end <= start:
                errors.append(f"{label}.end_seconds must be greater than start_seconds.")
            previous_start = float(start)

        confidence = shot.get("confidence")
        if confidence is not None and confidence not in CONFIDENCE_VALUES:
            errors.append(
                f"{label}.confidence must be one of: "
                + ", ".join(sorted(CONFIDENCE_VALUES))
            )

        camera = shot.get("camera")
        if isinstance(camera, dict):
            motion_type = camera.get("motion_type")
            if motion_type is not None and not isinstance(motion_type, str):
                errors.append(f"{label}.camera.motion_type must be a string or null.")

        policy = shot.get("policy", {})
        if not isinstance(policy, dict):
            errors.append(f"{label}.policy must be an object.")
        else:
            for layer, value in policy.items():
                if value not in POLICY_VALUES:
                    errors.append(
                        f"{label}.policy.{layer} must be one of: "
                        + ", ".join(sorted(POLICY_VALUES))
                    )

    duration = data.get("duration_seconds")
    if isinstance(duration, (int, float)) and shots:
        final_end = shots[-1].get("end_seconds")
        if isinstance(final_end, (int, float)) and final_end > duration:
            errors.append(
                f"Last shot ends at {final_end}s, beyond duration_seconds={duration}."
            )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("VIDEO_DECONSTRUCTION_OK " f"shots={len(shots)} evidence={evidence}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
