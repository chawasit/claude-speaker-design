# Manufacturing Offsets and Process-Aware Parameters

The single most common reason a part doesn't fit on first build:
**the CAD model used nominal dimensions, but the manufacturing process
added or subtracted material between the nominal and the final
part.** Every process — CNC, laser, FDM, SLA, sheet metal, plus the
finish coats applied after — has predictable offsets. Bake them into
your parameter table or you'll be re-cutting wood.

This file covers what offsets apply per process, the
process-aware parameter pattern that handles them cleanly, the
stack-up math when offsets compound, and what CAM can vs. cannot
compensate for.

## 1. The as-designed vs as-built gap

```
   CAD nominal                                       Final part
       |                                                  ^
       |                                                  |
       v                                                  |
   kerf comp ─┐                                           |
   tool radius │                                          |
   shrinkage ─┤                                           |
   chip-out ─┤        machining / printing  --------------+
   bridge sag ─┤                                          |
   first-layer ─┤                                         |
   spring-back ─┘                                         |
                                                          |
   ── then ──                                              |
                                                          |
   sanding    ─┐                                          |
   sealer     ─┤                                          |
   primer     ─┤   finishing      ----------------------+
   topcoat    ─┤
   veneer     ─┤
   anodize    ─┘
                                                          |
   ── then ──                                              |
                                                          |
   humidity   ─┐                                          |
   thermal    ─┤   service       -----------------------+
   creep      ─┘
```

Every step adds or removes material. The disciplined response: don't
treat CAD as "the final geometry" but as "nominal + named offsets
that compose to the actual modeled geometry."

## 2. Offsets by process

For each process, the typical sources of deviation from CAD nominal.

### FDM 3D printing (PLA, PETG, ASA, ABS, PC)

| Offset                       | Magnitude         | Direction                              |
|------------------------------|--------------------|-----------------------------------------|
| First-layer compression      | +0.10 to +0.15 mm  | Bottom face is larger than nominal     |
| XY shrinkage during cool     | 0.1-0.5 %          | Bulk part is smaller than nominal      |
| Hole shrinkage               | -0.10 to -0.20 mm  | Holes print smaller than CAD            |
| Outside slot/tab oversize    | +0.10 to +0.20 mm  | Outside walls print slightly fatter    |
| Bridge sag                   | +0.10 to +0.50 mm  | Long bridges sag downward into pocket  |
| Overhang slope               | +0.10 to +0.30 mm  | <45° overhangs droop                   |
| Layer adhesion gap           | 0 to 0.05 mm       | Z-stack of layer lines visible          |

**Process-aware parameters:**
```python
fdm_first_layer_compensation = 0.10  # bottom face larger
fdm_hole_oversize             = 0.20  # model holes 0.2 mm larger than nominal
fdm_outside_undersize         = 0.15  # model outside walls 0.15 mm smaller
fdm_xy_scale                  = 1.003 # 0.3% to compensate shrink
```

### SLA / DLP 3D printing (UV resin)

| Offset                       | Magnitude         | Notes                                   |
|------------------------------|--------------------|------------------------------------------|
| Cure shrinkage               | 0.5-1.5 %          | Bulk shrink during UV cure              |
| Z-axis pixel quantization    | ±25 µm             | Layer height limit                       |
| Wash residue removal         | -0.02 to -0.05 mm  | IPA wash dissolves uncured surface       |
| Post-cure thermal expansion  | +0.05 to +0.10 mm  | Resins warm during UV post-cure          |
| Tearing at unsupported areas | localized 0.1 mm   | Critical at small features               |

The slicer software usually compensates cure shrinkage automatically;
double-compensating in CAD over-corrects. Verify by measuring the
first print.

### CNC routing (wood / MDF / plywood)

| Offset                       | Magnitude         | Notes                                   |
|------------------------------|--------------------|------------------------------------------|
| Tool radius (internal corner) | ≥ tool_dia / 2    | Internal corners can't be sharper       |
| Kerf (cut width)              | = tool_dia        | CAM handles; CAD just designs final geometry |
| Climb-mill chip-out           | 0.05-0.1 mm tear  | Depends on cut direction vs grain        |
| End-grain chip-out (plywood)  | 0.5-1.0 mm        | Use a backer board to control            |
| Pocket-depth tolerance        | ±0.1 mm            | Machine Z-axis precision                 |
| Climb-mill face roughness     | 0.05-0.2 mm Ra    | Finer with finishing pass                |

