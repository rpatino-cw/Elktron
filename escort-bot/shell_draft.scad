// ============================================
// ESCORT BOT — SIDE PANEL ONLY
// ============================================
// Measured by Romeo 2026-03-19:
//   Tire diameter: 2.5" (63.5mm)
//   Gap between front & rear tires: 2.5" (63.5mm)
// ============================================

// --- MEASUREMENTS ---
wheel_d    = 63.5;     // 2.5" tire diameter
tire_gap   = 69.85;    // 2-3/4" gap between front & rear tires
wheel_r    = 76.2 / 2;         // 3" wide arches (38.1mm radius)

// --- SIDE PANEL DIMS ---
panel_h    = 127;      // 5" tall (to outside edge of ceiling)
wall       = 2.5;      // wall thickness
wheel_arch_h = 40;     // arch cutout height from bottom
panel_gap  = 114.3;    // 4.5" between the two side panels

// Panel length = front arch + gap + rear arch
// Axle-to-axle = tire_gap + wheel_d = 127mm
// Panel extends a bit past each wheel center
wx = (tire_gap + wheel_d) / 2;  // 63.5mm — wheel center from midpoint
panel_l    = wx * 2 + wheel_r * 2 + 10;  // total length with some margin

// --- BUILD ---
frame_head = 28.575;   // 1-1/8" — front arch stops here (frame head height)

module side_panel() {
    difference() {
        // Flat panel
        translate([-panel_l/2, 0, 0])
            cube([panel_l, wall, panel_h]);

        // Front wheel arch
        translate([wx, wall + 0.1, 0])
            rotate([90, 0, 0])
                cylinder(r=wheel_r, h=wall + 0.2, $fn=48);

        // Rear wheel arch
        translate([-wx, wall + 0.1, 0])
            rotate([90, 0, 0])
                cylinder(r=wheel_r, h=wall + 0.2, $fn=48);

        // Trim 1" from back end (length only, full height)
        translate([-panel_l/2 - 0.1, -0.1, -0.1])
            cube([25.4, wall + 0.2, panel_h + 0.2]);

    }
}

// Left panel
color("#2a2a2a")
    translate([0, panel_gap/2, 0])
        side_panel();

// Right panel (mirrored)
color("#2a2a2a")
    translate([0, -panel_gap/2 - wall, 0])
        side_panel();

// Ceiling — shortened 1" at back to match side panels
color("#333")
    translate([-panel_l/2 + 25.4, -panel_gap/2 - wall, panel_h - wall])
        cube([panel_l - 25.4, panel_gap + wall * 2, wall]);

// Back panel — moved forward 1", bottom fine-tuned
color("#2a2a2a")
    translate([-panel_l/2 + 25.4, -panel_gap/2 - wall, wheel_r - 4.0])
        cube([wall, panel_gap + wall * 2, panel_h - (wheel_r - 4.0)]);


// Front panel wall
color("#2a2a2a")
    translate([panel_l/2 - wall, -panel_gap/2 - wall, 0])
        cube([wall, panel_gap + wall * 2, panel_h]);

echo(str("Panel length: ", panel_l, " mm"));
echo(str("Panel height: ", panel_h, " mm"));
echo(str("Panel gap: ", panel_gap, " mm (4.5\")"));
echo(str("Wheel arch radius: ", wheel_r, " mm"));
echo(str("Axle-to-axle: ", tire_gap + wheel_d, " mm"));
