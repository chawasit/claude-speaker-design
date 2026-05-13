# Assembly-Locating Features

A *locating feature* is geometry built into a part that **forces the
mating part into a unique correct position** during assembly. Done
well, you assemble a multi-part build without jigs, clamps, layout
marks, or measurements — the parts only fit together one way.

For CNC-routed wood and CNC-milled metal, the cheapest and most
effective locating features are **grooves, dadoes, rabbets, and
keyed slots**. This file covers the geometry, the design rules, and
the patterns specific to speaker cabinets.

For 3D-printed locating features (boss-and-pocket, dovetail keys,
keyed bosses), see `joints-by-process.md`.

## 1. Why locating features matter

Without locating features:

- The builder eyeballs alignment from edges or layout marks.
- Glue-up requires multiple clamps + squaring jigs.
- A cabinet may shift 0.5-2 mm during clamping, going out of square.
- Driver cutouts, port positions, and brace locations drift relative
  to each other.
- "Squareness" becomes a verification problem rather than a
  built-in property.

With locating features:

- Parts only fit together one way.
- Glue-up can be done with simple body weight or light clamping.
- Alignment is automatic; squareness is constrained by geometry.
- Each panel's features (driver cutouts, port holes, internal
  geometry) reference the same datum, so they always align.

For a speaker cabinet built by a single person with a router and
some F-clamps, this is the difference between a cabinet that's
square the first time and one that needs to be re-built.

## 2. The basic groove (dado / rabbet)

A **groove** is a slot cut across the face of one panel; the
**tongue** (or the full edge of a mating panel) sits in it.

```
   top view, looking down at the bottom panel:

       +-------------------------+
       |                          |
       |     groove (dado)        |    <-- side panel will slot in here
       |    --------------|---    |
       |                  |       |
       |  inner face      |       |
       |                  |       |
       +------------------|-------+
                          |
                          | side panel (vertical)
                          |
```

The groove **constrains** the side panel to:

