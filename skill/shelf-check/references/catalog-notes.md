# Catalog notes

These notes were taken from UGOS Skill Creation Tool `uliya-skill-kit` 0.7.7, capability catalog 2.2.0. They are generation-time facts. A finalist NAS can return different fields. If a field is missing at runtime, treat it as unknown.

| Step | CLI action | Expert | Effect in catalog | Approval in catalog |
| --- | --- | --- | --- | --- |
| Confirm the list path | `ug-filesystem` `stat` | `file-agent` | read | none |
| Read a text list | `ug-filesystem` `cat` | `file-agent` | read | none |
| OCR a photo of a list | `ug-photo` `vision-ocr` | `photo-agent` | read | none |
| Look up titles | `ug-video` `shortlist` | `media-agent` | read | none |
| Duration | `ug-filemgr` `mediainfo` | `file-agent` | read | none |
| Checksums | `ug-filesystem` `sha256sum` | `file-agent` | read | none |
| Subtitle candidates | `ug-video` `subtitle-search` | `media-agent` | read | none |
| Save the card | `ug-knowledge` `save-text` | `knowledge-agent` | state-change | workflow |
| Download one subtitle | `ug-video` `subtitle-download` | `media-agent` | state-change | gateway |
| Play one chosen id | `ug-video` `search` with play | `media-agent` | catalog effect is read; the description says play can start playback | none |

`ug-video` `shortlist` accepts at most 12 titles and does not start playback. Its description says misses are recorded per title.

`ug-video` `subtitle-download` requires a `file-id` from a subtitle-search result. Do not invent that id.

`ug-video` `control` operations are pause, continue, previous, and next. Control cannot select a title. Do not use it to start the film.

`ug-video` `search` is labeled `effect: read` and `approval: none` in catalog 2.2.0, while its description says play can start playback immediately. That is a catalog tension. Shelf Check keeps play off the default path until the user picks one file, and a finalist test must show that preparing the card does not start the player.

`vision-ocr` reads a real image path the user named. A non-image is skipped. The catalog does not promise handwriting accuracy. Unreadable text stays unreadable.

No action in this workflow deletes, moves, or renames a video.
