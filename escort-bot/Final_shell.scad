// ============================================
// ESCORT BOT SHELL — v5 from scratch
// ============================================
// Built piece by piece from Romeo's measurements
// ============================================

// --- SIDE PANEL ---
panel_l   = 254;     // 10" long
panel_h   = 177.8;   // 7" tall
wall      = 2.5;     // wall thickness
panel_gap = 152.4;   // 6" between panels

// --- WHEEL ARCHES ---
arch_w     = 81.28;         // ~3.2" wide (gap between arches shrunk 20% total)
arch_h     = 57.15;         // 2.25" tall (shortened — fender raise covers bottom)
arch_r     = arch_w / 2;    // semicircle radius
tire_gap   = 63.5;          // 2.5" between tire inside edges
// Layout: 1" + 3" + 2" + 3" + 1" = 10"
arch_inset = 25.4;          // 1" from each edge
front_fender_raise = 12.7;  // front fender raised 0.5" from ground

// --- MOUNTING TABS (front wall, integrated) ---
mtab_w      = 15;           // tab width (Y)
mtab_depth  = 15;           // how far tab extends inward (-X)
mtab_thick  = wall;         // tab thickness (Z) — matches wall
mtab_hole_r = 1.25;         // M3 self-tap hole (2.5mm dia)
mtab_offset = 26/2 + 8.5 + 5;  // Y offset from center — just outside HC-SR04 eyes (13 + 8.5r + 5mm gap)

// --- UPPER CROSS-BRACE ---
brace_w     = wall;         // brace thickness (X) — same as wall
brace_h     = 20;           // brace height (Z)
brace_z     = 145;          // above vents (vents end ~135mm), below ceiling
brace_x     = -30;          // X position — rear of center (negative = toward back)
brace_tab_w = 15;           // screw tab width (X)
brace_tab_d = 12;           // screw tab depth extending outward through panel
brace_tab_hole_r = 1.25;   // M3 self-tap

// --- CYBERTRUCK SLOPE ---
slope_len  = 101.6;   // 4" — how far back the slope starts from front edge
slope_drop = 25.4;    // 1" — how much the front roofline drops
slope_x    = panel_l/2 - slope_len;  // X where slope begins

// --- VENTILATION (Testarossa strakes) ---
vent_count   = 4;
vent_h       = 4;       // slot height (mm) — tighter
vent_start_z = 95;      // first slot ~3.7" (raised a bit more)
vent_rake    = 8;       // degrees
vent_offsets = [0, 10, 21, 34];
vent_lengths = [140, 165, 180, 165];

// --- BUILD ---
module vent_strake(z, len) {
    rake = tan(vent_rake) * len / 2;
    translate([0, 1, z])
        hull() {
            translate([-len/2, 0, rake])
                rotate([90, 0, 0])
                    cylinder(h = wall + 2, r = vent_h/2, $fn = 40);
            translate([len/2, 0, -rake])
                rotate([90, 0, 0])
                    cylinder(h = wall + 2, r = vent_h/2, $fn = 40);
        }
}

module arch_cutout() {
    cube([arch_w, wall + 2, arch_h - arch_r]);
    translate([arch_r, 0, arch_h - arch_r])
        rotate([-90, 0, 0])
            cylinder(h = wall + 2, r = arch_r, $fn = 60);
}

// Side panel with Cybertruck slope built into the profile
module side_panel() {
    difference() {
        // Panel shape — polygon profile with slope
        rotate([90, 0, 0])
            linear_extrude(height = wall)
                polygon([
                    [-panel_l/2, 0],                      // bottom-rear
                    [panel_l/2, 0],                        // bottom-front
                    [panel_l/2, panel_h - slope_drop],     // top-front (lowered)
                    [slope_x, panel_h],                    // slope start
                    [-panel_l/2, panel_h]                  // top-rear
                ]);

        // Rear wheel arch (rectangle + semicircle top)
        translate([-panel_l/2 + arch_inset, 1, 0])
            rotate([90, 0, 0])
                linear_extrude(height = wall + 2)
                    union() {
                        square([arch_w, arch_h - arch_r]);
                        translate([arch_r, arch_h - arch_r])
                            circle(r = arch_r, $fn = 60);
                    }

        // Front wheel arch (rectangle + semicircle top)
        translate([panel_l/2 - arch_inset - arch_w, 1, 0])
            rotate([90, 0, 0])
                linear_extrude(height = wall + 2)
                    union() {
                        square([arch_w, arch_h - arch_r]);
                        translate([arch_r, arch_h - arch_r])
                            circle(r = arch_r, $fn = 60);
                    }

        // Front fender raise — cut bottom 0.5" of front fender
        translate([panel_l/2 - arch_inset, -wall - 1, 0])
            cube([arch_inset + 1, wall + 2, front_fender_raise]);

        // Testarossa ventilation strakes
        for (i = [0 : vent_count - 1])
            vent_strake(vent_start_z + vent_offsets[i], vent_lengths[i]);

    }
}

