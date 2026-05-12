# Fasteners, Pilot Holes, Glue, Sanding, and Finishing

Practical reference for the hardware and finishing decisions that
turn a CAD model into a built cabinet. Get these wrong in CAD and the
fabricator either has to re-drill, re-cut, or refuse the job. Get
them right and assembly takes hours, not days.

## 1. Metric (M-) machine screws

ISO 7045/7046/7380/4762 etc. specify thread, head, and length. For
DIY cabinet work, you'll touch M3 through M8.

### Common sizes

| Size | Major dia | Standard pitch | Fine pitch | Typical use                          |
|------|-----------|-----------------|------------|---------------------------------------|
| M2   | 2.0 mm    | 0.40 mm         | 0.25 mm    | Driver gaskets, light hardware       |
| M2.5 | 2.5 mm    | 0.45 mm         | 0.35 mm    | Small tweeter mounts, electronics    |
| M3   | 3.0 mm    | 0.50 mm         | 0.35 mm    | Tweeter mounts, terminal cups        |
| M4   | 4.0 mm    | 0.70 mm         | 0.50 mm    | Removable back panels, mid-driver mounts |
| M5   | 5.0 mm    | 0.80 mm         | 0.50 mm    | Woofer mounts (small drivers)        |
| M6   | 6.0 mm    | 1.00 mm         | 0.75 mm    | Woofer mounts, brace bolts           |
| M8   | 8.0 mm    | 1.25 mm         | 1.00 mm    | Spike feet, structural ties          |
| M10  | 10.0 mm   | 1.50 mm         | 1.25 mm    | Stand mounts, top-plate hardware     |

Default to standard pitch (the "coarse" series above) unless there's
a reason to use fine. Fine pitch holds torque better, threads more
slowly, less self-loosening; coarse pitch is more tolerant of
imperfect threads.

### Head types

| Head      | ISO  | Driver  | Profile  | Use case                                                |
|-----------|------|---------|----------|---------------------------------------------------------|
| Socket cap| 4762 | Hex key | Cylindrical, raised | Strong; counterbored cleanly into baffle    |
| Button    | 7380 | Hex key | Domed, low profile  | Pretty; less torque than socket cap         |
| Pan       | 7045 | Phillips/Pozi/Torx | Rounded, raised | General, low cost                       |
| Flat / countersunk | 7046 | Phillips/Pozi/Torx | 90° flush | Hidden hardware, flush with panel      |
| Hex       | 4017 | Wrench  | Hex flange | Structural, very high torque                          |

For removable back panels: **M4 socket cap** in a counterbored hole
with a brass heat-set insert is the cleanest professional solution.
**M4 pan-head** with a wood-screw insert (Spax or similar) into the
back panel is the cheap-and-fast alternative.

### Length convention

For pan / button / socket cap: length is measured **from under the
head** to the tip. For flat / countersunk: length is measured from
the **top of the head** (the flush surface) to the tip. Mixing these
up is the #1 mistake — pay attention.

### Material grades

- **A2 stainless** (304-equivalent): default for visible cabinet
  hardware. Won't rust, looks clean.
- **A4 stainless** (316-equivalent): marine environments only;
  overkill for indoor.
- **Class 8.8 or 10.9 steel** (zinc-plated): higher tensile strength
  for structural bolts; not for visible hardware.
- **Brass**: cosmetic, soft; don't torque heavily.

## 2. Threaded inserts (heat-set, press-fit, screw-in)

Inserts let you put a metal thread into wood or plastic, so machine
screws can engage repeatedly without stripping. Essential for
removable back panels, replaceable driver mounts, brace bolts, and
anywhere you'll undo/redo a fastener.

### Heat-set (thermoplastic; also works in MDF and softwoods)

A knurled brass insert melted into a pre-drilled hole with a
soldering iron tip. Standard for 3D-printed parts; works in MDF and
softwood (the iron fuses fiber rather than melts plastic).

Common manufacturers: McMaster (94459A series), Yardley, Voltive,
generic Aliexpress.

**Yardley / standard hex pattern:**

