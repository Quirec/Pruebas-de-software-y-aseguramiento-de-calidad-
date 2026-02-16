#!/usr/bin/env python3
"""
computeSales.py

Usage:
    python computeSales.py priceCatalogue.json salesRecord.json

Reads a product price catalogue (JSON) and a sales record (JSON),
computes totals, prints results to console, and writes them to
SalesResults.txt. Skips invalid rows but keeps executing.
"""

from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass, field
from typing import Any


RESULTS_FILENAME = "SalesResults.txt"


@dataclass
class SaleItem:
    """One product line inside a sale."""

    product: str
    quantity: float
    unit_price: float

    @property
    def line_total(self) -> float:
        """Quantity * unit_price (quantity may be negative)."""
        return self.quantity * self.unit_price


@dataclass
class SaleGroup:
    """Group items by SALE_ID."""

    sale_id: str
    sale_date: str = ""
    items: list[SaleItem] = field(default_factory=list)

    @property
    def subtotal(self) -> float:
        """Sum of all line totals for this sale."""
        return sum(item.line_total for item in self.items)


def eprint(message: str) -> None:
    """Print errors to stderr without stopping the program."""
    print(f"[ERROR] {message}", file=sys.stderr)


def load_json_file(path: str) -> Any:
    """Load JSON from disk with error handling."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        eprint(f"File not found: {path}")
    except json.JSONDecodeError as exc:
        eprint(f"Invalid JSON format in {path}: {exc}")
    except OSError as exc:
        eprint(f"Could not read {path}: {exc}")
    return None


def build_price_catalog(catalog_data: Any) -> dict[str, float]:
    """
    Convert catalogue list into dict: {title: price}.
    Skips invalid product entries but continues.
    """
    prices: dict[str, float] = {}

    if not isinstance(catalog_data, list):
        eprint("Price catalogue JSON must be a list of products.")
        return prices

    for idx, product in enumerate(catalog_data):
        if not isinstance(product, dict):
            eprint(f"Catalogue item #{idx} is not an object; skipped.")
            continue

        product_title = product.get("title")
        product_price = product.get("price")

        if not isinstance(product_title, str) or not product_title.strip():
            eprint(f"Catalogue item #{idx} has invalid 'title'; skipped.")
            continue

        try:
            price_num = float(product_price)
        except (TypeError, ValueError):
            eprint(
                f"Catalogue item #{idx} ('{product_title}') "
                "has invalid 'price'; skipped."
            )
            continue

        prices[product_title] = price_num

    return prices


def parse_sales(
    sales_data: Any,
    prices: dict[str, float],
) -> tuple[dict[str, SaleGroup], float, int]:
    """
    Parse sales records, compute totals, and count skipped rows.
    Returns: grouped_sales, grand_total, error_count
    """
    grouped: dict[str, SaleGroup] = {}
    grand_total = 0.0
    error_count = 0

    if not isinstance(sales_data, list):
        eprint("Sales record JSON must be a list of sales rows.")
        return grouped, grand_total, 1

    for idx, row in enumerate(sales_data):
        if not isinstance(row, dict):
            eprint(f"Sales row #{idx} is not an object; skipped.")
            error_count += 1
            continue

        sale_id = row.get("SALE_ID")
        sale_date = row.get("SALE_Date", "")
        product = row.get("Product")
        quantity = row.get("Quantity")

        if sale_id is None:
            eprint(f"Sales row #{idx} missing SALE_ID; skipped.")
            error_count += 1
            continue

        if not isinstance(product, str) or not product.strip():
            eprint(f"Sales row #{idx} has invalid Product; skipped.")
            error_count += 1
            continue

        if product not in prices:
            eprint(
                f"Sales row #{idx}: Product '{product}' "
                "not found in catalogue; skipped."
            )
            error_count += 1
            continue

        try:
            qty_num = float(quantity)
        except (TypeError, ValueError):
            eprint(
                f"Sales row #{idx}: invalid Quantity '{quantity}' "
                f"for '{product}'; skipped."
            )
            error_count += 1
            continue

        unit_price = prices[product]
        item = SaleItem(product=product, quantity=qty_num, unit_price=unit_price)

        sale_id_key = str(sale_id)
        if sale_id_key not in grouped:
            grouped[sale_id_key] = SaleGroup(
                sale_id=sale_id_key,
                sale_date=str(sale_date),
            )

        if not grouped[sale_id_key].sale_date and sale_date:
            grouped[sale_id_key].sale_date = str(sale_date)

        grouped[sale_id_key].items.append(item)
        grand_total += item.line_total

    return grouped, grand_total, error_count


def sale_sort_key(sale_id: str) -> tuple[int, str]:
    """Sort SALE_ID as numeric when possible, else as text."""
    try:
        return 0, f"{int(sale_id):012d}"
    except ValueError:
        return 1, sale_id


def format_report(
    grouped: dict[str, SaleGroup],
    grand_total: float,
    error_count: int,
    elapsed_seconds: float,
) -> str:
    """Create the report string for console and file."""
    lines: list[str] = []
    lines.append("SALES RESULTS")
    lines.append("=" * 60)
    lines.append(f"Sales (unique SALE_ID): {len(grouped)}")
    lines.append(f"Errors (skipped rows): {error_count}")
    lines.append("")

    for sale_id in sorted(grouped.keys(), key=sale_sort_key):
        sale = grouped[sale_id]
        lines.append(f"SALE_ID: {sale.sale_id}    DATE: {sale.sale_date}")
        lines.append("-" * 60)
        lines.append(
            f"{'Product':35} {'Qty':>8} {'Price':>10} {'Total':>12}"
        )

        for item in sale.items:
            product_short = item.product[:35]
            lines.append(
                f"{product_short:35} "
                f"{item.quantity:8.2f} "
                f"{item.unit_price:10.2f} "
                f"{item.line_total:12.2f}"
            )

        lines.append("-" * 60)
        lines.append(f"{'SUBTOTAL':>55} {sale.subtotal:12.2f}")
        lines.append("")

    lines.append("=" * 60)
    lines.append(f"{'GRAND TOTAL':>55} {grand_total:12.2f}")
    lines.append(f"Elapsed time (s): {elapsed_seconds:.6f}")
    lines.append("=" * 60)

    return "\n".join(lines) + "\n"


def main() -> int:
    """Program entrypoint."""
    start = time.perf_counter()

    if len(sys.argv) != 3:
        eprint("Usage: python computeSales.py priceCatalogue.json salesRecord.json")
        return 2

    catalog_path = sys.argv[1]
    sales_path = sys.argv[2]

    catalog_data = load_json_file(catalog_path)
    sales_data = load_json_file(sales_path)

    if catalog_data is None:
        catalog_data = []
    if sales_data is None:
        sales_data = []

    prices = build_price_catalog(catalog_data)
    grouped, grand_total, error_count = parse_sales(sales_data, prices)

    elapsed = time.perf_counter() - start
    report = format_report(grouped, grand_total, error_count, elapsed)

    print(report, end="")

    try:
        with open(RESULTS_FILENAME, "a", encoding="utf-8") as file:
            file.write(report)
    except OSError as exc:
        eprint(f"Could not write results file '{RESULTS_FILENAME}': {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
