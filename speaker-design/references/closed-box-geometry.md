# Closed-Box Geometry and Driver Response

`enclosures.md` covers the sealed alignment math (`F_c`, `Q_tc`,
`f_-3 dB`). `thiele-small.md` covers the driver's small-signal model.
`baffle-and-cabinet-acoustics.md` covers diffraction and panel /
internal modes. This file ties the three together: how the **physical
geometry** of a closed box — its volume, shape, aspect ratio, and the
driver's position on it — maps onto the **measured frequency
response** of the system.

The short version: a closed box affects the driver's response in **three
overlapping regions**, each with its own dominant geometry parameter:

| Band                 | What the cabinet does                       | Geometry knob                       |
|----------------------|---------------------------------------------|--------------------------------------|
| Below `F_c`          | adds stiffness → 2nd-order high-pass        | net internal volume `V_b`            |
| `F_c` to ~200 Hz     | sets alignment shape (Bessel/B2/peaked)     | `V_b` vs. `V_as` (sets `Q_tc`)       |
| 200 Hz – 1 kHz       | internal acoustic modes + panel modes color | dimensions, aspect ratio, bracing    |
| 800 Hz – 3 kHz       | baffle step + edge diffraction              | baffle width, edge geometry, driver placement |
| > 1 kHz              | nearly no cabinet effect                    | driver itself dominates              |

## 1. Volume → driver response (LF region)

A closed volume acts as a spring with stiffness `K_box = ρ₀ c² Sd² /
V_b`. The driver sees this stiffness in **parallel** with its own
suspension stiffness:

```
K_total = K_ms + K_box
       = K_ms · (1 + V_as / V_b)
```

The driver's mass `M_ms` is unchanged. So in-box resonance shifts up
from free-air `F_s` to:

```
F_c  = F_s · √(1 + V_as / V_b)
Q_tc = Q_ts · √(1 + V_as / V_b)
```

Numerically, for a `V_as = 17 L` 6.5" driver (`F_s = 36 Hz`, `Q_ts =
0.36`):

| `V_b` (L) | `V_as/V_b` | `F_c` (Hz) | `Q_tc`  | alignment      |
|-----------|------------|------------|---------|----------------|
| ∞         | 0          | 36         | 0.36    | (free air)     |
| 50        | 0.34       | 41.7       | 0.42    | very damped    |
| 25        | 0.68       | 46.8       | 0.47    | Bessel-ish     |
| 17        | 1.00       | 50.9       | 0.51    | between B2/B   |
| 12        | 1.42       | 56.0       | 0.56    | between B2/B   |
| 8         | 2.13       | 63.6       | 0.64    | near Butterworth |
| 6         | 2.83       | 70.5       | 0.71    | Butterworth B2 |
| 4         | 4.25       | 82.4       | 0.83    | peaked         |
| 2         | 8.5        | 110.7      | 1.11    | over-peaked    |

Smaller box: higher cutoff, higher Q, peakier response, **worse
transient behavior**. The 2 L box rolls off at 110 Hz with a +5 dB
peak — almost useless for a small woofer. Real sealed bookshelf designs
sit in the `V_as / V_b` = 1–2 region for `Q_tc` ≈ 0.6–0.8.

For an explicit response prediction from your driver and box volume,
use `tools/sealed_box.py`.

## 2. Net (effective) volume vs. external dimensions

The `V_b` in the formula is the **net internal air volume**. Builders
chronically over-estimate it by working from external dimensions. The
real number is:

```
V_b,net = V_b,external
        − V_panel_walls
        − V_driver_back (cone + magnet displacement)
        − V_bracing
        − V_crossover_board
        + V_stuffing_effect
        + V_activated_carbon_effect (if present)
