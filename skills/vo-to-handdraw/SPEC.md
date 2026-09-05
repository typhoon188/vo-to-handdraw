# Layer 1 Scene Spec v1.1

## Top-level

```json
{
  "meta": {
    "title": "string",
    "canvas": {"width": 960, "height": 540},
    "fps": 15,
    "background": "#F5EBD7",
    "ink": "#303030",
    "show_audit_subtitles": false,
    "timing_source": "srt | estimated_script",
    "asset_registry": {
      "optional_custom_asset": "relative/path.json"
    }
  },
  "vo_segments": [
    {"id":"vo_001","start_s":0.0,"end_s":5.5,"text":"..."}
  ],
  "scenes": [
    {
      "id": "scene_01",
      "source_segment_ids": ["vo_001"],
      "subtitle": "audit text",
      "duration_s": 7.5,
      "semantic_goal": "what this beat communicates",
      "visual_cues": ["asset names"],
      "actions": []
    }
  ]
}
```

## Generic actions

### path_draw
Progressively draws a vector polyline.

```json
{"type":"path_draw","id":"path1","start":0,"duration":2,"points":[[50,300],[400,250],[850,320]],"style":{"width":2}}
```

### asset_draw
Progressively draws a built-in or externally registered vector-path asset.

```json
{"type":"asset_draw","asset":"custom_asset","start":2,"duration":2.5,"x":500,"y":180,"scale":1.1}
```

### actor_follow_path
Moves a vector actor along a declared `path_draw` path.

```json
{"type":"actor_follow_path","asset":"bike_rider","path_ref":"path1","start":2,"duration":4,"scale":0.9}
```

### text_write
Progressively writes text while the hand tracks the writing endpoint.

```json
{"type":"text_write","text":"OUR STORY","start":5,"duration":2,"x":340,"y":120,"font_scale":0.8}
```

### hold
Timing placeholder.

```json
{"type":"hold","start":7,"duration":1}
```

## Production rules
- `timing_source` must be `srt`.
- Every VO segment must be covered by at least one scene.
- Every scene must reference its VO source segments.
- Every action must fit within its scene time window.
- `actor_follow_path.path_ref` must point to a path in the same scene.
- mask / wipe / clip-path / opacity reveal / hidden-image keys are forbidden.
