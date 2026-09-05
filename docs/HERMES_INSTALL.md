# Hermes Local Installation

This release uses Hermes' normal local skills directory: `~/.hermes/skills/`.

## 1. Install the skill folder
From the unpacked release directory:

```bash
bash install-local.sh
```

Equivalent manual command:

```bash
mkdir -p ~/.hermes/skills
cp -R skills/vo-to-handdraw ~/.hermes/skills/vo-to-handdraw
```

## 2. Install runtime dependencies

```bash
bash ~/.hermes/skills/vo-to-handdraw/scripts/bootstrap.sh
```

Requirements:
- Python 3
- ffmpeg / ffprobe
- Python packages in `requirements.txt`

On macOS, if ffmpeg is missing:

```bash
brew install ffmpeg
```

## 3. Verify the skill

```bash
hermes skills list | grep vo-to-handdraw
bash ~/.hermes/skills/vo-to-handdraw/scripts/verify.sh
```

Expected final line:

```text
VERIFY_OK
```

Installed skills are loaded by Hermes from `~/.hermes/skills/`. If Hermes is already running, start a new session or reset/reload the session after installation.

## 4. First smoke test in Hermes
Ask Hermes:

> Use the vo-to-handdraw skill. Create a draft hand-drawn video from the included `examples/vo/draft.txt`, render it to `/tmp/handdraw-test.mp4`, run QA, and report the output path and QA result.

Then test SRT timing:

> Use the vo-to-handdraw skill with `examples/vo/generic_trail.srt`, render an audit video to `/tmp/handdraw-srt-test.mp4`, and report whether the SRT timing and strict QA pass.