```

Typical adjustments for a 12 L gross internal cabinet:

| Adjustment                               | Δ V_b      |
|------------------------------------------|------------|
| 18 mm MDF panels, internal vs. external  | −0.7 L     |
| 6.5" driver basket + magnet              | −0.4 L     |
| Cross brace + small crossover board      | −0.3 L     |
| Modest stuffing (50 g long-fiber wool)   | +0.6 L     |
| **Net effective**                        | **~11.2 L**|

Two specific increases worth knowing:

**Stuffing effect**: porous absorber inside the cabinet shifts the
air's thermal behavior from **adiabatic** (no heat exchange with
walls) to **isothermal** (heat exchanged with fibers). Adiabatic
compression is stiffer than isothermal by the factor `γ = 1.4`. Fully
isothermal stuffing therefore makes the air look as if `V_b` were
enlarged by ~40 %. In practice, stuffing reaches only partial
isothermal behavior, gaining ~5–20 % effective volume. Re-measure
`F_c` after stuffing — the formula's prediction is off until you do.

**Activated carbon fill** (e.g. KEF's coal-bed sub treatment, some
DSP'd compact subs): the carbon adsorbs/desorbs air molecules at LF,
buffering pressure swings. Equivalent volume increase of 30–80 %,
strongly LF-biased. Engineered carbon volumes (e.g. ScanSpeak SC1)
let you build a sub in half the cabinet of its T/S target.

## 3. Box shape: response signatures

The closed-box LF equations care only about `V_b`. Everything **above**
LF — internal modes, diffraction, panel modes — cares about **shape**.

| Shape                          | LF behavior         | Mid response signature                                          |
|--------------------------------|----------------------|-----------------------------------------------------------------|
| Cube                           | per `V_b` formula   | strongest internal-mode coloration; ALL modes align at one freq |
| Rectangular (golden ratio)     | per formula         | smoothest mid for a flat-panel design                           |
| Truncated pyramid              | per formula         | non-parallel walls smear internal modes                         |
| Cylinder, axis vertical        | per formula         | radial modes split off length modes; better than cube           |
| Sphere / ovoid                 | per formula         | minimum internal modes (radial only); no diffraction edges      |
| Tapered "Nautilus" (B&W)       | per formula         | rear of driver radiates into damped exponential horn → no modes |
| Trapezoidal with slanted top   | per formula         | typical "high-end" compromise: spreads modes 5–15 %             |
| Open cardioid (with side vents)| modified LF         | rear wave used to cancel sidewall radiation                     |

For a given volume, **sphere is best, cube is worst, golden-ratio
rectangle is the engineering optimum**. Tapered designs are an
upgrade over rectangular when MDF and roundovers aren't enough.

## 4. Aspect ratio for rectangular boxes

The choice of `L_x : L_y : L_z` does not affect the LF response (only
`V_b` does). It controls **where the internal modes land** and **how
many coincide**.

Recommended ratios (each `≠ 1.0` and pairwise irrational):

- **Sepmeyer / Bonello (acoustics)**: 1.00 : 1.28 : 1.54
- **Louden**: 1.00 : 1.40 : 1.90
- **Golden ratio**: 1.000 : 1.618 : 2.618
- **Bolt**: 1.00 : 1.14 : 1.39 (smaller rooms — applies to cabinets too)

Avoid:

- Cubes: 1 : 1 : 1 — every mode triples up.
- Doubled dimensions: 1 : 1 : 2, 1 : 2 : 4 — modes pile at common
  multiples (`c/(2L)` of the short side also matches `c/L` of the
  long side).
- Integer ratios in general.

For a typical bookshelf with `V_b ≈ 12 L`, the Louden ratio
1 : 1.4 : 1.9 yields internal dimensions ~166 × 232 × 316 mm. The
lowest mode (long axis) sits at `c/(2·0.316) ≈ 543 Hz`, well into
the absorber-tractable region.

## 5. Driver placement on the front baffle

Two effects, both already covered, but here is the trade summary:

- **Diffraction** (see `baffle-and-cabinet-acoustics.md`): asymmetric
  placement (e.g. 30 % offset horizontally and ~25 % from the top)
  spreads the comb-nulls each edge produces across frequency. Avoid
  centered drivers on rectangular baffles unless the baffle is
  bordered by heavy roundovers or felt.
- **Internal-mode coupling**: a driver acoustically sees the cabinet
  cavity through its rear. If the cone's footprint sits at a **pressure
  antinode** of an internal mode, that mode couples strongly back
  through the cone and modulates the front radiation. If the cone is
  near a pressure **node** for that mode, coupling is weak.

The two requirements often conflict. Practical compromise: optimize
for diffraction first (asymmetric placement), then add internal
absorption to kill modes that happen to sit at the driver's location.

## 6. Driver mounting orientation

The geometry knob "where on the cabinet does the driver point":

| Mounting          | Typical use                | Trade                                             |
|-------------------|----------------------------|---------------------------------------------------|
| Front-firing      | default                    | conventional baffle step + diffraction            |
| Side-firing       | subs and isobaric           | suppresses front-baffle diffraction; off-axis to mains |
| Down-firing       | subs on carpet              | floor acts as baffle extension; needs ≥75 mm clearance |
| Rear-firing       | open / dipole               | reverses front/back radiation; needs DSP for hi-fi |
| Opposed (push-pull) | subs, high-power towers   | drivers facing opposite sides; **cabinet vibration cancels**, distortion drops 6–10 dB |
| Isobaric          | extreme low Vb              | two drivers in series, sharing one chamber: doubles effective `V_as`, halves `V_b` needed for given `F_c` |
| Acoustic suspension (cone radiates inward) | rare      | second cone serves as a giant passive radiator    |

**Force cancellation** (opposed mounting) is one of the highest-
leverage moves for a sealed subwoofer: place two identical drivers on
opposite faces of the cabinet, wired in phase, both pushing outward
together. The reaction forces on the cabinet cancel exactly,
eliminating the audible "cabinet wobble" that makes single-driver
subs sound less tight than they should.

## 7. Pressure compression and Vb nonlinearity at high SPL

The closed-box stiffness `K_box ∝ 1/V_b` is only linear for small
displacements. At max excursion the cone has swept volume `S_d · x`
out of `V_b`, raising internal pressure by:

```
P_box / P_atm ≈ (V_b / (V_b − S_d · x))^γ − 1
```

For a 6.5" driver (`S_d ≈ 132 cm²`, `Xmax ≈ 5 mm`) in a 12 L sealed
box:

```
ΔV / V_b = (132e-4 · 5e-3) / 12e-3 = 5.5 %
ΔP / P_atm ≈ 1.055^1.4 − 1 ≈ 7.8 %  → 158 dB SPL inside the box
```

Consequences:

- **Asymmetric box stiffness**: pushing the cone in raises internal
  pressure (stiffer); pulling out lowers it (softer). The resulting
  asymmetric `K_box(x)` adds **2nd harmonic distortion**, peaking near
  `F_c`.
- **Smaller box → more nonlinearity**: a 6 L sealed box with the same
  driver at Xmax sees ~11 % pressure swing → audibly more distortion
  near `F_c`. The clean-SPL ceiling drops 3–6 dB.
- **Distortion roll-off mid-band**: above `F_c` excursion drops 12 dB/oct
  in a sealed box, so pressure-compression distortion is
  fundamentally an LF-only problem. Above ~150 Hz it vanishes.

Mitigation: bigger box (cheapest), force-cancelling pair (also halves
swept volume per driver since each driver moves the same air into a
sealed half-volume), or driver with higher Xmax so you operate at
lower fractional excursion.

## 8. Geometry's effect on the **measured** driver response

Imagine sweeping the same driver in four configurations. Schematic
SPL response on-axis at 1 m:

```
Free air:
    rolls off 6 dB/oct below ~500 Hz (dipole), flat to breakup, breakup peak

