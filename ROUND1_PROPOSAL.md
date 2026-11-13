# Shelf Check

Round 1 proposal, UGREEN Hackathon 2026 on AI NAS. Track: Bring Memories to Life. Skill name: `shelf-check`.

## 1. What does your Skill do?

Shelf Check says which titles from a household watch list are on the UGREEN AI NAS, which are missing, which copies differ, and which fit before a time the user names.

## 2. Who is your target user, and what is their problem?

A family already wrote the Friday list, as a file or a photo of a note. The films may be in the NAS library, but duplicate rips, a smudged line, and unknown runtimes still hide what can start.

## 3. What is your solution?

The Skill checks only that list and returns one card. The verdict names one title that fits, asks the user to choose, or blocks a start with a reason per title. It never swaps in a similar film.

## 4. What is the main user flow?

The user names the list and an optional start and finish time. The Skill reads it, looks up at most twelve readable titles, and shows hits, checksums, duration, subtitles, and the verdict. A later yes can save, download one subtitle, or play one file.

## 5. How is your idea different?

Recommenders suggest films the house may not own. Subtitle tools assume a chosen video. Script-to-selects skills score a shoot. Shelf Check keeps list order, leaves a smudged line unread, and fills no gap. The Devpost gallery was unpublished on 13 November 2026. Closest public rivals: Skills Hub Personalized recommendations, Skills Hub Smart subtitle matching, and Script to Selects.

## 6. Which UGREEN AI NAS features, and where?

File-agent confirms the path and reads text. Photo-agent OCRs a photo list. Media-agent runs shortlist, which does not play, then subtitle-search on hits. File-agent adds duration and SHA-256. A later yes can save the card, download one subtitle, or play one id. Player control cannot start a title.

## 7. What is your technical approach?

The parent delegates to catalog 2.2.0 experts and passes only the real result forward. A missing path or id stops the next step. Reads need no approval. Saving the card needs workflow approval. Subtitle download needs gateway approval and the returned file id. Play stays off the default path because this catalog marks it approval none. Prefer the local model. No outside API.

## 8. What have you built so far? What is not built? What still needs a NAS?

Built: the Skill, six notes, and a rehearsal. Kit 0.7.7 returned static-pass, zero errors and zero warnings. Friday sample: Forest Journey fits 19:00 to 21:00, copies match, 118 minutes. Long Winter runs past. Missing Moon is absent. The smudged line is not matched. Nothing plays. A NAS is still required for install, OCR, shortlist, subtitles, and play.

## 9. How will you test your Skill if you become a Finalist?

Core test 1: two identical copies, one film past the clock, one missing title, and one unreadable line beside a similarly named file. The card names only the fit and plays nothing. Core test 2: with no clock, the verdict asks for a choice. Edge: a readable list and an empty index. The Skill says no results and stops.

## 10. What are the known limits, risks, or outside dependencies?

Shortlist stops at twelve titles. Failed OCR stays unreadable. Unknown duration cannot beat the clock. Matching bytes still need one path before play. A spoken yes is not platform approval. A NAS test must show the card does not start the player. There is no scheduler. A file outside the video index must stay a miss, which this folder rehearsal cannot prove.

## Third-party components and licenses

Excluded from the ten answers. The ZIP has no third-party code. Names are cited from UGREEN uliya-skill-kit 0.7.7, catalog 2.2.0, not redistributed. The rehearsal uses the Python 3 standard library and is Apache-2.0, Copyright 2026 LevelUpWorldHub. Cursor Grok 4.7 drafted the Skill text, this proposal, and the rehearsal. No API key is required.
