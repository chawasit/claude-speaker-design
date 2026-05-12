# Speaker Cabinet CAD

Patterns for parametric loudspeaker enclosures. Pair this file with
the `speaker-design` skill: the acoustic design produces a
specification (driver, `V_b`, port dimensions, baffle layout); this
file turns that specification into a manufacturable CAD model.

## Parameter table for a two-way bookshelf

Drive every dimension from a named parameter. The minimum useful set
for a standard sealed/ported bookshelf:

```
# === External dimensions ===
baffle_w              = 200 mm    # external front-baffle width
baffle_h              = 350 mm    # external front-baffle height
depth                 = 280 mm    # external depth front-to-back
panel_t               = 18 mm     # cabinet panel thickness

# === Derived internal ===
internal_w            = baffle_w - 2 * panel_t        # 164 mm
internal_h            = baffle_h - 2 * panel_t        # 314 mm
internal_d            = depth    - 2 * panel_t        # 244 mm
gross_internal_vol    = internal_w * internal_h * internal_d  # 12.57 L

# === Driver: woofer ===
woofer_cutout_d       = 152 mm    # cone-mounting hole diameter
woofer_flange_d       = 178 mm    # outer flange diameter (for recess)
woofer_flange_t       = 5 mm      # flange thickness (recess depth)
woofer_y_center       = 220 mm    # from cabinet bottom to woofer center
woofer_x_offset       = 0 mm      # from cabinet vertical centerline

# === Driver: tweeter ===
tweeter_cutout_d      = 86 mm
tweeter_flange_d      = 104 mm
tweeter_flange_t      = 4 mm
tweeter_y_center      = 295 mm
tweeter_x_offset      = 15 mm     # asymmetric → diffraction smoothing

# === Port ===
port_dia              = 60 mm
port_length           = 163 mm    # physical length (with end correction)
port_y_center         = 80 mm
port_x_offset         = 0 mm
port_position         = "rear"    # "front" | "rear" | "bottom"

# === Bracing ===
brace_count           = 1
brace_width           = 30 mm
brace_thickness       = 18 mm
brace_cutouts_per     = 2          # holes for wire/air passage per brace

# === Edges ===
front_roundover_r     = 25 mm     # baffle edge roundover radius
rear_chamfer          = 8 mm

# === Hardware ===
terminal_cup_w        = 90 mm
terminal_cup_h        = 50 mm
terminal_cup_inset    = 10 mm     # recess depth from rear surface

# === Joinery ===
joinery_style         = "rabbet"   # "butt" | "rabbet" | "lock-miter" | "domino"
rabbet_depth          = 9 mm       # half of panel_t typical
```

Many of these come straight from the acoustic spec (driver datasheet
→ cutout diameters, port-length calc → port dimensions, baffle-step
analysis → baffle width). Reference `cookbooks/bookshelf-2way.md` in
the `speaker-design` skill for an end-to-end derivation.

## Build order

1. **Parameters** (above).
2. **Main shell solid**: bounded by `baffle_w × baffle_h × depth`,
   hollowed to thickness `panel_t`.
3. **Internal-volume verification**: measure shelled volume; compare
   to `gross_internal_vol`. Should match before any cutouts.
4. **Driver cutouts**: hole + recess (flange relief) for each
   driver.
5. **Port**: hole through the appropriate panel + cylindrical port
   tube extending into the cabinet.
6. **Brace(s)**: horizontal or vertical solid pieces with cutouts.
7. **Terminal cup recess** on the rear panel.
8. **Roundovers** on visible baffle edges.
9. **Rear-panel split** if you want a removable back for crossover
   access.
10. **Final internal-volume measurement**: net after all cutouts and
    bracing. Compare to the design `V_b`.
11. **Export**: STEP for the assembled model, DXF for flat-pack
    panels, STL for any 3D-printed parts (terminal cup, port flare).

## Common geometric features

### Cabinet shell

Three equivalent approaches; pick based on what the MCP supports:

```
# Approach A: extrude + shell
1. sketch front baffle on XY plane (rectangle baffle_w × baffle_h)
2. extrude depth → solid box
3. shell with panel_t thickness, open face on rear OR all faces closed
   (then split off back panel later)

# Approach B: extrude two solids and subtract
1. sketch outer rectangle, extrude depth → outer body
2. sketch inner rectangle inset by panel_t, extrude (depth - 2*panel_t)
   → inner body
3. subtract inner from outer → shell

# Approach C: panel-by-panel
1. sketch each panel as a flat profile
2. extrude each by panel_t
3. position the six panels into a box
4. (Optional) add joinery cuts where panels meet
```

Approach A is cleanest for monolithic cabinets. Approach C is the
default for flat-pack designs intended for CNC routing on sheet
stock — see `manufacturability.md` for joinery.

### Driver cutouts (flush mount)

Two coaxial cylindrical cuts per driver:

```
# Outer recess (relief for the driver flange)
sketch_driver_flange (circle at woofer position, dia = woofer_flange_d)
cut to depth woofer_flange_t (from outside of baffle)

# Through-hole (cone clearance)
sketch_driver_cutout (circle at woofer position, dia = woofer_cutout_d)
cut through baffle thickness
```

