# FreeCAD Bridge

**STEP to SketchUp: named components, colors, bounded mesh repair and explicit surface handling.**

By **Yruam Kaffer de Faria** · Version **0.5.0** · Target: **SketchUp 2026 desktop / Windows**

[Full Portuguese documentation](README.md) · [Release notes](docs/RELEASE_0.5.0.md) · [License](LICENSE.txt)

Uses an installed FreeCAD command-line executable to convert STEP in the background. It preserves part placement, transfers available names/RGB colors when safely matched and reports per-part results. The package is unsigned.

## New in 0.5.0

- Merge near-coincident vertices within 0.0001 mm when a closed mesh has very thin triangles.
- Locally separate touching surface fans by 0.001 mm in Complete treatment mode.
- Recheck closure, winding, manifold edges/vertices, degeneracy, connected regions, bounds and mesh volume; reject out-of-limit attempts.
- Import loose shells/faces as explicitly labeled surfaces in Visualization mode.
- Solids Available mode omits rejected parts with names/reasons instead of silently losing geometry.
- Treat Existing JSON command; triangle colors retain provenance after the new adjustments.
- Preserve the 0.4.2 smoothing fix and 0.4.3 toolbar artwork.

## Install

Install [FreeCAD_Bridge_0.5.0.rbz](dist/FreeCAD_Bridge_0.5.0.rbz) through Extension Manager and restart SketchUp. Configure FreeCADCmd.exe, then choose STEP import. Linear deflection remains 0.001–100 mm, default 0.05 mm.

The interface is Portuguese: **Estrito** requires all parts to pass; **Visualização** includes surfaces/problem parts with labels; **Sólidos disponíveis** explicitly omits parts not approved by the converter and still checks included parts in SketchUp. **Completo** enables both mesh repairs; **Conservador** disables contact separation; **Sem reparos** disables optional repairs. Complete is the default and may displace local vertices by 0.001 mm.

The JSON toolbar button imports existing geometry unchanged. Use **Tratar JSON existente…** to apply treatments through FreeCADCmd. The source file is preserved. JSON reprocessing does not revalidate the original CAD geometry.

## Limits and validation

Curves remain polygonal. Open surfaces are not automatically capped. Names and colors must exist in the STEP; unmatched triangles may remain unpainted. Assembly hierarchy/shared definitions, textures, transparency and CAD features are not transferred. No universal solid guarantee or complete self-intersection test is provided.

The author confirmed the reference manual treatments in SketchUp. The new engine has synthetic tests and private geometry checks using Open CASCADE; these do not substitute host validation of the new Windows RBZ. FreeCAD 1.1 is the metadata target. macOS/Linux/SketchUp Web are not supported by the current executable-selection workflow.

Build and test with `python tools/build_release.py`, `python -m unittest discover -s tests -v` and `ruby tests/test_cleanup.rb`. Detailed limits and checks are in the Portuguese guides. No private commercial CAD files are distributed.

Copyright © 2026 Yruam Kaffer de Faria. PolyForm Noncommercial License 1.0.0. Independent project, not affiliated with FreeCAD, SketchUp or Trimble.