**Process-aware parameters:**
```python
cnc_tool_dia                = 6.0       # standard 1/4" router
cnc_internal_corner_r       = cnc_tool_dia/2 + 0.5  # tool radius + clearance
cnc_chip_out_end_grain      = 0.5       # add to end-grain cut dimensions
cnc_pocket_depth_tolerance  = 0.1       # account for CAM Z-step
```

### CNC milling (metal: aluminum, steel)

| Offset                       | Magnitude         | Notes                                   |
|------------------------------|--------------------|------------------------------------------|
| Tool radius                  | = tool_dia / 2     | Same as wood                             |
| Thermal growth during cut    | +0.02 to +0.05 mm  | Aluminum grows while cutting             |
| Drilled hole oversize        | +0.05 mm            | Drill walks; specify reamer for ±0.01    |
| Surface roughness            | 0.4-1.6 µm Ra     | Per spec                                 |
| Burr at sharp edges          | 0.05-0.2 mm        | Deburr in post-process                   |

### Laser cutting

| Offset                       | Magnitude         | Notes                                   |
|------------------------------|--------------------|------------------------------------------|
| Kerf width (acrylic)         | 0.10-0.20 mm       | Material- and speed-dependent             |
| Kerf width (plywood ≤6 mm)   | 0.20-0.40 mm       | Wider than acrylic, charred edge          |
| Beam taper                   | 0.05-0.10 mm        | Top of cut wider than bottom              |
| Heat-affected zone           | 0.1-0.5 mm char    | Plywood char (sand for clean assembly)    |
| Material warp                | 0.5-2 mm over 1 m   | Stress release in thin sheet              |

**Process-aware parameters:**
```python
laser_kerf_acrylic_3mm      = 0.10
laser_kerf_acrylic_6mm      = 0.15
laser_kerf_plywood_3mm      = 0.25
laser_kerf_plywood_6mm      = 0.35
laser_char_allowance        = 0.5   # to sand off the dark band
```

**Direction rule**: outside cuts (the perimeter, tab) **shrink** by
half the kerf on each side; inside cuts (slot, hole) **grow** by half
the kerf on each side. CAM handles this if you specify the kerf;
sketch-and-export skips CAM and needs CAD-side compensation.

### Waterjet

| Offset                       | Magnitude         | Notes                                   |
|------------------------------|--------------------|------------------------------------------|
| Kerf width                   | 0.8-1.2 mm         | Wider than laser; abrasive-dependent     |
| Taper                        | 0.5-2° (Δ ≈ 1 mm)  | Pierce side wider than exit              |
| Edge quality                 | 1.6 µm Ra typical   | Smooth for thicker plate                  |

### Sheet metal + brake bending

| Offset                       | Magnitude         | Notes                                   |
|------------------------------|--------------------|------------------------------------------|
| K-factor (neutral axis)      | 0.33-0.50          | Bend allowance per K · T                  |
| Spring-back                  | 1-3° steel, 3-5° Al | Over-bend by this much                   |
| Material flow at inside bend | 0.5-1.0 mm        | Use bend relief slots                     |
| Sheet thickness tolerance    | ±5 %                | Typical cold-rolled                       |

Bend allowance:
```
BA = 2π · (R + K · T) · (angle / 360°)
```
where R = inside bend radius, K = K-factor, T = material thickness.

### Hand finishing (sand / paint / lacquer)

| Step                        | Δ per face / coat   | Stack-up                                |
|-----------------------------|----------------------|------------------------------------------|
| Sanding (220 grit)          | -0.05 to -0.10 mm    | Single pass; finer grits less            |
| Sanding sealer / shellac    | +50 µm / coat        | Usually 1-2 coats                         |
| Primer / undercoat          | +50-100 µm / coat    | Usually 2-3 coats                         |
| Nitrocellulose lacquer      | +25-50 µm / coat     | 3-5 coats for piano gloss                |
| Polyurethane                | +50-100 µm / coat    | 2-3 coats                                  |
| Veneer + glue               | +500-1000 µm        | Single application                        |
| Paint (waterborne)          | +25-50 µm / coat    | 2-3 coats                                  |
| Powder coat                 | +80-120 µm           | Single bake                                |
| Anodize Type II             | +5-25 µm             | (penetrates and grows from surface)      |
| Anodize Type III (hardcoat) | +25-50 µm             | Up to 100 µm                              |

