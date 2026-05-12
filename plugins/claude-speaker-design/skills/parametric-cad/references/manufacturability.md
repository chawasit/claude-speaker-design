# Manufacturability (DFM) for CAD

Design for Manufacture: the constraints that a manufacturable model
must respect. Get these wrong and the part either cannot be made,
made expensively, or made wrong. They apply at the CAD stage —
fixing them in the shop is much costlier.

## Tolerances by process

| Process                | Typical tolerance | Notes                                    |
|------------------------|-------------------|------------------------------------------|
| Hand woodworking       | ±0.5 mm           | OK for cabinets; rough for joinery       |
| Table-saw + jig        | ±0.2 mm           | Excellent for square cuts                |
| CNC router (plywood/MDF)| ±0.1 mm          | Limited by tool deflection on long runs  |
| CNC mill (plastic/metal)| ±0.05 mm         | Standard for hardware-mating features    |
| Laser cutter (plywood ≤6 mm) | ±0.05 mm    | Kerf 0.1–0.3 mm; compensate in CAD       |
| Waterjet (any sheet)   | ±0.1 mm           | Kerf ~1 mm; compensate                   |
| FDM 3D print (PLA, PETG)| ±0.2 mm          | Layer height limits Z resolution         |
| SLA 3D print           | ±0.05 mm          | Hi-res; expensive; small build volume    |
| SLS 3D print (nylon)   | ±0.1 mm           | Good for functional parts                |
| Sheet metal (laser+brake) | ±0.5 mm        | Spring-back, K-factor variations         |
| Vacuum forming         | ±1 mm             | Outline crisp; depth poor                |

Design with the tolerance of the process you'll use, not the
tolerance of CAD. A 0.1 mm gap in CAD becomes either 0.0 mm
(interference fit) or 0.3 mm (sloppy) after hand-cutting plywood.

## Tool diameter and internal radii

A CNC tool cannot reach into an internal corner sharper than its own
radius. The minimum internal radius is:

```
r_min = tool_diameter / 2 + 0.1 mm (clearance)
```

Common end mills for CNC routing:

