# Copyright 2026 LevelUpWorldHub
# SPDX-License-Identifier: Apache-2.0
"""Build skill.zip with the shelf-check directory at the archive root."""

from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "shelf-check"
OUTPUT = ROOT / "skill.zip"


def main() -> None:
    files = [path for path in SKILL.rglob("*") if path.is_file()]
    if not files:
        raise SystemExit("skill directory is empty")
    for path in files:
        relative = path.relative_to(SKILL).as_posix()
        if relative != "SKILL.md" and not relative.startswith("references/"):
            raise SystemExit(f"refusing to pack {relative}")
        if path.suffix != ".md":
            raise SystemExit(f"refusing to pack non-markdown {relative}")
        if path.stat().st_size > 1024 * 1024:
            raise SystemExit(f"{relative} exceeds 1 MB")
    if OUTPUT.exists():
        OUTPUT.unlink()
    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files):
            relative = path.relative_to(SKILL).as_posix()
            archive.write(path, f"shelf-check/{relative}")
    if OUTPUT.stat().st_size > 10 * 1024 * 1024:
        raise SystemExit("zip exceeds 10 MB")
    print(f"wrote {OUTPUT} ({OUTPUT.stat().st_size} bytes, {len(files)} files)")


if __name__ == "__main__":
    main()
