# Tapered Rear Chambers (Nautilus-style)

The technique: instead of trapping the driver's rear wave in a sealed
or ported box, **channel it down a tapered tube where damping
material can absorb it before it reflects back through the cone.**
The B&W Nautilus (1993 prototype, 1999 production) is the iconic
example — literal nautilus-shell-shaped tapered tubes for the
midrange and tweeter — but the underlying acoustic idea applies to
any driver whose rear chamber resonance you want to eliminate.

This file covers the physics, design parameters, packaging
variants (straight, spiral, coiled), damping strategies, and when a
tapered rear chamber is the right tool vs alternative enclosures.

## 1. Why eliminate the rear chamber at all

A driver in a sealed or ported box sees the trapped air as part of
its load. That air also supports internal acoustic modes
(`references/baffle-and-cabinet-acoustics.md` § 3) and pushes back on
the cone through resonances at standing-wave frequencies. The cone
then re-radiates these resonances through the front face,
**modulating the music** with the cabinet's own signature.

Mitigation paths:

| Strategy                          | Mechanism                                        |
|-----------------------------------|--------------------------------------------------|
| Stuffed sealed/ported box         | Porous absorption of standing waves; cheap, ~5-10 dB modal reduction. |
| Heavy bracing + CLD damping       | Reduces panel radiation; doesn't fix internal modes. |
| Aperiodic vent                    | Damped resistive vent bleeds rear wave energy.   |
| **Tapered rear chamber**          | Rear wave propagates down the taper, gets absorbed before reflecting. |
| Open baffle / dipole              | No rear chamber; rear wave radiates to room.     |
| Transmission line                 | Tuned 1/4-wave column; absorbs above tuning, augments below. |

Tapered rear chambers belong to a family with TL and aperiodic
enclosures. The Nautilus is the **purest absorptive** version — its
goal isn't to enhance LF (like a TL) or vent any output (like aperiodic),
just to make the rear wave **disappear**.

## 2. The acoustic principle: reverse-flare loading

A tapered tube facing **away** from the listener is mathematically a
horn — but used in reverse. The driver's rear wave enters at the
**mouth** (the open end where the driver sits) and propagates down
toward the **throat** (the small or closed end).

Two things happen along the way:

1. **The taper presents a low, smooth acoustic impedance** to the
   cone's rear, so the rear wave isn't reflected back at the driver.
2. **The wave's energy is absorbed** by damping material along the
   tube length, so very little arrives at the closed end to reflect.

The taper rate sets the **cutoff frequency** below which the tube
ceases to load:

```
f_c = m · c / (4π)         (exponential flare constant m)
```

This is the same Webster equation as a forward-firing horn. **Below
`f_c`**, the tube acts like a stiff air spring — defeats the
purpose, rear wave reflects. **Above `f_c`**, the wave propagates
and can be absorbed. Design target: `f_c ≤ ½ × lowest passband
frequency` of the driver this chamber serves.

The tube length also matters independently: the tube should be **at
least λ/4 long at the lowest absorbed frequency**, so the wave has
distance to dissipate. For a 200 Hz lower cutoff (λ ≈ 1.7 m): tube
length ≥ 430 mm.

## 3. Practical sizing

