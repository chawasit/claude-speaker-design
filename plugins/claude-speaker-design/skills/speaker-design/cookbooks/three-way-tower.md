# Cookbook: 10" + 5" + 1" Three-Way Tower

A full-range floor-stander: 10" woofer in a ported lower chamber, 5"
mid in a sealed upper chamber, 1" dome tweeter. Crossovers at 250 Hz
and 2.5 kHz, LR4 throughout. Designed for mid-field listening (3–4 m)
at moderate-to-high SPL in a normal living room.

## Targets

| Spec                              | Target                                    |
|-----------------------------------|--------------------------------------------|
| Bandwidth                         | 35 Hz to 22 kHz (-3 dB)                   |
| Max SPL (1 m, 1% THD)             | 105 dB                                     |
| Sensitivity                       | ≥ 88 dB SPL / 2.83 V / 1 m                |
| Nominal impedance                 | 4 Ω (min ≥ 3 Ω)                            |
| External volume                   | < 60 L                                     |
| Listening distance                | 3–4 m, free-standing ≥ 50 cm from wall    |

## Driver choice

**Woofer (10")** — illustrative T/S:
- Fs = 28 Hz, Qts = 0.36, Vas = 75 L
- Re = 3.4 Ω, Le = 0.7 mH
- Sd = 350 cm², Xmax = 8 mm, BL = 10 T·m
- SPL/2.83V/1m = 89 dB
- F_breakup ≈ 700 Hz (paper/composite cone)

**Midrange (5")** — illustrative:
- Fs = 80 Hz, Qts = 0.5, Vas = 4 L
- Re = 5.0 Ω, Le = 0.2 mH
- Sd = 87 cm², Xmax = 3 mm
- SPL = 90 dB
- F_breakup ≈ 5.5 kHz (well above 2.5 kHz crossover)

**Tweeter (1" dome)** — same as bookshelf cookbook:
- Fs = 750 Hz, Re = 4.6 Ω
- SPL ≈ 90 dB

All three drivers nominally sensitivity-matched at 89–90 dB. With BSC
and L-pads, system sensitivity will be 86–87 dB.

## Enclosure: lower (ported, 10")

Run `ported_box.py`:

```
$ python tools/ported_box.py --fs 28 --qts 0.36 --vas 75
alignment     = B4
Vb            = 50.0 L  (alpha = Vas/Vb = 1.50)
Fb            = 28 Hz   (h = Fb/Fs ≈ 1.00)
f-3dB         = ~25 Hz
```

50 L net volume for the woofer chamber. With driver displacement
(~1.2 L), bracing (~0.5 L), and minimal stuffing, **gross internal
~52 L** for the lower chamber.

### Port

Cone Sd = 350 cm². For Fb = 28 Hz with a 75 mm diameter port:

```
$ python tools/port_length.py --fb 28 --vb 50 --dia 75 --sd 350 --xpeak 4
Port area     = 44.2 cm^2  (dia 75 mm)
End correction= 63.8 mm
Effective Lp  = 335.9 mm
Physical Lp   = 272.1 mm
Port velocity = 5.6 m/s peak (OK; < 17 m/s threshold)
```

272 mm port — fits along the back panel of the 350 mm tower depth;
flares preferred at both ends to reduce chuffing at high SPL.

### Excursion check

```
$ python tools/xmax_spl.py --sd 350 --xmax 8 --target-spl 105 --f-min 25 --f-max 100
```

A 10" with Xmax = 8 mm should hit 105 dB at 1 m by ~30 Hz (with port
gain). Below port tune (28 Hz), output drops 24 dB/oct and excursion
**rises** — protect with a 24 dB/oct high-pass at ~18 Hz (active) or
accept that the driver shouldn't see content below Fb.

## Enclosure: middle (sealed, 5")

```
$ python tools/sealed_box.py --fs 80 --qts 0.5 --vas 4 --qtc 0.7
Vb            = ~8.5 L  (alpha = 0.47)
Fc            = ~97 Hz
Qtc           = 0.7
f-3dB         = ~97 Hz
```

8.5 L sealed for the midrange. This gives `Q_tc = 0.7` (Butterworth)
with `F_c = 97 Hz`. Since crossover to woofer is at 250 Hz at LR4,
the mid's natural rolloff is well below — clean handoff.

Internal mid enclosure: ~9 L gross, with stuffing, in its own
isolated sub-chamber inside the tower. **Critical**: the mid chamber
must be acoustically isolated from the woofer chamber (separate
sealed sub-enclosure) — otherwise the woofer's huge pressure swings
modulate the mid's volume and add IMD.

## Cabinet layout

```
                 +-----+
                 |  T  |  <- tweeter at top
                 |     |
                 +-----+
                 |  M  |  <- midrange in own sealed chamber
                 |     |
                 +-----+
                 |     |
                 |     |
                 |  W  |  <- 10" woofer, ported chamber below
                 |     |
                 |     |
                 +-----+
                 |port |  <- rear-firing or front-slot port
                 +-----+
                 |feet |
                 +-----+

External: 250 mm W × 1050 mm H × 350 mm D
Internal volume: ~9 L (mid) + ~52 L (woofer) = 61 L total
```

The tweeter sits highest (acoustic center at ear height when
sitting). Mid below it (acoustic-center spacing ≤ 1λ at 2.5 kHz).
Woofer at the bottom, port on the rear panel or front-firing slot
between feet.

Tweeter offset 15 mm from baffle centerline for diffraction
smoothing. Stand height target: tweeter at 950 mm above floor.

## Crossover

Two crossovers — woofer/mid at 250 Hz, mid/tweeter at 2.5 kHz —
each LR4 acoustic.

```
$ python tools/crossover_lr.py --fc 250 --z 4 --order LR4 --re 3.4 --le 0.7
$ python tools/crossover_lr.py --fc 2500 --z 8 --order LR4 --re 5.0 --le 0.2
```

Plus:
- Zobel networks at both bandpass driver inputs.
- LCR notch on the woofer at ~700 Hz to kill the cone-breakup peak
  (verify with measurement; typical values around 2.2 mH + 4.7 µF + 3 Ω).
- L-pad on the tweeter for ~3 dB attenuation.

For **passive**, the woofer/mid crossover at 250 Hz requires a 6 mH
or larger inductor — expensive (~$50 each, air-cored). Many three-way
designs go **active for the woofer** (DSP amp drives it, with the
mid+tweeter on a passive crossover) to avoid the large inductor and
gain better LF EQ flexibility.

### Active variant

A **2.1-channel DSP active** approach:
- Woofer: DSP-driven, sealed/ported alignment in software, LR4 LP
  at 250 Hz. Linkwitz transform for LF extension if desired.
- Mid+tweeter: passive LR4 at 2.5 kHz; the DSP delivers a single
  pre-mixed signal at high voltage.

This is the modern "powered tower" topology (KEF Reference Meta,
some Genelec full-range, Buchardt).

## Baffle and box geometry

- Internal aspect ratio: woofer chamber 240 × 700 × 320 mm
  internal; ratio 1 : 2.9 : 1.3. Not great (the 1:2.9 should have
  more aspect on the 2.9 side) — partition the woofer chamber with
  a horizontal brace at the modal pressure node ~360 mm from one
  end.
- 25 mm roundovers on front vertical edges.
- 18 mm MDF + 25 mm bracing (the cabinet is taller, panels longer,
  thus bracing matters more).
- Internal stuffing only in the mid chamber and the top half of the
  woofer chamber (away from the port).

## Internal-volume verification chain

After CAD:

1. Net internal mid volume after driver displacement: target 8.5 L.
2. Net internal woofer volume after driver, port tube, and bracing:
   target 50 L.
3. Stuffing volume increase: ~0.5 L (don't over-stuff a ported box).

Use the parametric-cad cookbook for the CAD workflow; this design's
parameters drive the model.

## Verification checklist

- [ ] Impedance: two LF peaks bracketing 28 Hz with saddle ~Re = 3.4 Ω;
      sealed mid peak at ~97 Hz; smooth dip between (no double-
      humping from internal-mode coupling).
- [ ] Frequency response (gated + nearfield merge):
  - Woofer: flat to 250 Hz, LR4 rolloff above.
  - Mid: flat 100 Hz to 5 kHz, LR4 rolloff above 2.5 kHz.
  - Tweeter: flat 1.5 kHz to 20 kHz.
- [ ] Polar at 0°, 15°, 30°, 45°: smooth transition through both
      crossovers; no lobing in the listening window.
- [ ] Distortion at 96 dB SPL / 1 m: < 1 % above 200 Hz; < 3 % at 50 Hz.
- [ ] Port air velocity at max SPL: < 17 m/s (run xmax_spl + flow check).
- [ ] Panel knock test: dead, no ringing.

## Common adjustments

- **Tweeter level**: 3 dB L-pad is a guess; measure and refine ±1 dB.
- **Mid level**: with LR4 crossovers and 90 dB sensitivity in both
  mid and tweeter, mid may sit ~1 dB low after baffle step; verify.
- **BSC depth**: tall floorstanders are less affected than bookshelves
  (the floor restores partial 2π loading at LF). 2-3 dB BSC is
  typical.
- **Crossover frequencies**: 250 Hz and 2.5 kHz are conservative.
  Lower mid-tweeter to 2 kHz if tweeter is robust (Fs ≤ 700 Hz,
  Xmax ≥ 0.5 mm); raise to 3 kHz if conservative.

## Cross-references

- `speaker-design/cookbooks/bookshelf-2way.md` — same crossover
  philosophy, smaller scale.
- `speaker-design/references/closed-box-geometry.md` — mid chamber
  geometry.
- `speaker-design/references/baffle-and-cabinet-acoustics.md` —
  baffle layout decisions.
- `parametric-cad/cookbooks/speaker-cabinet-2way.md` — CAD workflow
  extends naturally.
