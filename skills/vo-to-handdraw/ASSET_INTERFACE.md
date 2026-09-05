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
