#!/usr/bin/env python3


from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def read_tokens(file_path: Path) -> Tuple[List[str], List[str]]:
    """Read tokens (words) from a text file, splitting on whitespace."""
    errors: List[str] = []
    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
    except OSError as exc:
        raise OSError(f"Cannot read file: {file_path}") from exc

    tokens: List[str] = []
    for line_no, raw in enumerate(text.splitlines(), start=1):
        raw = raw.strip()
        if not raw:
            continue
        # Split on any whitespace
        parts = raw.split()
        for part in parts:
            if part:
                tokens.append(part)
            else:
                errors.append(f"Line {line_no}: empty token encountered")
    return tokens, errors


def count_frequencies(tokens: List[str]) -> Dict[str, int]:
    """Count occurrences of each token."""
    freq: Dict[str, int] = {}
    for tok in tokens:
        freq[tok] = freq.get(tok, 0) + 1
    return freq


def format_results(freq: Dict[str, int], errors: List[str], elapsed_seconds: float) -> str:
    """Build output string for console and file."""
    lines: List[str] = []
    lines.append("WORD\tCOUNT")

    total = 0
    for word in sorted(freq.keys()):
        count = freq[word]
        total += count
        lines.append(f"{word}\t{count}")

    lines.append("")
    lines.append(f"Grand Total\t{total}")

    if errors:
        lines.append("")
        lines.append("Errors (non-fatal):")
        lines.extend(errors)

    lines.append("")
    lines.append(f"Elapsed time: {elapsed_seconds:.6f} seconds")
    return "\n".join(lines) + "\n"


def build_arg_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser."""
    parser = argparse.ArgumentParser(description="Count distinct words in a file.")
    parser.add_argument("input_file", help="Path to the input .txt file")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Entry point."""
    args = build_arg_parser().parse_args(argv)
    input_path = Path(args.input_file)

    start = time.perf_counter()
    try:
        tokens, errors = read_tokens(input_path)
    except OSError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    freq = count_frequencies(tokens)
    elapsed = time.perf_counter() - start
    output_text = format_results(freq, errors, elapsed)

    print(output_text, end="")

    try:
        with open("ConvertionResults.txt", "a", encoding="utf-8") as f:
            f.write("\n" + "=" * 60 + "\n")
            f.write(f"Input file: {input_path}\n")
            f.write(output_text)
    except OSError as exc:
        print(f"Warning: could not write StatisticsResults.txt: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
