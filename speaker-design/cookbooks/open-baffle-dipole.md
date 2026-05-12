# Cookbook: Open-Baffle Dipole

An H-frame open-baffle mid/HF dipole with a separately enclosed LF
section, inspired by Siegfried Linkwitz's LX521 / Pluto philosophy.
The dipole midrange + tweeter eliminate enclosure resonances and
deliver a uniquely "live" sound; the boxed LF handles the dipole's
acoustic shortfall below ~200 Hz.

Open-baffle / dipole isn't for everyone — needs ≥1 m of rear-wall
clearance and a fairly large baffle for usable bass — but for those
with space, it's a distinct architecture worth knowing.

## Targets

| Spec                            | Target                                  |
|---------------------------------|------------------------------------------|
| Bandwidth                       | 40 Hz to 22 kHz (-3 dB)                |
| Max SPL (1 m, 1% THD)           | 100 dB                                   |
| Sensitivity (with DSP EQ)       | 85 dB SPL / 2.83 V / 1 m               |
| Listening distance              | 2.5–3.5 m, ≥ 1 m from rear wall        |
| Topology                        | Open-baffle dipole mid/HF + sealed LF assist |

## Topology

Dipole = open baffle = no enclosure. Radiation pattern is figure-8
horizontally: maximum on-axis, minimum at ±90°, opposite phase at
180°. The ±90° null is acoustically advantageous: sidewall first
reflections are not excited.

Below the baffle's effective frequency (where path length around the
edge equals λ/2), front and rear radiation cancel — output falls
6 dB/octave. Drivers with high BL and high Xmax + DSP EQ compensate.

Above the baffle frequency: clean dipole pattern, very low cabinet
coloration (no enclosure to color anything).

## Driver choice

**LF (per side, in sealed cabinet)**: 12" subwoofer driver.
Illustrative T/S as in `sealed-subwoofer.md`. Two drivers per side,
opposed-mounted (force cancellation) for low cabinet vibration.
Tuned for 40 Hz extension.