| Driver type           | Lowest frequency | Cutoff target | Length target |
|-----------------------|--------------------|----------------|----------------|
| Tweeter (1" dome)     | 2 kHz             | 1 kHz          | ~85 mm        |
| Mid (4-5")             | 300 Hz            | 150 Hz         | ~570 mm       |
| Midbass (6.5-8")       | 100 Hz            | 50 Hz          | ~1.7 m        |
| Woofer (10"+)          | 30 Hz             | 15 Hz          | ~5.7 m        |

Tweeter-sized Nautilus tubes are pocket-sized and trivial to
implement (B&W and many DIY designs do this). Mid-range tubes are
manageable. Full LF Nautilus is impractical — even B&W's flagship
Nautilus combines a long mid/HF tapered tube with a conventional
sealed sub for the bottom octave.

## 4. Taper profile choices

| Profile         | Equation               | Behavior                                |
|------------------|------------------------|------------------------------------------|
| Conical          | `A(x) = A_0 + k·x` linear | Simplest; predictable but less ideal loading |
| Exponential      | `A(x) = A_0 · e^(-m·x)` | Classic Nautilus; constant flare rate   |
| Hyperbolic       | Salmon's family         | Trade LF loading vs HF smoothness        |
| Tractrix         | `r(x) = a·sech(x/a)`    | Constant spherical wavefront curvature   |

Exponential is the standard. Tractrix-shaped Nautilus tubes are
sometimes used for tweeter rear chambers where wavefront control
within the tube matters.

For a tube with throat area `A_t` and mouth area `A_0`, the
exponential's flare constant:

```
m = (1/L) · ln(A_0 / A_t)
f_c = m · c / (4π)
```

For an exponential tube 500 mm long, mouth 80 cm² (4" dia), throat
4 cm² (~2.5 mm dia):
```
m = (1/0.5) · ln(80/4) = 2 · ln(20) ≈ 6.0 (per m)
f_c = 6.0 · 343 / (4π) ≈ 164 Hz
```

This tube works above ~160 Hz — appropriate for a midrange driver
crossing in at 200 Hz.

## 5. Damping strategy

Without damping, the tapered tube is just a long resonator; the
wave reaches the throat, reflects, and comes back. **Damping is
required**, distributed appropriately:

- **Light at the mouth**: don't block the cone's rear motion;
  preserve low acoustic impedance.
- **Heavy at the throat**: where the wave's amplitude has built up
  through the contraction; absorb it before it reflects.
- **Gradient stuffing**: density ramps from low at the mouth to
  high at the throat. Long-fiber wool, polyester batting, or melamine
  foam.
- **Inner-wall lining vs core stuffing**: the wall lining preserves
  cross-section better; core stuffing absorbs more per unit length
  but reduces effective volume.

Some DIY Nautilus implementations use **3D-printed lattice damping
mandrels** — a structured infill that absorbs without packing
fiber. Effective in the mid range; less so below 100 Hz.

Damping density rule of thumb: ~5 g/L for moderate absorption,
~15 g/L for heavy. Don't pack solid — that creates a hard
reflector. Loose, even distribution along the tube length.

## 6. Packaging: straight, spiral, coiled

Acoustically, a 1 m straight tube and a 1 m spiral tube are
**equivalent** (assuming smooth taper and no kinks at the bends).
The spiral is a packaging trick to fit a long tube into a small
footprint — B&W's literal nautilus shape solved a volume problem,
not an acoustic one.

| Packaging       | Pros                              | Cons                                  |
|------------------|-----------------------------------|----------------------------------------|
| Straight tube    | Easy to build; smooth taper       | Long footprint                         |
| Bend (single elbow) | Halves footprint              | Slight reflection at the bend          |
| Helix / coil     | Compact; uniform internal geometry | Tricky to maintain smooth taper        |
| Logarithmic spiral (Nautilus) | Iconic; very compact   | Hardest to build; mostly aesthetic     |

For DIY: a **straight exponential tube** with a smooth wall is the
easiest and works as well as the spiral. A 3D-printed spiral is a
photogenic option for show pieces but adds complexity for no
acoustic gain.

### Bends and kinks

A smooth bend with radius ≥ 4× tube cross-section's smaller
dimension introduces negligible reflection. Sharp bends (90° or
sharper without radius) act as partial reflectors and introduce HOMs
(higher-order modes) — the same problem horns have. Keep bend radii
generous.

## 7. Decoupling from the main cabinet

If the tapered chamber is for a midrange driver, the woofer in the
main cabinet creates significant pressure swings. **Isolate** the
tube from the woofer chamber:

- Mount the tube's flange to the baffle with a **compressible
  gasket** (closed-cell foam or rubber).
- Use a **separate sub-enclosure** if the tube is internal to a
  larger cabinet (e.g. inside a tower).
- Pad the tube exterior with constraint-layer damping (CLD) to
  prevent it from radiating sympathetically to woofer panel
  modes.

For a fully separate tube (mounted externally, like the B&W
Nautilus), this is automatic.

## 8. When to use a tapered rear chamber

**Good fit:**
- Reference-grade midrange where any coloration matters.
- Tweeter rear-loading for the cleanest top end (B&W uses these on
  most premium models, not just the Nautilus).
- DIY full-range driver in a back-loaded tapered pipe (a hybrid of
  Nautilus and BLH).
- 3D-printed mid/HF prototypes where the spiral is easy to print.

**Poor fit:**
- LF (< 80 Hz): tube length becomes impractical.
- Compact bookshelves: the tube wants real estate.
- Builds where the cabinet aesthetic is industrial / minimal — the
  tube's organic shape clashes.
- High-power PA: tapered tubes pack less SPL per liter than
  conventional alignments.

## 9. Comparison to alternatives

| Approach              | Coloration | Size penalty | LF performance | Cost      |
|------------------------|-------------|----------------|------------------|------------|
| Sealed box + stuffing | medium      | small          | good (small box) | low       |
| Ported box + stuffing | medium      | small          | very good        | low       |
| Aperiodic / damped vent | low-med  | small          | moderate         | low-med   |
| Transmission line     | low         | medium-large    | very good (augmented) | medium |
| Tapered rear chamber  | very low    | medium (mid only) | doesn't help LF | high      |
| Open baffle / dipole  | very low    | large          | needs assist     | medium    |

The tapered chamber wins for **midrange coloration** at the cost of
volume per liter of woofer-equivalent enclosure. It is **not** a
bass-loading strategy — for a multi-way design, the woofer still
needs a conventional sealed or ported box (or its own large TL or
horn).

## 10. DIY design workflow

1. **Pick the driver's lowest passband frequency** `f_low` (e.g.
   200 Hz for a midrange crossed at 250 Hz LR4).
2. **Set tube cutoff** `f_c ≤ f_low / 2` (e.g. 100 Hz).
3. **Set tube length** `L ≥ c / (4 · f_c)` (e.g. ≥ 860 mm).
4. **Pick mouth area** equal to driver's `S_d` or slightly larger.
5. **Pick throat area** = mouth / (e^(m·L)) (e.g. 1-5 cm²).
6. **Choose taper profile** (exponential default; tractrix for
   tweeter where wavefront matters).
7. **Choose packaging** (straight if space allows; coil/spiral for
   compact).
8. **Plan damping**: gradient from light at mouth to heavy at
   throat.
9. **Build the tube**: CNC laminated wood, cast urethane, 3D-printed
   plastic, or rolled metal sheet.
10. **Test**: measure the driver's impedance free-air vs in the
    tube. The tube should **suppress the free-air Fs peak** by
    10-15 dB without introducing new peaks above ~200 Hz. If the
    Fs peak is still strong, the tube cutoff is too high or
    damping is insufficient.

## 11. CAD parametric model

For a parametric exponential tapered tube:

```python
# Design parameters
tube_mouth_dia   = 95 mm        # match driver Sd
tube_throat_dia  = 10 mm
tube_length      = 800 mm
tube_taper_profile = "exponential"  # or "conical", "tractrix"

# Derived
tube_mouth_area  = π · (tube_mouth_dia/2)²
tube_throat_area = π · (tube_throat_dia/2)²
flare_constant_m = ln(tube_mouth_area / tube_throat_area) / tube_length
cutoff_f_c       = flare_constant_m · 343 / (4π)
quarter_wave_low = 343 / (4 · tube_length)
```

For 3D-printing: a swept loft along the central axis with the area
profile interpolated by the flare constant. For CNC laminated wood:
slice into rings 10-20 mm thick, each with the local cross-section,
glue-stack and turn smooth.

## 12. Speaker-cabinet integration example

For a three-way tower (see `cookbooks/three-way-tower.md`) with a
Nautilus tapered chamber for the mid:

```
   front (driver mounted here)
       |
       v
   +------+
   | mid  |              <-- 5" mid in own sealed chamber
   |======|              <-- silicone-isolated flange
   |  /\  |              <-- tapered tube starts wide
   | /  \ |
   ||   ||              <-- internal damping ramps up
   ||   ||
   ||   ||
   |   |              <-- tube ends (closed throat with foam)
   +-----+

   The mid's rear-firing tapered tube replaces the conventional
   sealed sub-enclosure. The woofer sits below in its own
   conventional ported chamber.
```

Tube spec for a 5" mid (Fs = 80 Hz, working 200 Hz–2.5 kHz):
- Mouth dia = 100 mm (matching `S_d`)
- Throat dia = 12 mm
- Length = 600 mm
- Cutoff `f_c` ≈ 130 Hz (well below 200 Hz passband)
- Damping: lightly stuffed at mouth, gradient to heavy at throat

Result: mid passband response within ±1 dB of anechoic prediction;
free-air impedance Fs peak suppressed > 10 dB; cabinet coloration
inaudible above 100 Hz.

## Cross-references

- `references/enclosures.md` — broader alignment context
  (sealed, ported, BP, horn, TL).
- `references/closed-box-geometry.md` — sealed-box alternative for
  the same driver role.
- `references/baffle-and-cabinet-acoustics.md` — internal modes
  that this design eliminates.
- `references/horns-and-waveguides.md` — the Webster equation
  used here, applied in reverse.
- `references/measurement.md` — verifying the tube's effect on
  driver impedance.
