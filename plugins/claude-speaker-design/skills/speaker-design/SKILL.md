---
name: speaker-design
description: Use when designing, building, measuring, simulating, or troubleshooting any loudspeaker, speaker, speaker box, subwoofer, tweeter, woofer, midrange, studio monitor, headphone, IEM, hi-fi system, PA system, line array, soundbar, or DIY audio project — or the room it plays in. Covers Thiele/Small driver parameters; enclosure types (sealed box, ported / vented / bass-reflex, bandpass, horn, transmission line, open-baffle dipole, Nautilus / tapered rear chamber, spiral / back-loaded); cabinet sizing, port tuning, and port chuffing; passive and active/DSP crossovers (LR2, LR4, FIR, IIR, Linkwitz transform); baffle step compensation, edge diffraction, panel and internal modes; cabinet materials (MDF, plywood, HDF, cone, dome, voice coil, magnet, surround, spider); driver types (moving-coil, compression driver, ribbon, AMT, planar magnetic, electrostatic, coaxial); phase plugs; horns and waveguides (tractrix, exponential, OS waveguide, constant-directivity); point-source vs line-array system topology; subwoofer design and multi-sub placement (Welti); room acoustics, listening setup (equilateral triangle, toe-in, listener height, first reflections, SBIR), and acoustic treatment (bass traps, broadband absorbers, diffusers, LEDE, RT60); measurement workflows (REW, gated quasi-anechoic, impedance sweeps, T/S extraction by added mass, impulse and step response, group delay, Klippel large-signal, polar / CTA-2034 spinorama); reference target curves (Harman, B&K, ISO 226 equal-loudness, AES2, IEC 60268); and the wave-acoustics physics underneath.
---

# Speaker Design

Reference knowledge and tools for loudspeaker engineering. Use this
skill whenever a question touches transducers, enclosures, crossovers,
acoustic measurement, or audible behavior of physical sound sources.

## Three layers

1. **Physics of sound** — wave behavior, SPL, radiation, room interaction.
2. **Acoustic properties** — measurable system behavior (FR, distortion,
   directivity, impedance) and the parameters that drive it.
3. **Materials and construction** — what a speaker is built from, and
   how each part's physical properties surface in the acoustic result.

## Routing table

Load the reference closest to the user's question. Skim only — don't
preload everything; this skill is structured for progressive disclosure.

| User is asking about                                | Load                                |
|-----------------------------------------------------|-------------------------------------|
| sound waves, SPL math, room modes, near/far field   | `references/physics-of-sound.md`    |
| frequency response, distortion, directivity, Q      | `references/acoustic-properties.md` |
| Fs, Qts, Vas, BL, Xmax, datasheet interpretation    | `references/thiele-small.md`        |
| sealed / ported / bandpass / horn / TL tuning       | `references/enclosures.md`          |
| crossover order, slope, alignment, BSC, Zobel       | `references/crossovers.md`          |
| cone, surround, magnet, voice coil, cabinet stock   | `references/materials.md`           |
| compression, ribbon, AMT, planar, electrostatic     | `references/driver-types.md`        |
| REW, gating, Klippel, polar, T/S extraction         | `references/measurement.md`         |
| subwoofers, multi-sub, room gain, sub integration   | `references/subwoofers.md`          |
| active speakers, FIR/IIR DSP, room correction       | `references/dsp-and-active.md`      |
| baffle step, edge diffraction, panel/internal modes | `references/baffle-and-cabinet-acoustics.md` |
| closed-box geometry, shape, Vb, driver placement    | `references/closed-box-geometry.md` |
| room modes, image method, FEM/FDTD, multi-sub sim   | `references/room-response-simulation.md` |
| horn flare, waveguide, OS, tractrix, CD, Hornresp   | `references/horns-and-waveguides.md` |
| Nautilus / tapered rear chamber, spiral back, rear-wave absorption | `references/tapered-rear-chambers.md` |
| compression-driver phase plug, coaxial bullet, tangerine | `references/phase-plugs.md` |
| point source, coaxial, line array, CBT, splay       | `references/point-source-and-line-arrays.md` |
| listening triangle, toe-in, height, first-reflection | `references/listening-setup.md`     |
| absorbers, bass traps, diffusers, LEDE, T_60         | `references/acoustic-treatment.md`  |
| spinorama (CTA-2034), Harman target, standards       | `references/standards-and-targets.md` |
| impulse / step response, group delay, audibility     | `references/time-domain.md`         |
| over-ear, IEM, planar, Harman headphone target       | `references/headphones.md`          |
| terminology lookup (cross-skill)                     | `references/glossary.md`            |
| foundational papers, books, standards, web resources | `references/bibliography.md`        |

