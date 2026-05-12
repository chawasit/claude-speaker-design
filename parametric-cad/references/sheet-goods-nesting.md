# Sheet Goods and Panel Nesting

Speakers built from plywood, MDF, or HDF are essentially flat-pack
furniture: six (or more) panels, each cut from a larger sheet. The
nesting problem is **fitting all the panels onto the minimum number
of sheets**, with grain orientation, kerf, and tool clearance
respected.

This file covers panel preparation, nesting strategies (manual and
automated), kerf accounting, joinery-cut placement, and outputting
DXFs the fabricator can use directly.

## 1. Standard sheet sizes

| Material        | Standard sheet sizes (mm)                          |
|-----------------|-----------------------------------------------------|
| MDF             | 1220 × 2440 (4'×8'); 1525 × 3050 (5'×10')          |
| Baltic birch ply| 1525 × 1525 (5'×5'); 1220 × 2440                   |
| HDF             | 1220 × 2440                                         |
| Plywood (CDX, oak) | 1220 × 2440                                       |
| Particle board  | 1220 × 2440                                         |
| Solid wood      | varies; usually 200–300 mm widths × 2000–3000 mm long |

For DIY cabinetry, work primarily in 1220 × 2440 sheets — the
"4×8" standard — unless your shop has a wider-bed CNC.

## 2. Per-cabinet panel set

For a typical bookshelf (200 × 350 × 280 mm external, 18 mm MDF):

| Panel        | Dimensions       | Notes                                |
|--------------|------------------|--------------------------------------|
| Front baffle | 200 × 350 mm     | driver cutouts, roundover            |
| Rear baffle  | 200 × 350 mm     | terminal cup, port, screws to split  |
| Top          | 164 × 280 mm     | (internal-fit panel)                 |
| Bottom       | 164 × 280 mm     | (internal-fit panel)                 |
| Left side    | 350 × 280 mm     | (sits flush)                         |
| Right side   | 350 × 280 mm     |                                      |
| Brace        | 244 × 164 mm     | with two clearance holes             |

Total area for one cabinet: ~0.85 m². A 1220×2440 sheet = ~3.0 m². So
**3-4 cabinets fit on one sheet** with reasonable nesting (allowing
~10 % waste).

For a stereo pair: nest both cabinets together. Often more efficient
than nesting one at a time.

## 3. Grain orientation

Plywood and solid wood have **directional grain**. Bending stiffness
is higher with the grain than across it; for cabinet panels, this
matters for panel resonance. For a 350 × 280 mm side panel, choose
grain direction to maximize the longer span's stiffness:

- **Plywood**: face-veneer grain typically runs along the long
  dimension by convention; this is usually the right orientation
  for cabinet sides.
- **Solid wood**: grain parallel to the long edge for best
  stiffness.

For MDF and HDF: **no grain**, so orientation doesn't matter
mechanically. Decorative finishes (veneer over MDF) reintroduce a
grain choice — match grain across joining panels for aesthetics.

When nesting, **lock grain direction** for each panel before
optimizing the layout. Rotating a panel 90° to fit a tighter layout
is fine for MDF, not for plywood.

## 4. Kerf accounting

The cutter (router bit, saw blade, laser) removes material equal to
its diameter (router/blade) or width (laser kerf).

| Cutter             | Kerf width      | Notes                                  |
|--------------------|-----------------|----------------------------------------|
| 6 mm router bit    | 6 mm radial     | each cut is 6 mm wide                 |
| 3 mm router bit    | 3 mm radial     | detail / inside corners                |
| Table saw (combo)  | 3.2 mm (typical)| varies by blade                       |
| CNC table saw      | 4 mm (typical)  | thicker blade for accuracy            |
| Laser (plywood ≤ 6 mm) | 0.15–0.3 mm | depends on power, speed              |
| Waterjet            | 1 mm            | wider than laser                       |

For nesting calculations, **add the kerf to each panel's
dimensions** on the cut side. A 200 × 350 mm panel cut by a 6 mm
router bit needs 206 × 356 mm of sheet (3 mm radial on each cut).
Nesting tools typically handle this automatically — just specify the
kerf in the tool settings.

### When CAM handles kerf vs when you do

- **CAM software offsets toolpaths inside or outside the sketched
  line.** The CAD model is the **final geometry**. CAM compensates.
  Recommended approach for CNC.
- **Pre-offset in CAD.** The sketched line is already adjusted for
  kerf. Used when the fabricator's CAM doesn't know your kerf, or
  for laser-cut DXFs that get cut "as-drawn."
- **Test cut**. Cut a known dimension on the actual material with
  the actual tool, measure, refine. Mandatory for any new
  material/tool combination.

## 5. Joinery-cut placement

For joinery patterns (rabbet, dado, etc.) on edges of panels, the
DXF must include those cuts. Two approaches:

### Approach A: Each panel exported with its full feature set

Export the panel's outline + interior cuts + edge profile (e.g.
rabbet) as a single DXF. The CAM operator routes the outline last,
then performs the inner cuts.

### Approach B: Joinery in a separate operation

Outline DXFs only; joinery cuts done by a separate setup (template
+ router-table) or a separate CAM file. Simpler DXF but more shop
setups.

For DIY, Approach A is faster overall. For high-volume production,
B may be more efficient.

## 6. Nesting tools

| Tool                     | Approach                              | Cost              |
|--------------------------|---------------------------------------|--------------------|
| Manual (graph paper)     | DIY layout                            | free               |
| OpenScale (DXF arrangement) | semi-automated                      | free               |
| SVG-Nest (web-based)     | optimization, web upload              | free               |
| Deepnest                 | desktop, optimization                  | free, open-source  |
| OptiCutter               | shop / production                     | paid               |
| Sigmanest                | industrial CNC                         | paid               |
| Fusion 360 Nest          | inside Fusion, paid add-on            | paid               |

