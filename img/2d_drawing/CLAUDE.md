# Photo-to-3D Pipeline — Canonical Reference

## The Pipeline (6 Stages)

```
[Photo(s)] → 1.TRACE (user, per view) → JSON line data per view
              ↓ APPROVAL
           → 2.ANALYZE (Claude, per view) → annotated 2D canvas per view
              ↓ APPROVAL
           → 3.MERGE (Claude) → unified mm dimensions + multi-view blueprint
              ↓ APPROVAL
           → 4.ASCII 3D PREVIEW (Claude) → isometric ASCII wireframe HTML
              ↓ APPROVAL
           → 5.3D MODEL (Claude) → Three.js interactive model
              ↓ APPROVAL
           → 6.ASSEMBLY PAGE (Claude) → build guide with all 3D parts
```

Each stage has a **user approval gate** before advancing.

---

## Stage 1: TRACE (User)

- **Tool:** `~/dev/tracer/index.html` — generic photo-to-outline tracer
- **Input:** Reference photo(s) — one per view (top-down, side, front, etc.)
- **Output:** JSON array of line segments with endpoints + optional bend control points, **one per view**
- **What user does:** Load image, drag red endpoint handles to trace edges, drag blue handles to bend curves, export JSON
- **Multi-view:** Trace each orthographic view separately. Minimum: 1 view. Ideal: 3 views (top, side, front) for full 3D coverage.
- **Approval gate:** User reviews traced lines against each photo, confirms accuracy

## Stage 2: ANALYZE (Claude)

- **Tool:** HTML canvas page (Claude builds it)
- **Input:** JSON line data from Stage 1 + original reference photo, **one per view**
- **Output:** Annotated 2D canvas — lines remapped to a clean canvas with labels, measurements, region classification. **One HTML file per view.**
- **What Claude builds:** A DPR-scaled canvas with grid, toggle controls, sidebar panels (Measurements, Regions, Line Data), dimension lines with arrows, and region hover highlighting
- **Reference implementations:**
  - `chassis_topdown_frame_analysis.html` (top-down — 51 lines, 10 regions)
  - `chassis_side_frame_analysis.html` (side view — 14 lines, 6 regions)
  - `chassis_front_frame_analysis.html` (front view — 11 lines, 5 regions)
- **Required style:** Space Grotesk + JetBrains Mono, `#0a0a0c` bg, amber `#c9943a` accents, grid layout (canvas + 380px sidebar), `.panel` cards with `.stat-row` measurements, `.region-item` hover highlight, `.ctrl-btn` toggles, dimension arrows with dashed extension lines
- **Required panels:** Geometry Measurements, Identified Regions (with color dots + hover), Orientation/Context notes, Line Data summary
- **Required toggles:** Grid, Numbers, Regions, Dimensions, Zones (minimum)
- **Approval gate:** User confirms annotations are correct and complete **for each view**

## Stage 3: MERGE (Claude) — CRITICAL STEP

> This stage replaces the old Proportion Table (2.5) and 2D Component Diagram (3). It combines all views into unified dimensional data before any 3D work begins.

- **Input:** All approved Stage 2 analyses (one per view) + their raw trace line data
- **Output:** Two things:
  1. **Unified Dimension Table** — every component with X, Y, Z measurements in mm, sourced from real pixel data across views
  2. **Multi-View Blueprint HTML** — engineering-drawing-style page with top/side/front on one canvas, shared dimension lines, component labels

### Process

1. **Collect** all approved Stage 2 analyses
2. **Pick reference dimension** per view — longest clearly measurable line, assign known mm value
3. **Compute px→mm** per view (each photo has different scale/perspective)
4. **Map axes across views:**
   - Top-down X = Side X (length along chassis)
   - Top-down Y = Front X (width of chassis)
   - Side Y = Front Y = Z (height)
5. **Cross-reference** — same component measured in multiple views must agree within tolerance
6. **Resolve conflicts** — if views disagree, note it and ask user
7. **Output unified dimension table** — every component: name, X position, Y position, Z position, width, depth, height (all in mm)
8. **Output multi-view blueprint HTML** — engineering drawing with top/side/front views, shared dimension lines

### Hard rules

- NO Stage 4 until this table is approved
- Every traced line from every view must appear in the table
- Z-heights MUST come from side/front view data, NOT guessed
- Cross-view disagreements flagged for user resolution
- All positions computed from pixel data, not estimated

- **Output path:** `~/hackathon/2d_manual_3d/{component}_merged_blueprint.html`
- **Approval gate:** User confirms all mm values, component groupings, and cross-view consistency

---

## Stage 4: ASCII 3D PREVIEW (Claude)

- **Tool:** HTML page with `<pre>` block (Claude builds it)
- **Input:** Approved Stage 3 MERGE (unified dimension table)
- **Output:** Isometric ASCII wireframe of all components — monospace `<pre>` tag
- **What Claude builds:** Single HTML file with ~150 LOC JS inline ASCII renderer. Isometric projection, Bresenham line algo, box-drawing characters. Controls: rotate (4 angles), view toggle, label toggle, zoom.
- **Style:** Same design system — Space Grotesk + JetBrains Mono, `#0a0a0c` bg, `#c9943a` accents
- **Purpose:** Lightweight 3D validation before investing in Three.js. Catches proportion/position errors early.
- **No external dependencies.** Zero npm, zero cloning.
- **Key difference from old pipeline:** All Z-heights now come from real traced side/front data via Stage 3, not guessed.
- **Output path:** `~/hackathon/2d_manual_3d/{component}_ascii3d.html`
- **Approval gate:** User confirms 3D interpretation looks correct before proceeding to Stage 5

