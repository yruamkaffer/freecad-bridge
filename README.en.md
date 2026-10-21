# FreeCAD Bridge

**STEP to SketchUp, with named components, colors and solid checks.**

By **Yruam Kaffer de Faria** · Version **0.4.1** · Target: **Windows / SketchUp 2026 desktop**

[Português — full documentation](README.md)

FreeCAD Bridge uses an installed FreeCAD command-line executable to convert STEP files in the background. It creates a component per solid, attempts geometry repair, removes coplanar subdivisions with matching materials and checks the final components with SketchUp solid detection.

## New in 0.4.1

Linear deflection now accepts **0.001 to 100 mm**, keeping the **0.05 mm** default. Larger values allow coarser approximations for large models, but may reduce detail and change the outline. Angular settings also affect tessellation. This range change does not repair geometry or replace edge smoothing.

## Toolbar — introduced in 0.4.0

A dockable/floating toolbar with five actions: STEP import, JSON import, FreeCADCmd setup, diagnostics and project information. Commands are shared with the Extensions menu. Import actions are disabled while a background conversion is running. The native toolbar API restores its previous location and visibility.

![Toolbar icons and actions](docs/assets/barra_ferramentas.png)

This is an icon guide, not a screenshot of SketchUp. Use **Extensions → FreeCAD Bridge → Mostrar barra de ferramentas** to show a hidden toolbar. See the [toolbar guide](docs/BARRA_DE_FERRAMENTAS.md).

This is a UI-only update based on 0.3.0. Conversion and geometry reconstruction are unchanged; previous model-specific import issues remain possible. Private diagnostic builds are not included.

## Install

1. Install FreeCAD and locate `FreeCADCmd.exe`.
2. Download [FreeCAD_Bridge_0.4.1.rbz](dist/FreeCAD_Bridge_0.4.1.rbz).
3. Install through SketchUp Extension Manager and restart SketchUp.
4. Open **Extensions → FreeCAD Bridge → Configurar FreeCADCmd** and select the executable.
5. Choose **Importar STEP automaticamente**, select a STEP file and start with `0.05 mm` linear deflection.

The package is unsigned. Consult SketchUp loading policy settings if blocked. The interface and detailed documentation are currently in Portuguese.

## Behavior

**Estrito** requires valid CAD, a closed converted mesh and a solid final SketchUp component; failure blocks or rolls back the whole import. **Visualização** allows problematic geometry with warnings. The report includes STEP indices, names, status, Locate and text export.

Names and RGB colors are transferred when present and safely matched. Per-face colors require matching triangles and may be incomplete after repair or alternate tessellation. Curves become polygonal geometry. CAD features, parameters, textures, transparency and physical materials are not transferred. Assemblies become positioned components inside a group; hierarchy and shared definitions are not preserved.

The previous workflow was used by the author. Core logic passed isolated checks. The toolbar passed syntax/resource/package checks; behavior and placement restoration in SketchUp still need host validation. FreeCAD 1.1 is the metadata target, with no certified version matrix. The current workflow does not support macOS, Linux or SketchUp Web.

## Example

Import [the synthetic red tetrahedron](examples/tetraedro_vermelho.json) with the JSON icon to check the JSON path, 10 mm dimensions, color and report without FreeCAD conversion.

## Development

```sh
python tools/build_release.py
python -m unittest discover -s tests -v
```

See [architecture](docs/ARQUITETURA.md), [JSON format](docs/FORMATO_JSON.md) and [contribution guidelines](CONTRIBUTING.md). Offline tests do not verify either host application.

## License

Copyright © 2026 Yruam Kaffer de Faria. **PolyForm Noncommercial License 1.0.0**: public source with noncommercial permissions under the full [terms](LICENSE.txt), not unrestricted commercial use. The holder may grant separate permissions. FreeCAD and SketchUp are external dependencies; this project is not affiliated with or certified by their vendors.
