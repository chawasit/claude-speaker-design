# Joint Design by Manufacturing Process

Different fabrication processes require fundamentally different joint
geometry. A dovetail that's trivial in CNC plywood is impractical in
FDM print; a snap-fit perfect for FDM doesn't make sense in MDF; a
tab-and-slot perfect for laser-cut acrylic is wrong for sheet metal.

This file is organized by process. For each, it covers the **tolerance
budget**, the **joint types that work**, the **geometry constraints**,
and the **adhesives / fasteners** typical for that process. The last
section covers **mixed-material joints** where two processes meet.

Pair this file with `manufacturability.md` (process tolerance table,
kerf, tool-diameter rules) and `fasteners-and-finishing.md` (M-screws,
inserts, glue, silicone).

## 1. Tolerance budget at a glance

| Process              | Practical tolerance | Suitable for         |
|----------------------|---------------------|----------------------|
| FDM 3D print         | ±0.2 mm             | enclosures, brackets, port flares |
| SLA / DLP 3D print   | ±0.05 mm            | small precision parts, gears, threaded mates |
| SLS nylon            | ±0.1 mm             | functional parts, snap-fits |
| CNC routed wood/MDF  | ±0.1 mm             | cabinet panels, baffles |
| CNC milled metal     | ±0.025 mm           | structural mounts, magnet plates |
| Laser-cut sheet (≤6 mm) | ±0.05 mm         | flat-pack panels, gaskets |
| Waterjet sheet       | ±0.1 mm             | thicker metal, stone |
| Sheet metal + brake  | ±0.5 mm at bends    | enclosures, brackets |
| FDM flexible (TPU)   | ±0.3 mm             | gaskets, hinges, isolators |

At every interface between two processes, the **looser tolerance
dominates**. Design clearances around it.

## 2. FDM 3D printing (PLA, PETG, ASA, ABS, PC)

The dominant DIY plastic process. Layer-by-layer extrusion.

### Tolerance and clearances

- **Free fit** (sliding parts): +0.3 to +0.4 mm radial clearance
  between mating surfaces.
- **Press fit** (held by friction): +0.15 to +0.2 mm clearance.
- **No clearance / "designed tight"**: -0.05 to 0 mm — only feasible
  if the part is post-machined.
- **Bridges and overhangs**: 45° rule; longer bridges sag.

### The anisotropy rule

FDM layer adhesion is much weaker than the bulk material. Pulling
layers apart needs ~30 % of the cross-section strength compared to
shearing along the layer plane.

**Design implication**: orient joint loading **in the XY plane**, not
along Z. A snap-fit oriented with its cantilever Z-axis snaps off
after 1-2 uses; the same snap-fit oriented in XY survives hundreds.

### Joint types suitable for FDM

| Joint                  | Use                                       |
|------------------------|--------------------------------------------|
| Heat-set insert + M-screw | Default for repeated assembly           |
| Captive nut pocket      | Slot in print to drop nut, bolt from other side; cheap alternative to inserts |
| Cantilever snap-fit     | One-time or low-cycle; thicken base to prevent fatigue |
| Living hinge            | Only in flexible plastics (TPU, PP); PLA fatigues in 5-10 cycles |
| Press-fit pin           | Boss-and-hole alignment; needs glue for permanence |
| Boss + pocket + adhesive | Strong permanent joint                   |
| Threaded post (FDM-printed thread) | Avoid below M5; threads strip after few cycles |

### Adhesives for FDM

| Glue                | Bond strength on FDM       | Notes                          |
|---------------------|----------------------------|---------------------------------|
| Cyanoacrylate (CA)  | Strong on PLA/PETG          | Use accelerator; gap-fill poor  |
| 2-part epoxy        | Strong, gap-filling         | 5-min for speed, 24-hr for max strength |
| Polyurethane (Gorilla) | Strong but foams         | OK for plastic-to-wood          |
| PVA wood glue       | **Does NOT bond FDM**       | Never use on plastic            |
| Solvent welding (acetone PLA, MEK PETG) | Strong | Surface finish suffers          |

