# Copyright 2026 LevelUpWorldHub
# SPDX-License-Identifier: Apache-2.0

import re
import sys
import unittest
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from render_proposal import WORD_LIMIT, answer_word_count  # noqa: E402


class ProposalTests(unittest.TestCase):
    def test_ten_answers_stay_within_500_words(self):
        text = (ROOT / "ROUND1_PROPOSAL.md").read_text(encoding="utf-8")
        count = answer_word_count(text)
        self.assertLessEqual(count, WORD_LIMIT)
        self.assertGreaterEqual(count, 400)
        submission = (ROOT / "SUBMISSION.md").read_text(encoding="utf-8")
        self.assertIn(str(count), submission)

    def test_pdf_is_a_small_real_pdf(self):
        pdf = ROOT / "ROUND1_PROPOSAL.pdf"
        self.assertTrue(pdf.is_file(), "render ROUND1_PROPOSAL.pdf before packaging")
        data = pdf.read_bytes()
        self.assertTrue(data.startswith(b"%PDF"))
        self.assertLessEqual(len(data), 1024 * 1024)
        streams = []
        for match in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", data, re.S):
            streams.append(zlib.decompress(match.group(1)))
        visible = b" ".join(streams)
        self.assertIn(b"Shelf Check", visible)
        self.assertIn(b"What does your Skill do?", visible)
        self.assertIn(b"Third-party components and licenses", visible)


if __name__ == "__main__":
    unittest.main()
