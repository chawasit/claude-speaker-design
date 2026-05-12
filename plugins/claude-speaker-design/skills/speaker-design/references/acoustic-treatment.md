# Acoustic Treatment

The room is part of the speaker. Below the Schroeder frequency,
room modes can swing SPL ±10 dB at the listening seat — bigger than
any speaker design can overcome. Above Schroeder, reflections add
spaciousness when controlled and smear localization when uncontrolled.
The cure is treatment: porous absorbers, tuned absorbers, and
diffusers, placed strategically.

This file covers the materials, the placements, the math for sizing
panels, and how to decide when treatment is enough vs. when to
keep adding.

## 1. The three treatment categories

| Treatment           | Mechanism                                | Effective range          |
|---------------------|------------------------------------------|---------------------------|
| Broadband absorber  | Porous: friction dissipation in fibers   | ~100 Hz to 20 kHz         |
| Bass trap (tuned)   | Helmholtz, membrane, or thick porous     | 30 Hz to 300 Hz           |
| Diffuser            | Scatters specular reflections            | 300 Hz to 5 kHz typically |

A well-treated mixing room typically uses all three. A normal
listening room often gets by with broadband absorbers + bass traps
in corners.

## 2. Porous absorber physics

A porous absorber works by friction: air moves through the fibrous
material, drags against fibers, and acoustic energy becomes heat.
Effectiveness depends on:

1. **Thickness** (more = lower frequency).
2. **Flow resistivity** σ (Pa·s/m²): too low and waves pass straight
   through; too high and they reflect off the surface.
3. **Distance from wall (air gap)**: positions the absorber at a
   velocity maximum for the target frequency, where porous
   absorption is most effective.

### Approximate absorption coefficient

For a porous panel of thickness `d` mounted at distance `s` from a
hard wall:

- **No air gap**: peak absorption at frequency where `d ≈ λ/4`, i.e.
  `f = c / (4d)`.
- **With air gap `s`**: peak absorption shifts down to
  `f ≈ c / (4(d + s))`.

For 50 mm of mineral wool (σ ≈ 8000–20000 Pa·s/m²):
- Direct on wall: peak around 1.7 kHz (1/4 wavelength = 50 mm).
- Plus 50 mm air gap: peak around 860 Hz.
- Plus 200 mm air gap: peak around 343 Hz.

Below the peak, absorption falls 6–12 dB/oct. Above the peak, stays
close to 1.0 to about 5×peak frequency before declining.

### Flow resistivity choices

| Material                              | σ (Pa·s/m²)     | Notes                              |
|---------------------------------------|------------------|-------------------------------------|
| Rockwool / Roxul Safe'n'Sound         | 8,000–10,000    | "broadband" standard               |
| Owens Corning 703 (rigid fiberglass)  | 20,000          | denser; mid/HF emphasis            |
| Owens Corning 705                     | 33,000          | very dense; HF; reflective at LF   |
| Open-cell acoustic foam (Auralex etc.)| 5,000–15,000    | varies by product                   |
| Compressed polyester                  | 10,000–15,000   | safer to handle than mineral wool   |

For LF bass-trap use: 8,000–10,000 Pa·s/m². For mid/HF first-reflection
treatment: 15,000–25,000 Pa·s/m². The intuition: low σ for LF (waves
need to penetrate to get to the velocity maximum); high σ for HF
(wave is absorbed near the surface).

### Panel thickness for target frequency

Rule of thumb: to cover down to frequency `f`, total thickness
(material + air gap) ≥ `c / (4f)`:

| Target lowest f | Total depth | Typical build                           |
|-----------------|-------------|------------------------------------------|
| 1 kHz           | 86 mm       | 50 mm material on wall                  |
| 500 Hz          | 172 mm      | 50 mm + 100 mm air gap, or 150 mm material |
| 300 Hz          | 286 mm      | 100 mm + 200 mm air gap                 |
| 100 Hz          | 858 mm      | 300 mm + 500 mm air gap (corner trap)   |
| 50 Hz           | 1716 mm     | Impractical with porous alone; use Helmholtz |

A "first-reflection" panel for the 500 Hz–8 kHz band is typically
50–100 mm of fluffy mineral wool in a frame.

## 3. Bass traps (low-frequency treatment)

### Thick porous

A corner-stacked block of 100–200 mm thick mineral wool, ideally
straddling **two walls and the floor or ceiling**. Corners are
modal-pressure maxima for all axial modes — absorbing there is
maximally efficient per square meter of treatment.

