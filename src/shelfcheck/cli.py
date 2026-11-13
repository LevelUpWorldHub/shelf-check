# Copyright 2026 LevelUpWorldHub
# SPDX-License-Identifier: Apache-2.0
"""Run the Shelf Check rehearsal against a sample tree."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from shelfcheck.library import FactsError, load_list, load_media
from shelfcheck.rules import build_card, parse_clock, parse_list, render_card

ROOT = Path(__file__).resolve().parents[2]
DEMO_ROOT = ROOT / "samples" / "friday-night"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="shelf-check")
    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser("demo", help="run the Friday-night sample")
    demo.add_argument("--start", default="19:00")
    demo.add_argument("--before", default="21:00")

    check = sub.add_parser("check", help="check one sample tree")
    check.add_argument("--root", type=Path, required=True)
    check.add_argument("--list", dest="list_path", type=Path, required=True)
    check.add_argument("--start", default=None)
    check.add_argument("--before", default=None)

    args = parser.parse_args(argv)
    try:
        if args.command == "demo":
            return _run(DEMO_ROOT, DEMO_ROOT / "list.txt", args.start, args.before)
        return _run(args.root, args.list_path, args.start, args.before)
    except (ValueError, FactsError, FileNotFoundError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


def _run(root: Path, list_path: Path, start: str | None, finish: str | None) -> int:
    if not root.is_dir():
        print(f"error: missing sample root: {root}", file=sys.stderr)
        return 1
    text = load_list(list_path)
    lines = parse_list(text)
    start_min = parse_clock(start) if start else None
    finish_min = parse_clock(finish) if finish else None
    media = load_media(root)
    card = build_card(lines, media, start_min, finish_min)
    try:
        label = str(list_path.relative_to(root))
    except ValueError:
        label = str(list_path)
    sys.stdout.write(
        render_card(card, list_label=label, start=start, finish=finish, rehearsal=True)
    )
    if card.readable_count == 0 or card.overflow:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
