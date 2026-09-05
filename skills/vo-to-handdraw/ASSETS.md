# Layer 1 Assets

## Brand hand
`assets/feminine-hand-fineline-v1.svg` is a fixed transparent vector asset with a calibrated pen-tip anchor and SHA256 metadata in `feminine-hand-fineline-v1.json`.

The hand is deliberately isolated from business-domain artwork. It can be replaced by a later approved brand-hand asset without changing the renderer, scene spec, planner, or Layer 2 integration.

## Built-in starter vocabulary
The runtime includes a small domain-neutral starter vocabulary used for proof and smoke tests. Higher layers should inject product-specific artwork through the external asset registry instead of modifying the renderer.

## External assets
See `ASSET_INTERFACE.md`. External assets are fixed vector polylines and are progressively stroked by the same renderer. They do not introduce hidden raster reveals.