### Pitfalls

- **Threading directly into FDM** — strips after 2-3 cycles even with
  M3+ screws. Use a heat-set insert.
- **Sharp internal corners** — concentrate stress at first layer
  boundaries. Add 1-2 mm fillets internally.
- **Long bridges over pockets** — sag and ruin captive-nut fits.
  Add support structures or reduce bridge length.
- **First-layer compression** — bottom of the print is slightly
  fatter than CAD; account for ±0.1 mm on bottom-face fits.

## 3. SLA / DLP 3D printing (UV resin)

Higher resolution (0.025-0.05 mm layer height). More brittle than
FDM in most resins.

### Tolerance and clearances

- **Free fit**: +0.1 to +0.15 mm.
- **Press fit**: +0.05 mm.
- **Threaded posts**: M2 and up are reliable (unlike FDM).
- **Wall thickness minimum**: 1.0 mm for structural; 0.5 mm for cosmetic.

### Joint types suitable for SLA

| Joint                  | Use                                       |
|------------------------|--------------------------------------------|
| Direct printed thread (M3+) | Works! Unlike FDM. Tap-test before relying. |
| Interference-fit boss   | Brittle — design margin; SLA cracks easily under impact |
| Tab + slot              | Tight tolerance lets these be near-zero clearance |
| Press-fit metal insert  | Pre-cooled insert tapped in carefully     |
| Threaded post + nut     | Strong, repeatable                        |

### Adhesives

- **UV resin (the same resin)**: paint joint, expose to UV — chemical weld.
- **CA**: works well on most resins.
- **Epoxy**: strong, gap-filling.
- **Heat-set inserts**: marginal — resin is brittle, doesn't deform plastically.

### Pitfalls

- **Brittle failure** — no plastic deformation warning before crack.
  Don't expect impact resistance.
- **Snap-fits crack** in flexure rather than spring back.
- **Living hinges impossible** in standard resins.
- **UV exposure post-print** — yellowing, embrittlement; coat with
  UV-resistant lacquer for outdoor use.

## 4. CNC routed wood / plywood / MDF

The cabinet-builder's standard. Subtractive cutting with end mills.

### Tolerance and clearances

- **Cabinet panel fit**: ±0.1 mm achievable; design for ±0.2 mm.
- **Driver cutout to flange**: +1-2 mm radial clearance (drivers
  vary, gasket needs space).
- **Joinery fit (rabbet, dado)**: 0 to +0.1 mm — too loose and
  glue starves; too tight and panels bind.
- **Tool diameter dictates internal corner radius**: r ≥ tool radius.

### Joint types suitable for CNC wood

| Joint                  | Strength    | Notes                                |
|------------------------|-------------|---------------------------------------|
| Butt joint + glue       | Moderate   | Cheap; needs alignment aid (biscuit, dowel) |
| Rabbet                  | High       | Hides end grain; cabinet standard     |
| Dado (groove)           | High       | Captures a panel along its edge       |
| Through-finger / box joint | Very high | CNC-cuttable; needs dog-bone reliefs |
| Lock miter              | Very high   | Specialty bit; 45° self-aligning      |
| Mortise-and-tenon       | Very high   | CNC-cut; allows mechanical fastening  |
| Pocket-screw (Kreg)     | High        | Drilled holes only; mechanical fastener |
| Domino / loose tenon    | Very high   | Mortise CNC-cut; loose tenon inserted |

### Dog-bone relief at internal corners

A 90° internal corner cannot be cut by a round end mill — it leaves
a corner radius equal to the tool radius. For mating joints (e.g. a
tab fitting into a slot), this matters: a square tab won't seat in
a slot with rounded internal corners.

