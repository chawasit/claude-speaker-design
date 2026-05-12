---
name: speaker-design
description: Use when designing, analyzing, measuring, or troubleshooting loudspeakers, headphones, and acoustic enclosures. Covers driver selection (moving-coil, compression, ribbon, AMT, planar magnetic, electrostatic), Thiele/Small parameters, enclosure alignments (sealed, ported, bandpass, horn, transmission line, open baffle), passive and active/DSP crossovers, baffle diffraction, room acoustics, measurement (REW, gated quasi-anechoic, Klippel large-signal), cone/cabinet materials, subwoofer integration, and the wave-acoustics physics underlying all of it.
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

All scripts take CLI args, print results in SI, and warn when an input
violates a model assumption (e.g. `ka > 1` for piston-band T/S).

## Worked examples

`cookbooks/` carries end-to-end design walkthroughs. Read one before
the user's first real project — they show how the pieces compose.

- `cookbooks/bookshelf-2way.md` — 6.5" + 1" dome bookshelf, ported, LR4.
- `cookbooks/sealed-subwoofer.md` — 12" sealed sub with Linkwitz
  transform and a single PEQ for room mode 1.

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