For a typical **piano-black on MDF** finish (sanding sealer × 2, black
primer × 2, color × 3, clear × 5):
```
total_buildup = 2*50 + 2*75 + 3*40 + 5*40 = 470 µm per face
```

For a **clear lacquer on plywood** (sealer × 1, lacquer × 3):
```
total_buildup = 50 + 3*40 = 170 µm per face
```

A driver cutout designed at exactly the manufacturer's "cutout
diameter" will bind after a piano-gloss finish — the diameter
effectively shrinks by 2 × 470 µm = ~1 mm. Add `2 × finish_buildup`
radial clearance to the cutout in CAD.

### Service-time offsets (humidity, thermal)

These don't apply at build time but do affect long-term fit:

| Material            | Swell per 10% RH     | CTE (µm / m / °C)    |
|----------------------|----------------------|------------------------|
| MDF                  | +0.20 % across grain | 4-8                    |
| Plywood              | +0.05 % across grain | 4-6                    |
| Solid wood (radial)  | +0.10 % across grain | 4-6                    |
| Solid wood (tangential) | +0.20 % across grain | 4-6                |
| Aluminum             | 0                    | 23                     |
| Steel                | 0                    | 11-13                  |
| Acrylic              | 0                    | 70-90                  |
| PLA / PETG / ABS     | 0                    | 70-90                  |

For outdoor or attic-mounted assemblies spanning two materials, gap
allowances must accommodate the larger CTE × span × ΔT product. A
1 m aluminum panel rivet-bolted to a 1 m wood frame moves 18 mm
relative at 80°C swing — slotted holes required.

## 3. Tolerance stack-up

When multiple parts assemble, the worst-case error is the **sum** of
individual tolerances (assuming worst-case orientation). For mating
features that must clear or fit:

```
required_clearance ≥ Σ |tolerance_i|
```

**Example: driver flange seating in baffle cutout.**

Sources of tolerance:
- Manufacturer flange OD: ±0.5 mm (datasheet)
- CNC baffle cutout: ±0.1 mm (router precision)
- Finish coats (lacquer, both sides): ±0.05 mm per side × 2 = ±0.1 mm
- Driver gasket compressed: +0.5 mm
- Cabinet panel skew: ±0.2 mm

Worst-case stack: 0.5 + 0.1 + 0.1 + 0.5 + 0.2 = **1.4 mm radial**.

Cutout in CAD = flange_nominal + 2 × 1.4 = nominal + 2.8 mm. Round
to 3 mm for safety.

The "statistical" (RSS) stack-up sums the squares:
```
typical_clearance ≈ √(Σ tolerance_i²) = √(0.25 + 0.01 + 0.01 + 0.25 + 0.04) ≈ 0.75 mm
```

Use RSS for typical-case sizing, worst-case for "must never fail"
mating. For a one-off cabinet build, worst-case; for high-volume,
RSS plus a safety factor.

## 4. The process-aware parameter pattern

The CAD model's parameter table separates into **three sections**:

### Section A — Design intent (the dimensions you actually want)

These describe the final-product spec, before any process or
finishing offsets. From the speaker-design cookbook:

```python
# Design intent
baffle_w_target           = 200 mm   # the cabinet's actual outside width
baffle_h_target           = 350 mm
depth_target              = 280 mm
panel_t_nominal           = 18 mm
internal_vb_target        = 12.3 L   # acoustic spec
driver_cutout_d_target    = 152 mm   # datasheet
port_dia_target           = 60 mm
```

### Section B — Process compensation

Per-process offsets. **Only one process is active per part**; switch
processes by editing this section.

```python
# Process compensation for CNC plywood + lacquer finish:
cnc_tool_dia              = 6 mm
cnc_internal_corner_r     = 3 mm + 0.5 mm    # tool radius + clearance
cnc_chip_out_end_grain    = 0.5 mm
finish_buildup_per_face   = 0.4 mm            # 3 coats lacquer
driver_gasket_t           = 0.5 mm

# If switching to a 3D-printed prototype:
# fdm_first_layer_compensation = 0.10 mm
# fdm_hole_oversize            = 0.20 mm
# fdm_xy_scale                 = 1.003
# finish_buildup_per_face      = 0 mm        # no finish on FDM
```

