

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import List, Optional, Tuple

HEX_DIGITS = "0123456789ABCDEF"


def parse_integers(file_path: Path) -> Tuple[List[int], List[str]]:
    """Parse integers from a text file; supports one token per line or whitespace."""
    values: List[int] = []
    errors: List[str] = []

    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
    except OSError as exc:
        raise OSError(f"Cannot read file: {file_path}") from exc

    for line_no, raw in enumerate(text.splitlines(), start=1):
        raw = raw.strip()
        if not raw:
            continue
        for token in raw.split():
            try:
                # Only allow base-10 integers as per the assignment.
                values.append(int(token))
            except ValueError:
                errors.append(f"Line {line_no}: invalid integer -> {token!r}")

    return values, errors


def to_binary(n: int) -> str:
    """Convert integer to binary string using repeated division by 2."""
    if n == 0:
        return "0"
    sign = ""
    if n < 0:
        sign = "-"
        n = -n

    bits: List[str] = []
    while n > 0:
        bits.append(str(n % 2))
        n //= 2
    bits.reverse()
    return sign + "".join(bits)


def to_hexadecimal(n: int) -> str:
    """Convert integer to hex string using repeated division by 16."""
    if n == 0:
        return "0"
    sign = ""
    if n < 0:
        sign = "-"
        n = -n

    digits: List[str] = []
    while n > 0:
        digits.append(HEX_DIGITS[n % 16])
        n //= 16
    digits.reverse()
    return sign + "".join(digits)


def format_results(values: List[int], errors: List[str], elapsed_seconds: float) -> str:
    """Build output string for console and file."""
    lines: List[str] = []
    lines.append("ITEM\tDECIMAL\tBINARY\tHEXADECIMAL")

    for idx, val in enumerate(values, start=1):
        lines.append(f"{idx}\t{val}\t{to_binary(val)}\t{to_hexadecimal(val)}")

    if errors:
        lines.append("")
        lines.append("Errors (invalid tokens were ignored):")
        lines.extend(errors)

    lines.append("")
    lines.append(f"Elapsed time: {elapsed_seconds:.6f} seconds")
    return "\n".join(lines) + "\n"


def build_arg_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Convert integers in a file to binary and hexadecimal."
    )
    parser.add_argument("input_file", help="Path to the input .txt file")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Entry point."""
    args = build_arg_parser().parse_args(argv)
    input_path = Path(args.input_file)

    start = time.perf_counter()
    try:
        values, errors = parse_integers(input_path)
    except OSError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    elapsed = time.perf_counter() - start
    output_text = format_results(values, errors, elapsed)

    print(output_text, end="")

    try:
        with open("ConvertNumbersResults.txt", "a", encoding="utf-8") as f:
            f.write("\n" + "=" * 60 + "\n")
            f.write(f"Input file: {input_path}\n")
            f.write(output_text)
    except OSError as exc:
        print(f"Warning: could not write StatisticsResults.txt: {exc}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