## Calculation tools

Executable helpers live in `tools/`. Run them from this directory.
Prefer them to manual arithmetic — they bake in unit handling and end
corrections you will otherwise forget.

| Tool                          | What it computes                              |
|-------------------------------|-----------------------------------------------|
| `tools/ts_from_added_mass.py` | T/S parameters from free-air + added-mass Fs  |
| `tools/sealed_box.py`         | F_c, Q_tc, -3 dB from T/S and box volume      |
| `tools/ported_box.py`         | B4/QB3/C4 box and Fb from T/S                 |
| `tools/port_length.py`        | Port length from area, Vb, target Fb          |
| `tools/crossover_lr.py`       | Linkwitz-Riley filter component values        |
| `tools/xmax_spl.py`           | Displacement-limited SPL vs. frequency        |
| `tools/room_modes.py`         | Axial/tangential/oblique modes, Schroeder freq |
| `tools/group_delay.py`        | Filter group delay vs. audibility threshold   |
| `tools/diffraction_olson.py`  | Baffle step + edge diffraction prediction     |

All scripts take CLI args, print results in SI, and warn when an input
violates a model assumption (e.g. `ka > 1` for piston-band T/S).

## Worked examples

`cookbooks/` carries end-to-end design walkthroughs. Read one before
the user's first real project — they show how the pieces compose.

- `cookbooks/bookshelf-2way.md` — 6.5" + 1" dome bookshelf, ported, LR4.
- `cookbooks/sealed-subwoofer.md` — 12" sealed sub with Linkwitz
  transform and a single PEQ for room mode 1.
- `cookbooks/three-way-tower.md` — 10" + 5" + 1" floor-stander, ported
  LF, sealed mid, optional active LF.
- `cookbooks/open-baffle-dipole.md` — H-frame dipole mid/HF with
  boxed LF assist; Linkwitz-school architecture.
- `cookbooks/active-studio-monitor.md` — DSP-active 6.5" + 1" with
  waveguide, Linkwitz transform, FIR option.

## Design workflow

When the user is actually designing (not just asking a conceptual
question), walk them through:

1. **Targets** — bandwidth, max SPL, distortion ceiling, size,
   placement, room. Without targets, every parameter is arbitrary.
2. **Topology** — number of ways, driver sizes, transducer types.
   Sanity-check against target SPL and bandwidth.
3. **Alignment per driver** — Thiele/Small for LF; horn/waveguide for
   HF. Predict response, excursion, port velocity.
4. **Crossover** — pick acoustic target slopes (LR2, LR4 are common),
   derive electrical components accounting for driver impedance
   (Zobel, LCR notches), check on/off-axis blend.
5. **Baffle and room** — baffle step compensation (BSC), edge
   diffraction, room gain below Schroeder, boundary loading.
6. **Measure and iterate.** Simulation is a starting point, not an
   answer. Gated quasi-anechoic + nearfield merge gives a usable
   in-room prediction.

## Output discipline

- Show formulas with variables defined, in SI units, with assumptions
  noted (e.g. "valid for ka < 1", "small-signal only", "lossless box").
- Cite the formula a value came from, not just the number.
- Prefer plots/diagrams for transfer functions, impedance, polar
  response; if the environment can't render, describe the shape (slope,
  peak frequency, Q) explicitly.
- Distinguish **electrical**, **mechanical**, and **acoustical**
  domains when discussing impedance, Q, or power. Mixing them silently
  is the most common error in DIY speaker writing.

## Pitfalls and red flags

If you see any of these in a user's design or question, flag it
explicitly:

- **Tuning a ported box below Fs** without a steep electrical high-pass
  — guarantees cone unloading and mechanical failure on low content.
- **Crossing a tweeter within 1× of its Fs** at a slope < LR4 — burns
  voice coils, raises distortion above audibility.
- **Reading datasheet sensitivity as "loudness"** — it ignores baffle
  step, room boundary, and impedance dips. The real in-room number is
  often 3–6 dB lower than the spec.
- **Designing the crossover from electrical filter formulas alone**
  without measured driver response — the acoustic slope is what
  matters, not the filter slope.
- **Believing a port works below its tuning frequency** — below Fb the
  port unloads the cone, output drops 24 dB/oct, and excursion peaks.
- **Stuffing a port** — kills the resonance you designed for.
- **Using "more damping = better"** — over-stuffed boxes lose
  efficiency and bloat the effective volume unpredictably.
- **Quoting Q without specifying which Q** — Qts, Qes, Qms, Qtc, Q of a
  filter, Q of a notch are all different things.
- **Conflating efficiency and sensitivity** — see `acoustic-properties.md`.
