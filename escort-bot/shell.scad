// ============================================
// ESCORT BOT SHELL — Clean Minimal Box v3
// ============================================
// Amazon confirmed: chassis 10" x 6" x 2.5"
// Wheels + tires: 3" tall (76.2mm diameter)
// Wheel spec: 65mm OD rubber, 45mm ID hub
//
// F5 = preview | F6 = render | File > Export STL
// Print: 0.2mm layer, 15% infill, no supports
// ============================================

// --- DIMENSIONS (mm) ---
chassis_l  = 254;      // 10" front-to-back
chassis_w  = 152;      // 6" side-to-side
wheel_d    = 76.2;     // 3" wheel+tire diameter
wheel_w    = 76.2;     // 3" wheel+tire width
wheel_r    = wheel_d / 2 + 3;  // 41.1mm — radius + 3mm clearance

// Ground to tallest point: 6.5" (165mm)
// Ground to top plate: 2.5" (63.5mm) — Amazon confirmed
// Shell height: 165 - 63.5 = 101.5mm + 3.5mm margin
shell_h    = 105;
wall       = 2.5;
tol        = 0.8;      // slide-on fit gap per side
corner_r   = 3;

// Derived outer dims
inner_l = chassis_l + tol * 2;
inner_w = chassis_w + tol * 2;
outer_l = inner_l + wall * 2;
outer_w = inner_w + wall * 2;

// Wheel arch height — wheels poke above the support plate
// Chassis total 63.5mm, wheel 76.2mm → wheel tops are ~12mm above chassis top
// Support plate is ~15mm below chassis top → wheels ~27mm above plate
wheel_arch_h = 50;    // taller shell = wheels are lower relative to shell top

// Wheel positions from center (estimated — update after Rapha measures)
wx = 97;              // front/back wheel center from chassis center
wy = outer_w / 2;    // wheels at the side walls

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
        // Outer box
        rounded_rect(outer_l, outer_w, shell_h, corner_r);

        // Hollow (open bottom)
        translate([0, 0, -0.1])
            rounded_rect(inner_l, inner_w, shell_h - wall + 0.1, corner_r);

        // --- WHEEL ARCHES (4 corners) ---
        // 3" tall x 3" wide wheels — need full clearance
        for (side = [1, -1]) {
            for (fb = [1, -1]) {
                // Arch: semicircle (wheel_r tall) x wheel_w+6mm deep into/past wall
                translate([fb * wx, side * (wy - wheel_w/2 - 3), 0])
                    hull() {
                        cylinder(r=wheel_r, h=wheel_arch_h, $fn=48);
                        translate([0, side * (wheel_w + 6), 0])
                            cylinder(r=wheel_r, h=wheel_arch_h, $fn=48);
                    }
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
echo(str("=== ESCORT BOT SHELL v3 ==="));
echo(str("Outer: ", outer_l, " x ", outer_w, " x ", shell_h, " mm"));
echo(str("Inner: ", inner_l, " x ", inner_w, " mm"));
echo(str("Wheel arch: ", wheel_r*2, "mm wide x ", wheel_arch_h, "mm tall"));
echo(str("Wheel assumed: 3 inches (76.2mm) diameter"));
echo(str("Wall: ", wall, "mm | Tol: ", tol, "mm/side"));
