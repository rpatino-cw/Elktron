# 2D Manual to 3D — Conversion Workspace (Stage 3-4)

> **This folder is the Stage 3-4 workspace** of the Photo-to-3D Pipeline. Full pipeline docs: `../img/2d_drawing/CLAUDE.md`

## What This Folder Is

This is the working directory for the manual 2D-to-3D conversion pipeline in the Elktron hackathon project. When a 2D blueprint (created in `../img/2d_drawing/`) is approved, the conversion work — tracing outlines into 3D geometry, extruding profiles, adding mounting features — happens here. This folder holds intermediate working files, conversion scripts, and in-progress 3D models before they are finalized and moved to `../3d-reference/`.

Think of this as the workshop bench. `../img/2d_drawing/` is where you draft the blueprint. This folder is where you turn that flat drawing into a 3D object. `../3d-reference/` is where the finished model lives.

## Current Status

**This folder is currently empty.** It will be populated when:
1. A 2D blueprint in `../img/2d_drawing/` is approved by the user
2. The conversion process from 2D to 3D begins

The first likely use case is converting the chassis frame blueprint into a 3D model for planning the mast mount position, camera placement, and Pi mounting on the LK-COKOINO 4WD chassis.

## The 2D → 3D Pipeline

```
Step 1: Reference Image (../img/)
  │  Photo of chassis, part, or component
  │
  ▼
Step 2: 2D Blueprint (../img/2d_drawing/)
  │  Clean line drawing traced from reference
  │  MUST be approved before proceeding
  │  See ../img/2d_drawing/CLAUDE.md for workflow rules
  │
  ▼
Step 3: Conversion Work (THIS FOLDER — 2d_manual_3d/)
  │  Working files: traced outlines, extrusion profiles
  │  Scripts: OpenSCAD, Blender Python, or FreeCAD macros
  │  In-progress 3D models being refined
  │
  ▼
Step 4: Finished 3D Model (../3d-reference/)
  │  Final STL, OBJ, GLB, or STEP file
  │  Ready for 3D printing, simulation, or Blender import
```

## Approval Gate — CRITICAL

**Do NOT start 3D conversion work without an approved 2D blueprint.** The approval gate exists in `../img/2d_drawing/CLAUDE.md` and requires:
1. A clean 2D line drawing exists in `../img/2d_drawing/`
2. The user has explicitly approved it

This prevents wasted effort converting inaccurate geometry into 3D. If the 2D drawing is wrong, the 3D model will be wrong — and 3D mistakes are harder to catch and more expensive to fix (especially if 3D printed).

## Expected File Types

### Input Files (from 2d_drawing/)
- `.svg` — Vector line drawings (preferred for conversion — scalable, clean geometry)
- `.dxf` — CAD interchange format (if exported from a drawing tool)
- `.png` / `.jpg` — Raster blueprints (less ideal but workable with tracing)

### Working Files (created in this folder)
- `.scad` — OpenSCAD scripts that programmatically build 3D geometry from 2D profiles
- `.py` — Blender Python scripts that automate extrusion, filleting, or assembly
- `.FCStd` — FreeCAD project files (if using FreeCAD for conversion)
- `.blend` — Blender working files (keep these here, not in `../robotics-site/`)
- `.svg` with annotations — Marked-up 2D drawings showing extrusion depths, fillet radii, etc.

### Output Files (moved to ../3d-reference/ when done)
- `.stl` — For 3D printing
- `.obj` — General interchange
- `.glb` — For web viewers and simulations
- `.step` — For CAD interchange

## Conversion Methods

### Method 1: Blender (Manual)
1. Import 2D blueprint as background image
2. Trace outline with mesh or curve tools
3. Extrude to correct thickness
4. Add holes, slots, mounting features
5. Export to STL/OBJ/GLB

### Method 2: Blender Python (Semi-Automated)
1. Write a `.py` script that creates geometry programmatically
2. Define dimensions from the approved 2D drawing
3. Run script in Blender to generate the model
4. Allows easy iteration when dimensions change

The Blender MCP server is available (`mcp__blender__execute_blender_code`) and can run Python code directly in a connected Blender instance. This is the fastest path for iterating on 3D geometry.

### Method 3: OpenSCAD (Fully Parametric)
1. Write a `.scad` file defining the 2D profile with `polygon()`
2. Extrude with `linear_extrude()`
3. Add holes with `difference()` and `cylinder()`
4. Export to STL
5. Best for parts with precise dimensions and regular geometry

### Method 4: FreeCAD (CAD-Native)
1. Import DXF from 2D drawing
2. Pad/extrude profiles
3. Add features (pockets, fillets, chamfers)
4. Export to STEP/STL

## Naming Convention

Working files in this folder use the pattern:

```
{component}_{stage}_{version}.{ext}

Stages:
  outline  — 2D profile extraction
  extruded — First 3D extrusion
  featured — Holes, slots, mounts added
  final    — Ready to move to ../3d-reference/

Examples:
  chassis_frame_outline_v1.svg
  chassis_frame_extruded_v1.blend
  chassis_frame_featured_v2.blend
  chassis_frame_final_v2.stl      → move to ../3d-reference/
  mast_mount_outline_v1.scad
  mast_mount_final_v1.stl         → move to ../3d-reference/
```

## Likely First Projects

Based on the current Elktron hardware plan:

1. **Chassis frame** — The LK-COKOINO acrylic frame. Reference images in `../img/` (especially `car_measurements.jpg`, `frame_overall_view.jpg`, `car_all_sides_view.jpg`). A 3D model helps plan where to drill/mount the PVC mast, Pi, motor driver, and battery pack.

2. **Mast mount** — The PVC pipe (1" Schedule 40, ~4 ft) that raises the camera. A 3D model of the T-connector + chassis attachment helps verify clearance and stability.

3. **Camera mount** — The Arducam pan/tilt platform sits on top of the mast. Modeling this verifies the camera's field of view at rack height.

4. **Custom end effector** (SO-101 arm) — If the stock gripper doesn't work for optic seating, a custom 3D-printed end effector would be designed here.

## Rules

1. **Never skip the 2D approval gate.** No 3D conversion without an approved 2D blueprint.
2. **Keep working files here, finished files in `../3d-reference/`.** This folder is a workspace, not an archive.
3. **Version everything.** Use `_v1`, `_v2` suffixes. Do not overwrite previous versions.
4. **Document dimensions.** When creating extrusion profiles, note where each dimension came from (which reference image, which measurement).
5. **If measurements are uncertain**, flag them. Use a comment like `// TODO: verify this dimension from car_measurements.jpg` in scripts.
6. **Clean up after completion.** Once a final model is in `../3d-reference/`, working files here can be archived or deleted (user's choice).
