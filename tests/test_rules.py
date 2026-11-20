# Copyright 2026 LevelUpWorldHub
# SPDX-License-Identifier: Apache-2.0

import hashlib
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from shelfcheck.library import load_list, load_media
from shelfcheck.rules import (
    SHORTLIST_LIMIT,
    MediaItem,
    build_card,
    parse_clock,
    parse_list,
    render_card,
)


def _item(name: str, payload: bytes, duration: int | None, subtitles: str | None) -> MediaItem:
    return MediaItem(
        relative_path=f"video/{name}.mkv",
        key=name.lower(),
        sha256=hashlib.sha256(payload).hexdigest(),
        duration_min=duration,
        subtitle_languages=subtitles,
    )


class ParseTests(unittest.TestCase):
    def test_unreadable_lines_are_not_titles(self):
        lines = parse_list("Forest Journey\n\n[unreadable]\n???\nUNREADABLE: smudge\n")
        self.assertEqual([line.text for line in lines if line.readable], ["Forest Journey"])
        self.assertEqual(len([line for line in lines if not line.readable]), 3)

    def test_clock_rejects_overnight_guess(self):
        with self.assertRaises(ValueError):
            parse_clock("25:00")


class CardTests(unittest.TestCase):
    def test_friday_sample_names_one_title_and_hides_the_extra_film(self):
        root = ROOT / "samples" / "friday-night"
        lines = parse_list(load_list(root / "list.txt"))
        media = load_media(root)
        card = build_card(lines, media, parse_clock("19:00"), parse_clock("21:00"))
        text = render_card(card, list_label="list.txt", start="19:00", finish="21:00")
        self.assertEqual(card.verdict, "one-title")
        self.assertEqual(card.verdict_title, "Forest Journey")
        self.assertIn("2 copies, same bytes", text)
        self.assertIn("fit: yes", text)
        self.assertIn("fit: no", text)
        self.assertIn("Missing Moon", text)
        self.assertIn("on shelf: no", text)
        self.assertIn("not matched to any file", text)
        self.assertIn("Playback: not started", text)
        self.assertNotIn("Night Market", text)
        self.assertIn("not a NAS run", text)
        self.assertIn("1 file(s) on disk were not on the readable list", text)

    def test_identical_bytes_in_the_sample(self):
        root = ROOT / "samples" / "friday-night" / "video"
        original = (root / "Forest Journey.mkv").read_bytes()
        copy = (root / "Forest Journey (copy).mkv").read_bytes()
        self.assertEqual(original, copy)

    def test_empty_shelf_reports_no_results_and_does_not_invent(self):
        root = ROOT / "samples" / "empty-shelf"
        lines = parse_list(load_list(root / "list.txt"))
        media = load_media(root)
        card = build_card(lines, media, None, None)
        text = render_card(card, list_label="list.txt")
        self.assertEqual(card.verdict, "blocked")
        self.assertEqual(card.library_hits, 0)
        self.assertIn("no results", text)
        self.assertNotIn("Named title:", text)

    def test_unreadable_line_does_not_match_a_similar_file(self):
        lines = parse_list("Forest Journey\n[unreadable]\n")
        media = [
            _item("Forest Journey", b"a", 90, "en"),
            _item("Night Market", b"b", 90, "en"),
        ]
        # keys are the name lowercased by the helper; Night Market key is "night market"
        media[1] = MediaItem(
            relative_path=media[1].relative_path,
            key="night market",
            sha256=media[1].sha256,
            duration_min=90,
            subtitle_languages="en",
        )
        card = build_card(lines, media, parse_clock("19:00"), parse_clock("21:00"))
        text = render_card(card, list_label="list.txt", start="19:00", finish="21:00")
        self.assertEqual(card.verdict_title, "Forest Journey")
        self.assertNotIn("Night Market", text)

    def test_split_hashes_are_not_a_start(self):
        lines = parse_list("Forest Journey\n")
        media = [
            _item("Forest Journey", b"cut-a", 90, "en"),
            MediaItem(
                relative_path="video/Forest Journey (copy).mkv",
                key="forest journey",
                sha256=hashlib.sha256(b"cut-b").hexdigest(),
                duration_min=90,
                subtitle_languages="en",
            ),
        ]
        card = build_card(lines, media, parse_clock("19:00"), parse_clock("21:00"))
        self.assertTrue(card.rows[0].split)
        self.assertEqual(card.verdict, "blocked")
        self.assertIsNone(card.verdict_title)

    def test_conflicting_durations_on_matching_bytes_do_not_fit(self):
        lines = parse_list("Forest Journey\n")
        digest = hashlib.sha256(b"same-bytes").hexdigest()
        media = [
            MediaItem("video/a.mkv", "forest journey", digest, 90, "en"),
            MediaItem("video/b.mkv", "forest journey", digest, 100, "en"),
        ]
        card = build_card(lines, media, parse_clock("19:00"), parse_clock("21:00"))
        self.assertFalse(card.rows[0].split)
        self.assertIsNone(card.rows[0].duration_min())
        self.assertEqual(card.verdict, "blocked")
        text = render_card(card, list_label="list.txt", start="19:00", finish="21:00")
        self.assertIn("duration_min: unknown", text)
        self.assertNotIn("Named title:", text)

    def test_unknown_duration_cannot_fit_a_deadline(self):
        lines = parse_list("Forest Journey\n")
        media = [_item("Forest Journey", b"a", None, None)]
        card = build_card(lines, media, parse_clock("19:00"), parse_clock("21:00"))
        self.assertEqual(card.verdict, "blocked")
        text = render_card(card, list_label="list.txt", start="19:00", finish="21:00")
        self.assertIn("duration_min: unknown", text)
        self.assertIn("subtitles: unknown", text)

    def test_without_a_deadline_two_hits_ask_for_a_choice(self):
        lines = parse_list("Forest Journey\nLong Winter\n")
        media = [
            _item("Forest Journey", b"a", 118, "en"),
            _item("Long Winter", b"b", 150, None),
        ]
        card = build_card(lines, media, None, None)
        self.assertEqual(card.verdict, "choose")
        self.assertIsNone(card.verdict_title)

    def test_more_than_twelve_titles_are_not_partially_checked(self):
        titles = "\n".join(f"Title {index}" for index in range(1, SHORTLIST_LIMIT + 2))
        lines = parse_list(titles)
        media = [_item("Title 1", b"a", 10, None)]
        card = build_card(lines, media, None, None)
        self.assertEqual(card.verdict, "not-checked")
        self.assertEqual(card.rows, [])
        self.assertEqual(len(card.overflow), SHORTLIST_LIMIT + 1)
        text = render_card(card, list_label="list.txt")
        self.assertIn("Lookup: not run", text)
        self.assertNotIn("Title 1", text.split("Titles, in list order:")[1])

    def test_boundary_duration_fits_at_the_exact_finish(self):
        lines = parse_list("Forest Journey\n")
        media = [_item("Forest Journey", b"a", 120, "none")]
        card = build_card(lines, media, parse_clock("19:00"), parse_clock("21:00"))
        self.assertEqual(card.verdict, "one-title")
        text = render_card(card, list_label="list.txt", start="19:00", finish="21:00")
        self.assertIn("fit: yes", text)
        self.assertIn("subtitles: none", text)

    def test_demo_command_exits_zero(self):
        completed = subprocess.run(
            [sys.executable, "-m", "shelfcheck", "demo"],
            cwd=ROOT,
            env={**dict(**{k: v for k, v in __import__("os").environ.items()}), "PYTHONPATH": str(ROOT / "src")},
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Named title: Forest Journey", completed.stdout)
        self.assertNotIn("Night Market", completed.stdout)


if __name__ == "__main__":
    unittest.main()