| Tool diameter | Min internal radius | Typical use                  |
|---------------|---------------------|------------------------------|
| 6 mm (¼")    | 3 mm                | Cabinet panel features       |
| 3 mm (⅛")    | 1.5 mm              | Driver cutout, detail        |
| 1.5 mm       | 0.8 mm              | Fine joinery, tight pockets  |

If your CAD has a square 90° internal corner, the CNC will either
leave a small fillet (default) or "overcut" by drilling into the
corner (bad — weakens the part). Always add explicit fillets of
radius ≥ `r_min` to internal corners.

External corners (convex) can be as sharp as the tool can hold; no
constraint there.

## Joinery (for wooden cabinets)

The choice of joint affects strength, alignment difficulty,
finishing, and how the CAD model is structured (per-panel exports
require joinery to be modeled into each panel's profile).

### Butt joint

Two panels meet at a 90° edge, glued. Simplest. CAD: nothing special
to model — the panels just touch.

- Strength: moderate, depends entirely on glue area + clamp pressure.
- Visible glue line at the corner.
- Best with biscuits, dowels, or a Domino for alignment.
- Cabinet weight bias: outer "lip" of one panel is exposed grain;
  veneer or paint to match.

### Rabbet

A step cut along one edge so the mating panel sits inside it. The
rabbet's depth is half to two-thirds of the panel thickness.

```
rabbet_depth   = panel_t * 0.5     # 9 mm in 18 mm stock
rabbet_width   = panel_t            # the mating panel's thickness
```

Stronger than butt; aligns automatically; hides the end grain of one
panel. Standard for high-end DIY cabinets.

CAD: cut a step along the receiving edge before assembling panels.

### Lock miter / drawer-lock

A two-cut miter that interlocks with itself. Made on a router table
with a single bit; cabinet panels go through the bit twice (vertical
and horizontal pass).

- Strongest visible miter joint; no end grain showing.
- Requires a specialty bit (~$80).
- CAD: model the lock-miter profile on both mating edges. Most CNC
  routers can cut the same profile with a custom toolpath.

### Domino / mortise & tenon

Loose-tenon joinery: cut matching slots in both panels, glue a
floating wooden tenon between them.

- Excellent alignment + strength.
- Requires a Festool Domino tool or equivalent — not CNC-trivial.
- CAD: model the domino slots as parametric pockets.

### Finger / box joint

Interlocking square fingers along an edge. Strong, visible.

- Mostly aesthetic in cabinet design.
- CNC-routable with a standard end mill; just be careful with
  internal corner radii (`r_min` ≥ tool radius).

### Mitered

Both panels cut at 45° so the joint disappears at the corner.

- Cleanest aesthetic, weakest joint without reinforcement.
- Reinforce with biscuits, splines, or internal corner blocks.
- CAD: model the miter as a 45° cut on each panel's edge.

## Kerf compensation

Subtractive cutting removes material equal to the cutting tool's
diameter (router) or beam (laser). For inside-cut features (e.g.
the driver cutout in the baffle), the cutter's center follows the
sketched line, so the removed circle is `(tool_d / 2)` larger than
intended on each side.

Three strategies:

1. **Offset in CAM**: the CAM software offsets the toolpath inside
   or outside the sketched line. The CAD model is the **final
   geometry** (the hole as it should appear); CAM handles the
   compensation.
2. **Offset in CAD**: the CAD model already accounts for kerf — the
   sketched circle is `(tool_d)` smaller than the target hole.
   Brittle, only acceptable for one-off jobs where CAM isn't
   parametric.
3. **Test cut**: cut a known dimension, measure, adjust parameter.
   Always do this for a new material or new tool.

For laser cutting, kerf is ~0.1–0.3 mm. For plasma cutting, ~1 mm.
For CNC routing with a 6 mm end mill, ~6 mm radial — much larger
than laser kerf.

## Driver cutouts: get the diameter right

Manufacturer datasheets list a "cutout diameter" — the through-hole
the driver should sit in. Some manufacturers list the cone diameter
or the flange diameter instead; check carefully.

Standard practice:

- **Cutout (cone clearance)**: datasheet value + 0 mm. The driver
  flange overlaps; the cone doesn't touch.
- **Flange recess**: 1 mm larger than the flange diameter on each
  side (so flange OD + 2 mm). Depth = flange thickness + 0.5 mm
  (for gasket clearance).
- **Mounting holes**: drill in CAD or leave for the installer;
  match the driver's mounting bolt pattern.

If you're flush-mounting a driver with a gasket, the gasket eats
0.5–1 mm of recess depth. Plan for it.

## Hardware features

| Hardware                         | CAD feature needed                       |
|----------------------------------|------------------------------------------|
| Wood screw (#8, ¼")              | Pilot hole at appropriate diameter      |
| M4 screw + threaded insert       | Hole sized for insert (typ. 6 mm OD)   |
| T-nut                            | Pilot hole + prong relief on back side |
| Pocket-screw joinery             | Pocket-hole sketched at correct angle  |
| Cam-lock (RTA furniture)         | Cam recess + dowel pin hole            |
| Hidden hinge (35 mm cup)         | 35 mm hole on door, machine screws on frame |
| Spring-clip terminal cup         | Rectangular pocket per cup outline     |

Threaded inserts (heat-set or press-fit) are the standard for
designs that may be opened repeatedly. Model their pilot hole, not
the threaded engagement — the insert provides the thread.

## Material-specific notes

### MDF

- Uniform density; routes cleanly; no grain to fight.
- Sucks up finish; needs primer/sanding sealer.
- Heavy. Dust is a respiratory hazard.
- Cannot hold screws into end grain — use threaded inserts or
  through-bolts.
- Tolerance: ±0.1 mm CNC, ±0.3 mm hand.

### Baltic-birch plywood

- Stiffer than MDF per unit thickness; lighter.
- Visible plies on edges (aesthetic feature or veneer to cover).
- Holds screws better than MDF, including into end grain.
- Layer count varies by thickness (5-ply at 12 mm, 9-ply at 18 mm,
  etc.); buy by ply count, not just thickness, for consistent
  bending stiffness.

### HDF (high-density fiberboard)

- Same family as MDF but denser; better acoustic properties.
- More expensive; harder to cut.
- Almost no internal voids — good for thin panels.

### Aluminum / steel (for high-end cabinets, mid sections, supports)

- CNC milling required for precision.
- Anodize (Al) or powder coat (steel) for finish.
- Bonded to internal structure with epoxy or mechanical fasteners.
- Heavy; great for vibration damping when CLD'd.

### 3D-printed terminal cups, port flares, internal brackets

- FDM in PETG or ASA for cabinet-internal parts (heat resistance).
- SLA for tweeter waveguides or other smooth-surface parts.
- Tolerance on screw holes: model 0.3 mm larger than nominal for FDM.

## Surface finishing

A cabinet often needs to be finished outside the CAD model, but
finishing thickness adds dimensional change:

| Finish                   | Build-up per coat | Coats typical |
|--------------------------|-------------------|---------------|
| Sanding sealer / primer  | 50–100 µm         | 2             |
| Lacquer                  | 25–50 µm          | 3–5           |
| Polyurethane             | 50–100 µm         | 3             |
| Veneer (+ glue)          | 0.5–1.0 mm        | 1 layer       |
| Paint (waterborne)       | 25–50 µm          | 3             |
| Powder coat              | 80–120 µm         | 1             |

For driver cutouts, the finish adds material to the inside diameter
— most installers ignore this (it's within the gasket's give), but
for precision flush-mount jobs add 0.2 mm to the cutout to keep
clearance after finishing.

## DFM checklist

Before sending a CAD file to a fabricator or CAM:

- [ ] All internal corners have fillet ≥ `r_min` of the planned tool.
- [ ] Wall thicknesses ≥ minimum for the material (MDF: 12 mm
      minimum for structural panels; ply: 6 mm; FDM print: 2 mm
      perimeter walls).
- [ ] No "thin slivers" (features < 1 mm thick): they break or fail
      to print/cut.
- [ ] Hole diameters reflect any kerf compensation (or are flagged
      for CAM to handle).
- [ ] Tolerances on mating features (driver cutout, panel joinery,
      hardware holes) match the process tolerance.
- [ ] No undercuts that the chosen process can't produce (e.g.
      lateral pockets in 3-axis CNC).
- [ ] Joinery is parametric — change `panel_t` from 18 mm to 25 mm
      and the joints adapt.
- [ ] STEP export passes a check in the receiving CAD/CAM.
- [ ] DXF panel exports include all kerf-compensated features.
- [ ] Mass / volume reports agree with the BOM.
