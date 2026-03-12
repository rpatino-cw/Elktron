# `2d_drawing` Rules

Create a 2D blueprint that matches the reference image as exactly as possible.

## Rules
- Do not simplify geometry.
- Do not guess missing features.
- Preserve true outer contours, holes, slots, cutouts, curves, angles, and proportions.
- If a feature is circular, draw it circular.
- Do not make all holes or slots the same unless the image clearly shows that.
- Trace brackets and complex edges faithfully.
- Use symmetry only where clearly supported by the image.

## Workflow
1. Inspect the image.
2. Trace the 2D geometry faithfully.
3. Save the first blueprint draft in `2d_drawing`.
4. Stop and wait for user approval.
5. Do not create any 3D file until the user explicitly approves the 2D drawing.

## If exact tracing is not possible
Ask questions first. Do not guess.

Examples:
- Can you provide a clearer image?
- Can you provide dimensions or a known scale?
- Should unclear holes/slots be omitted or estimated?
- Is this for exact CAD, CNC, or laser cutting?

## Hard stop
No final 3D file before:
1. the 2D draft is created in `2d_drawing`
2. the user approves it