For an asymmetric tweeter offset (the diffraction-smoothing pattern),
locate the tweeter `tweeter_x_offset` to one side of the cabinet
centerline. Same offset on both speakers of a stereo pair? **Mirror
the second cabinet's CAD** so the offsets point inward (toward each
other) — the tweeters then face the listener's centerline.

### Port

If the port is a simple straight tube:

```
sketch_port_axis on the chosen panel, circle dia = port_dia at (port_x_offset, port_y_center)
cut through the panel
extrude_tube from inside edge of the panel inward by
  (port_length - panel_t),
  outer dia = port_dia + 2 mm,
  inner dia = port_dia
```

For a flared port (slot, trumpet), the tube becomes a sweep or loft
along the port axis with the flare profile. Tractrix or radial flare
is standard at port mouth; see `references/horns-and-waveguides.md`
in the speaker-design skill.

For a slot port (long rectangular port), substitute a rectangular
cross-section for the circular one; the acoustic math (Sp, end
correction) generalizes — see `tools/port_length.py`.

### Bracing

A single transverse brace is usually sufficient for a bookshelf-sized
cabinet:

```
sketch_brace on the YZ plane at x = baffle_w / 2
rectangle: width = brace_width, height = internal_h
positioned at mid-depth (center of cabinet)
extrude by brace_thickness, symmetric about the sketch plane
cut circular holes for wire/air passage (e.g. 2 × dia 40 mm)
```

Larger cabinets use a "window brace" (a flat plate with a large
cutout) or matrix bracing (intersecting rectangles). Drive these
from `brace_count` parameter so the user can iterate without
re-cutting wood.

### Edge roundovers

Apply **last**. Most CAD MCPs implement fillets per edge or per face;
select the four vertical front-baffle edges (or all four
front-baffle edges for a full roundover):

```
fillet edges: front_top, front_bottom, front_left, front_right
radius = front_roundover_r
```

Verify by render — fillets are the most common source of
"unexpected geometry" in cabinet CAD because edge selection at the
LLM level is fragile.

### Rear-panel split

For a removable back to access the crossover:

```
sketch_split_plane: rectangle on a plane offset panel_t from the rear,
   matching internal dimensions
split body using this plane
rename two halves: shell_main, shell_back
```

Drill matching countersunk M4 holes through both for assembly
screws. Spacing: ~8 holes around the perimeter for a typical
bookshelf, more for larger cabinets.

### Terminal cup

A standard 90 × 50 mm terminal cup needs a flush-mount recess:

```
sketch_terminal_cup on rear panel: rectangle, terminal_cup_w × terminal_cup_h
cut to depth terminal_cup_inset
cut through-holes for binding posts: 2 × dia ~10 mm, spaced per cup
```

## Verification of internal volume

The whole point of the cabinet CAD is to produce an enclosure with
the target net internal `V_b`. The measurement chain:

1. **Gross internal** = `internal_w × internal_h × internal_d`.
2. **− driver displacement** (basket + magnet volume; ~0.4 L for a
   6.5", ~0.1 L for a tweeter, ~1.5 L for a 12" subwoofer driver).
   Many MCPs let you import a driver STEP from a manufacturer and
   subtract it directly.
3. **− brace volume**: `brace_width × internal_h × brace_thickness × brace_count`
   minus brace cutout volumes.
4. **− port volume** (if the port intrudes into the cabinet):
   `π × (port_dia/2)² × (port_length - panel_t)`.
5. **− crossover board volume** (if internal): ~0.2–0.5 L typical.
6. **+ stuffing recovery** (5–15 %): added after measurement, not in
   CAD.

Have the MCP measure the **filled body volume** of the enclosed air
region after all the above subtractions, and compare to the design
`V_b` from the acoustic spec. Target: within 5 % of design `V_b`
before stuffing. If short, increase external dimensions slightly.

## Export checklist

Different downstream tools want different formats:

| Output                        | Format        | Notes                            |
|-------------------------------|---------------|----------------------------------|
| CNC mill (3D)                 | STEP or IGES  | Whole shell as solid             |
| CNC router (flat panels)      | DXF           | One per panel, with joinery cuts |
| Laser cutter (acrylic, ply)   | DXF           | 2D outlines + kerf compensation  |
| 3D printer (terminal cup, port flare) | STL   | Watertight mesh, mm units        |
| FEA modal analysis            | STEP          | For panel mode prediction        |
| Render / marketing image      | OBJ or glTF   | Mid-poly, with materials         |
| Manufacturing drawing         | PDF + DXF     | Dimensioned 2D                   |

DXF panel exports: project each panel face flat, dimension joinery
features, include the driver cutout on the front baffle. Many CAD
MCPs lack drawing tools; if so, do panel exports manually one face
at a time.

## Cross-references

- `speaker-design/cookbooks/bookshelf-2way.md` — acoustic spec that
  produces the parameter values used here.
- `speaker-design/references/baffle-and-cabinet-acoustics.md` —
  why driver offset and roundovers matter.
- `speaker-design/references/closed-box-geometry.md` — why
  aspect ratio and stuffing volume need to be accounted for.
- `references/manufacturability.md` — DFM constraints for CNC,
  laser, and 3D-printed parts.
- `cookbooks/speaker-cabinet-2way.md` — worked end-to-end CAD build
  of the bookshelf design.
