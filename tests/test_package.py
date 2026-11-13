# Copyright 2026 LevelUpWorldHub
# SPDX-License-Identifier: Apache-2.0

import json
import os
import subprocess
import sys
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "shelf-check"
ZIP_PATH = ROOT / "skill.zip"


class PackageTests(unittest.TestCase):
    def test_skill_tree_is_markdown_only(self):
        files = [path for path in SKILL.rglob("*") if path.is_file()]
        self.assertTrue(files)
        for path in files:
            relative = path.relative_to(SKILL).as_posix()
            self.assertTrue(relative == "SKILL.md" or relative.startswith("references/"))
            self.assertTrue(relative.endswith(".md"))

    def test_every_reference_is_linked(self):
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for path in (SKILL / "references").glob("*.md"):
            self.assertIn(f"](references/{path.name})", skill)

    def test_zip_matches_the_skill_tree(self):
        subprocess.check_call([sys.executable, str(ROOT / "tools" / "package_skill.py")], cwd=ROOT)
        with zipfile.ZipFile(ZIP_PATH) as archive:
            names = archive.namelist()
        self.assertTrue(all(name.startswith("shelf-check/") for name in names))
        self.assertNotIn("shelf-check/", names)  # no directory-only entries required
        payloads = [name for name in names if not name.endswith("/")]
        self.assertIn("shelf-check/SKILL.md", payloads)
        for name in payloads:
            self.assertTrue(name.endswith(".md"), name)
            info_size = zipfile.ZipFile(ZIP_PATH).getinfo(name).file_size
            self.assertLessEqual(info_size, 1024 * 1024)
        self.assertLessEqual(ZIP_PATH.stat().st_size, 10 * 1024 * 1024)
        self.assertLessEqual(len(payloads), 100)

    def test_official_checker_when_kit_is_present(self):
        kit = Path(os.environ.get("ULIYA_SKILL_KIT", "/tmp/uliya/uliya-skill-kit"))
        script = kit / "scripts" / "check-skill.mjs"
        if not script.is_file():
            self.skipTest("UGOS Skill Creation Tool is not on disk")
        completed = subprocess.run(
            ["node", str(script), str(SKILL)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(report["status"], "static-pass")
        self.assertEqual(report["summary"]["errors"], 0)
        self.assertEqual(report["summary"]["warnings"], 0)


if __name__ == "__main__":
    unittest.main()