**Solution**: cut "dog-bone" reliefs — small circles at the corners
that allow the mating tab to seat. The relief is invisible from the
outside (covered by the tab) and adds 0.1-0.2 mm of forgiveness.

```
   slot from above:
   +---+   +---+
   |    \ /    |
   |     O    | <-- dog-bone relief; circle radius ≥ tool radius
   |    /  \   |
   +---+   +---+
```

### Adhesives

PVA wood glue (Titebond II) is the standard. See
`fasteners-and-finishing.md` for the full table.

### Pitfalls

- **End-grain glue joints are weak**. Pre-seal MDF/plywood end-grain
  with thinned PVA before final joint application.
- **Plywood face vs edge** — face glue is strong; edge-to-edge
  needs reinforcement (biscuits, dominoes).
- **MDF cannot hold screws** in end grain without a threaded insert.
- **Plywood layer count matters** for stiffness; specify by ply count,
  not just thickness.

## 5. CNC milled metal (aluminum, steel, brass)

### Tolerance and clearances

- **General machining**: ±0.025 mm achievable; design ±0.05 mm.
- **Threaded holes**: tap-drill per `fasteners-and-finishing.md`
  pilot table.
- **Press fits (H7/p6 etc.)**: per ISO 286 standard fits.
- **Internal corners**: end mill radius dictates minimum; broached
  or wire-EDM for true sharp corners.

### Joint types suitable for metal

| Joint                  | Use                                       |
|------------------------|--------------------------------------------|
| Tapped hole + machine screw | Default for assembled metal           |
| Tongue-and-groove       | Self-aligning; common in motor structures |
| Lap joint + through-bolts | High shear strength                     |
| Welded butt / fillet    | Permanent; needs material continuity      |
| Dowel pin + bolt        | Precise alignment; dowel locates, bolt clamps |
| Press-fit bushing       | Used for bearings; H7/p6 typical fit      |
| Helicoil / wire insert  | Repair / reinforcement for stripped thread |
| Loctite + threaded fastener | Vibration-resistant; semi-permanent  |

### Adhesives for metal

- **2-part epoxy** (West, JB-Weld): strong; surface prep critical.
- **Anaerobic threadlocker** (Loctite): vibration resistance.
- **Cyanoacrylate**: small parts only; no gap.
- **Structural acrylic** (Plexus, 3M DP-810): bonds dissimilar
  metals well.

### Pitfalls

- **Galvanic corrosion** between dissimilar metals — isolate with
  rubber or paint at the joint.
- **Stripped threads in aluminum** are common; use threaded inserts
  in higher-cycle assemblies.
- **Spring-back of cold-finished steel** — design for the steady-
  state, not the as-machined dimension.

## 6. Laser-cut sheet (acrylic, plywood ≤6 mm, leather)

The flat-pack process. Cuts are very precise; kerf is the main
geometric concern.

### Tolerance and clearances

- **Tab-and-slot fit**: ±0.05 mm achievable with kerf compensation.
- **Press-fit tab**: -0.05 to 0 mm (designs at "exact" CAD size
  because the kerf widens the slot).
- **Free-fit tab**: +0.1 to +0.2 mm clearance after kerf comp.
- **Kerf widths**: acrylic 0.1-0.2 mm; plywood 0.2-0.4 mm.

### Joint types suitable for laser

| Joint                  | Use                                       |
|------------------------|--------------------------------------------|
| Tab + slot             | The canonical laser joint; press-fit       |
| Finger (box) joint     | Interlocking; high glue area               |
| T-slot for bolt + nut  | Slot accepts captive nut, bolt fastens    |
| Living hinge (plywood) | Kerf-line array creates flexible region   |
| Slot + cam-lock        | Removable; cam compresses joint            |
| Stacked-layer + dowel  | Multiple layers aligned by pin             |

### T-slot detail

