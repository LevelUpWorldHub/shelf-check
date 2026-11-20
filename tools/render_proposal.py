# Copyright 2026 LevelUpWorldHub
# SPDX-License-Identifier: Apache-2.0
"""Render ROUND1_PROPOSAL.md to a PDF with fpdf2. Refuses a 500-word overrun."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ROUND1_PROPOSAL.md"
OUTPUT = ROOT / "ROUND1_PROPOSAL.pdf"
WORD_LIMIT = 500


def answer_word_count(markdown: str) -> int:
    start = markdown.index("## 1.")
    end = markdown.index("## Third-party")
    body = markdown[start:end]
    total = 0
    for block in re.split(r"\n(?=## \d+\. )", body.strip()):
        lines = block.splitlines()
        total += len("\n".join(lines[1:]).split())
    return total


def main() -> None:
    markdown = SOURCE.read_text(encoding="utf-8")
    count = answer_word_count(markdown)
    if count > WORD_LIMIT:
        raise SystemExit(f"{count} answer words exceeds {WORD_LIMIT}")
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(18, 18, 18)
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    for raw in markdown.splitlines():
        line = raw.replace("`", "").rstrip()
        if not line:
            pdf.ln(3)
            continue
        if line.startswith("# "):
            pdf.set_font("Helvetica", "B", 16)
            pdf.multi_cell(0, 8, line[2:])
            pdf.ln(2)
            pdf.set_font("Helvetica", size=11)
            continue
        if line.startswith("## "):
            pdf.ln(1)
            pdf.set_font("Helvetica", "B", 12)
            pdf.multi_cell(0, 7, line[3:])
            pdf.set_font("Helvetica", size=11)
            continue
        pdf.multi_cell(0, 6, line)
    pdf.output(OUTPUT)
    size = OUTPUT.stat().st_size
    if size > 1024 * 1024:
        raise SystemExit(f"PDF is {size} bytes")
    print(f"wrote {OUTPUT} ({size} bytes, {count} answer words)")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"error: {error}", file=sys.stderr)
        raise
