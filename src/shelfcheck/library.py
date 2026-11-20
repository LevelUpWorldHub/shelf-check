# Copyright 2026 LevelUpWorldHub
# SPDX-License-Identifier: Apache-2.0
"""Read a sample NAS tree. Media bytes are hashed. Facts files are fixtures."""

from __future__ import annotations

import hashlib
from pathlib import Path

from shelfcheck.rules import MEDIA_EXTENSIONS, MediaItem, normalize_title


class FactsError(ValueError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_media(root: Path) -> list[MediaItem]:
    video = root / "video"
    if not video.is_dir():
        raise FileNotFoundError(f"missing video directory: {video}")
    items: list[MediaItem] = []
    files = sorted(
        (path for path in video.rglob("*") if path.is_file() and path.suffix.lower() in MEDIA_EXTENSIONS),
        key=lambda path: path.relative_to(root).as_posix(),
    )
    for path in files:
        facts_path = path.with_suffix(".facts.txt")
        duration, subtitles = _read_facts(facts_path)
        relative = path.relative_to(root).as_posix()
        items.append(
            MediaItem(
                relative_path=relative,
                key=normalize_title(path.stem),
                sha256=sha256_file(path),
                duration_min=duration,
                subtitle_languages=subtitles,
            )
        )
    return items


def _read_facts(path: Path) -> tuple[int | None, str | None]:
    if not path.is_file():
        return None, None
    duration: int | None = None
    subtitles: str | None = None
    seen_duration = False
    seen_subtitles = False
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            raise FactsError(f"{path}:{line_number}: expected key: value")
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key == "duration_min":
            if seen_duration:
                raise FactsError(f"{path}:{line_number}: duplicate duration_min")
            seen_duration = True
            if value == "":
                duration = None
            else:
                try:
                    duration = int(value)
                except ValueError as error:
                    raise FactsError(f"{path}:{line_number}: duration_min is not an integer") from error
                if duration < 0:
                    raise FactsError(f"{path}:{line_number}: duration_min is negative")
        elif key == "subtitle_languages":
            if seen_subtitles:
                raise FactsError(f"{path}:{line_number}: duplicate subtitle_languages")
            seen_subtitles = True
            subtitles = None if value == "" else value
        else:
            raise FactsError(f"{path}:{line_number}: unknown fact {key}")
    return duration, subtitles


def load_list(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"missing list: {path}")
    return path.read_text(encoding="utf-8")