| Insert | OD     | Length | Pilot hole | Min wall thickness |
|--------|--------|--------|------------|---------------------|
| M2     | 3.5 mm | 4.0 mm | 3.2 mm     | 1.5 mm              |
| M3     | 4.6 mm | 5.7 mm | 4.0 mm     | 2.0 mm              |
| M4     | 6.4 mm | 8.1 mm | 5.6 mm     | 2.5 mm              |
| M5     | 7.1 mm | 9.5 mm | 6.4 mm     | 3.0 mm              |
| M6     | 8.7 mm | 12.7 mm| 7.9 mm     | 3.5 mm              |
| M8     | 11.1 mm| 12.7 mm| 9.9 mm     | 4.5 mm              |

Installation: pilot the hole, set the insert on it, press the
soldering-iron tip (with insert adapter) onto it. Push **slowly,
square to the surface**, until the insert is flush. Holds 200–400 N
pullout in MDF; 400–600 N in hardwood; less in particleboard.

### Press-fit / barbed (no heat)

Driven in with a hammer or arbor press. Common for hardwood; not
ideal for MDF (the fibers crush, no grip). The grip relies on
external barbs gouging the surrounding material.

- E-Z LOK series #400-#440 (steel, brass).
- TIME-SERT for repair work.

Holds well in hardwood; marginal in MDF (heat-set is better there).

### Screw-in (with external wood thread + internal machine thread)

Looks like a stubby wood screw with a hex socket inside. Driven in
with a hex key.

- E-Z LOK 400-Z, Spax, etc.
- McMaster 93105A series.

Pros: very strong in solid wood; no need for special tools; can
re-tap if the wood splits. Cons: takes a large pilot hole; not for
thin walls.

**Pilot hole** for screw-in inserts: roughly 80–85 % of the insert's
external OD. Check manufacturer datasheet — wrong pilot splits the
panel.

### Choosing an insert type

| Material        | Default          | Notes                              |
|-----------------|------------------|-------------------------------------|
| 18 mm MDF       | Heat-set         | E-Z LOK or Yardley M4/M5            |
| Plywood         | Heat-set or screw-in | Heat-set holds slightly better  |
| Solid hardwood  | Screw-in          | Strong grip with proper pilot      |
| Particleboard   | Heat-set + epoxy | Particleboard alone is fragile     |
| FDM 3D print    | Heat-set          | Standard for parametric speaker parts |
| SLA 3D print    | Heat-set (carefully) or epoxy + nut | SLA is brittle; gentle heat   |

## 3. Wood screws

Sized by gauge (number) + length in inches in the US/UK; or by
diameter + length in mm in metric. Cabinet builders move between
both systems.

### Gauge → diameter

| Gauge | Diameter | Metric equivalent |
|-------|----------|--------------------|
| #4    | 2.84 mm  | M2.8              |
| #6    | 3.51 mm  | M3.5              |
| #8    | 4.17 mm  | M4                |
| #10   | 4.83 mm  | M5                |
| #12   | 5.50 mm  | M5.5              |

For cabinet work: **#8 or #10 (4–5 mm)** is the default for
panel-to-panel joinery. **#6** for trim and accessories. **#12** for
heavy structural attachment.

### Lengths

Rule of thumb: screw length = 2 × the thickness of the panel being
attached, **plus** the thickness of any panel it passes through. For
attaching an 18 mm panel to another panel: 36 + 18 = 54 mm minimum;
use a 60–65 mm screw. Don't exceed the substrate thickness in solid
wood (split risk).

### Thread types

- **Coarse thread**: deep, widely-spaced threads. Default for
  softwood, MDF, plywood. Hold faster.
- **Fine thread**: shallow, closely-spaced. Default for hardwood.
  Less likely to split.
- **Particle-board / chipboard screws**: deep coarse threads,
  high-friction surface. Cheap; the only screw that holds reliably
  in particleboard.

### Drive types

| Drive       | Pros                                  | Cons                          |
|-------------|---------------------------------------|--------------------------------|
| Phillips    | Universal, common                     | Cams out under torque         |
| Pozidriv (Pozi) | Better than Phillips; common in EU | Easy to confuse with Phillips |
| Square (Robertson) | High torque, no cam-out       | Less common in US             |
| Torx (T15-T30) | Best torque, no cam-out           | Need the right bit            |

