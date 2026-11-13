# Copyright 2026 LevelUpWorldHub
# SPDX-License-Identifier: Apache-2.0
"""Decision rules for a household watch-list shelf card.

The rules mirror skill/shelf-check/references/decision-rules.md.
Duration and subtitle values are inputs. This module never invents them.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

SHORTLIST_LIMIT = 12
MEDIA_EXTENSIONS = {".mkv", ".mp4", ".mov", ".avi", ".m4v"}

_COPY_SUFFIX = re.compile(r"(?:\s*\(copy\)|\s+copy)$", re.IGNORECASE)
_PUNCT = re.compile(r"[^a-z0-9\s]+")
_SPACE = re.compile(r"\s+")
_QUESTIONS = re.compile(r"^[\s?]+$")
_TIME = re.compile(r"^(\d{2}):(\d{2})$")


@dataclass(frozen=True)
class ListLine:
    number: int
    text: str
    readable: bool

    @property
    def key(self) -> str:
        return normalize_title(self.text) if self.readable else ""


@dataclass(frozen=True)
class MediaItem:
    relative_path: str
    key: str
    sha256: str
    duration_min: int | None
    subtitle_languages: str | None
    """None means unknown. 'none' means an explicit no-candidate fact."""


@dataclass
class TitleRow:
    title: str
    copies: list[MediaItem] = field(default_factory=list)

    @property
    def hashes(self) -> set[str]:
        return {item.sha256 for item in self.copies}

    @property
    def split(self) -> bool:
        return len(self.hashes) > 1

    @property
    def same_bytes(self) -> bool:
        return len(self.copies) > 1 and not self.split

    def duration_min(self) -> int | None:
        durations = {item.duration_min for item in self.copies}
        durations.discard(None)
        if len(durations) == 1:
            return next(iter(durations))
        return None

    def subtitles(self) -> str | None:
        values = {item.subtitle_languages for item in self.copies}
        if values == {None}:
            return None
        known = {value for value in values if value is not None}
        if len(known) == 1 and None not in values:
            return next(iter(known))
        if len(known) == 1 and None in values:
            return None
        return None


@dataclass
class Card:
    readable_count: int
    unreadable: list[ListLine]
    rows: list[TitleRow]
    verdict: str
    verdict_title: str | None
    blocked_reasons: list[str]
    overflow: list[str]
    library_hits: int
    notes: list[str]

    @property
    def stopped_without_lookup(self) -> bool:
        return bool(self.overflow) or self.readable_count == 0


def normalize_title(value: str) -> str:
    text = value.strip()
    text = _COPY_SUFFIX.sub("", text)
    text = text.lower()
    text = _PUNCT.sub(" ", text)
    text = _SPACE.sub(" ", text).strip()
    return text


def parse_clock(value: str) -> int:
    match = _TIME.match(value.strip())
    if not match:
        raise ValueError(f"time must be HH:MM, got {value!r}")
    hour = int(match.group(1))
    minute = int(match.group(2))
    if hour > 23 or minute > 59:
        raise ValueError(f"time must be HH:MM, got {value!r}")
    return hour * 60 + minute


def parse_list(text: str) -> list[ListLine]:
    lines: list[ListLine] = []
    for index, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if not stripped:
            continue
        readable = _is_readable(stripped)
        lines.append(ListLine(number=index, text=stripped, readable=readable))
    return lines


def _is_readable(stripped: str) -> bool:
    if stripped.lower() == "[unreadable]":
        return False
    if stripped.lower().startswith("unreadable:"):
        return False
    if _QUESTIONS.match(stripped):
        return False
    return True


def fit_label(
    duration_min: int | None,
    start: int | None,
    finish: int | None,
) -> str:
    if start is None and finish is None:
        return "not-applicable"
    if start is None or finish is None:
        raise ValueError("start and finish must be given together")
    if finish <= start:
        raise ValueError("finish time must be later on the same day")
    if duration_min is None:
        return "unknown"
    end = start + duration_min
    if end > 24 * 60:
        return "no"
    return "yes" if end <= finish else "no"


def build_card(
    lines: list[ListLine],
    media: list[MediaItem],
    start: int | None = None,
    finish: int | None = None,
) -> Card:
    unreadable = [line for line in lines if not line.readable]
    readable = [line for line in lines if line.readable]
    notes: list[str] = []
    if (start is None) ^ (finish is None):
        raise ValueError("start and finish must be given together")

    if len(readable) > SHORTLIST_LIMIT:
        return Card(
            readable_count=len(readable),
            unreadable=unreadable,
            rows=[],
            verdict="not-checked",
            verdict_title=None,
            blocked_reasons=[
                f"{len(readable)} readable titles exceed the {SHORTLIST_LIMIT}-title shortlist limit"
            ],
            overflow=[line.text for line in readable],
            library_hits=0,
            notes=["No titles were looked up."],
        )

    rows: list[TitleRow] = []
    used: set[str] = set()
    for line in readable:
        copies = [item for item in media if item.key == line.key and item.key]
        for item in copies:
            used.add(item.relative_path)
        rows.append(TitleRow(title=line.text, copies=copies))

    ignored = [item.relative_path for item in media if item.relative_path not in used]
    if ignored:
        notes.append(
            f"{len(ignored)} file(s) on disk were not on the readable list and are not named."
        )

    deadline = start is not None and finish is not None
    eligible: list[TitleRow] = []
    reasons: list[str] = []
    for row in rows:
        if not row.copies:
            reasons.append(f"{row.title}: not on the shelf")
            continue
        if row.split:
            reasons.append(f"{row.title}: copies differ")
            continue
        label = fit_label(row.duration_min(), start, finish)
        if deadline and label == "unknown":
            reasons.append(f"{row.title}: duration unknown, so it cannot beat the clock")
            continue
        if label == "no":
            reasons.append(f"{row.title}: runs past the finish time")
            continue
        eligible.append(row)

    hits = sum(1 for row in rows if row.copies)
    if not readable:
        verdict = "no-results"
        verdict_title = None
        reasons = ["no readable titles"]
    elif hits == 0:
        verdict = "blocked"
        verdict_title = None
    elif len(eligible) == 1:
        verdict = "one-title"
        verdict_title = eligible[0].title
    elif len(eligible) > 1:
        verdict = "choose"
        verdict_title = None
    else:
        verdict = "blocked"
        verdict_title = None

    return Card(
        readable_count=len(readable),
        unreadable=unreadable,
        rows=rows,
        verdict=verdict,
        verdict_title=verdict_title,
        blocked_reasons=reasons,
        overflow=[],
        library_hits=hits,
        notes=notes,
    )


def render_card(
    card: Card,
    *,
    list_label: str,
    start: str | None = None,
    finish: str | None = None,
    rehearsal: bool = True,
) -> str:
    lines: list[str] = []
    if rehearsal:
        lines.append("Shelf Check (local rehearsal, not a NAS run)")
        lines.append(
            "Duration and subtitle lines are fixture facts, not NAS subtitle-search results."
        )
    else:
        lines.append("Shelf Check")
    lines.append(f"List: {list_label}")
    if start and finish:
        lines.append(f"Clock: {start} to {finish}")
    lines.append(f"Readable titles: {card.readable_count}")
    lines.append(f"Unreadable lines: {len(card.unreadable)}")
    lines.append(f"Library hits: {card.library_hits}")
    lines.append(f"Verdict: {card.verdict}")
    if card.verdict_title:
        row = next(item for item in card.rows if item.title == card.verdict_title)
        if row.same_bytes:
            lines.append(
                f"Named title: {card.verdict_title} (pick either path; the bytes match)"
            )
        else:
            lines.append(
                f"Named title: {card.verdict_title} (confirm before any playback)"
            )
    lines.append("Playback: not started")
    if card.overflow:
        lines.append("Lookup: not run")
        lines.append("Titles waiting for a shorter list:")
        for title in card.overflow:
            lines.append(f"  - {title}")
    lookup_empty = card.readable_count == 0 or (
        not card.overflow and card.rows and card.library_hits == 0
    )
    if lookup_empty:
        lines.append("no results")
    lines.append("")
    lines.append("Titles, in list order:")
    if not card.rows:
        lines.append("  (none looked up)")
    for row in card.rows:
        lines.extend(_render_row(row, start, finish))
    if card.unreadable:
        lines.append("")
        lines.append("Unreadable:")
        for line in card.unreadable:
            lines.append(f"  line {line.number}: {line.text}")
            lines.append("  not matched to any file")
    if card.blocked_reasons and card.verdict != "one-title":
        lines.append("")
        lines.append("Why it is not a single start:")
        for reason in card.blocked_reasons:
            lines.append(f"  - {reason}")
    elif card.blocked_reasons and card.verdict == "one-title":
        lines.append("")
        lines.append("Set aside:")
        for reason in card.blocked_reasons:
            lines.append(f"  - {reason}")
    if card.notes:
        lines.append("")
        lines.append("Notes:")
        for note in card.notes:
            lines.append(f"  - {note}")
    lines.append("")
    return "\n".join(lines)


def _render_row(row: TitleRow, start: str | None, finish: str | None) -> list[str]:
    start_min = parse_clock(start) if start else None
    finish_min = parse_clock(finish) if finish else None
    label = fit_label(row.duration_min() if row.copies else None, start_min, finish_min)
    if not row.copies:
        shelf = "no"
    elif row.split:
        shelf = f"{len(row.copies)} copies, bytes differ"
    elif row.same_bytes:
        shelf = f"{len(row.copies)} copies, same bytes"
    else:
        shelf = "1 copy"
    duration = row.duration_min()
    duration_text = "unknown" if duration is None else str(duration)
    subtitles = row.subtitles()
    subtitle_text = "unknown" if subtitles is None else subtitles
    output = [
        f"- {row.title}",
        f"  on shelf: {shelf}",
    ]
    for item in row.copies:
        output.append(f"  path: {item.relative_path}")
        output.append(f"  sha256: {item.sha256}")
    output.append(f"  duration_min: {duration_text}")
    if start and finish and row.copies:
        output.append(f"  fit: {label}")
    elif start and finish:
        output.append("  fit: not-applicable")
    output.append(f"  subtitles: {subtitle_text}")
    output.append("  playback: not started")
    return output
