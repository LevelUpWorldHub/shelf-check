# Shelf card

Show the card in this order. Use the words the expert returned. Leave a fact out rather than inventing a value.

1. List path the user named.
2. Clock, only when both times were given.
3. Count of readable titles and count of unreadable lines.
4. Count of library hits.
5. Verdict: one named title, a choice, a block, or lookup not run.
6. The sentence `Playback: not started`.
7. One block per readable title, in list order: shelf status, paths, checksums when returned, duration, fit when a clock was given, subtitle fact.
8. Unreadable lines, each with its line number and the words `not matched to any file`.
9. The reasons other titles were set aside, when the verdict is not a free choice among equals.

A block is useful. Show misses in the same card as hits.

The local rehearsal prints the same fields and adds a banner that the run is not a NAS run. That banner is not part of the NAS card. The rehearsal also labels duration and subtitle lines as fixture facts when they came from a sidecar file.

# Four verdicts

These illustrations apply the decision rules to stated facts. They are not NAS output, and they are not permission to invent a fact the experts did not return.

## One title

Clock 19:00 to 21:00. Forest Journey has two copies and one checksum, and the duration is 118 minutes, so it fits. Long Winter is present, and 150 minutes runs past 21:00. Missing Moon is not on the shelf. One list line is unreadable. An extra file is on disk and is not named.

Verdict: one title, Forest Journey. Say that either path is the same film. Playback has not started.

## Choose

The same three titles, and no clock. Forest Journey and Long Winter are both present, and their copies do not differ. Missing Moon is not on the shelf.

Verdict: choose. Keep list order. Do not pick for the user. Playback has not started.

## Blocked

Readable titles were looked up, and every one missed.

Verdict: blocked. Say no results. Do not offer a different film. Playback has not started.

## Lookup not run

The list has 13 readable titles.

Verdict: lookup not run. Ask which 12 to keep. Do not look up a silent subset.