For cabinet work, **Torx (T20 or T25)** is the best modern choice if
your screws + bits agree. Spax and modern construction screws are
Torx-by-default.

### Specialty cabinet screws

- **Confirmat** (cabinet screws with hex/Torx head): 7 mm diameter,
  fixed lengths (50 mm common). Designed for cam-lock-style joinery
  in melamine-faced board. Requires a stepped pilot drill.
- **Cabinet/euro screws**: 4.5 mm shank with a 7 mm flat head; used
  for hinge cup mounting.
- **Pocket screws** (Kreg-style): self-tapping with washer-head;
  threads only on the lower half so they pull joints together.

## 4. Pre-drill / pilot hole reference

A correctly sized pilot hole is non-negotiable in cabinet work. Too
small splits the panel; too large reduces holding power; way too
large makes the screw spin.

### Wood-screw pilot hole table

For each screw, drill a **shank clearance hole** through the upper
piece and a **pilot hole** into the lower piece.

| Screw  | Shank clearance | Pilot, softwood | Pilot, hardwood | Pilot, MDF | Counterbore |
|--------|------------------|------------------|-------------------|-------------|--------------|
| #4     | 2.8 mm          | 1.6 mm           | 1.9 mm            | 1.9 mm      | n/a          |
| #6     | 3.5 mm          | 2.0 mm           | 2.4 mm            | 2.4 mm      | 6 mm         |
| #8     | 4.2 mm          | 2.4 mm           | 2.8 mm            | 3.0 mm      | 8 mm         |
| #10    | 4.8 mm          | 2.8 mm           | 3.2 mm            | 3.5 mm      | 9 mm         |
| #12    | 5.5 mm          | 3.2 mm           | 3.5 mm            | 4.0 mm      | 10 mm        |

MDF wants a slightly larger pilot than equivalent softwood to prevent
"mushrooming" around the hole — the screw drives the broken-up fiber
into a swell.

### Machine-screw clearance + tap drill table

For M-screws passing through one panel and threading into another (or
into an insert):

| Screw | Clearance hole (close fit, ISO H7) | Tap drill (for cutting threads in metal) | Self-tapping pilot in MDF/plywood |
|-------|-------------------------------------|------------------------------------------|------------------------------------|
| M2    | 2.2 mm                              | 1.6 mm                                   | 1.5 mm                             |
| M2.5  | 2.7 mm                              | 2.05 mm                                  | 2.0 mm                             |
| M3    | 3.2 mm                              | 2.5 mm                                   | 2.5 mm                             |
| M4    | 4.3 mm                              | 3.3 mm                                   | 3.3 mm                             |
| M5    | 5.3 mm                              | 4.2 mm                                   | 4.2 mm                             |
| M6    | 6.4 mm                              | 5.0 mm                                   | 5.0 mm                             |
| M8    | 8.4 mm                              | 6.8 mm                                   | 6.8 mm                             |
| M10   | 10.5 mm                             | 8.5 mm                                   | 8.5 mm                             |

For inserts: use the **insert manufacturer's pilot recommendation**,
not these (the insert's external thread is different from a
machine-screw thread).

### Countersink depth

Flat-head screws sit flush when the countersink is `0.85 × head OD`
deep. For a #8 flat-head (head OD ~8 mm): countersink 7 mm deep with
a 90° cutter, hole 4.2 mm.

### Counterbore for socket cap

For an M4 socket cap head (7 mm OD, 4 mm height): counterbore 7.5 mm
diameter × 4.5 mm deep so the head sits flush. M5: 8.5 mm × 5.5 mm.
M6: 10 mm × 6.5 mm.

## 5. Sanding

For an enclosure that will be painted, lacquered, or veneered.

### Grit progression

