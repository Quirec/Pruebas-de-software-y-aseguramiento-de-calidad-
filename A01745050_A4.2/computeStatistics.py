
from __future__ import annotations

import argparse
import math
import sys
import time
from pathlib import Path
from typing import List, Optional, Tuple


def parse_numbers(file_path: Path) -> Tuple[List[float], List[str]]:
    """Parse numbers from a text file, one token per line (also supports whitespace)."""
    numbers: List[float] = []
    errors: List[str] = []

    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
    except OSError as exc:
        raise OSError(f"Cannot read file: {file_path}") from exc

    for line_no, raw in enumerate(text.splitlines(), start=1):
        raw = raw.strip()
        if not raw:
            continue
        # Allow whitespace-separated tokens on a single line as well.
        for token in raw.split():
            try:
                numbers.append(float(token))
            except ValueError:
                errors.append(f"Line {line_no}: invalid number -> {token!r}")

    return numbers, errors


def mean(values: List[float]) -> float:
    """Compute arithmetic mean."""
    total = 0.0
    for v in values:
        total += v
    return total / len(values)


def median(sorted_values: List[float]) -> float:
    """Compute median from a sorted list."""
    n = len(sorted_values)
    mid = n // 2
    if n % 2 == 1:
        return sorted_values[mid]
    return (sorted_values[mid - 1] + sorted_values[mid]) / 2.0


def mode(values: List[float]) -> Optional[float]:
    """
    Compute mode.

    If all values occur only once, returns None.
    If there are multiple modes, returns the smallest one (deterministic).
    """
    freq = {}
    for v in values:
        freq[v] = freq.get(v, 0) + 1

    max_count = 0
    modes: List[float] = []
    for val, count in freq.items():
        if count > max_count:
            max_count = count
            modes = [val]
        elif count == max_count:
            modes.append(val)

    if max_count <= 1:
        return None
    return min(modes)


def population_variance(values: List[float], avg: float) -> float:
    """Compute population variance (divide by N)."""
    total = 0.0
    for v in values:
        diff = v - avg
        total += diff * diff
    return total / len(values)


def population_std(values: List[float], avg: float) -> float:
    """Compute population standard deviation."""
    return math.sqrt(population_variance(values, avg))


def format_results(
    values: List[float],
    errors: List[str],
    elapsed_seconds: float,
) -> str:
    """Build output string for console and file."""
    if not values:
        header = "No valid numeric data found.\n"
        err_block = ""
        if errors:
            err_block = "Errors:\n" + "\n".join(errors) + "\n"
        footer = f"\nElapsed time: {elapsed_seconds:.6f} seconds\n"
        return header + err_block + footer

    sorted_values = sorted(values)
    avg = mean(values)
    med = median(sorted_values)
    mod = mode(values)
    var = population_variance(values, avg)
    std = math.sqrt(var)

    lines: List[str] = []
    lines.append("Descriptive Statistics")
    lines.append("-" * 24)
    lines.append(f"Count: {len(values)}")
    lines.append(f"Mean: {avg}")
    lines.append(f"Median: {med}")
    lines.append(f"Mode: {mod if mod is not None else 'N/A'}")
    lines.append(f"Population Std Dev: {std}")
    lines.append(f"Population Variance: {var}")

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
        description="Compute statistics from a text file of numeric values."
    )
    parser.add_argument("input_file", help="Path to the input .txt file")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Entry point."""
    args = build_arg_parser().parse_args(argv)
    input_path = Path(args.input_file)

    start = time.perf_counter()
    try:
        values, errors = parse_numbers(input_path)
    except OSError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    elapsed = time.perf_counter() - start
    output_text = format_results(values, errors, elapsed)

    print(output_text, end="")
    try:
        with open("StatisticsResults.txt", "a", encoding="utf-8") as f:
            f.write("\n" + "=" * 60 + "\n")
            f.write(f"Input file: {input_path}\n")
            f.write(output_text)
    except OSError as exc:
        print(f"Warning: could not write StatisticsResults.txt: {exc}", file=sys.stderr)


    return 0


if __name__ == "__main__":
    raise SystemExit(main())
