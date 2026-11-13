# Shelf Check

Shelf Check is a Round 1 skill for the UGREEN Hackathon 2026 on AI NAS. A household points it at a watch list. It reports which titles are in the video library, which copies match, which fit before a finish time, and which line could not be read. It does not offer a substitute film.

The NAS package is Markdown only, in `skill/shelf-check/`. `skill.zip` is that folder, packed so the archive root is `shelf-check/`. The Python under `src/shelfcheck/` is a local rehearsal. It is not part of the ZIP and it does not talk to a NAS.

## Run the demo

```bash
PYTHONPATH=src python3 -m shelfcheck demo
```

That reads `samples/friday-night/` and prints the shelf card. Sample videos are tiny stand-in files, not real films. Duration and subtitle lines come from sibling `.facts.txt` fixtures. The card says so.

Check another tree:

```bash
PYTHONPATH=src python3 -m shelfcheck check \
  --root samples/empty-shelf \
  --list samples/empty-shelf/list.txt
```

Exit code 0 means a card was printed. Exit code 2 means there was nothing readable to look up, or more than 12 titles so lookup did not run. Exit code 1 is a bad path or a bad clock.

## Tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The package test rebuilds `skill.zip`. If the official UGOS Skill Creation Tool is unpacked at `/tmp/uliya/uliya-skill-kit`, or at the directory in `ULIYA_SKILL_KIT`, one test runs `scripts/check-skill.mjs` and expects `static-pass` with zero warnings.

The kit used here was `uliya-skill-kit` 0.7.7 from the starter-kit page:

https://ai.ugreen.com/pages/hackathon-starter-kit

The last local checker report is `evidence/checker-0.7.7.json`.

## Layout

| Path | Role |
| --- | --- |
| `skill/shelf-check/SKILL.md` | Skill entry point |
| `skill/shelf-check/references/` | Rules, card, catalog notes, tests, disclosures |
| `skill.zip` | Pre-test package for Devpost |
| `src/shelfcheck/` | Local rehearsal |
| `samples/` | Simulated library trees |
| `ROUND1_PROPOSAL.md` | Proposal source |
| `ROUND1_PROPOSAL.pdf` | PDF to upload |
| `SUBMISSION.md` | Draft Devpost fields |
| `BRIEF.md` | Scope, cut list, rivals, demo |
| `JUDGE.md` | Scores against the official criteria |

## Pack the ZIP again

```bash
python3 tools/package_skill.py
```

The packer refuses anything that is not Markdown under `SKILL.md` or `references/`.

## License

Apache-2.0. Copyright 2026 LevelUpWorldHub. See `LICENSE`.
