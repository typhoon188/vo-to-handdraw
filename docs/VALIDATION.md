# Validation Record

This document records the verification state of the public Layer-1 `vo-to-handdraw` skill.

## Hermes validation — 2026-09-05

The already-installed skill was exercised through Hermes rather than bypassed with an ad-hoc renderer.

| Check | Result |
| --- | --- |
| Skill callable by Hermes | PASS |
| Draft VO → MP4 | PASS |
| SRT timing | PASS |
| VO alignment | PASS |
| Trail example | PASS |
| Love Story example | PASS |
| Retirement example | PASS |
| Same renderer for all three domains | YES |
| Deterministic SHA256 | PASS |
| Production without SRT rejected | PASS |
| Mask/wipe spec rejected | PASS |

Hermes deterministic trail hash from the local validation run:

```text
c729f8e6d35e98d2fe43ec784bf82a4f649e65dab38d4aa7eb5b2c8d182c5ce9
```

## GitHub Actions validation — 2026-09-05

Workflow: `.github/workflows/ci.yml`

Reference runner:

- Ubuntu 24.04
- Python 3.11.16
- FFmpeg
- Cairo

The first public CI run completed successfully. The following workflow steps all returned `success`:

- Install system dependencies
- Install Python dependencies
- Production validation
- Cross-domain smoke and deterministic tests

Production test evidence from CI:

```text
PASS
scene_count 4
deterministic_sha256 c8cd750aad7ae8adbdacbe3c92e55fc2fd7a3d291fd1eee1f8ef0d629ce85856
audio_video_streams ['audio', 'video']
```

Cross-domain smoke test evidence:

```text
PASS
trail_demo_sha256 1384ffa488436f49ba0bbe009c9d1a0cd5bf3f5e3ffa04724931e1dd275870ee
validated_specs 3
```

The three independently rendered domain examples had distinct hashes:

```text
trail      1384ffa488436f49ba0bbe009c9d1a0cd5bf3f5e3ffa04724931e1dd275870ee
love       42f33e5112155582390449e8f728bca6be1c826bf87aa220d0bcab98feac087d
retirement 1144b3a9146fa0b2a1c07e74d94706603e3e3f7057a687528285ade29b019301
```

## What these tests establish

The validation demonstrates that the public Layer-1 engine can:

1. consume a draft script or SRT timeline;
2. generate or accept a normalized scene plan;
3. perform strict QA before rendering;
4. progressively render hand-drawn scenes using one generic runtime;
5. mux optional voice-over audio into the final MP4;
6. render multiple domains without modifying the Layer-1 renderer;
7. reproduce byte-identical output for the same deterministic test input;
8. reject production plans without verified SRT timing and reject forbidden reveal mechanisms.

## What these tests do not establish

They do not claim that the bundled art assets are the final aesthetic choice for every product, nor that raw audio transcription is part of Layer 1. Domain research, proprietary asset selection, GPX/map intelligence, and product-specific storytelling belong in upstream/private planning layers.
