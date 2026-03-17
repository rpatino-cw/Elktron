# img/ — Active Image Assets

## What This Folder Is

This folder contains **only images that are actively referenced** by HTML pages or README.md. All other reference images, product photos, PDFs, and documentation have been moved to `../reference/`.

## Current Contents

| File | Referenced By | Purpose |
|------|--------------|---------|
| `car_1.jpg` | `robotics-site/index.html` (CSS background-image) | Chassis photo for landing page |
| `car_all_sides_view.jpg` | `robotics-site/index.html` | Multi-angle chassis view |
| `car_parts.jpg` | `robotics-site/index.html` | Disassembled parts layout |
| `frame_overall_view.jpg` | `robotics-site/index.html` | Acrylic frame top-down |
| `escort-bot-render.png` | `README.md` | Clean 3D render of escort bot |

## Subdirectory

### `2d_drawing/`
Blueprint workspace with its own `CLAUDE.md`. Contains `frame_trace.html` (canvas tool) and traced reference images. Do not move — `frame_trace.html` uses relative paths to images in this folder.

## Rules

1. **Only actively-referenced images belong here.** If an image isn't in an `src=`, `href=`, or `url()` attribute somewhere, it goes in `../reference/`.
2. **Reference material** (product photos, PDFs, measurements, Amazon listings) lives in `../reference/`.
3. **New images** should be added here only if they'll be referenced by an HTML page or README.
