# External Asset Interface

Layer 1 owns animation, not business artwork. Higher layers can inject fixed vector path assets through `meta.asset_registry`.

Example:

```json
{
  "meta": {
    "asset_registry": {
      "custom_landmark": "assets/custom_landmark.json"
    }
  }
}
```

`custom_landmark.json`:

```json
{
  "paths": [
    [[10, 10], [30, 20], [50, 5]],
    [[20, 40], [40, 60]]
  ]
}
```

The renderer treats these exactly like built-in path assets and draws them progressively. No hidden raster or mask reveal is introduced.

## Product-approved hand overlay

Higher layers may also supply the fixed visible drawing-hand overlay used by the renderer:

```json
{
  "meta": {
    "hand_asset": "assets/approved-hand.png",
    "hand_width": 170
  }
}
```

Supported hand files: PNG, WebP, and SVG. Relative paths are resolved from the scene-spec file.

For PNG/WebP, provide sidecar metadata with the same basename:

```json
{
  "native_size": [1448, 1086],
  "tip_anchor_px": [284, 842]
}
```

For SVG, use `viewbox` and `tip_anchor_viewbox` as before.

The hand is a visible UI/animation overlay only. It is not a hidden finished-art image and is never used to reveal completed artwork. The runtime does not regenerate it; the higher product layer can lock a reviewed asset and its pen-tip calibration deterministically.
