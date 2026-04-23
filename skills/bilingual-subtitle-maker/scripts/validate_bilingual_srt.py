#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


TIME_RE = re.compile(
    r"^(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> "
    r"(\d{2}):(\d{2}):(\d{2}),(\d{3})$"
)
CJK_RE = re.compile(r"[\u3400-\u9fff]")
LATIN_RE = re.compile(r"[A-Za-z]")
ZH_COMFORT_LIMIT = 22
ZH_REVIEW_LIMIT = 28
EN_COMFORT_LIMIT = 50
EN_REVIEW_LIMIT = 50
TERMINAL_PUNCT_RE = re.compile(r"[。．.,，!?？;；:：]$")
FIRST_LATIN_RE = re.compile(r"[A-Za-z]")


@dataclass
class Cue:
    index: int
    start_ms: int
    end_ms: int
    lines: list[str]


def parse_time(match: re.Match[str], offset: int) -> int:
    hours = int(match.group(offset))
    minutes = int(match.group(offset + 1))
    seconds = int(match.group(offset + 2))
    millis = int(match.group(offset + 3))
    return ((hours * 60 + minutes) * 60 + seconds) * 1000 + millis


def split_blocks(text: str) -> list[list[str]]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        return []
    return [block.split("\n") for block in re.split(r"\n{2,}", normalized)]


def parse_srt(path: Path) -> tuple[list[Cue], list[str]]:
    errors: list[str] = []
    cues: list[Cue] = []

    for block_no, block in enumerate(split_blocks(path.read_text(encoding="utf-8-sig")), start=1):
        if len(block) < 3:
            errors.append(f"Block {block_no}: expected index, timecode, and text lines.")
            continue

        try:
            index = int(block[0].strip())
        except ValueError:
            errors.append(f"Block {block_no}: invalid cue index {block[0]!r}.")
            continue

        match = TIME_RE.match(block[1].strip())
        if not match:
            errors.append(f"Cue {index}: invalid timecode {block[1]!r}.")
            continue

        start_ms = parse_time(match, 1)
        end_ms = parse_time(match, 5)
        lines = [line.strip() for line in block[2:] if line.strip()]
        cues.append(Cue(index=index, start_ms=start_ms, end_ms=end_ms, lines=lines))

    return cues, errors


def validate(cues: list[Cue]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    previous_end = -1

    for expected_index, cue in enumerate(cues, start=1):
        if cue.index != expected_index:
            errors.append(f"Cue {cue.index}: expected sequential index {expected_index}.")

        if cue.start_ms >= cue.end_ms:
            errors.append(f"Cue {cue.index}: start time must be before end time.")

        if cue.start_ms < previous_end:
            errors.append(f"Cue {cue.index}: overlaps or goes backward from previous cue.")

        previous_end = cue.end_ms

        if len(cue.lines) != 2:
            errors.append(f"Cue {cue.index}: expected exactly 2 text lines, got {len(cue.lines)}.")
            continue

        zh_line, en_line = cue.lines
        zh_len = len(zh_line)
        en_len = len(en_line)
        if zh_len > ZH_REVIEW_LIMIT:
            warnings.append(
                f"Cue {cue.index}: Chinese line exceeds review limit "
                f"({zh_len}/{ZH_REVIEW_LIMIT} chars)."
            )
        elif zh_len > ZH_COMFORT_LIMIT:
            warnings.append(
                f"Cue {cue.index}: Chinese line exceeds comfort length "
                f"({zh_len}/{ZH_COMFORT_LIMIT} chars)."
            )
        if en_len > EN_REVIEW_LIMIT:
            warnings.append(
                f"Cue {cue.index}: English line exceeds review limit "
                f"({en_len}/{EN_REVIEW_LIMIT} chars)."
            )
        elif en_len > EN_COMFORT_LIMIT:
            warnings.append(
                f"Cue {cue.index}: English line exceeds comfort length "
                f"({en_len}/{EN_COMFORT_LIMIT} chars)."
            )
        if not CJK_RE.search(zh_line):
            warnings.append(f"Cue {cue.index}: first line has no CJK characters.")
        if not LATIN_RE.search(en_line):
            warnings.append(f"Cue {cue.index}: second line has no Latin letters.")
        if TERMINAL_PUNCT_RE.search(zh_line):
            warnings.append(f"Cue {cue.index}: Chinese line ends with punctuation.")
        if TERMINAL_PUNCT_RE.search(en_line):
            warnings.append(f"Cue {cue.index}: English line ends with punctuation.")
        first_latin = FIRST_LATIN_RE.search(en_line)
        if first_latin and first_latin.group(0).islower():
            warnings.append(f"Cue {cue.index}: English line starts with lowercase.")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a bilingual zh/en SRT file.")
    parser.add_argument("srt", type=Path)
    args = parser.parse_args()

    if not args.srt.exists():
        print(f"File not found: {args.srt}", file=sys.stderr)
        return 1

    cues, parse_errors = parse_srt(args.srt)
    errors, warnings = validate(cues)
    errors = parse_errors + errors

    for warning in warnings:
        print(f"warning: {warning}")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"OK: {len(cues)} cues validated, {len(warnings)} warnings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