```
Stage          Grit    Removes                       Leaves
----------------------------------------------------------------------
Heavy stock     60-80   Glue squeeze-out, big tears   Coarse scratches
Bulk shaping    100-120 Mill marks, planer ripples   Visible scratches
Pre-finish      150-180 Cross-grain scratches        Fine, ready for sealer
Pre-veneer/topcoat 180-220 Sealer raise               Smooth, ready
Between coats   320-400 Topcoat raise / nibs         Velvety
Wet sand topcoat 600-1500 Surface texture             Glass-smooth
Polish          2000-4000 Sanding scratches           Mirror gloss
```

Skip no more than one grit step. Going 80 → 220 leaves 80-grit
scratches that the 220 paper can't reach — they show through the
finish.

### Hand vs power

- **Random orbital** (5" or 6"): the workhorse. Up to 220 for most
  cabinet work.
- **Detail sander** (delta head, mouse): for inside corners.
- **Block sanding by hand**: 320+ for flat surfaces; required for
  rubbing out a finish.
- **Belt sander**: only for stock removal on edges and faces of
  hardwood; tears MDF.

### Sanding direction

Across the grain in early stages; with the grain in finishing
stages (180 grit and finer). For MDF and other engineered
materials, direction doesn't matter, but uniform pressure does.

### Edge prep

If applying veneer, sand to 220 and apply a light coat of vinyl
sealer or wood glue thinned 50% to seal the edge fibers — otherwise
they swell with the adhesive and telegraph through.

## 6. Finishing

### Common product families

| Family              | Finish look       | Drying    | Recoat | Pros                           | Cons                       |
|---------------------|-------------------|-----------|--------|--------------------------------|----------------------------|
| Nitrocellulose lacquer | Glossy, hard   | 30 min    | 1 hr   | Easy spray, sands well, glossy | Solvent stink; not durable to UV |
| Pre-cat lacquer (CV)| Glossy, very hard | 1 hr     | 2 hr   | Pro furniture standard         | Pro spray equipment        |
| Water-based polyurethane | Satin/gloss   | 1 hr      | 2-4 hr | Low VOC, easy cleanup          | Plasticky look             |
| Oil-based polyurethane | Warm, amber-tinted | 4-6 hr | 12-24 hr | Forgiving, durable           | Slow; ambering              |
| Spar urethane       | Glossy            | 4-6 hr    | 12 hr  | UV-stable                      | Soft; for outdoor          |
| Conversion varnish  | Very hard         | 1 hr      | 4 hr   | Industry standard for kitchens | Two-component, short pot life |
| Tung oil / Danish   | Matte, in-the-wood| 6-12 hr   | 24 hr  | Easy, repairable               | Modest protection          |
| Shellac             | Warm amber        | 30 min    | 1 hr   | Pre-stain sealer; reversible   | Not water-resistant        |
| Automotive 2K       | High-gloss show   | 30 min    | 4 hr   | Mirror finish                  | Skill; respirator required  |

### Schedule for a black piano-gloss bookshelf

The "high-end commercial" look most DIY builders try to copy:

```
1. Fill grain (water-based grain filler, 2 coats, sand 220 between).
2. Sealer coat: spray vinyl sealer or shellac-based primer. 1 coat.
3. Sand 320.
4. Base color (black primer or pigmented lacquer). 2-3 coats, sand 400 between.
5. Clear topcoat (lacquer or 2K auto clear). 4-6 coats, sand 600 between coats 2-3.
6. Cure 2-7 days depending on system.
7. Wet sand: 800 → 1200 → 1500.
8. Polish: cutting compound → finishing polish on a foam pad.
```

Total time: 1-2 weeks per pair. Material cost ~$50-100 per pair.

### Schedule for a satin natural-wood look

```
1. Sand to 180.
2. Optional: water-pop the surface to raise grain, sand 220.
3. Stain (oil-based, water-based, or dye). Wipe on, wipe off after
   directed dwell time.
4. Sand lightly 320 if grain raised again.
5. Seal: shellac wash coat (1 lb cut) OR sealer.
6. Topcoat: 2-3 coats wipe-on or spray polyurethane, sand 320-400
   between.
7. Cure 1 week before sanding/polishing.
8. Optional final rub: 0000 steel wool + paste wax for satin sheen.
```

### Spray vs brush vs wipe-on

- **HVLP spray gun** (high-volume low-pressure): pro-level finish.
  ~$200 for a starter setup + compressor.
