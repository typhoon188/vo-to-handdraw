# VO-to-Handdraw

[![CI](https://github.com/typhoon188/vo-to-handdraw/actions/workflows/ci.yml/badge.svg)](https://github.com/typhoon188/vo-to-handdraw/actions/workflows/ci.yml)

A Hermes-ready Layer-1 skill for turning voice-over scripts and SRT timelines into deterministic hand-drawn MP4 video.

`vo-to-handdraw` is deliberately domain-agnostic: the same renderer can drive trail, love-story, retirement, education, product-explainer, and other scene-based hand-drawn videos by supplying different scene specs and vector assets.

## What it does

- progressive vector path drawing
- visible hand + pen following the active stroke
- SRT-driven production timing
- actor motion along paths
- progressive text writing
- multi-scene rendering
- optional voice-over audio muxing
- normalized scene-plan and QA report output
- strict rejection of mask / wipe / clip-path / hidden-finished-image reveal patterns
- deterministic rendering for identical inputs
- external asset registry so domain-specific artwork can stay outside Layer 1

## Install in Hermes

```bash
hermes skills install typhoon188/vo-to-handdraw/skills/vo-to-handdraw
```

See [`docs/HERMES_INSTALL.md`](docs/HERMES_INSTALL.md) for local installation and validation.

## Requirements

- Python 3.11+
- FFmpeg / ffprobe
- Cairo runtime
- Python dependencies from `skills/vo-to-handdraw/requirements.txt`

On Ubuntu, the CI reference environment installs:

```bash
sudo apt-get install -y ffmpeg libcairo2
```

## Quick start

Draft mode accepts plain text and is useful for planning or previews:

```bash
cd skills/vo-to-handdraw
python handdraw.py examples/vo/draft.txt /tmp/handdraw-draft.mp4
```

Production mode requires SRT-verified timing:

```bash
python handdraw.py \
  examples/vo/generic_trail.srt \
  /tmp/handdraw-production.mp4 \
  --production
```

With voice-over audio:

```bash
python handdraw.py \
  voiceover.srt \
  final.mp4 \
  --audio voiceover.mp3 \
  --production
```

The pipeline writes the final MP4 plus normalized plan and QA JSON next to the output unless explicit paths are supplied.

## Scene primitives

Layer 1 currently supports these generic primitives:

- `path_draw`
- `asset_draw`
- `actor_follow_path`
- `text_write`
- `hold`

Domain planners should compile their own semantics into these primitives rather than modifying the renderer.

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

GitHub Actions independently passed on Ubuntu 24.04 / Python 3.11, including production validation, external asset rendering, audio+video output, cross-domain smoke tests, and deterministic SHA checks. See [`docs/VALIDATION.md`](docs/VALIDATION.md).

## Layer boundary

This repository contains only the generic Layer-1 hand-drawn video engine and its Hermes skill wrapper.

It intentionally does **not** contain domain-specific business intelligence such as MTB trail fingerprinting, GPX/elevation analysis, route intelligence, proprietary map logic, or private product asset libraries. Those belong in an upstream planner that emits a Layer-1 scene spec.

Raw-audio ASR is also intentionally out of scope for this version: production rendering expects an SRT or equivalent verified timeline rather than guessing timing from audio alone.

## License

MIT