A T-slot is a slot with a wider section partway through, sized to
capture a nut (typically M3 or M4). Bolt threads through one panel
into the captured nut on a perpendicular panel.

```
   panel A (with bolt hole)
      |
      |   <-- bolt goes here, through hole
      |
   ===|===  panel B with T-slot
      ‾‾‾  |||| (nut sits here, perpendicular to bolt)
```

Used in laser-cut furniture, electronics enclosures, and any
demountable laser-cut design.

### Adhesives

| Material      | Standard adhesive                    |
|---------------|---------------------------------------|
| Acrylic       | Solvent weld (dichloromethane, IPS Weld-On 4) |
| Plywood       | PVA / Titebond II                     |
| Leather       | Contact cement                        |
| Laser ply edge | Lightly seal with thinned PVA before veneer |

### Pitfalls

- **Acrylic stress crack at sharp internal corners** — add fillets
  ≥ R1 mm at all internal corners.
- **Heat-affected zone** — laser char on plywood edges; sand or
  seal before assembly.
- **Material warp** — thin sheets warp from cut-stress release; design
  joints to constrain.
- **Kerf direction** — top of cut is wider than bottom; mating tabs
  fit better if cut sides match (both "up" or both "down").

## 7. Sheet metal (laser/punched + brake bending)

### Tolerance and clearances

- **At straight edges**: ±0.1 mm.
- **At bent edges**: ±0.5 mm due to K-factor and spring-back.
- **Hole-to-hole on the same face**: ±0.1 mm.
- **Hole-to-hole across a bend**: ±0.5 mm.

### Joint types suitable for sheet metal

| Joint                  | Use                                       |
|------------------------|--------------------------------------------|
| Tab + slot + bend tab   | Self-locking when bent into place        |
| Hemmed edge             | Folded back for safety + strength        |
| Riveted lap joint       | Permanent; through-rivet plus locktite-like |
| Welded butt / fillet    | Permanent; needs deburring                |
| PEM nuts / standoffs    | Pressed-in threaded fasteners; precision threading from sheet stock |
| Cam-lock                | Removable; furniture-style                 |
| Mortise-tab through hole | Self-aligning during welding              |

### Pitfalls

- **Spring-back** — over-bend by a few degrees and use prototypes
  to dial in.
- **Bend radius minimum** — 1× material thickness for aluminum,
  2-3× for stainless.
- **Material flow at sharp corners** — round to 1× thickness inside;
  add reliefs.

## 8. Flexible 3D print (TPU, NinjaFlex, PP)

The exception to FDM rules — these print flexibly but with poor
detail resolution.

- **Tolerance**: ±0.3 mm.
- **Living hinges**: viable; designed for >10,000 cycles in TPU.
- **Snap-fits**: very forgiving; high elongation allows large
  deflection without breaking.
- **Press-fit gaskets**: the flexible material seals against rigid
  parts.
- **Adhesive**: CA or polyurethane; difficult to bond to anything
  else due to low surface energy.

## 9. Multi-material joints

Each process has its tolerance; **at the interface, the looser
tolerance dominates**. Design clearances for the looser process.

### Common pairings

| Combination          | Standard joint                        | Notes                                  |
|----------------------|----------------------------------------|----------------------------------------|
| FDM + wood           | Heat-set insert in print, M-screw through wood | Allow ±0.3 mm wood, ±0.2 mm print |
| FDM + metal          | Captive nut in print, bolt + washer through metal | Print is the "movable" side  |
| Wood + acrylic       | Bolt through with thick washers       | CTE mismatch: acrylic 70 × wood 5 µm/m/°C |
| Wood + sheet metal   | Pop rivets or pan-head screws         | Pre-drilled metal, pilot in wood        |
| Metal + 3D print     | Threaded post on metal, captive nut in print | Print accommodates the tolerance |
| Acrylic + sheet metal | T-slot + machine screw + captive nut  | Use rubber gasket between to absorb tolerance |

