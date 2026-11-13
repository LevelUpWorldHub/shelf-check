# Disclosures

## Principal work in this Hackathon

The Skill, its decision rules, and the shelf-card workflow were written for the UGREEN Hackathon 2026 on AI NAS. No earlier Skill was reused.

## Third-party components inside this package

None. This package is Markdown only. It does not vendor a model, a library, or the UGOS Skill Creation Tool.

Capability names and approval values are cited from UGREEN's UGOS Skill Creation Tool, package `uliya-skill-kit` 0.7.7, catalog version 2.2.0, downloaded from the official starter-kit page. That tool is not included here. Its license is UGREEN's. Shelf Check does not redistribute it.

## Local rehearsal, outside this package

The repository that developed this Skill also contains a Python 3 rehearsal under `src/shelfcheck` and sample files under `samples/`. That code uses the Python standard library only. It is licensed Apache-2.0, Copyright 2026 LevelUpWorldHub. It is not part of this ZIP. It hashes sample bytes and reads `.facts.txt` sidecars for duration and subtitle fixtures. Those sidecars are not NAS results.

## AI tools

Cursor Grok 4.7 drafted this Skill, the reference notes, the proposal, and the rehearsal, and ran the local tests and the official static checker. The workflow was checked against catalog 2.2.0 rather than against memory of the API. No NAS was available, so no NAS output was invented.

## Data handling

The intended NAS run stays on the device. The default path does not call an outside service. Do not send list text, stills, or video paths to a cloud model. Prefer the NAS local model. If only a cloud model is available, stop and tell the user before any list or image is read.
