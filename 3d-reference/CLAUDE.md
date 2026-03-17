# 3D Reference — Model References and 3D Assets

## What This Folder Is

This folder is designated for storing 3D reference files used in the Elktron hackathon project. These include STL files, OBJ exports, STEP files, Blender exports, or any 3D model references that inform the physical design of the two robots (SO-101 Arm and Escort Bot).

## Three.js Page in This Folder

| File | Three.js Ver | What It Renders |
|------|-------------|-----------------|
| `pi5-3d-model.html` | v0.162.0 | Interactive 3D model of Raspberry Pi 5 board, components labeled |

**Full 3D map:** See `../CLAUDE.md` → "Three.js / 3D Websites — Complete Map" for all 11 Three.js pages.

## Current Status

**This folder is mostly empty (besides the Pi 5 3D model page).** It was created as a placeholder during the project setup phase. As the hackathon progresses (hardware arriving March 11–18, 2026), this folder will be populated with:

- **Chassis 3D models** — If the LK-COKOINO chassis frame is modeled in Blender or CAD for planning the mast mount, camera placement, and Pi mounting position
- **Mast assembly models** — The escort bot mast (PVC pipe + T-connector + camera mount) may need a 3D reference for fabrication
- **SO-101 arm references** — The HiWonder SO-ARM101 kit ships with STL files for 3D-printed parts. If any custom end effectors or mounts are designed, they go here
- **Rack mock-up models** — If a simplified 42U rack model is created for simulation or demo purposes
- **Blender scene exports** — The main Blender file lives at `../robotics-site/elktron-robots.blend`, but any exported assets (GLB, OBJ, STL) intended for reuse should be copied here

## Relationship to Other Folders

| Related Folder | What It Has | How It Connects |
|----------------|-------------|-----------------|
| `../img/` | 2D reference photos (chassis measurements, wiring, parts) | 2D references are traced into drawings in `../img/2d_drawing/`, which may then inform 3D models stored here |
| `../img/2d_drawing/` | 2D line blueprints created from reference images | The 2D → 3D pipeline: reference photo → 2D drawing (approval gate) → 3D model here |
| `../robotics-site/` | `elktron-robots.blend` — main Blender project file | Scene-level 3D assets live in the Blender file; exportable standalone assets go here |
| `../2d_manual_3d/` | Manual 2D-to-3D conversion workspace | Working files during the conversion process; finished 3D output moves here |
| `../escort-bot/Soldier.glb` | GLB model used in the escort bot simulation | Simulation-specific models stay with their HTML files; general-purpose 3D refs go here |

## Intended Workflow

1. **Reference images** are collected in `../img/` (photos, PDFs, Amazon listings)
2. **2D blueprints** are traced from those images in `../img/2d_drawing/` following its CLAUDE.md workflow (trace → draft → approval)
3. **3D models** are created from approved 2D blueprints and placed here
4. **Blender scenes** may import models from here into the main `.blend` file

This folder is downstream of the 2D drawing approval gate. Do not create 3D models here without an approved 2D blueprint unless the model is being imported from an external source (vendor STL, downloaded asset, etc.).

## File Naming Convention

When files are added, use this naming pattern:

```
{component}_{description}_{version}.{ext}

Examples:
  chassis_frame_v1.stl
  mast_assembly_v2.obj
  so101_custom_gripper_v1.stl
  rack_mockup_42u.glb
  camera_mount_pantilt_v1.step
```

## Supported Formats

| Format | Use Case |
|--------|----------|
| `.stl` | 3D printing (SO-101 parts, custom mounts) |
| `.obj` | General interchange, Blender import |
| `.glb` / `.gltf` | Web viewers, Three.js simulations |
| `.step` / `.stp` | CAD interchange (if using Fusion 360 or FreeCAD) |
| `.blend` | Blender native (prefer keeping main scene in `../robotics-site/`) |
| `.fbx` | Animation interchange (if needed) |

## This Folder Is Stage 4 of the Photo-to-3D Pipeline

| Stage | Name | Folder |
|-------|------|--------|
| 1 | Trace | `~/dev/tracer/index.html` |
| 2 | Frame Analysis | `../img/2d_drawing/` |
| 3 | 2D Diagram | `../2d_manual_3d/` |
| **4** | **3D Model** | **This folder** |
| 5 | Assembly Page | `../escort-bot/assembly.html` (and similar) |

Three.js requirements for Stage 4 output:
- **Version:** v0.170.0 via CDN importmap
- **Geometry:** Inline only — all shapes built in code, no external model files
- **Controls:** OrbitControls for camera interaction
- **Labels:** Part labels visible on hover or always-on

Full pipeline docs: `../img/2d_drawing/CLAUDE.md`

## Rules

1. **Do not store working/draft files here** — only completed or reference-quality models
2. **Version your files** — use `_v1`, `_v2` suffixes rather than overwriting
3. **Include a comment in commit messages** describing what the model represents and its source (hand-modeled, vendor-provided, exported from Blender, etc.)
4. **Large files (>50MB)** should be tracked via Git LFS if this repo uses it, or noted in this CLAUDE.md with a download link
5. **Vendor-provided STLs** (like HiWonder SO-101 parts) should be kept unmodified in a `vendor/` subfolder to distinguish them from custom designs
