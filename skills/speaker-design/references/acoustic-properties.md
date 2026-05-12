# Acoustic Properties

The system-level behaviors you measure and specify. Each property has a
target range, a measurement method, and a set of design knobs that move
it.

## Frequency response

The magnitude of the on-axis SPL transfer function vs. frequency, at a
specified distance, drive level, and environment (anechoic, in-room,
nearfield-merged).

- **Target shape (anechoic, on-axis):** flat ±2 dB from cutoff to
  ~10 kHz, with a gentle 1–3 dB downward tilt above for natural in-room
  balance ("Harman target", "B&K curve").
- **Cutoff (-3 dB):** depends on enclosure alignment (see `enclosures.md`).
  For full-range monitors, 40–50 Hz; for satellites/sub systems,
  80 Hz with the sat handed off to a subwoofer.
- **Measurement:** gated 1/12-oct smoothed FFT in a moderately damped
  room. Window length sets the lowest valid frequency: a 5 ms gate
  cuts off at ~200 Hz. Below that, splice in nearfield + diffraction
  loss.

Common deviations and causes:

| Bump or dip                             | Likely cause                                            |
|-----------------------------------------|---------------------------------------------------------|
| broad peak at port tune Fb              | bass-reflex working as intended                         |
| narrow peak at 1–4 kHz, breakup region  | cone modal resonance — material/shape issue             |
| 100–300 Hz suckout                      | floor bounce (cancellation at λ/4 to floor)             |
| 1–3 dB rise above ~500 Hz on axis       | baffle step transition; needs BSC if listened far-field |
| ragged top end off-axis only            | tweeter beaming, edge diffraction, surround resonance   |

## Sensitivity / efficiency

Two different things, often confused.

- **Sensitivity:** SPL at 1 m for 2.83 V input (= 1 W into 8 Ω, 0.5 W
  into 4 Ω). Units: dB SPL / 2.83 V / 1 m. Typical home speakers:
  82–92 dB. Pro PA drivers: 95–105 dB.
- **Efficiency:** acoustic power out / electrical power in, in percent.
  Relate to sensitivity (8 Ω, full-space) via
  `η ≈ 10^((SPL_1W1m − 112)/10)`. So 90 dB SPL/W/m ≈ 0.4 % efficient.

Sensitivity scales with `BL² / (R_e · M_ms²)` for direct radiators, so
strong motors and light cones win — at the cost of `Vas` and box size.

## Impedance

The electrical impedance `Z_e(f)` seen by the amplifier. For a sealed
driver:

```
Z_e(f) = R_e + j ω L_e + Z_mot(f)
```

with motor impedance `Z_mot = (BL)² / Z_mech` reflecting mechanical
behavior into the electrical domain. The shape:

- DC: `R_e` (voice-coil resistance).
- Peak at `Fs` (sealed) or two peaks bracketing `Fb` (ported), height
  set by `Qms` and `Qes`.
- Gentle rise above ~1 kHz from voice-coil inductance `L_e`.

**Minimum impedance** (`Z_min`, usually 50–300 Hz) is what matters for
amplifier load. A "4 Ω" speaker is typically a 6.5 Ω driver with `Z_min`
near 3.2 Ω. Most amps tolerate `Z_min ≥ 3 Ω`; below that, current
clipping and protection circuits engage.

## Phase and group delay

For listening quality, **minimum-phase** behavior (no excess delay)
matters more than literal phase flatness. Phase rotates 180° across
each crossover and resonance — that's physics, not a defect.

- **Group delay** `τ_g = −dφ/dω` is the perceived envelope delay vs.
  frequency. Audible threshold: ~1.5 cycles, so τ_g ≈ 5 ms at 80 Hz is
  the limit before "boomy" bass.
- Ported boxes have higher group delay near `Fb` than sealed; transient
  response trades for extension.
- Linear-phase / FIR crossovers eliminate phase distortion at the cost
  of latency (typically 10–30 ms) and pre-ringing.

## Directivity / polar response

How SPL varies with off-axis angle vs. frequency. Specifications:

- **Beamwidth** (e.g. "90° × 60° at −6 dB"): the angle within which the
  response is down ≤6 dB from on-axis, in horizontal × vertical.
- **DI (Directivity Index):** dB above an omni source of equal radiated
  power. Increases with frequency for direct radiators.
- **Constant-directivity** designs aim for a flat DI vs. frequency
  through the listening band, since room reflections (the
  "power response") shape perceived timbre.

Crossover regions are where directivity discontinuities show up. Match
the woofer `ka ≈ 2` to the tweeter `ka ≈ 0.5` and the polar pattern
collapses smoothly across the crossover.

## Distortion

- **THD (Total Harmonic Distortion):** RMS sum of harmonic amplitudes
  / fundamental. Target < 1 % at reference level above 100 Hz, < 10 %
  below 50 Hz at max SPL.
- **IMD (Intermodulation Distortion):** sidebands from two-tone tests
  (SMPTE, CCIF). More audible than THD because the products are
  non-harmonic.
- **Multitone / Klippel:** measure full nonlinearity vs. drive level
  and extract large-signal parameters `BL(x)`, `K_ms(x)`, `L_e(x, i)`.

Dominant distortion sources by frequency:
- `< 100 Hz`: cone displacement → `BL(x)` and `K_ms(x)` nonlinearity.
- `100 Hz – 1 kHz`: motor `L_e(i)` modulation, magnet flux modulation.
- `> 1 kHz`: surround/cone breakup, voice-coil rocking, ferrofluid in
  tweeters.

## Power handling and thermal compression

- **Continuous power:** what the voice coil can dissipate without
  exceeding 200–250 °C. Limited by coil mass, former material (kapton,
  fiberglass, aluminum), and venting.
- **Peak/program:** short-burst limit, usually 2× continuous.
- **Power compression:** as the coil heats, `R_e` rises (~+0.4 %/°C
  for copper). At 200 °C above ambient, `R_e` doubles → ~3 dB less
  output for the same input voltage. Real PA systems hit 3–6 dB
  compression at thermal limit.

## Excursion limits

- **Xmax:** linear one-way excursion where `BL` and `K_ms` stay within
  10 % of small-signal value. Set by gap height, magnet geometry, and
  spider linearity.
- **Xmech:** absolute physical limit (former bottoms, surround tears).
- Required peak excursion for a target SPL:

```
x_peak = √2 · p_ref · 10^(SPL/20) · r / (ρ₀ · S_d · f² · 2π²)
```

For 110 dB at 1 m, 40 Hz, a 6.5" cone (`S_d ≈ 130 cm²`): ~9 mm peak.
Most 6.5" drivers max out at Xmax ≈ 4–6 mm — so you need a bigger cone
or multiple drivers.
