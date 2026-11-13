# Validation plan

Round 1 has no NAS. The local rehearsal checks the decision rules on a sample tree. It is not a shortlist, an OCR engine, or a subtitle search. Finalist day is when those experts run.

## Core test 1

Library index contains two byte-identical copies of one film, one longer film, and one extra film that is not on the list. The list has the first film, the longer film, a title that is not in the index, and one unreadable line.

Pass when the card names only the first film as the single fit before the stated finish time, says the two copies match, says the longer film runs past, says the absent title is not on the shelf, and does not name the extra film. Playback stays stopped.

## Core test 2

Same library, no finish time.

Pass when the verdict asks the user to choose between the two films that are on the shelf, and still does not name the extra film or the unreadable line as a match.

## Edge case

A readable list, and a video folder with no indexed titles. The rehearsal uses an empty `video` directory as the stand-in.

Pass when the card says no results, names no start, and does not suggest another film.

## Extra finalist checks

- A file on disk that the video index does not return must stay a miss.
- More than 12 readable titles must produce no shortlist call.
- Two copies with different checksums must block that title.
- A spoken yes before the card must not save, download, or play.
- Saving and subtitle download must show platform approval, then a verified path or an explicit failure.
- Card preparation must not start the player, including when search play is approval none.
