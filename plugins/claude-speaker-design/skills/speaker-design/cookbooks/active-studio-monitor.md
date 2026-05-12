# Cookbook: Active Studio Monitor with DSP

A 6.5" + 1" two-way active monitor with DSP plate amp. Target: clean
flat anechoic response, controlled directivity, suitable for mixing
at 1.5–2 m. Compared to the passive bookshelf cookbook: same drivers,
but each driver gets its own amplifier channel and DSP-derived
crossover; FIR option for linear-phase critical-listening builds.

## Targets

| Spec                              | Target                                |
|-----------------------------------|----------------------------------------|
| Bandwidth                         | 40 Hz to 22 kHz (-3 dB)               |
| Max SPL (1 m, 1 % THD)            | 105 dB                                 |
| Anechoic response (1/12 oct)      | ±1.5 dB, 100 Hz – 10 kHz              |
| Directivity (DI variation)        | ≤ 2 dB through crossover               |
| Listening distance                | 1.5–2 m, nearfield to mid-field        |
| Latency                           | < 30 ms (FIR) or < 1 ms (IIR)         |

## Drivers

Same 6.5" woofer and 1" dome as `bookshelf-2way.md`. Adding a
**waveguide** on the tweeter to control its dispersion to match the
woofer's at the crossover frequency — typical for modern active
monitors (Genelec 8341, Neumann KH 120, Adam A7V).

### Tweeter waveguide

A small (~120 mm OD) elliptical waveguide flush-mounted with the
tweeter dome. Reduces the tweeter's wide-pattern character at the
crossover frequency, where the 6.5" woofer is starting to beam.

- Crossover at 2 kHz: 6.5" woofer beamwidth ~85° at 2 kHz.
- 1" dome on flat baffle: beamwidth ~140° at 2 kHz.
- 1" dome with 90×60 waveguide: beamwidth ~90° at 2 kHz.

The match is now smooth — directivity DI variation through crossover
< 2 dB.

## Enclosure

Same 12.3 L ported (or 13 L sealed if you prefer transient response
over LF efficiency). For an active design, **sealed + DSP** is the
modern preference:

- Linkwitz transform for LF extension.
- Cleaner transient response.
- No port chuffing at high SPL.

```
$ python tools/sealed_box.py --fs 36 --qts 0.36 --vas 17 --qtc 0.7
Vb ≈ 13 L, Fc ≈ 51 Hz, Qtc = 0.7
```

LT shift from `(Fc, Qtc) = (51, 0.7)` to `(Fp, Qp) = (40, 0.5)`:
about 5 dB of boost at 40 Hz. The 6.5" with Xmax = 5 mm at 105 dB SPL
at 40 Hz needs ~8 mm excursion — slightly past Xmax. Solutions: limit
SPL at 40 Hz to 100 dB (typical nearfield monitor spec); or pair with
sub for full-range work.

## DSP chain

A modern DSP plate amp (Hypex Fusion FA122, miniDSP plate amp+DSP, or
DIY with miniDSP 2x4HD + Class D amps) implements:

```
Input ─── HP @ 30 Hz ─── Linkwitz Transform ─── Per-driver split
                                                       │
                                                       ├─ LP @ 2 kHz LR4 ─── EQ ─── Woofer amp
                                                       │
                                                       └─ HP @ 2 kHz LR4 ─── EQ + Delay ─── Tweeter amp
```

### Woofer chain

- **Subsonic HP** at 30 Hz, 24 dB/oct (prevent infrasonic content
  from eating excursion budget).
- **Linkwitz transform** biquad: source (Fc=51 Hz, Qtc=0.7) →
  target (Fp=40 Hz, Qp=0.5).
- **LP** at 2 kHz, LR4.
- **Driver EQ**: any per-driver corrections from measurement —
  typically 1-2 PEQs to flatten the in-baffle response.
- **Excursion limiter**: predict cone displacement from filter chain
  output; attenuate input when displacement exceeds 4.5 mm (10 %
  Xmax margin).
- **Thermal limiter**: model voice-coil temperature from RMS power,
  reduce gain above 180 °C.

### Tweeter chain

- **HP** at 2 kHz, LR4.
- **Driver EQ**: 1-3 PEQs to flatten the in-baffle response,
  including the on-axis rise from the waveguide.
- **Delay**: 50–100 µs to time-align with the woofer (compensate
  for tweeter being physically forward of the woofer's voice coil
  in many baffle geometries).
- **Thermal limiter**.

### Optional: FIR linear-phase

A 4096-tap FIR at 96 kHz adds ~21 ms latency but delivers:
- Linear phase across crossover (no phase rotation through fc).
- Magnitude correction at 1 dB resolution.
- Cancellation of any minimum-phase driver irregularities.

Generated in REW or rePhase from measured driver responses. Load
into the DSP plate amp's FIR convolution engine. Cost: latency
(unacceptable for live use; fine for mixing).

## Cabinet

Same 200×350×280 mm external as the bookshelf, **plus**:
- Dedicated rear bay for DSP plate amp (typically 100×200×80 mm).
- Heat sink ventilation around the amp (slot vents on rear panel).
- Optionally: angled baffle (5–10° toward listener) for typical
  desktop or near-field placement.

The amp bay shares the cabinet interior but is **sealed off
acoustically** — the driver chamber and amp chamber are separate
sub-enclosures so amplifier-cooling vents don't leak air into the
acoustic volume.

## Verification checklist

- [ ] Anechoic FR (gated 1 m): ±1.5 dB from 100 Hz to 10 kHz.
- [ ] Nearfield + diffraction merge: smooth Linkwitz-transform
      rolloff to 35 Hz with peak excursion < Xmax.
- [ ] On-axis vs ±15°: < 2 dB variation through crossover (waveguide
      effect verified).
- [ ] Polar: 90° × 60° beamwidth through 1-10 kHz (consistent with
      waveguide directivity).
- [ ] Distortion at 96 dB SPL / 1 m: < 0.5 % above 200 Hz, < 2 %
      at 50 Hz, < 5 % at 30 Hz (LT-stressed region).
- [ ] Group delay (FIR mode): < 0.5 ms variation across band (after
      compensating for the constant FIR latency).
- [ ] Excursion limiter triggers at 4.5 mm — verify by sweeping at
      max input level; cone should not exceed.
- [ ] Thermal protection: confirm gain reduction kicks in after
      ~10 min at max-SPL pink noise.

## Cross-references

- `speaker-design/cookbooks/bookshelf-2way.md` — the passive
  equivalent of this design.
- `speaker-design/references/dsp-and-active.md` — FIR vs IIR,
  Linkwitz transform.
- `speaker-design/references/standards-and-targets.md` — what
  anechoic flat looks like.
- `speaker-design/references/baffle-and-cabinet-acoustics.md` —
  waveguide and baffle design.
- `parametric-cad/cookbooks/speaker-cabinet-2way.md` — CAD; the
  amp-bay sub-enclosure is the main addition.
