// ============================================
// ESCORT BOT SHELL — Clean Minimal Box v4
// ============================================
// MEASURED by Romeo 2026-03-19:
//   Total width (tire-to-tire): 6" (152.4mm)
//   Tire width: 1" (25.4mm) each
//   Tire diameter: 2.5" (63.5mm)
//   Gap between front & rear tires: 2-3/8" (60.3mm)
//   Chassis length: 10" (254mm, Amazon confirmed)
// Mounting: L-brackets at 4 corners
//
// F5 = preview | F6 = render | File > Export STL
// Print: 0.2mm layer, 15% infill, no supports
// ============================================

// --- DIMENSIONS (mm) — REAL MEASUREMENTS ---
chassis_l  = 254;      // 10" front-to-back (Amazon confirmed)
chassis_w  = 100;      // frame body width (152mm tire-to-tire - 2x25.4mm tires = 101.2mm - clearance)
wheel_d    = 63.5;     // 2.5" tire diameter (measured)
wheel_w    = 25.4;     // 1" tire width (measured)
tire_gap   = 60.3;     // 2-3/8" gap between front & rear tires (measured)
wheel_r    = wheel_d / 2 + 3;  // 34.75mm — radius + 3mm clearance

// Shell height: keeping 105mm (ground-to-tallest ~165mm, plate at ~63.5mm)
shell_h    = 105;
wall       = 2.5;
tol        = 0.8;      // slide-on fit gap per side
corner_r   = 3;

// Derived outer dims
inner_l = chassis_l + tol * 2;
inner_w = chassis_w + tol * 2;
outer_l = inner_l + wall * 2;
outer_w = inner_w + wall * 2;

// Wheel arch height — how tall the arch cutout is from the bottom
// Tires are 63.5mm diameter, poke ~6mm above the support plate
wheel_arch_h = 40;

// Wheel positions — DERIVED FROM TIRE GAP MEASUREMENT
// Axle-to-axle = tire_gap + wheel_d = 60.3 + 63.5 = 123.8mm
// wx = half that distance from chassis center
wx = (tire_gap + wheel_d) / 2;  // ~61.9mm from center
wy = outer_w / 2;               // wheels at the side walls

// L-bracket mounting — 4 corners
bracket_hole_d = 5;    // M3 or M4 screw + clearance
bracket_tab_w  = 12;   // tab width
bracket_tab_d  = 12;   // tab depth (inward from wall)
bracket_tab_h  = 3;    // tab thickness
bracket_z      = 15;   // height above bottom edge
// Bracket tab inset from wheel arch (so they don't collide)
bracket_inset  = 20;   // mm inboard from wheel arch center

// Mast hole
mast_d = 35;          // 1" PVC + clearance
mast_x = 0;
mast_y = -40;         // rear-center

// HC-SR04 front face
sr04_eye_r   = 8.5;
sr04_eye_gap = 26;
sr04_z       = 52;    // mid-height of shell

// USB-C rear slot
usbc_w = 16;
usbc_h = 10;
usbc_z = 5;

// Top vents over Pi
vent_w     = 50;
vent_h     = 2.5;
vent_count = 5;
vent_gap   = 8;
vent_x     = 35;

// ============================================
// BUILD
// ============================================

module rounded_rect(l, w, h, r) {
    hull() {
        for (x = [-l/2+r, l/2-r])
            for (y = [-w/2+r, w/2-r])
                translate([x, y, 0])
                    cylinder(r=r, h=h, $fn=16);
    }
}