For DIY: **Deepnest** or **SVG-Nest** are the standard free options.
Input: DXF files of each panel. Output: nested DXF for one or more
sheets, with kerf clearance.

A typical Deepnest workflow:

1. Export each cabinet panel as DXF from CAD.
2. Open Deepnest, import all DXFs.
3. Set sheet size (1220 × 2440), kerf (default 6 mm for router,
   0.2 mm for laser).
4. Lock rotation for grain-sensitive panels.
5. Run optimization. Get a nested layout.
6. Export the nested DXF.
7. Send the nested DXF to the fabricator or load into the CNC.

For ~10 panels (one cabinet) nested on one sheet, optimization
typically returns ~90 % material utilization.

## 7. Manual nesting heuristics

If you don't have nesting software, manual layout works for small
panel counts:

1. **Sort panels** by largest dimension descending.
2. **Place largest panels first**, along one edge of the sheet.
3. **Fill gaps** with smaller panels.
4. **Rotate** small panels 90° to fit if grain doesn't matter.
5. **Common edges**: place panels so cuts can be shared (one cut
   defines two panel edges).

A common pattern for a bookshelf set: place the two long sides
along the long edge of the sheet (parallel), nest the rear baffles
between them, nest the front baffles between, and use the remaining
strip for top/bottom/brace.

For a stereo pair (2 cabinets), this typically fills one 1220 × 2440
sheet at ~80 % utilization. Three cabinets per sheet at ~85 %. Four
at ~90 %.

## 8. DXF export conventions

Most CNC operators want DXFs in **AutoCAD R12 or R14** flavor, in
**millimeters**, with all geometry on a **single layer** (or layers
named meaningfully for cut depth — see below).

### Layer conventions for multi-pass CAM

```
Layer "OUTLINE"        — outer cut (cuts through panel)
Layer "CUTOUT"         — through-holes (driver, port)
Layer "POCKET_5MM"     — flange recess at 5 mm deep
Layer "POCKET_4MM"     — tweeter flange recess at 4 mm deep
Layer "POCKET_8MM"     — terminal cup recess
Layer "DADO"           — joinery (rabbets, dadoes) at specified depth
Layer "PILOT_3MM"      — pilot holes for screws
```

The CAM operator assigns toolpath per layer; depth either from layer
name or per-operation. Document the convention in a `README.txt` in
the DXF folder.

### What MCP tools usually produce

Most CAD MCPs' `export_dxf` writes a single layer with all geometry.
You may need to:

1. Export the full-cabinet STEP from the MCP.
2. Open in a 2D-capable tool (LibreCAD, AutoCAD, QCAD, DraftSight).
3. Project to a flat plane per panel; rearrange to layers; save as
   DXF.

Tedious but unavoidable until MCP servers improve in this area.

## 9. Material-shopping list per cabinet

For the bookshelf cookbook (one cabinet, 18 mm MDF):

| Item                    | Quantity | Notes                                |
|--------------------------|----------|---------------------------------------|
| 18 mm MDF sheet          | ~0.85 m²  | 4 cabinets per 1220×2440 sheet       |
| Brace stock (18 mm)     | 0.04 m²  | from cabinet sheet                    |
| Port tube material      | 1 each    | PVC pipe Ø60 mm × 200 mm; or 3D-printed |
| Hardware: M4 screws     | 12        | Removable back × 8; brace × 4         |
| Heat-set inserts M4     | 12        | Match screws                          |
| Wood glue (PVA)         | 100 ml   | Titebond II or equivalent             |
| Silicone (neutral cure) | 100 ml   | Sealing seams                         |
| Damping material        | 200 g    | Long-fiber wool or polyester batting  |
| Driver (woofer)         | 1         |                                       |
| Driver (tweeter)        | 1         |                                       |
| Terminal cup            | 1         |                                       |
| Crossover components    | varies   | See crossover cookbook                |
| Foam gasket strip       | 1.2 m    | Removable-back perimeter              |

Multiply by 2 for a stereo pair.

## 10. Cut order in CAM

For each panel, the CAM toolpath order typically is:

1. **Pre-drill pilot holes** (small bit).
2. **Pocket / recess cuts** (medium bit, at depth).
3. **Through-cutouts** for driver, port, terminal (medium bit through).
4. **Outline cut** last (any bit, cuts through, releases the panel).

Cutting the outline first releases the panel from the sheet — it
moves under the cutter, ruining subsequent operations. **Tabs**
(thin uncut sections in the outline) hold the panel in place during
pocket/cutout operations; the operator hand-cuts these after.

A nested layout includes tabs by default in modern CAM software.

## 11. Quick sanity checks

Before sending DXFs to the shop:

- [ ] Units are millimeters (not inches, not arbitrary).
- [ ] Geometry is closed (no open contours that confuse the
      toolpath).
- [ ] All inner corners ≥ tool radius.
- [ ] Material thickness in the DXF filename or notes (so the
      operator picks the right stock).
- [ ] Visible cut depth for each layer (or single-depth simple
      file).
- [ ] Total area accounting matches the BOM material order.

## Cross-references

- `references/manufacturability.md` — kerf, tool diameter, joinery.
- `references/parametric-modeling.md` — driving panel dimensions
  from parameters.
- `references/speaker-cabinet-cad.md` — what panels are typically
  produced for a cabinet.
- `references/fasteners-and-finishing.md` — hardware BOM that the
  panels reference.