1. The correct X position (along the long axis).
2. The correct Y position (across the face).
3. The correct rotation (the panel can't tilt).

The only remaining freedom is sliding along the groove's length —
typically constrained by another groove perpendicular to it, or by
butting into another panel.

### Groove dimensions

```
groove_width    = panel_t + clearance
groove_depth    = 0.4 to 0.5 × panel_t      (rule of thumb)
clearance       = +0 to +0.1 mm              (slip fit; tight, glue-friendly)
```

For 18 mm panels:
- Groove width: 18.1 mm (slip-fit) or 18.0 mm (press-fit + sanding)
- Groove depth: 7-9 mm

Too shallow (< 1/3 × panel thickness): joint is weak, can shear.
Too deep (> 1/2 × panel thickness): the carrying panel is weakened,
and CNC time grows.

### Dado vs rabbet vs groove (terminology)

- **Groove**: cut runs **with** the grain.
- **Dado**: cut runs **across** the grain (perpendicular).
- **Rabbet**: an L-shaped step on the **edge** (not the middle) of a
  panel; equivalent to half a groove.

Engineering-wise they're all the same: a slot that captures a panel
edge. CAM and routers don't care which name applies. Use whichever
fits the CAD convention you're working with.

## 3. Locating patterns for a speaker cabinet

A typical bookshelf cabinet (front + back + 4 sides) has 12 panel
edges. Each can carry a groove or be captured by one. The pattern
below uses **dado-captured sides + rabbet-captured front/back**:

```
   exploded view, bottom panel only:

      +-----------------------------+
      |      ┌─────dado─────┐        |   <-- top panel sits in this dado on the bottom panel
      |   ┌──┘            └──┐       |
      |   |                  |        |
      |   |   inner cavity   |        |
      |   |                  |        |
      |   └──┐            ┌──┘        |
      |      └─────dado─────┘         |   <-- another dado for the other side
      +-----------------------------+
                |          |
              dado     dado    <-- two perpendicular dadoes for the sides
              (sides    (sides
              slot in   slot in
              here)     here)
```

Each side panel has two **tabs** at its bottom edge that mate with
the dadoes on the bottom panel. Repeat on top panel: dadoes on the
top capture tabs on the top of each side.

The front and back baffles fit into **rabbets** along the front and
rear edges of the four other panels.

Result: the cabinet self-aligns on assembly. Glue the side panels
into the bottom dadoes; once those set (30 minutes for PVA), drop
the top panel onto the top tabs (no clamps needed; gravity holds
it). Glue the front and back baffles into their rabbets. Done.

### Common patterns

| Pattern               | Joint type       | Use                              |
|-----------------------|------------------|----------------------------------|
| Through-dado          | Dado all way across | Sides into bottom               |
| Stopped dado          | Dado stops short of edge | Invisible from outside    |
| Through-rabbet        | Rabbet on edge   | Front/back baffle into sides     |
| Stopped rabbet        | Rabbet stops short | Hidden from one side            |
| Sliding dovetail      | Tapered groove   | Strong, self-locking; CNC-cuttable |
| Tongue and groove     | Tongue on one, groove on mate | Edge-to-edge wide panels |
| Drawer-lock joint     | Routed interlock | Cabinet drawer fronts            |
| Dog-bone keyhole      | Keyed slot       | Removable panel that slides on   |

## 4. Self-aligning brace pattern

Internal braces benefit from the same approach. A horizontal brace
across a cabinet's interior should locate itself between the side
panels:

```
   side panel A     brace          side panel B
       |              |                  |
       v              v                  v
   +-----+    +----------------+      +-----+
   |     |    |                |      |     |
   | dado| =>>|     brace      |<<=== |dado |
   |     |    |                |      |     |
   +-----+    +----------------+      +-----+

   The brace ends are sized to slot into the dadoes on the inner
   faces of the side panels. Brace location is locked by the dado
   positions, which are referenced from the panel datum.
```

The brace has **tab ends** that fit the dadoes; this constrains both
its X position (depth into cabinet) and Z position (height). Glue is
optional for the brace ends — the dado captures them mechanically.

## 5. Key features for "only one way to assemble"

A symmetric cabinet can be assembled with panels swapped — front
panel where the back goes, etc. Sometimes that's fine; sometimes a
panel has different features (a port on the back, a driver cutout
on the front) that make the swap wrong.

**Key features** are intentional asymmetries that prevent wrong-way
assembly:

| Asymmetry                       | What it prevents                |
|---------------------------------|-----------------------------------|
| Offset dado position (left side ≠ right side) | Swapping side panels |
| Slightly different brace cutout sizes | Inserting brace upside-down |
| Notch at top corner of one side panel | Inverting a panel       |
| Different groove depth per side  | Mixing top/bottom panels  |

For a cabinet with a tweeter offset on the baffle, the baffle is
already asymmetric; key it to one side of the cabinet so the
listener faces the offset correctly when assembled.

## 6. Geometry that works in CAM

CAM (the toolpath generation step) imposes a few constraints on
locating features:

- **Internal corners ≥ tool radius + clearance** — see
  `manufacturability.md`. Add dog-bone reliefs for sharp internal
  90° corners in dadoes.
- **Maximum depth per pass**: typical 1/2 × tool diameter per pass
  for hardwood, 1× for plywood/MDF. Deep dadoes need multi-pass
  programs.
- **Tabs to hold panel** — when cutting the panel's outline last,
  leave 0.5-1 mm tabs at multiple points so the panel doesn't move.
  Cut tabs after CAM completes by hand.
- **Climb vs conventional milling** affects edge quality on the
  visible face; tell CAM to climb-mill the visible faces and
  conventional-mill the others.

## 7. Sliding dovetail (the strongest groove)

A **sliding dovetail** is a groove with a trapezoidal cross-section,
slightly tapered. Tang-on the mating panel matches the trapezoid.
The joint can only be assembled by **sliding** the mating panel into
the groove from one end — once seated, it cannot pull straight out.

Cross-section:
```
      /‾‾‾‾‾‾‾\
     /          \      <-- dovetail bit angle (10° typical)
    /            \
   /              \
   ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾   <-- panel face
```

Pros: very strong; mechanically locked in tension perpendicular to
the slide direction. Won't pull apart without breaking the wood.

Cons: requires a dovetail router bit (1/2" 10° is common); the
mating panel's tongue must be cut to match the bit angle exactly.
Tighter tolerance than a straight dado.

Use case: a removable internal brace that you want to be able to
slide in for service. Or a cabinet back panel that locks in place
along one axis.

## 8. Speaker-cabinet worked example

For the bookshelf cookbook with 18 mm MDF, the parametric design
adds the following to the model:

```python
# Locating-feature parameters
panel_t                  = 18 mm
dado_clearance           = 0.05 mm
groove_width             = panel_t + dado_clearance   # 18.05 mm
groove_depth             = 9 mm                        # 0.5 × panel_t

# Side panels: bottom edge tabs that mate with bottom panel's dadoes
side_panel_bottom_tab_w  = panel_t
side_panel_bottom_tab_d  = groove_depth - 0.5 mm       # bottoms out short

# Bottom panel: two perpendicular dadoes
bottom_panel_dado_inset  = panel_t                     # dado inset = panel thickness
bottom_panel_dado_length = baffle_w_target - 2*panel_t

# Front/back baffles: rabbet on the four inner edges of sides+top+bottom
baffle_rabbet_depth      = panel_t / 2
baffle_rabbet_width      = panel_t + dado_clearance

# Brace: tabs at each end that fit into side-panel dadoes (which are at
# the brace position).
brace_side_dado_y        = baffle_h_target / 2
brace_end_tab_h          = panel_t
brace_end_tab_d          = groove_depth - 0.5 mm
```

CAM outputs:

- Bottom panel DXF: outline + 2 dadoes for the side tabs + rabbet at the front and rear edges.
- Top panel DXF: same.
- Side panel DXF: outline + bottom tab profile + top tab profile + middle dado (for brace) + rabbet at front and rear edges.
- Front baffle DXF: outline (no dadoes — it fits in the rabbets).
- Rear baffle DXF: same.
- Brace DXF: outline with tab profile at each end.

Assembly sequence (no clamps required for primary alignment):

1. Bottom panel down.
2. Side panels slide into bottom-panel dadoes; PVA on tab faces.
3. Brace slides into the side-panel dadoes at mid-height; PVA on tab faces.
4. Top panel drops onto top-of-side tabs; PVA on tab faces.
5. Front baffle slides into the rabbet on the visible side; PVA on rabbet.
6. Rear baffle (or removable back) into the rear rabbet.

Total time saved per cabinet (vs. butt-joint with clamping): 30-60 minutes
of clamp setup and verification. Result: square cabinet first time.

## 9. Common pitfalls

- **Dado too tight**: panel binds before bottoming out. 0.05 mm
  clearance is the sweet spot for slip-fit. 0 mm fits work only
  with perfect CNC and perfect material thickness — rare.
- **Dado depth equal to panel thickness**: the carrying panel is
  weakened in line with the dado. Use 1/3 to 1/2 depth.
- **No dog-bone reliefs**: sharp internal corners can't be cut by a
  round-end mill; mating tabs won't seat fully.
- **Forgetting that MDF compresses**: dadoes in MDF deform under PVA
  glue pressure. Don't rely on press-fit alone.
- **Wrong-way assembly with no keying**: cabinet can be put together
  inside-out. Add asymmetric features.
- **Designing the joint without checking CAM accessibility**: the
  CNC needs lead-in/lead-out room. Internal dadoes that don't reach
  the panel edge need to be cut as pockets, with associated tool
  paths.
- **Stopped dadoes with sharp ends**: the rounded end of the
  stopped dado (left by the cutter) must be accommodated by the
  mating tab — either by rounding the tab end or by adding a
  dog-bone at the dado end.

## 10. When NOT to use locating features

- For one-off prototypes where you'll iterate the design and rebuild
  the cabinet several times: butt joints + biscuits are faster.
- For very small parts (< 50 mm) where dado depth is a large
  fraction of the panel.
- For materials that don't machine well: thin plywood (< 6 mm)
  doesn't hold deep dadoes; MDF crumbles at thin tab ends.
- For visible joinery where butt-joint aesthetics are preferred.

## 11. Comparing to other assembly aids

| Method                  | Self-aligning? | Cost                         |
|-------------------------|----------------|-------------------------------|
| Butt + biscuits          | Partial        | Biscuit jointer (~$200)       |
| Butt + dowels            | Yes (linear)   | Dowel jig (~$50)              |
| Domino (loose tenon)     | Yes            | Festool Domino ($1000)        |
| Pocket-screw (Kreg)      | No (mechanical) | Kreg jig (~$50)              |
| Dado / rabbet / groove   | Yes            | Just the CNC, already paid for |
| Sliding dovetail         | Yes (very strong) | Dovetail bit (~$30)        |
| Locking miter            | Yes            | Lock-miter bit (~$80)        |
| Drawer lock              | Yes            | Drawer-lock bit (~$60)       |

For CNC-built cabinets, dadoes/rabbets are essentially free — the
CNC is already cutting the panel outlines, and adding a dado is
just another toolpath. Compare to biscuits or dominos which require
a separate tool, jig, and operation.

## Cross-references

- `manufacturability.md` — tool diameter and dog-bone relief rules.
- `joints-by-process.md` — process-specific joint geometry.
- `manufacturing-offsets.md` — clearance for tolerance stack-up.
- `parametric-modeling.md` — parameterizing joinery.
- `speaker-cabinet-cad.md` — where dadoes show up in the cabinet
  model.
- `cookbooks/speaker-cabinet-2way.md` — full worked example.