module shell() {
    difference() {
        union() {
            // Outer box
            rounded_rect(outer_l, outer_w, shell_h, corner_r);

            // --- L-BRACKET MOUNTING TABS (4 corners, inside) ---
            for (fb = [1, -1]) {
                for (side = [1, -1]) {
                    translate([
                        fb * (inner_l/2 - bracket_tab_w/2 - bracket_inset),
                        side * (inner_w/2 - bracket_tab_d),
                        bracket_z
                    ])
                        cube([bracket_tab_w, bracket_tab_d, bracket_tab_h]);
                }
            }
        }

        // Hollow (open bottom)
        translate([0, 0, -0.1])
            rounded_rect(inner_l, inner_w, shell_h - wall + 0.1, corner_r);

        // --- WHEEL ARCHES (4 corners) ---
        // 2.5" diameter x 1" wide tires — measured 2026-03-19
        for (side = [1, -1]) {
            for (fb = [1, -1]) {
                // Arch: wheel_r radius x (wheel_w + 6mm clearance) deep
                translate([fb * wx, side * (wy - wheel_w/2 - 3), 0])
                    hull() {
                        cylinder(r=wheel_r, h=wheel_arch_h, $fn=48);
                        translate([0, side * (wheel_w + 6), 0])
                            cylinder(r=wheel_r, h=wheel_arch_h, $fn=48);
                    }
            }
        }

        // --- L-BRACKET SCREW HOLES (through the tabs) ---
        for (fb = [1, -1]) {
            for (side = [1, -1]) {
                translate([
                    fb * (inner_l/2 - bracket_tab_w/2 - bracket_inset),
                    side * (inner_w/2 - bracket_tab_d/2),
                    bracket_z - 0.1
                ])
                    cylinder(d=bracket_hole_d, h=bracket_tab_h + 0.2, $fn=24);
            }
        }

        // --- MAST HOLE (top) ---
        translate([mast_x, mast_y, shell_h - wall - 0.1])
            cylinder(d=mast_d, h=wall + 0.2, $fn=48);

        // --- HC-SR04 EYES (front wall) ---
        for (dy = [-sr04_eye_gap/2, sr04_eye_gap/2]) {
            translate([outer_l/2, dy, sr04_z])
                rotate([0, 90, 0])
                    cylinder(r=sr04_eye_r, h=wall*2, center=true, $fn=32);
        }

        // --- USB-C SLOT (rear wall) ---
        translate([-outer_l/2 - 0.1, -usbc_w/2, usbc_z])
            cube([wall + 0.2, usbc_w, usbc_h]);

        // --- VENT SLOTS (top) ---
        for (i = [0 : vent_count - 1]) {
            translate([
                vent_x - vent_w/2,
                i * vent_gap - (vent_count - 1) * vent_gap / 2,
                shell_h - wall - 0.1
            ])
                cube([vent_w, vent_h, wall + 0.2]);
        }

        // --- REAR WIRE SLOT (bottom of back wall) ---
        translate([-outer_l/2 - 0.1, -30, 0])
            cube([wall + 0.2, 60, 12]);

        // --- SIDE WIRE SLOT (bottom of left wall) ---
        translate([-20, outer_w/2 - wall - 0.1, 0])
            cube([40, wall + 0.2, 10]);
    }
}

// ============================================
// RENDER
// ============================================

color("#2a2a2a") shell();

// Info
echo(str("=== ESCORT BOT SHELL v4 — MEASURED ==="));
echo(str("Outer: ", outer_l, " x ", outer_w, " x ", shell_h, " mm"));
echo(str("Inner: ", inner_l, " x ", inner_w, " mm"));
echo(str("Wheel: ", wheel_d, "mm dia x ", wheel_w, "mm wide (MEASURED)"));
echo(str("Wheel arch: ", wheel_r*2, "mm arc x ", wheel_arch_h, "mm tall"));
echo(str("Tire gap: ", tire_gap, "mm | Axle-to-axle: ", tire_gap + wheel_d, "mm"));
echo(str("Wheel center offset (wx): ", wx, "mm from center"));
echo(str("L-bracket holes: ", bracket_hole_d, "mm at Z=", bracket_z, "mm"));
echo(str("Wall: ", wall, "mm | Tol: ", tol, "mm/side"));