## Stage 5: 3D MODEL (Claude)

- **Tool:** Three.js v0.170.0 (Claude builds it)
- **Input:** Approved ASCII preview from Stage 4 + Stage 3 unified dimension table
- **Output:** Interactive 3D model — rotate, zoom, labeled parts
- **What Claude builds:** A Three.js page with inline geometry (no external model files), OrbitControls, labeled meshes matching the dimension table exactly
- **Reference implementation:** `~/playground/raspberry-pi-5/index.html`
- **Requirements:**
  - Three.js v0.170.0 via CDN importmap
  - Inline geometry only — all shapes built in code
  - OrbitControls for camera interaction
  - Part labels visible on hover or always-on
  - All dimensions sourced from Stage 3 table — no guessing
- **Output path:** `~/hackathon/3d-reference/{component}_3d_model.html`
- **Approval gate:** User confirms 3D model matches the real component

## Stage 6: ASSEMBLY PAGE (Claude)

- **Tool:** Three.js + `design-system.css` (Claude builds it)
- **Input:** Approved 3D models from Stage 5 (one or more components)
- **Output:** Interactive build guide — step-by-step assembly with 3D models at each step
- **What Claude builds:** A multi-step assembly page where each step shows the relevant 3D parts, exploded views, wiring connections, and written instructions
- **Reference implementation:** `~/hackathon/escort-bot/assembly.html`
- **Requirements:**
  - Uses `design-system.css` for consistent styling with other hackathon pages
  - Step navigation (prev/next)
  - 3D models embedded per step
  - Exploded view toggle where applicable
- **Output path:** `~/hackathon/escort-bot/{component}_assembly.html`
- **Approval gate:** User confirms the assembly sequence is correct and buildable

---

## Rules

- **Do not simplify geometry.** Trace what you see, not what you think it should be.
- **Do not guess missing features.** If something is unclear, ask.
- **Do not guess Z-heights.** They MUST come from side/front view trace data.
- **Preserve true outer contours, holes, slots, cutouts, curves, angles, and proportions.**
- **If a feature is circular, draw it circular.** Do not approximate.
- **Do not make all holes or slots the same** unless the image clearly shows that.
- **Trace brackets and complex edges faithfully.**
- **Use symmetry only where clearly supported by the image.**

## Hard Stops

1. **No skipping stages.** Every component goes through all 6 stages in order.
2. **No ASCII preview before approved MERGE.** Stage 4 requires Stage 3 approval.
3. **No 3D model before approved ASCII preview.** Stage 5 requires Stage 4 approval.
4. **No assembly page before approved 3D model.** Stage 6 requires Stage 5 approval.
5. **No Z-heights from imagination.** Every height value must trace back to a side or front view pixel measurement.
6. **If exact tracing is not possible,** ask questions first:
   - Can you provide a clearer image?
   - Can you provide dimensions or a known scale?
   - Should unclear holes/slots be omitted or estimated?
   - Is this for exact CAD, CNC, or laser cutting?

---

## File Naming Convention

| Stage | Pattern | Example |
|-------|---------|---------|
| 1 | `{component}_{view}_trace.json` | `chassis_topdown_trace.json` |
| 2 | `{component}_{view}_frame_analysis.html` | `chassis_side_frame_analysis.html` |
| 3 | `{component}_merged_blueprint.html` | `chassis_merged_blueprint.html` |
| 4 | `{component}_ascii3d.html` | `chassis_ascii3d.html` |
| 5 | `{component}_3d_model.html` | `chassis_3d_model.html` |
| 6 | `{component}_assembly.html` | `chassis_assembly.html` |

## Pipeline Folder Map

| Stage | Working Directory |
|-------|-------------------|
| 1 (Trace) | User's tracer tool — output JSON goes to `hackathon/img/2d_drawing/` |
| 2 (Analyze) | `hackathon/img/2d_drawing/` |
| 3 (Merge) | `hackathon/2d_manual_3d/` |
| 4 (ASCII Preview) | `hackathon/2d_manual_3d/` |
| 5 (3D Model) | `hackathon/3d-reference/` |
| 6 (Assembly) | `hackathon/escort-bot/` or component-appropriate location |

---

## Files in This Folder

| File | Stage | What |
|------|-------|------|
| `CLAUDE.md` | — | This file — canonical pipeline reference |
| `frame_trace.html` | 2 | Frame tracing tool (canvas-based) |
| `chassis_topdown_frame_analysis.html` | 2 | Top-down view analysis (51 lines, 10 regions) |
| `chassis_side_frame_analysis.html` | 2 | Side view analysis (14 lines, 6 regions) |
| `chassis_front_frame_analysis.html` | 2 | Front view analysis (11 lines, 5 regions) |
| `chassis_frame_traced.html` | 2 | Original top-down analysis (22 lines, superseded) |
| `2d_car_reference.png` | 1 | Car reference image for tracing |
| `rc_chassis_frame_lines.png` | 1 | Traced frame lines output |