**Mid (open baffle)**: 8" or 10" driver with low Qts and high BL
(Eminence Alpha 10, GR-Research 8" Neo). Illustrative:
- Fs = 35 Hz, Qts = 0.35, Vas = 100 L
- Sd = 220 cm², Xmax = 5 mm, BL = 12 T·m
- SPL = 96 dB / 2.83 V / 1 m

**Tweeter (open baffle)**: open-back planar magnetic, ribbon, or
front-back-matched dome (B&G Neo3, RAAL ribbons, dipole-modified
soft dome with rear baffle drilled).

## Mid-baffle dimensions

For an "H-frame" or simple flat baffle, the dipole rolloff begins at:

```
f_dipole = c / (2 × baffle_path_length)
```

where `baffle_path_length` is the average distance from cone front
to cone rear around the baffle. For a flat baffle 60 cm wide:
`f_dipole ≈ 343 / (2 × 0.6) = 286 Hz`.

So a 60 cm flat baffle is usable down to ~286 Hz with no EQ; below
that, 6 dB/oct DSP boost. To extend to 200 Hz: 100 cm baffle.

H-frame: two side panels create a "U-shape" trough behind the driver.
The folded path length is the equivalent baffle width — packs more
acoustic width into less physical footprint.

For our 100 dB target at 200 Hz with 4-driver array per side:
- Per-driver SPL at 200 Hz: ~100 dB - 6 dB (4 drivers, summed) ≈ 94 dB.
- Excursion at 94 dB / 200 Hz: ~1 mm.
- With +12 dB DSP boost at 60 Hz to compensate dipole rolloff:
  excursion grows to ~16× = 16 mm. Driver Xmax = 5 mm → distortion
  rises sharply. The dipole midrange section can extend only to
  ~200 Hz before excursion limits.
- LF below 200 Hz: handled by separate boxed sub (sealed, 2 × 12"
  per side).

## LF section (boxed)

Two opposed-mounted 12" subs per side, each in its own sealed
chamber. Effective Vb per chamber: 50 L → 100 L total per side.

Use `sealed_box.py` with `Qtc = 0.7`:

```
$ python tools/sealed_box.py --fs 22 --qts 0.45 --vas 95 --qtc 0.7
Vb ≈ 65 L, Fc ≈ 35 Hz, Qtc = 0.7
```

Sealed LF with Linkwitz transform to 25 Hz (see
`sealed-subwoofer.md` for details).

Crossover to mid section at 80 Hz, LR4. The LF section is **mono**
in summed mode (low frequencies don't carry stereo cues).

## Crossover

| Region                | Crossover                       |
|------------------------|----------------------------------|
| LF → Mid               | 80 Hz, LR4, mono-sum to mid     |
| Mid → Tweeter          | 1.5 kHz, LR4, 6 dB tweeter L-pad |
| DSP dipole compensation | +6 dB/oct boost below 286 Hz   |

The dipole compensation is the **defining DSP feature**: a 6 dB/oct
boost below the baffle's effective cutoff to flatten the dipole
rolloff. Combined with the 80 Hz LR4 high-pass, the mid only sees
boost in a narrow 80–286 Hz window — manageable for a high-BL driver.

## Baffle geometry

Open baffle constructed as an H-frame:

```
          +---+
          | M |       <- 8" or 10" midrange (open baffle, both sides radiate)
          +---+
            |
            |
        +---+---+
        |       |
        | wings |     <- side panels (300 mm wide each, perpendicular to baffle)
        |       |
        +-------+
        |       |
        |  LF   |     <- separate enclosure with 2 opposed 12" subs
        |       |
        +-------+
```

Wings extend the effective baffle path length without adding overall
width. A 60 cm flat baffle with 30 cm wings on each side has
effective path ≈ 60 + 30 = 90 cm; dipole onset ≈ 190 Hz.

## Placement

- **Minimum 1 m from rear wall** — the rear radiation has to bounce
  around without immediately reflecting back to the listener.
- **Toe-in to cross in front of listener**: standard equilateral
  triangle. The ±90° null reduces sidewall reflection naturally.
- **Listener position** > 2.5 m for the dipole's "open" character.
  Nearfield listening defeats the dipole's spaciousness advantage.
- **Symmetric placement** more critical than for direct-radiator
  speakers — the figure-8 pattern is sensitive to room asymmetry.

## Verification checklist

- [ ] Mid-section response (gated, 1 m): flat 200 Hz to 1.5 kHz, dipole
      rolloff 200 Hz down (without DSP).
- [ ] With DSP boost: flat 80 Hz to 1.5 kHz.
- [ ] LF section response: flat to 25 Hz with LT.
- [ ] Crossover summing: smooth through 80 Hz handoff.
- [ ] Horizontal polar at 0°, 30°, 60°, 90°: smooth figure-8 with
      strong null at ±90°.
- [ ] Distortion at 96 dB SPL / 1 m: < 3 % at 100 Hz (high excursion
      region for mid), < 1 % above 300 Hz.

## What's different from a normal speaker

- **No cabinet coloration**: no enclosure resonances, no
  diffraction from cabinet edges. The "open" sound is real.
- **Sidewall null**: ±90° figure-8 null means sidewall first
  reflections are not excited. Reduces room dependence relative to
  conventional designs.
- **Need lots of cone area + Xmax**: dipole rolloff is real and
  must be compensated.
- **Need DSP**: open-baffle without DSP boost is mid-and-treble-only.
  DSP is core to the design.

## Cross-references

- `speaker-design/references/driver-types.md` — open-baffle section.
- `speaker-design/references/subwoofers.md` — open-baffle sub
  alternatives.
- `speaker-design/references/dsp-and-active.md` — Linkwitz transform
  and dipole-compensation EQ.
- `speaker-design/references/listening-setup.md` — placement is
  more critical for dipoles.
- `bibliography.md` — Linkwitz's web archive at linkwitzlab.com.
