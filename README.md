# VO-to-Handdraw

A Hermes-ready skill for turning voice-over scripts and SRT timelines into deterministic hand-drawn videos.

## What it does

`vo-to-handdraw` converts a normalized voice-over plan into scene-based hand-drawn animation with:

- progressive vector drawing
- visible hand + pen
- SRT-driven timing
- actor motion along paths
- progressive text writing
- strict QA against mask/wipe/hidden-image reveal
- deterministic MP4 rendering

The skill is intentionally domain-agnostic. Trail videos, love-story videos, retirement videos, and other use cases can all use the same Layer-1 renderer by supplying different scene specs and assets.

## Install in Hermes

```bash
hermes skills install typhoon188/vo-to-handdraw/skills/vo-to-handdraw
```

See [`docs/HERMES_INSTALL.md`](docs/HERMES_INSTALL.md) for local installation and validation.

## Validation status

Validated in Hermes on 2026-09-05:

- Skill discovery: PASS
- Draft VO → MP4: PASS
- SRT timing: PASS
- VO alignment: PASS
- Trail / Love Story / Retirement through one renderer: PASS
- Deterministic rendering: PASS
- Production without SRT correctly rejected: PASS
- Mask/wipe specs correctly rejected: PASS

## Layer boundary

This repository contains only the generic Layer-1 hand-drawn video skill. Domain-specific business planning—such as MTB trail fingerprinting, GPX analysis, route intelligence, or proprietary map/product logic—is intentionally outside this public repository.

## License

MIT
