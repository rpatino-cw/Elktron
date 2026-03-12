# Hackathon Reference Images — Asset Library

## What This Folder Is

This is the central image and document library for the Elktron hackathon project. It contains reference photos, product listings, technical diagrams, and measurement images used during the design and planning phase of the Escort Bot chassis. These files are NOT code — they are visual references that inform hardware decisions, 3D modeling, wiring, and assembly.

When working in this folder, you are typically doing one of: analyzing a reference image to extract measurements, creating a 2D drawing from a photo, identifying parts or features in an image, or organizing assets for the build team.

## Folder Structure

```
img/
├── CLAUDE.md                  # THIS FILE — asset manifest and context
├── 2d_drawing/                # Subfolder for 2D line blueprints (has its own CLAUDE.md)
│   └── CLAUDE.md              # Workflow rules: trace reference → 2D draft → approval → 3D
│
├── ── CHASSIS REFERENCE PHOTOS ──────────────────────────
├── car_all_sides_view.jpg     # Multi-angle view of the 4WD chassis (top, bottom, sides)
├── car_measurements.jpg       # Chassis with dimension callouts — critical for 3D modeling
├── car_parts.jpg              # Exploded/disassembled view showing individual components
├── car_wire_diagram.jpg       # Wiring diagram for motor connections
├── car_battery.jpg            # Battery compartment / holder placement
├── frame_overall_view.jpg     # Acrylic frame top-down view — shows hole patterns and slots
│
├── ── AMAZON PRODUCT PHOTOS ─────────────────────────────
├── car_1.jpg                  # LK-COKOINO 4WD chassis — Amazon listing photo angle 1
├── car_2.jpg                  # Listing photo angle 2
├── car3.jpg                   # Listing photo angle 3
├── car4.jpg                   # Listing photo angle 4
├── car_5.jpg                  # Listing photo angle 5
├── car_6.jpg                  # Listing photo angle 6
├── Car_9.jpg                  # Listing photo angle 9
├── car_ad.jpg                 # Amazon advertising banner image
├── 2b5f086c-a837-4262-ac8a-  # Amazon CDN product image (UUID filename from download)
│   728979f34a27.__CR0,0,...   #   → This is a cropped banner from the listing page
│
├── ── PRODUCT DOCUMENTATION (PDFs) ──────────────────────
├── amazon_car.pdf             # Full Amazon product listing page — saved as PDF
│                              #   LK-COKOINO 4WD Robot Car Chassis Kit
│                              #   Contains: specs, features, included parts, dimensions
├── amazon_car_comments.pdf    # Amazon customer reviews/comments — saved as PDF
│                              #   Useful for: common issues, assembly tips, compatibility notes
├── 4WD Robot Car chassis      # Cokoino official product documentation PDF
│   Kit – Cokoino.pdf          #   Contains: specs, assembly overview, part list
│
├── ── 2D REFERENCES ─────────────────────────────────────
├── 2d_car                     # 2D reference image (NO FILE EXTENSION — likely .jpg or .png)
│                              #   Needs to be renamed with proper extension
│
├── ── OTHER HARDWARE ────────────────────────────────────
├── cable-net.png              # Cable management / network cable reference image
│                              #   Related to rack scanning feature of the escort bot
├── raspberry pi above vew.jpg # Raspberry Pi board — top-down photo (overhead angle)
│                              #   Reference for Pi 5 placement on chassis
└── .DS_Store                  # macOS metadata (ignore)
```

## Image Categories

### Category 1: Chassis Technical References (USE THESE FOR MODELING)
These are the most important images in the folder — they contain real measurements, hole patterns, and component layouts needed for accurate 3D modeling or 2D drawing.

| File | What It Shows | Use For |
|------|---------------|---------|
| `car_measurements.jpg` | Chassis with labeled dimensions | Extracting exact measurements for CAD/3D |
| `car_all_sides_view.jpg` | Multi-angle chassis views | Understanding 3D proportions |
| `car_parts.jpg` | Disassembled component layout | Identifying individual parts for BOM |
| `car_wire_diagram.jpg` | Motor wiring schematic | Verifying wiring against `escort-bot/WIRING.md` |
| `car_battery.jpg` | Battery holder placement | Planning power layout on chassis |
| `frame_overall_view.jpg` | Top-down acrylic frame | Hole patterns, mounting points, slot positions |

### Category 2: Amazon Product Photos (VISUAL REFERENCE ONLY)
Marketing photos from the Amazon listing. Useful for overall appearance and assembled state, but do not rely on these for measurements — they are promotional, not technical.

Files: `car_1.jpg` through `Car_9.jpg`, `car_ad.jpg`, the UUID-named `.jpg`

### Category 3: Documentation PDFs
- `amazon_car.pdf` — The full product listing. Contains specs, dimensions, and included parts list. Read this first when you need to know what ships in the box.
- `amazon_car_comments.pdf` — Customer reviews. Contains assembly tips, known issues, compatibility warnings from real users.
- `4WD Robot Car chassis Kit – Cokoino.pdf` — Official Cokoino documentation. More detailed specs than the Amazon listing.

### Category 4: Non-Chassis Hardware
- `cable-net.png` — Network cable / cable management reference. Relates to the rack scanning feature.
- `raspberry pi above vew.jpg` — Pi board photo. Used for planning where the Pi mounts on the chassis.

## Known Issues

1. **`2d_car` has no file extension.** This file should be renamed to `2d_car.jpg` or `2d_car.png` depending on its actual format. Run `file 2d_car` to detect the format, then rename.

2. **UUID filename is not human-readable.** The file `2b5f086c-a837-4262-ac8a-728979f34a27.__CR0,0,970,300_PT0_SX970_V1___.jpg` is an Amazon CDN URL artifact. Consider renaming to `amazon_banner_crop.jpg`.

3. **Inconsistent naming.** Some files use underscores (`car_1.jpg`), some don't (`car3.jpg`). One uses title case (`Car_9.jpg`). Not critical but worth normalizing if doing a cleanup pass.

4. **`raspberry pi above vew.jpg` has a typo** — "vew" should be "view". Consider renaming to `raspberry_pi_top_view.jpg`.

5. **No subdirectories for categories.** As the folder grows, consider splitting into `chassis/`, `product-photos/`, `docs/`, `other-hardware/`.

## Relationship to Other Folders

- **`../CKK0011-main/`** — The official Cokoino repo with assembly tutorials and driver code. The PDFs here are the Amazon-side documentation; CKK0011-main has the manufacturer-side tutorials.
- **`../escort-bot/`** — The software that runs on the built chassis. `WIRING.md` there should match `car_wire_diagram.jpg` here.
- **`2d_drawing/`** — Subfolder for creating 2D line blueprints traced from these reference images. Has its own CLAUDE.md with a strict workflow: trace → draft → approval → 3D.

## Rules for Working in This Folder

1. **Do not delete original reference images.** Even if duplicates exist, keep originals until the build is complete.
2. **New images should use descriptive names** — `chassis_bottom_view.jpg`, not `IMG_4521.jpg`.
3. **PDFs are read-only references.** Do not modify them.
4. **2D drawings go in `2d_drawing/`.** Follow the CLAUDE.md workflow there.
5. **When analyzing an image for measurements**, state your confidence level. If the image is unclear, ask for a clearer photo or manual measurement before committing to dimensions.
