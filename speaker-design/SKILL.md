---
name: speaker-design
description: Use when designing, analyzing, or troubleshooting loudspeakers and related acoustic systems — including driver selection, Thiele/Small parameters, enclosure types (sealed, ported, bandpass, horn, transmission line), crossover networks, cone and cabinet materials, frequency response and directivity, room acoustics, and the underlying physics of sound (wave equation, SPL, impedance, radiation).
---

# Speaker Design

This skill carries reference knowledge for loudspeaker engineering across
three layers, in increasing abstraction:

1. **Physics of sound** — wave behavior, SPL, radiation, room interaction.
2. **Acoustic properties** — measurable system behavior (FR, distortion,
   directivity, impedance) and the parameters that drive it.
3. **Materials and construction** — what physical parts you build a speaker
   from, and how their properties show up in the acoustic result.

## When to load which reference

Skim this file first, then load the reference document closest to the
user's question. Most real questions span layers — for example, choosing a
cone material requires understanding what cone breakup is (acoustics) and
why stiffness-to-mass ratio governs it (physics).

| Topic the user asks about                          | Load                                     |
|----------------------------------------------------|------------------------------------------|
| sound waves, SPL math, room modes, near/far field  | `references/physics-of-sound.md`         |
| frequency response, distortion, directivity, Q     | `references/acoustic-properties.md`      |
| Fs, Qts, Vas, BL, Xmax, driver datasheets          | `references/thiele-small.md`             |
| sealed / ported / bandpass / horn / TL tuning      | `references/enclosures.md`               |
| crossover order, slope, alignment, BSC, Zobel      | `references/crossovers.md`               |
| cone, surround, magnet, voice coil, cabinet stock  | `references/materials.md`                |

## Design workflow

When the user is actually designing a speaker (not just asking a
conceptual question), walk them through this loop:

1. **Define the target** — bandwidth, max SPL, distortion ceiling, size,
   placement, room. Without targets, every parameter is arbitrary.
2. **Pick a driver topology** — number of ways, driver sizes, cone/dome
   choices. Sanity-check against the target SPL and bandwidth.
3. **Choose the enclosure alignment** for each driver. Use Thiele/Small
   to predict low-end response; pick sealed for transient accuracy and
   small box, ported for ~3 dB more efficiency near tuning, etc.
4. **Design the crossover** — pick acoustic target slopes (LR2, LR4 are
   common), then derive electrical components accounting for driver
   impedance (Zobel, LCR notches as needed) and on-axis blend.
5. **Account for baffle and room** — baffle step compensation (BSC),
   diffraction from cabinet edges, room gain below the Schroeder
   frequency, boundary loading.
6. **Measure and iterate.** Simulations are starting points, not answers.
   Gated quasi-anechoic measurements above ~200 Hz + nearfield merge
   below it gives a usable in-room prediction.

## Output discipline

- Show formulas with their variables defined, in SI units, with the
  assumptions noted (e.g. "valid for ka < 1", "small-signal only",
  "lossless box").
- When citing a value, give the formula it came from, not just the number.
- Prefer plots/diagrams over prose for transfer functions, impedance, and
  polar response — if the environment can't render them, describe the
  shape (slope, peak frequency, Q) explicitly.
- Distinguish **electrical**, **mechanical**, and **acoustical** domains
  when discussing impedance, Q, or power. Mixing them silently is the
  most common error in DIY speaker writing.