### Section C — Derived (the dimensions modeled in CAD)

Combine A + B:

```python
# Derived for CAD model
internal_w        = baffle_w_target - 2 * panel_t_nominal
internal_h        = baffle_h_target - 2 * panel_t_nominal
internal_d        = depth_target    - 2 * panel_t_nominal
driver_cutout_d   = driver_cutout_d_target + 2 * finish_buildup_per_face \
                    + 2 * driver_gasket_t + 1 mm   # tolerance margin
port_baffle_hole  = port_dia_target + 0.4 mm       # FDM port fits with 0.2 mm clearance per side
internal_corner_r = cnc_internal_corner_r
```

Now:
- Changing **finish from lacquer to oil** → edit `finish_buildup_per_face` to ~0.05 mm. Driver cutout shrinks automatically.
- Switching cabinet from CNC plywood to **FDM prototype** → swap Section B values. Model rebuilds with FDM-appropriate offsets.
- Changing **driver model** → edit `driver_cutout_d_target` (Section A). Process compensation stays untouched.

This separation makes the CAD model **portable across processes**
and **legible** — anyone reading the parameter table can tell what is
design intent vs what is process workaround.

## 5. What CAM compensates vs what CAD must compensate

The boundary matters: applying the same offset twice (CAM + CAD)
over-shrinks the part. Applying neither leaves it under-sized.

| Offset                              | Who handles it       |
|-------------------------------------|------------------------|
| CNC/laser tool kerf (cut width)     | CAM (if tool specified) |
| Internal corner radius              | CAD (geometry constraint) |
| Sheet-metal bend allowance / K-factor | CAM (most CAM packages) |
| Mating clearance for assembly        | CAD                    |
| Finish coat buildup                  | CAD                    |
| Material swelling/shrinkage          | CAD                    |
| Tolerance stack-up                   | CAD                    |
| FDM shrinkage scale                  | Slicer (treat as CAM)   |
| FDM hole oversize                    | CAD                    |
| FDM first-layer compression          | CAD                    |
| SLA cure shrinkage                   | Slicer (treat as CAM)   |
| Laser beam taper                     | CAD (if precise) or accepted |

**Rule of thumb**: if it changes the **path the cutter follows**,
CAM handles it. If it changes the **final geometry seen by the
user**, CAD handles it. When in doubt, ask the operator before
applying both layers.

## 6. Verification: as-built vs as-designed

After fabrication of the first part, measure and compare:

| Measurement                  | Target           | Common failure mode                  |
|------------------------------|-------------------|--------------------------------------|
| Mating fits                  | Slip-fit, no bind  | Forgot kerf comp or finish buildup   |
| Squareness                   | < 1 mm over 1 m    | Panel skew during glue-up             |
| Internal volume              | ±2 % of target     | Finish coats or panel swelling        |
| Joint gap                    | < 0.1 mm consistent | Joinery cut accuracy                  |
| Driver flush-mount           | ±0.5 mm seat       | Cutout depth wrong                    |

Record the as-built vs as-designed gap. **Feed it back into the
parameter table** for the next build:

```python
# After first cabinet:
# - driver cutout was 0.3 mm too tight after lacquer → +0.3 mm
# - panel skew added 0.2 mm to depth → no action; cabinet was within spec
# - internal Vb came out 11.8 L not 12.3 L → CNC tool slightly under nominal

cnc_actual_tool_dia_correction  = -0.1 mm    # tool measured 5.9 mm not 6.0
driver_cutout_extra_clearance   = 0.3 mm
```

The next cabinet is built with the corrected parameters and meets
the design spec on the first try.

## 7. Speaker-cabinet example (worked)

For the bookshelf cookbook (CNC plywood shell + lacquer + FDM port +
FDM terminal cup), the parameter section becomes:

```python
# --- A. Design intent ---
baffle_w_target       = 200 mm
baffle_h_target       = 350 mm
depth_target          = 280 mm
panel_t_nominal       = 18 mm
internal_vb_target    = 12.3 L

driver_cutout_d_target = 152 mm        # datasheet
driver_flange_d_target = 178 mm
port_dia_target        = 60 mm
port_length_target     = 163 mm        # acoustic spec

# --- B. Process compensation ---
# CNC plywood for the shell:
cnc_tool_dia                  = 6 mm
cnc_internal_corner_r         = cnc_tool_dia/2 + 0.5 mm
cnc_chip_out_end_grain        = 0.5 mm

# Lacquer finish (sealer × 2 + lacquer × 3):
finish_buildup_per_face       = 0.20 mm      # 2 × 50µm + 3 × 40µm

# FDM port flare and terminal cup:
fdm_hole_oversize             = 0.20 mm
fdm_outside_undersize         = 0.15 mm

# Driver-gasket compression:
driver_gasket_t               = 0.5 mm

# Tolerance margin (stack-up):
mating_clearance              = 1.0 mm

# --- C. Derived ---
internal_w           = baffle_w_target - 2 * panel_t_nominal
internal_h           = baffle_h_target - 2 * panel_t_nominal
internal_d           = depth_target    - 2 * panel_t_nominal

driver_cutout_d      = driver_cutout_d_target \
                        + 2 * finish_buildup_per_face \
                        + 2 * driver_gasket_t \
                        + mating_clearance         # = 152 + 0.4 + 1.0 + 1.0 = 154.4 mm

driver_flange_d_recess = driver_flange_d_target + 2 * finish_buildup_per_face \
                          + 2 * mating_clearance   # = 178 + 0.4 + 2 = 180.4 mm

port_baffle_hole     = port_dia_target + fdm_outside_undersize \
                        + mating_clearance         # = 60 + 0.15 + 1.0 = 61.15 mm
                                                   # (FDM port outside ≈ 60 - 0.15 = 59.85; fits with ~1.3 mm clearance)

internal_corner_r    = cnc_internal_corner_r       # = 3.5 mm
```

If the next build switches to a **3D-printed prototype cabinet**
(instead of CNC plywood), only Section B changes:

```python
# All CNC compensation → 0
# Add FDM compensation for the shell:
fdm_first_layer_compensation = 0.10 mm
fdm_xy_scale                 = 1.003
fdm_outside_undersize        = 0.15 mm
# Finish: bare FDM, no coats
finish_buildup_per_face      = 0 mm
```

The Section C formulas continue to work; the model rebuilds with
the new offset values; all derived dimensions update.

## 8. Common pitfalls

- **Modeling at nominal**: parts don't fit; redo. Always include at
  least mating clearance + finish allowance.
- **Double-compensation**: applying kerf in BOTH CAM and CAD →
  over-shrinks. Pick one layer per offset.
- **Hard-coded literals in 12 sketches**: scattered "0.2 mm" values
  that you can't change globally. Always replace with named parameter.
- **Single offset for multiple processes**: a "kerf" parameter that
  works for laser but is wrong for CNC. Separate by process or by
  feature.
- **Ignoring finish on cabinets**: piano-gloss finish eats 1 mm of
  cutout diameter. Drivers bind.
- **Confusing scale and offset**: FDM shrinks by 0.3% (scale, affects
  bulk) AND oversizes holes by 0.2 mm (offset, affects features).
  Both apply; they're independent.
- **No verification loop**: building part 2 with the same wrong
  parameters as part 1. Measure and update.
- **Missing CTE on outdoor / car / unconditioned spaces**: aluminum
  bracket bolted to plywood at -10°C bottoms out at 40°C.

## 9. Quick checklist before fabrication

Before exporting the first STEP / DXF / STL:

- [ ] All design-intent dimensions in named parameters (Section A).
- [ ] Process-compensation parameters in their own section (B).
- [ ] Derived parameters express the relationship (C).
- [ ] Each mating fit includes appropriate clearance (worst-case or
      RSS stack-up depending on stakes).
- [ ] Each finished face includes finish buildup compensation.
- [ ] Internal corner radii respect tool diameter.
- [ ] CAM operator briefed on kerf-comp assumption.
- [ ] Test cut planned for the first part of a new design.
- [ ] Plan in place to update parameters from first-build measurements.

## Cross-references

- `manufacturability.md` — process tolerance tables, joinery, kerf
  general.
- `joints-by-process.md` — process-specific joint geometry.
- `fasteners-and-finishing.md` — finish coat buildup per material.
- `parametric-modeling.md` — the parameter-driven design philosophy
  that makes this approach work.
- `speaker-cabinet-cad.md` — where these offsets show up in the
  cabinet model.
- `cookbooks/speaker-cabinet-2way.md` — the integrated example.