Large baffle (IEC):
    flat to driver Fs, then sharp 12 dB/oct rolloff at Fs; flat above

Closed box V_b = V_as:
    flat to ~F_c = √2·Fs, then 12 dB/oct rolloff; same midrange as IEC

Closed box V_b = V_as/3:
    flat to ~F_c = 2·Fs, then 12 dB/oct rolloff; mild peak at F_c if Qtc>0.7
```

Mid/HF response (above ~F_c · 3) is essentially **independent of `V_b`**.
What changes the midrange response when you switch boxes is the box's
**geometric** properties — internal modes, panel modes, baffle width
— not its volume.

This is why the rule "measure free-air response, then add the modeled
LF alignment" works as a first approximation. The midrange response
you measure in the final box differs from free-air mostly by:

1. **Baffle step**: +6 dB above `f_bs ≈ 115/W`. Predictable.
2. **Edge diffraction comb**: ±2 dB ripples in 800–3000 Hz. Depends
   on driver placement on the baffle.
3. **Internal-mode coupling**: ±1–3 dB narrow peaks at the cabinet's
   mode frequencies. Worst unstuffed; controllable with absorbent.
4. **Panel resonance leakage**: ~-15 to -25 dB radiated noise from
   walls at panel mode frequencies. Audible but small compared to
   direct radiation; controllable with bracing.

If you measure the final speaker and the mid response is worse than
predicted (after BSC) by >3 dB anywhere, the cabinet geometry is
likely the culprit. In order of probability: stuffing inadequate
(rebuild), edges too sharp (add felt/roundovers), driver too close to
a mode antinode (move driver or add internal partition tuned to
that mode).

## 9. Quick design rules

For a small sealed two-way or subwoofer:

1. **Pick `V_b` to land `Q_tc` between 0.55 and 0.80.** Below 0.5 the
   transient is great but cutoff is high; above 0.8 you get an
   audible peak.
2. **Internal aspect ratio 1 : 1.4 : 1.9** (or thereabouts). Never a
   cube.
3. **Internal volume ≥ 1.2 × the nominal target** — once you account
   for braces, driver displacement, and stuffing recovery, the net
   matches your design.
4. **One transverse brace per panel span > 200 mm.** Pushes panel
   modes out of audibility.
5. **25 mm roundovers on visible edges**, or felt strips around the
   tweeter.
6. **Driver offset 15–30 mm from the vertical centerline** of the
   baffle, and 30–40 % from the top.
7. **Long-fiber wool or polyester batting** on the rear and one side
   wall, ~0.5 kg/m³, glued in place so it doesn't settle.
8. **Sealed means sealed**: silicone every joint, gasket the driver
   flange, and verify with the impedance sweep (single clean peak,
   no double-bump). A 0.5 % leakage halves perceived `Q_tc`.

Verify with `tools/sealed_box.py` for the LF math, then with an
impedance sweep on the finished box (see `references/measurement.md`)
to confirm `F_c` lands where you designed it.