// --- ASSEMBLY ---
color("#2a2a2a") {
    // Left panel
    translate([0, -panel_gap/2, 0])
        side_panel();

    // Right panel
    translate([0, panel_gap/2 + wall, 0])
        side_panel();

    // Side panel mounting tabs — between wheel arches, shelves extend inward
    // Left panel tab (shelf goes +Y inward)
    difference() {
        translate([-mtab_w/2, -panel_gap/2, 0])
            cube([mtab_w, mtab_depth + wall, mtab_thick]);
        translate([0, -panel_gap/2 + wall + mtab_depth/2, -1])
            cylinder(h = mtab_thick + 2, r = mtab_hole_r, $fn = 24);
    }
    // Right panel tab (shelf goes -Y inward)
    difference() {
        translate([-mtab_w/2, panel_gap/2 - mtab_depth, 0])
            cube([mtab_w, mtab_depth + wall, mtab_thick]);
        translate([0, panel_gap/2 - mtab_depth/2, -1])
            cylinder(h = mtab_thick + 2, r = mtab_hole_r, $fn = 24);
    }

    // Upper cross-brace — horizontal bar spanning both side panels (no external tabs)
    translate([brace_x - brace_w/2, -panel_gap/2, brace_z])
        cube([brace_w, panel_gap, brace_h]);

    // Back mounting tabs — long shelves extending inward
    btab_depth = 30;  // twice the front tab depth
    for (side = [-1, 1]) {
        difference() {
            translate([-panel_l/2, side * mtab_offset - mtab_w/2, 0])
                cube([btab_depth + wall, mtab_w, mtab_thick]);
            // Screw hole centered on shelf
            translate([-panel_l/2 + wall + btab_depth/2, side * mtab_offset, -1])
                cylinder(h = mtab_thick + 2, r = mtab_hole_r, $fn = 24);
        }
    }

    // Back wall with score lines (cut to open door)
    door_frame = 25;       // margin from edges (15% smaller door)
    door_sill  = 30;       // margin from bottom (15% smaller door)
    score_d    = 1.2;      // score line depth (half the wall)
    score_w    = 0.6;      // score line width
    door_w     = panel_gap + wall * 2 - door_frame * 2;
    door_h     = panel_h - door_sill - door_frame;
    difference() {
        translate([-panel_l/2, -panel_gap/2 - wall, 0])
            cube([wall, panel_gap + wall * 2, panel_h]);
        // Score lines — rectangle outline on outside face
        // Bottom line
        translate([-panel_l/2 - 0.01, -panel_gap/2 + door_frame - wall, door_sill])
            cube([score_d, door_w, score_w]);
        // Top line
        translate([-panel_l/2 - 0.01, -panel_gap/2 + door_frame - wall, door_sill + door_h - score_w])
            cube([score_d, door_w, score_w]);
        // Left line
        translate([-panel_l/2 - 0.01, -panel_gap/2 + door_frame - wall, door_sill])
            cube([score_d, score_w, door_h]);
        // Right line
        translate([-panel_l/2 - 0.01, -panel_gap/2 + door_frame - wall + door_w - score_w, door_sill])
            cube([score_d, score_w, door_h]);
    }

    // Back door handle — recessed finger pull (modern flush style)
    // Scoop cut into the wall so fingers can hook under and pull
    handle_w    = 40;      // width of the pull
    handle_r    = 6;       // radius of the finger scoop
    handle_z    = door_sill + 15;  // just above door bottom score line
    // Scoop: horizontal half-cylinder carved into outside face
    translate([-panel_l/2 - 0.01, 0, handle_z])
        rotate([0, -90, 0])
            rotate([0, 0, 90])
                linear_extrude(height = score_d + 0.5)
                    intersection() {
                        translate([-handle_w/2, 0])
                            square([handle_w, handle_r]);
                        scale([handle_w/2 / handle_r, 1])
                            circle(r = handle_r, $fn = 40);
                    }
    // Lip above the scoop — thin shelf to grip
    handle_lip = 2;
    translate([-panel_l/2 - handle_lip, -handle_w/2, handle_z + handle_r - 1])
        hull() {
            cube([handle_lip, handle_w, 1.5]);
            translate([handle_lip - 0.5, 0, 1.5])
                cube([0.5, handle_w, 0.5]);
        }

    // Front wall (lowered by slope) with HC-SR04 slot + honeycomb grille
    hc_eye_r    = 8.5;    // 17mm dia (16mm sensor + 1mm clearance)
    hc_spacing  = 26;     // center-to-center of the two transducers
    hc_z        = 50.8;   // 2" from ground — robot eye height
    // Honeycomb grille parameters
    hex_r       = 2.5;    // hexagon radius (smaller still)
    hex_gap     = 1.2;    // wall between hexagons
    hex_step_y  = (hex_r + hex_gap/2) * 2;           // horizontal spacing
    hex_step_z  = (hex_r + hex_gap/2) * sqrt(3);     // vertical spacing
    hex_zone_y  = panel_gap * 0.7;    // grille width (70% of front face)
    hex_zone_z0 = 75;                 // grille bottom Z (above eyes)
    hex_zone_z1 = panel_h - slope_drop - 15;  // grille top Z (margin from top)
    difference() {
        translate([panel_l/2 - wall, -panel_gap/2 - wall, front_fender_raise])
            cube([wall, panel_gap + wall * 2, panel_h - slope_drop - front_fender_raise]);
        // Left eye
        translate([panel_l/2 - wall - 1, -hc_spacing/2, hc_z])
            rotate([0, 90, 0])
                cylinder(h = wall + 2, r = hc_eye_r, $fn = 40);
        // Right eye
        translate([panel_l/2 - wall - 1, hc_spacing/2, hc_z])
            rotate([0, 90, 0])
                cylinder(h = wall + 2, r = hc_eye_r, $fn = 40);
        // Honeycomb grille — hex cutouts above eyes
        for (row = [0 : floor((hex_zone_z1 - hex_zone_z0) / hex_step_z)]) {
            offset_y = (row % 2 == 0) ? 0 : hex_step_y / 2;
            z = hex_zone_z0 + row * hex_step_z;
            if (z >= hex_zone_z0 && z <= hex_zone_z1)
                for (col = [-floor(hex_zone_y / hex_step_y / 2) : floor(hex_zone_y / hex_step_y / 2)]) {
                    y = col * hex_step_y + offset_y;
                    if (abs(y) < hex_zone_y / 2)
                        translate([panel_l/2 - wall - 1, y, z])
                            rotate([0, 90, 0])
                                cylinder(h = wall + 2, r = hex_r, $fn = 6);
                }
        }
    }

    // Front mounting tabs — horizontal shelves, wall itself is the vertical L
    for (side = [-1, 1]) {
        difference() {
            translate([panel_l/2 - wall - mtab_depth, side * mtab_offset - mtab_w/2, front_fender_raise])
                cube([mtab_depth + wall, mtab_w, mtab_thick]);
            // Screw hole centered on shelf (not in wall portion)
            translate([panel_l/2 - wall - mtab_depth/2, side * mtab_offset, front_fender_raise - 1])
                cylinder(h = mtab_thick + 2, r = mtab_hole_r, $fn = 24);
        }
    }

    // Ceiling — flat rear section
    wire_hole_r = 5;  // 10mm diameter wire pass-through
    difference() {
        translate([-panel_l/2, -panel_gap/2 - wall, panel_h])
            cube([panel_l - slope_len, panel_gap + wall * 2, wall]);
        // Center hole for wires
        translate([(-panel_l/2 + slope_x) / 2, 0, panel_h - 1])
            cylinder(h = wall + 2, r = wire_hole_r, $fn = 40);
    }

    // Ceiling — sloped front section (polyhedron)
    translate([slope_x, -panel_gap/2 - wall, 0])
        polyhedron(
            points = [
                [0, 0, panel_h],                                         // 0
                [0, panel_gap + wall * 2, panel_h],                      // 1
                [slope_len, 0, panel_h - slope_drop],                    // 2
                [slope_len, panel_gap + wall * 2, panel_h - slope_drop], // 3
                [0, 0, panel_h + wall],                                  // 4
                [0, panel_gap + wall * 2, panel_h + wall],               // 5
                [slope_len, 0, panel_h - slope_drop + wall],             // 6
                [slope_len, panel_gap + wall * 2, panel_h - slope_drop + wall] // 7
            ],
            faces = [
                [0,2,3,1],   // bottom
                [4,5,7,6],   // top
                [0,4,6,2],   // left
                [3,7,5,1],   // right
                [0,1,5,4],   // back
                [2,6,7,3]    // front
            ]
        );
}

// (no separate door — score lines on back wall instead)

echo(str("Panel: ", panel_l, " x ", panel_h, " mm, gap: ", panel_gap, " mm"));