- **Aerosol cans**: 1-2 cabinets only; consistent finish; expensive
  per coat.
- **Brush**: cheap, slow, leaves brush marks unless using a true
  varnish-brush technique.
- **Wipe-on**: foolproof for oils and thinned polys. Builds slowly
  (4-8 coats vs 2-3 for spray).
- **Foam roller + tip-off**: passable on flat panels.

### Dust nibs and rubbing out

After final coat, before polishing:

- Sand with 600/800/1200/1500 progressively to remove dust nibs,
  orange peel, and brush marks.
- Polish with a foam pad and successive compounds (Menzerna,
  Meguiar's, 3M Perfect-It).

### Drying environment

- Temperature: 18-22 °C (65-72 °F) ideal.
- Humidity: 30-60 %. Above 70 % causes blushing (white haze) in
  lacquer.
- Dust: vacuum the spray space; tack-cloth between coats.

## 7. Glue

| Glue                       | Open time | Clamp time | Cure time | Best use                       |
|----------------------------|-----------|------------|-----------|---------------------------------|
| Titebond Original (PVA I)  | 5 min     | 30 min     | 24 hr     | Interior cabinet joinery       |
| Titebond II (PVA, water-resistant) | 5 min | 30 min | 24 hr  | Default for cabinets           |
| Titebond III (PVA, waterproof) | 8 min | 30 min   | 24 hr     | Outdoor or wet exposure        |
| Polyurethane (Gorilla)     | 20 min    | 1 hr       | 24 hr     | Foams; gap-filling; oily woods |
| Epoxy (slow, e.g. West)    | 20-90 min | 4 hr       | 24-48 hr  | Structural; gap-filling; metals|
| 5-min epoxy                | 5 min     | 10 min     | 1 hr      | Quick repairs; jigs            |
| Cyanoacrylate (CA)         | 10 sec    | 30 sec     | 5 min     | Small parts; accelerator pen   |
| Hide glue                  | 5 min     | 12 hr      | 24 hr     | Restoration; reversible joints |
| Construction adhesive (PL Premium) | 10 min | 24 hr   | 7 days    | Heavy panels; non-flat surfaces|

### Selecting glue

- **Default for cabinet joinery**: Titebond II. Strength exceeds the
  surrounding wood; predictable squeeze-out; easy cleanup with damp
  cloth before cure.
- **MDF edges**: pre-seal with thinned PVA (50:50 with water), let
  dry, then glue. Otherwise the MDF wicks the glue and starves the
  joint.
- **Driver gasket / port to baffle**: silicone or polyurethane (see
  below) — not PVA, which can shrink/crack with thermal cycling.
- **Speaker terminal cup to panel**: silicone — must remain
  removable for crossover service.
- **Bracing to panels**: PVA + clamping; never glue a brace into
  position with hot glue or CA — both will fail under thermal cycle.
- **3D-printed accessories to wood**: epoxy or polyurethane glue,
  not PVA (doesn't bond to most thermoplastics).

### Open time vs clamp time vs cure time

- **Open time**: how long after applying glue you can still
  reposition the joint.
- **Clamp time**: minimum time the joint must be clamped to develop
  joint strength enough to release.
- **Cure time**: time to full strength.

Most cabinet glues take 30 min clamp / 24 hr cure. Don't unclamp
early — the joint feels solid but won't be fully strong for hours.

### Applying glue

- Cover both mating surfaces fully but thinly.
- For end-grain joints (much weaker): apply glue, let absorb 60
  seconds, apply a second coat, then assemble.
- Clamp until you see a small bead of squeeze-out at every edge of
  the joint.
- Wipe squeeze-out with a damp cloth before it skins (within 5-10
  min for PVA). Cured squeeze-out is much harder to remove.

## 8. Silicone and other sealants

Speakers need to be **sealed**. A 0.5 % air leak in a sealed box
halves perceived Q_tc and drops F_c by 5-10 %. A leaky port seal
reduces saddle depth in impedance and bleeds the LF response.

### Types

| Sealant                  | Cure   | Removability | Compatibility  | Best for                            |
|--------------------------|--------|---------------|-----------------|--------------------------------------|
| 100% silicone (RTV)      | 24 hr  | Cuttable, not solvent-removable | Stick to glass, metal, MDF | Driver gasket, terminal cup, port-to-panel |
| Acrylic-latex caulk      | 24 hr  | Cuttable      | Paintable; OK on porous   | Cabinet panel joinery (paint-grade) |
| Polyurethane (Sikaflex)  | 24 hr  | Difficult to remove | Sticks to anything    | Permanent panel joinery, edge sealing |
| Butyl-rubber gasket tape | n/a    | Removable     | Self-adhesive   | Driver flange gasket                |
| Closed-cell foam tape    | n/a    | Removable     | Self-adhesive   | Removable panel gaskets             |

### Acetic-cure vs neutral-cure silicone

- **Acetic-cure** (smells like vinegar during cure): cheap, common
  in hardware stores. Releases acetic acid, which **attacks copper**.
  Don't use on or near voice coils, crossover components, or wiring.
- **Neutral-cure / oxime-cure** (mild ammonia smell or odorless):
  more expensive; safe for electronics. Use this for any sealant in
  contact with copper, brass, or driver components.

For cabinet sealing **always use neutral-cure**. Standard
hardware-store "100% silicone" is usually acetic-cure — read the label.

### Cabinet sealing strategy

A sealed cabinet's leak budget is sub-millimeter on a metric-meter
panel — i.e. essentially zero tolerance. Belt-and-suspenders approach:

1. **Internal seams**: bead of acrylic-latex caulk **inside** every
   panel-to-panel joint after dry-fitting. Squeeze the joint while
   the bead is still wet so it skins under compression.
2. **Driver flange**: butyl-rubber gasket tape or closed-cell foam
   gasket between driver and baffle. Tightening the driver
   compresses the gasket; verify with an impedance sweep showing a
   clean single peak (sealed) or saddle (ported).
3. **Terminal cup**: neutral-cure silicone bead around the cup's
   inner flange before screwing down. Wire pass-through should also
   be silicone-filled.
4. **Port flange-to-baffle**: neutral-cure silicone around the port's
   mounting flange.
5. **Removable back panel**: closed-cell foam gasket strip around the
   perimeter; screws compress it.

### Application technique

- **Bead size**: 3-5 mm for cabinet seams; 2 mm for driver flanges.
- **Smoothing**: dipped finger in soapy water; or a silicone-spatula
  tool. Do it within 5 minutes of laying the bead.
- **Cure environment**: ventilate. Acetic cure off-gasses for 12-24
  hr; neutral cure for 24-72 hr (no smell, but uncured silicone is
  still active).
- **Don't bridge**: silicone in the **joint**, not on top of it.
  Top-coating silicone with paint or lacquer almost always fails (the
  finish doesn't bond to silicone).

### Removing silicone

Cut with a sharp knife, then peel. Solvent removers (Goof Off
silicone-specific, Permatex) soften residue. There is no "dissolve
in solvent" path — silicone is a thermoset.

## 9. Quick CAD-side checklist for hardware features

When modeling, every hardware site needs to be parametric:

- [ ] Pilot/clearance hole **diameter** matches the spec for the
      planned screw + material.
- [ ] Hole **depth** is at least screw length + 2 mm clearance.
- [ ] Counterbore / countersink diameter and depth match the head
      style (flat / pan / socket cap).
- [ ] Insert pilot hole matches the **specific insert's** datasheet,
      not a generic value.
- [ ] Insert recess (if visible) is dimensioned so the insert sits
      flush.
- [ ] Driver mount holes match the **driver's** mounting bolt
      pattern (PCD + count from datasheet) and clearance.
- [ ] Removable-back screw layout is symmetric and spaces ≤ 80 mm
      apart for a reasonable seal.
- [ ] Glue grooves (if used in joinery) are sized for adhesive
      flow without starving the joint.
- [ ] Any silicone-bead recess is at least 3 mm wide × 2 mm deep.

When in doubt, drill smaller and enlarge with a hand reamer after
test-fitting — the inverse is impossible.
