# Semantic Planner Contract

The preferred planner for this Skill is the language model executing the Skill. `auto_plan.py` is a deterministic fallback and smoke-test planner, not the quality ceiling.

For a real VO script, the model must:

1. Read the complete VO before creating any scene.
2. Compress the narration into 3–6 visually meaningful beats rather than one scene per sentence.
3. For every beat, preserve `source_segment_ids` so every scene is traceable to the VO.
4. Choose only visual cues supported by the narration or by assets explicitly supplied by the caller.
5. Keep each scene visually simple: normally 2–5 primary elements.
6. Prefer a visual progression with one clear focal action rather than a static collage.
7. Use generic Layer-1 actions only: `path_draw`, `asset_draw`, `actor_follow_path`, `text_write`, `hold`.
8. Never encode business-domain logic in the renderer.
9. Never use mask, wipe, clip-path, opacity reveal, or a hidden finished image.
10. In production, timing must be grounded in SRT or another verified transcript timeline.

The output of the semantic planner is a `SPEC.md`-conformant JSON file consumed by the generic renderer.