### CTE (Coefficient of Thermal Expansion) considerations

For joints across materials in temperature-varying environments
(speaker cabinets see 10-50°C internal temp swings):

| Material        | CTE (µm/m/°C)   |
|------------------|------------------|
| PLA             | 70-80           |
| PETG            | 70              |
| ABS             | 80-90           |
| Aluminum         | 23               |
| Steel            | 11-13            |
| Acrylic          | 70-90            |
| MDF / plywood    | 4-8 (anisotropic)|
| Glass            | 4-9              |

Over a 1 m span with 30°C swing: 3D print expands 2.1 mm, aluminum
0.7 mm, plywood 0.15 mm. Use slotted holes (allow ±2 mm slot length)
when a long span crosses materials with very different CTE.

## 10. Speaker cabinet examples

Tying it back to designs in the speaker-design cookbooks:

- **Cabinet shell** (CNC plywood/MDF, rabbet joinery + PVA glue).
- **Driver flange recess** (CNC).
- **Removable back panel** (CNC; heat-set inserts + M4 socket-cap screws).
- **Port flare** (FDM PETG; heat-set insert at flange + bolt through
  baffle; silicone gasket on flange face).
- **Terminal cup** (FDM; heat-set inserts for binding posts; silicone
  gasket to cabinet).
- **Internal brace** (CNC plywood; tongue-in-dado captured between
  side panels).
- **Crossover mounting board** (FDM or laser acrylic; tab-and-slot to
  internal brace).
- **Grille frame** (laser-cut aluminum; PEM nuts; M3 magnets press-fit
  in the cabinet baffle for grille retention).

Each part of the cabinet uses its **best-fit process**. The
parametric CAD model accommodates all of them — STEP for CNC and
metal, STL for 3D print, DXF for laser. See
`cookbooks/speaker-cabinet-2way.md` for the integrated workflow.

## 11. Quick selection guide

For a given joint, pick a process by:

1. **Strength under expected load** — FDM weakest in Z; wood weakest
   in end-grain; metal strongest overall.
2. **Repeated assembly** — inserts / threads needed; avoid press-fits.
3. **Cosmetic visibility** — laser edges show kerf char; wood needs
   finishing; metal anodizes well; SLA finishes smooth.
4. **Cost per unit** — FDM cheapest in small quantities; CNC and laser
   scale with sheet utilization.
5. **Material continuity** — same material in one process is simpler
   than mixed; only mix when the geometry truly needs it.

### Joint pattern by need (quick lookup)

| Need                    | FDM           | CNC wood            | Laser              | Metal              |
|-------------------------|---------------|---------------------|--------------------|--------------------|
| Reversible fastening    | Heat-set + M-screw | Threaded insert + M-screw | T-slot + M-screw | Threaded hole + M-screw |
| Permanent joint         | Adhesive + press-fit | PVA glue           | Solvent weld / PVA | Weld / epoxy        |
| Self-aligning           | Boss + pocket | Dovetail            | Tab + slot         | Dowel pin + bolt   |
| Flex hinge              | Living hinge (TPU) | Impractical    | Plywood kerf array | Sheet-metal hinge   |
| Snap fit                | Cantilever snap | Impractical       | Tab snap           | Machined snap       |
| Strong corner           | Avoid (Z-weak) | Lock miter / dovetail | Finger joint    | Welded             |
| High-cycle (>100 cycles)| Heat-set + M-screw | Threaded insert | T-slot + M-screw   | Threaded hole       |

## Cross-references

- `manufacturability.md` — tolerance table, kerf, tool diameters,
  internal corner radius rules.
- `fasteners-and-finishing.md` — M-screws, threaded inserts, glue
  table, silicone, surface prep.
- `speaker-cabinet-cad.md` — where each joint type fits in a real
  cabinet build.
- `cookbooks/speaker-cabinet-2way.md` — integrated workflow using
  multiple processes.
