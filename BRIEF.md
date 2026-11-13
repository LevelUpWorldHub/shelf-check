# Shelf Check brief

## Idea

Shelf Check is a UGREEN AI NAS skill for a household that already chose what to watch. It turns that list into a shelf card: which titles are in the video library, which copies are the same bytes, which run past a finish time, and which line could not be read. The verdict names one safe start, asks for a choice, or blocks and says why. It does not recommend a substitute.

Track: Bring Memories to Life (official rules and overview). The unpublished gallery filter used different labels, including Understand Your Life. Use the memories track that the live Devpost form shows.

Skill id: `shelf-check`.

## Demo moment

One command on the sample tree:

`PYTHONPATH=src python3 -m shelfcheck demo`

The list is Forest Journey, Long Winter, Missing Moon, and an unreadable line. The folder also holds Night Market, which is not on the list. The clock is 19:00 to 21:00.

The card produced by that command on 13 November 2026:

- Verdict: one-title. Named title: Forest Journey (pick either path; the bytes match).
- Forest Journey is two copies with the same SHA-256, duration 118 minutes, fit yes, subtitle fixture `en`.
- Long Winter is one copy, duration 150 minutes, fit no.
- Missing Moon is not on the shelf.
- The unreadable line is not matched to any file.
- Night Market is not named.
- Playback: not started.
- The banner says this is a local rehearsal, and that duration and subtitle lines are fixture facts.

That refusal is the moment. A nearby film on disk is not offered for a smudged line.

## Scope for this round

Deadline is Sunday 15 November 2026, 11:45 pm PT. This slice is the decision card, the Markdown skill, and a local rehearsal. It is sized to about half the time left.

## Cut list

- Music set-list mode. The catalog can search songs, and a practice list would reuse the same verdict. Not in this round.
- Automatic subtitle download. Download stays an optional step after the card, and the rehearsal never downloads.
- Playback in the rehearsal. The sample files are not videos. `ug-video control` cannot start a chosen title.
- Recommendations, posters, and "more like this".
- A scheduler or a Friday reminder. Skills are on demand.
- Album creation and file moves. Nothing is deleted, moved, or renamed.
- Multi-user taste profiles.
- Handwriting OCR inside the rehearsal. The sample list uses an explicit `[unreadable]` line. Live OCR waits for a NAS.
- Proof that a file on disk but outside the video index stays a miss. Shortlist is an index lookup. The rehearsal walks `video/`, which stands in for the index only.

## Rivals

The project gallery at https://ugreenhackathon.devpost.com/project-gallery said, on 13 November 2026, that the managers had not published it. Overlap was checked on the Skills Hub and on public Devpost pages, not on a hidden gallery.

1. Skills Hub, Personalized recommendations v1.0.0. It recommends movies from viewing preferences. Shelf Check does not infer taste. It checks a list the household already wrote.
2. Skills Hub, Smart subtitle matching v1.0.0. It matches subtitles for a video that is already chosen. Shelf Check asks whether the title is even on the shelf, and it does not download during the card.
3. Script to Selects, https://devpost.com/software/script-to-selects. It scores NAS footage against a production script and lists shots still to film. Shelf Check is a household watch list. An unmatched title is a miss, not a prompt to shoot something else.

Other public pages (warranty packs, home inventories, final-version finders, photo-library health) solve different jobs. They are why this is not another receipt binder.

## What a finalist day would add

Run the two core tests and the empty-index edge case on the assigned iDX6011 Pro. Confirm that preparing the card does not start playback, that save-text and subtitle-download wait for platform approval, and that shortlist misses stay misses.