Effective from ~80 Hz to ~500 Hz with typical builds. For deeper
absorption, scale up: a "superchunk" trap (40 cm × 40 cm × 250 cm
tall mineral wool in a corner) gets down to ~50 Hz.

### Helmholtz resonators

A sealed cavity with a port (slit, perforated panel, or single
hole). Tuned to a specific frequency:

```
f = (c / 2π) · √(A / (V · L_eff))
```

where `A` is port area, `V` is cavity volume, `L_eff` is the effective
port length (physical + end correction).

- Very narrow absorption band (Q = 10–30); a 60 Hz resonator
  absorbs at 56–64 Hz and basically nothing above or below.
- Effective when targeting one specific room mode that EQ alone
  can't fix.
- DIY-able with sheet wood + perforated panel + mineral wool
  packing.

### Membrane absorbers

A sealed cavity with a wood or metal membrane on the front. The
membrane resonates at:

```
f = 60 / √(m · d)    Hz (approximately, m in kg/m², d in m)
```

where `m` is membrane areal mass and `d` is cavity depth.

For 3 mm plywood (m ≈ 2.0 kg/m²) on a 100 mm cavity:
`f = 60 / √(0.2) ≈ 134 Hz`.

Modest LF absorption (α ≈ 0.5–0.7), wider band than Helmholtz
(Q = 3–8), but harder to build well.

### Tuned vs broadband

