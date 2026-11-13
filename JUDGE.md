# Judge log

Criteria are the four equally weighted Round 1 criteria from the official rules. Scores are 1 to 10. A missing NAS run is not treated as a deduction, because the rules say a lack of NAS runtime evidence does not by itself lower a Round 1 score. Scores below 9.5 name a gap that the next round can actually close.

## Round 1

Evidence used: `evidence/checker-0.7.7.json` (`static-pass`, 0 errors, 0 warnings, kit 0.7.7, catalog 2.2.0), `PYTHONPATH=src python3 -m unittest discover -s tests` (18 tests), and `PYTHONPATH=src python3 -m shelfcheck demo`.

| Criterion | Score |
| --- | ---: |
| User Value | 9.0 |
| Innovation & Differentiation | 8.5 |
| Technical Quality | 9.0 |
| AI NAS Fit & Validation | 9.0 |

### User Value

The household problem, the list-then-card flow, and the Friday rehearsal are clear. The card names one film, sets two others aside, and does not play anything. Empty lists and an over-long list stop instead of inventing a title.

Gap: a judge who only reads the ZIP never sees a finished card. The verdict words live in the rehearsal, not in the skill package.

### Innovation & Differentiation

The no-substitute rule, the split-checksum block, and the clock filter are different from Skills Hub recommendations, subtitle matching, and Script to Selects. The gallery itself was unpublished on 13 November 2026.

Gap: the package can still be read as "call shortlist and summarize." It does not yet show, in the skill the judges upload, that the parent must apply fixed verdict rules and must not ask a model to improvise a similar film.

### Technical Quality

The official checker returned static-pass. Tests cover the Friday sample, the hidden extra file, split bytes, unknown duration, the 12-title stop, and the empty shelf. All five delegation statuses are named. Writes sit behind a later yes.

Gap: conflicting durations on copies of one title are specified and untested.

### AI NAS Fit & Validation

Shortlist, OCR, mediainfo, SHA-256, subtitle search, save-text, and subtitle-download are real catalog actions, and the default path keeps the list on the NAS. The play step is kept off that path because catalog 2.2.0 marks it approval none.

Gap: the same as user value. The NAS-shaped result is easier to see in Python than in the skill a judge opens.

### Top gaps to close next

1. Put a worked card, labeled as a rehearsal illustration, inside the skill package.
2. Say that the parent applies `decision-rules.md` and does not delegate the verdict to an expert.
3. Add a unit test for conflicting durations.
