# Draft Devpost submission

These are draft fields for the UGREEN Hackathon 2026 on AI NAS submission form. The live form was not opened, because it requires a Devpost account. Required uploads below are taken from the official rules, not guessed from a screenshot. Where the form's track label differs from the rules, use the memories track the form actually shows.

Do not submit this repository link as a required Round 1 item. The rules say Round 1 does not require a code repository link or a demo video.

## Project name

Shelf Check

## Tagline

Which films from your own list are actually on the NAS, and which one fits before the time you named.

## Track

Bring Memories to Life.

The rules and the overview use that name. On 13 November 2026 the gallery filter instead listed Understand Your Life and Explore Your Imagination. Pick the form option that matches the memories track.

## Elevator description

Shelf Check reads a watch list a household already wrote, as a text file or a photo of a note, and returns one card. Each readable title is on the shelf or missing. Duplicate copies are either the same bytes or a real split. A finish time keeps a film that would run past it off the verdict. An unreadable line is not matched to a nearby file. Nothing plays, downloads, or gets saved until a separate yes.

## Built with

UGOS Skill Creation Tool (uliya-skill-kit 0.7.7), capability catalog 2.2.0, Uliya skill Markdown, Python 3 standard library for the local rehearsal only.

## Files to upload

1. `ROUND1_PROPOSAL.pdf`. Separate PDF, under 1 MB. The ten answers in the source are 498 English words. License notes sit after those answers and are excluded from that count.
2. `skill.zip`. Pre-test Skill package. Archive root is the `shelf-check/` directory: `SKILL.md` plus `references/*.md`. Under 10 MB. No scripts, credentials, or sample videos.

## What the ten PDF answers cover

The PDF uses the ten prompts from the official rules: one-sentence purpose, user and problem, solution, core flow, difference from other tools, NAS capabilities by step, technical approach, what is built and unbuilt, two core tests and one edge case, and known limits.

## Team

Individual. Representative: LevelUpWorld. Copyright holder for the rehearsal and the license: LevelUpWorldHub.

No team consent attachment is included. Add names and signatures on the form if the form asks and if more than one person enters.

## AI tools

Cursor Grok 4.7 drafted the Skill, the proposal, and the rehearsal, and ran the tests and the official static checker. The workflow was checked against catalog 2.2.0. Disclose the same sentence if the form has an AI-tools field. It is also in `skill/shelf-check/references/disclosures.md`.

## Try it out

Not required for Round 1. Local demo, which is not a NAS run:

`PYTHONPATH=src python3 -m shelfcheck demo`

## What was not verified on the form

The exact character limits, thumbnail requirement, and custom question widgets on "Enter a Submission" were not visible without a logged-in Devpost session. The PDF and ZIP requirements were taken from:

- https://ugreenhackathon.devpost.com/
- https://ugreenhackathon.devpost.com/rules
- https://ugreenhackathon.devpost.com/resources
- https://ai.ugreen.com/pages/hackathon-starter-kit

## Checker

`evidence/checker-0.7.7.json` records a `static-pass` from kit 0.7.7: zero errors, zero warnings. That file is a local log. It is not part of `skill.zip`.