A typical room treatment plan:
- **Corners**: 2-3 thick porous superchunks for the 60–300 Hz region.
- **One or two Helmholtz traps** for specific room modes (e.g. a 35 Hz
  axial mode that even thick porous can't reach).
- **Front and rear walls**: broadband absorbers for first reflections
  and front-wall SBIR.

## 4. Diffusers

A diffuser scatters specular reflections into a hemisphere, breaking
up the comb-filter pattern an early reflection would otherwise create.

### Why diffuse instead of absorb

- **Absorber**: removes the energy → quieter room → less reverberant
  → can feel dead.
- **Diffuser**: redirects the energy → spreads spatially and
  temporally → preserves liveness without coloration.

A treatment plan with all absorbers risks an "anechoic-chamber"
feel. Mixing absorbers (for problem reflections) with diffusers
(for the rear wall, behind the listener) is the common balance.

### Diffuser types

| Type                       | Bandwidth        | Notes                              |
|----------------------------|------------------|-------------------------------------|
| Schroeder QRD (quadratic residue) | ~1 octave centered on design freq | classic; well-understood   |
| Schroeder PRD (primitive root)    | ~1 octave         | wider lobe coverage         |
| Skyline / 2D primitive root        | broadband across 2 octaves | best at scattering uniformly |
| Geometric (pyramids, hemispheres)  | broadband but uneven | aesthetic; cheap            |
| Polycylindrical (BBC binary array) | ~1 octave         | rare but effective; flat fronts |

QRD diffusers are the dominant choice — well-studied since
Schroeder's 1975 paper, easy to build, predictable behavior.

For a 1 kHz QRD diffuser: well depth = c/2f ≈ 17 cm; well count = 7
or 11 (primes); period = 7 or 11 wells. Wider working range needs
deeper wells.

### Where to use diffusers

- **Rear wall** (behind listener): the most common diffuser
  location. Scatters the listener-position reflection that
  otherwise hits the back of the head.
- **Front wall** (between speakers): less common; usually absorbers
  here to control SBIR.
- **Ceiling cloud**: hybrid absorber-front + reflective-back can
  combine absorption + diffusion vertically.

## 5. First reflections and the "mirror trick"

See `listening-setup.md` for the mirror procedure to locate
sidewall, floor, and ceiling first-reflection points. Treat the
points with **broadband absorber** (50–100 mm thick, 50×50 cm to
80×80 cm panel).

Floor: a thick rug between the speakers and listener absorbs HF
floor bounce. Doesn't help below 500 Hz.

Ceiling: a "cloud" panel suspended at the first-reflection point
above the listener. Or hang absorbers over the speaker plane (the
"compact array" cloud).

## 6. LEDE (Live End, Dead End)

A studio control-room treatment philosophy: the "speaker end" is
dead (absorbent), the "listener end" is live (reflective, often with
diffusers). The intent: direct sound from the speakers is
uncolored by early reflections, but the room remains acoustically
"alive" enough to feel natural.

Standard implementations:
- Front wall, sidewalls (speaker third): broadband absorbers.
- Floor: rug between speakers and listener.
- Rear wall: diffusion.
- Ceiling: cloud above speakers and listener.

LEDE is most common in mixing rooms and audiophile listening
rooms. Less common in home theater rooms (where multi-channel
surround needs all walls to support reflective decay).

## 7. RT60 (reverberation time)

`T_60` is the time for SPL to fall 60 dB after the source stops.
Target ranges:

| Space                       | T_60 target (500 Hz)   |
|-----------------------------|------------------------|
| Anechoic chamber            | < 0.05 s               |
| Critical mixing room        | 0.2–0.3 s              |
| Hi-fi listening room        | 0.3–0.5 s              |
| Comfortable living room     | 0.4–0.6 s              |
| Untreated empty bedroom     | 0.6–1.0 s              |
| Concert hall                | 1.5–2.5 s              |
| Cathedral                   | 5–8 s                  |

Sabine's formula:

```
T_60 = 0.161 · V / (S · α_avg)    (V in m³, S in m²)
```

For a 50 m³ room with all surfaces having average absorption
α = 0.1: T_60 ≈ 0.7 s. Adding 3 m² of broadband absorber
(α ≈ 0.85): effective Sα goes from 12 to 14.5 → T_60 drops to 0.6 s.

In practice: every panel of 80×60 cm broadband absorber drops T_60
by about 5–10 % in a typical residential room. Real rooms diverge
from Sabine at LF; below ~150 Hz, mode-by-mode analysis is more
useful than T_60.

## 8. Treating a room: a procedure

For a typical living-room-sized listening space:

1. **Measure baseline**. Sweep at the listening seat. Note: worst
   modal peaks, T_60 per band, first-reflection times from impulse
   response.
2. **Treat corners first**. 2-4 superchunks of 200 mm mineral wool
   in vertical floor-to-ceiling corners. Re-measure.
3. **Treat first reflections**. Absorbers at sidewall (mirror-trick
   points), front-wall behind the speakers, and a small ceiling
   cloud. Re-measure.
4. **Rear wall**. A diffuser or absorber depending on the room's
   character. If T_60 is now too short, install diffuser; if still
   reverberant, more absorber.
5. **Tune with PEQ**. After treatment is "good enough", measure
   again and EQ remaining modal peaks (never nulls).
6. **Listen for a week** on familiar material. Resist over-treating.

A "good enough" target for a residential listening room:
- T_60 (500 Hz, listening position): 0.35–0.45 s.
- Frequency response at the seat, post-EQ: ±4 dB from 30 Hz to 5 kHz.
- First-reflection arrival > 6 ms after direct (gives speakers
  enough "head start" for stereo image to lock).

## 9. Acoustic-treatment math: a working budget

For a 50 m³ room targeting T_60 = 0.4 s:

```
Required total absorption Sα = 0.161 · V / T_60 = 0.161 · 50 / 0.4 = 20.1 m²
Existing absorption (carpet, furniture, drywall):
  carpet (15 m², α=0.4)      = 6 m²
  furniture, walls (rest, α=0.1) ≈ 5 m²
  total existing             = 11 m²
Need to add:                 ≈ 9 m² of α=1.0 absorber
i.e. 9 panels of 60×80 cm broadband absorber (each ~0.5 m² at α≈0.9).
```

Distribute these around the room — not all on one wall.

## 10. What NOT to do

- **Don't carpet/foam the entire room**. T_60 below 0.2 s feels
  oppressive; treble dies first because porous foam absorbs HF
  preferentially → midbass-heavy "fog".
- **Don't use thin foam** (25 mm "egg crate" or studio foam) below
  500 Hz. It doesn't absorb LF; you just get false confidence.
- **Don't trap one corner only** — symmetry matters for stereo
  image. Trap pairs of corners.
- **Don't EQ a null** in the bass region (a null at the seat is a
  null in the room — boosting just makes the null worse and the
  ringing longer). Move the speaker or the listener, or add a
  second sub.
- **Don't ignore the floor**. A bare hard floor between speakers
  and listener is the worst single early-reflection contributor.
- **Don't treat ceilings without measuring** — they often need less
  than the manufacturer ad copy suggests.

## Cross-references

- `references/listening-setup.md` — placement before treatment.
- `references/room-response-simulation.md` — predict modes and decay
  before installing.
- `references/measurement.md` — REW workflow for treatment
  before/after comparison.
- `references/subwoofers.md` — multi-sub is treatment for room modes
  at the source, not the receiver.
- `references/standards-and-targets.md` — what response/decay to aim
  for.
