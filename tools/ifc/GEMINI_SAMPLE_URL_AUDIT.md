# Gemini sample URL audit

Audited on 2026-08-03 by downloading candidates and opening them with
IfcOpenShell 0.8.5.

| Candidate | Result | Value |
|---|---|---|
| BOT Duplex house | Verified | IFC2X3; 21 spaces, 113 walls, 50 openings, 14 doors, 24 windows; Bonsai import/save passed |
| buildingSMART IfcScript `Slab.ifc` | Verified | IFC4; minimal material-layer/slab relationship fixture |
| xeokit duplex URL | Not available | HTTP 404; do not use without a corrected repository path |
| IfcOpenShell `cube.ifc` URL | Not available | HTTP 404 at the cited v0.8.0 path |
| buildingSMART Building_A URL | Not available | HTTP 404 at the cited path; use the official repository archive instead |
| KIT FZK Haus | Previously verified | IFC4; native wall/opening/fill relationships; Bonsai import/save passed |

## Useful additions to the test suite

The BOT duplex is the best new reference for residential scale, spaces,
furniture, doors/windows, relationships, and space boundaries. The slab file is
useful as a small material-layer regression fixture. The KIT FZK Haus remains
the best reference for a compact, well-known architectural opening model.

The report's automation idea is useful, but the downloader should record URL,
HTTP result, byte size, SHA-256, IFC schema, and validation status. A URL alone
is not evidence of provenance or availability.
