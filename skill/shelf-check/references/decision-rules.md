# Decision rules

Apply these rules in order after the list text and the shortlist result are known. Use only facts those steps returned.

## List lines

- Ignore a blank line.
- A line is unreadable when it is `[unreadable]` in any letter case, when it begins with `UNREADABLE:`, or when it is only question marks and spaces.
- Every other non-blank line is a readable title. Keep the trimmed wording for display.
- The match key is the display text in lowercase, with punctuation replaced by spaces, with repeated spaces collapsed, and with a trailing ` (copy)` or ` copy` removed. Build the same key for a video file name, without its extension.
- An unreadable line has no match key. Do not compare it with the library.

## Lookup scope

- Look up readable titles only, in list order.
- If more than 12 readable titles remain, look up nothing. Ask which 12 to keep. Twelve is the ug-video shortlist maximum.
- A library file whose key matches no readable title must not appear on the card, even when the bytes sit beside a matched file.
- Do not add a title the list did not contain.

## Copies

Group matched files by title.

- No file: the title is not on the shelf.
- One file: one copy.
- More than one file and one SHA-256: same bytes. Either path is the same film, and playback still needs one chosen path.
- More than one SHA-256: the copies differ. Do not prefer the newer time, the larger file, or the name that says final.

## Duration, subtitles, and the clock

- Duration is unknown unless mediainfo returned it for that path. Conflicting durations across same-byte copies make duration unknown.
- Subtitles are unknown unless subtitle-search returned a fact for that path. An explicit statement of no candidates is `none`, which is not the same as unknown.
- If the user gave both a start time and a later finish time on the same day, a known duration fits only when the start plus that duration lands at or before the finish, and not after midnight. Unknown duration does not fit. A title that is not on the shelf has no fit line.
- If the user gave neither time, do not invent a bedtime and do not mark a fit.

## Verdict

- No readable titles: stop. There is no verdict title.
- More than 12 readable titles: the verdict is that lookup did not run.
- A title can be started only when it is on the shelf, its copies do not differ, and, when a clock was given, the duration is known and fits.
- One such title: name it. If the bytes match across paths, say either path is the same film. Playback still waits for a chosen path.
- Several such titles: list them in list order and do not pick one.
- None: block, and list the reason for each readable title. Reasons are only: not on the shelf, copies differ, duration unknown, or runs past the finish time.

## What the card must not do

- Do not start playback, download a subtitle, or save a note as part of building the card.
- Do not fill a miss with a similar title.
- Do not match an unreadable line.
