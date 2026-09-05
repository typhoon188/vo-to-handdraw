---
name: vo-to-handdraw
description: Convert voice-over scripts or verified SRT timelines into deterministic hand-drawn MP4 videos with a visible hand and pen, progressive vector drawing, actor movement, text writing, and strict no-mask/no-wipe QA.
version: 1.1.0
metadata:
  hermes:
    tags: [video, animation, handdraw, voiceover, srt, ffmpeg]
---

# VO-to-Handdraw — Layer 1

## Purpose
Turn a voice-over script/timeline plus a generic scene plan into a genuine hand-drawn video. This skill is domain-agnostic: it does not decide what a mountain-bike trail, love-story product, retirement product, or other business object means.

## When to use
Use this skill when the user asks to turn narration, a script, an SRT, or a prebuilt scene plan into a hand-drawn video.

## Required pipeline
1. Read the entire narration before planning visuals.
2. For ordinary 30–60 second narration, compress it into roughly 3–6 meaningful visual beats rather than illustrating every sentence.
3. Preserve narration provenance using `source_segment_ids` on each scene.
4. Express each scene using only the generic animation primitives below.
5. Run strict QA before render.
6. Render true progressive vector strokes; the visible hand/pen follows the active drawing endpoint.
7. If voice-over audio is supplied, mux it into the final MP4.

## Generic primitives
- `path_draw`
- `asset_draw`
- `actor_follow_path`
- `text_write`
- `hold`

See `SPEC.md` for the scene-plan schema and `ASSET_INTERFACE.md` for external asset injection.

## Hard visual rules
Never use:
- mask reveal
- wipe reveal
- clip-path reveal
- opacity reveal of a finished picture
- a hidden finished raster image beneath the drawing surface

## Production timing rule
A production run requires a verified SRT transcript/timeline. Plain text is allowed for draft planning only. Do not invent production timing from raw audio.

## Layer boundary
Layer 1 may receive fixed external vector-path assets through `meta.asset_registry`. It must not infer domain-specific landmarks, product rules, map meaning, or trail/business identity. Those belong to a higher-level planner.

## Preferred semantic planning
The model executing this skill should understand the complete narration and author a scene plan itself when quality matters. `planner/auto_plan.py` is a deterministic fallback/smoke-test planner, not the quality ceiling.

## Commands
First-time environment setup:

```bash
bash scripts/bootstrap.sh
```

Draft from a text script:

```bash
bash scripts/run.sh examples/vo/draft.txt /tmp/handdraw-draft.mp4 --audit
```

Production from verified SRT plus voice-over audio:

```bash
bash scripts/run.sh voiceover.srt final.mp4 --audio voiceover.mp3 --production
```

Use a model-authored scene plan:

```bash
bash scripts/run.sh voiceover.srt final.mp4 --plan scene_plan.json --audio voiceover.mp3 --production
```

Verify the installation/runtime:

```bash
bash scripts/verify.sh
```
