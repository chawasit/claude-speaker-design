# Cookbook: 6.5" + 1" Two-Way Bookshelf, Ported, LR4

A worked end-to-end design showing how the skill's references and tools
compose. Targets a typical hi-fi bookshelf: small enough for a desktop,
loud enough for a living room at moderate distances.

## Targets

| Spec                         | Target                                   |
|------------------------------|-------------------------------------------|
| Bandwidth                    | 45 Hz (-3 dB) to 20 kHz                  |
| Max SPL (1 m, 1 % THD)       | 100 dB                                    |
| Sensitivity                  | ≥ 84 dB SPL / 2.83 V / 1 m               |
| Nominal impedance            | 6 Ω, min ≥ 3.5 Ω                          |
| Volume (external)            | ≤ 18 L                                    |
| Placement                    | Free-standing, ≥ 50 cm from rear wall     |

## Driver choice

For 100 dB at 1 m with the woofer carrying down to 50 Hz, we need
either a high-excursion 6.5" or a 7"–8" driver. We pick a 6.5" with
`Xmax ≥ 5 mm` to keep the cabinet small.

**Woofer (illustrative T/S, datasheet-style):**

- Fs = 36 Hz, Qts = 0.36, Vas = 17 L
- Re = 5.4 Ω, Le = 0.55 mH
- Sd = 132 cm², Xmax = 5 mm
- BL = 6.2 T·m, SPL (2.83 V/1 m, anechoic 2π) = 87 dB
- F_breakup ≈ 4.8 kHz

**Tweeter:**

- 1" soft-dome, Fs = 750 Hz, Re = 4.6 Ω, Le = 0.04 mH
- Sensitivity ≈ 90 dB / 2.83 V / 1 m
- Recommended fc ≥ 1.8 kHz at LR4

Tweeter is 3 dB hotter than the woofer; we'll attenuate with an L-pad.

## Enclosure alignment

`Qts = 0.36` is right in the middle of B4 (SBB4) territory. Run the
ported-box tool:

```
$ python tools/ported_box.py --fs 36 --qts 0.36 --vas 17
alignment     = B4
Vb            = 12.3 L  (alpha = Vas/Vb = 1.38)
Fb            = 36 Hz   (h = Fb/Fs = 1.00)
f-3dB         = 32 Hz
```

12.3 L net volume. With 18 mm MDF and accounting for driver/port
displacement (~0.7 L) and minimal stuffing (~5 % effective volume
increase), aim for **13 L gross internal**. External dimensions
roughly 200 × 350 × 280 mm (W × H × D).

### Port

Cone Sd = 132 cm². Peak excursion at Fb for 100 dB at 1 m is ~3 mm.
Pick a 60 mm diameter port (Sp = 28.3 cm²); compute length:

```
$ python tools/port_length.py --fb 36 --vb 12.3 --dia 60 \
                              --sd 132 --xpeak 3
Port area     = 28.3 cm^2  (dia 60 mm)
End correction= 25.5 mm
Effective Lp  = 188.9 mm
Physical Lp   = 163.4 mm  <-- cut this length
Port velocity = 8.4 m/s peak  (OK)
```

163 mm port — fits diagonally in the 280 mm cabinet depth, or fits
straight if mounted to the rear panel. Velocity 8.4 m/s is well under
the 17 m/s chuffing threshold.

### Sanity checks

- **Cone excursion at Fb at target SPL**: `tools/xmax_spl.py --sd 132
  --xmax 5 --target-spl 100 --f-min 35 --f-max 80 --steps 6`. Should
  show ≥ 100 dB above ~50 Hz; expect ~96 dB at 35 Hz (port unloading
  helps above tune; below it falls off rapidly).
- **Internal modes**: 350 mm internal height → fundamental mode at
  ~490 Hz, well in the woofer's band. Stuff the rear and top walls
  with long-fiber wool, ~0.5 kg/m³ density.
- **Panel modes**: 350 × 280 mm side panels in 18 mm MDF → first mode
  ~210 Hz. Add one transverse brace at panel midpoint to push it to
  ~840 Hz, out of the worst audibility band.

## Baffle and diffraction

Baffle width 200 mm → baffle step centered at ~575 Hz. For a free-
standing speaker we plan ~3 dB BSC.

Driver placement: tweeter at (W/2 + 15 mm, 60 mm from top), woofer
below it offset 10 mm to the same side. The asymmetry spreads
diffraction comb-nulls across frequency. 25 mm roundovers on the
vertical edges + 15 mm chamfers on the top/bottom edges.

## Crossover (acoustic-target LR4 at 2 kHz)

Tweeter Fs = 750 Hz; we cross at 2 kHz (2.7 × Fs) at LR4 → safe.
Woofer breakup is at 4.8 kHz; LR4 puts the woofer 24 dB down by
4 kHz, so the breakup peak should sit ≥ 18 dB below in-band. May
still need a notch (verify with measurement).

Start with textbook LR4 values:

```
$ python tools/crossover_lr.py --fc 2000 --z 8 --order LR4 \
                               --re 5.4 --le 0.55
LR4 crossover at 2000 Hz into 8.0 ohm (resistive-load idealization)

Low-pass section (to woofer):
  L1_H = 0.900 mH    C1_F = 7.03 uF
  L2_H = 0.450 mH    C2_F = 14.07 uF

High-pass section (to tweeter):
  C1_F = 7.03 uF     L1_H = 0.450 mH
  C2_F = 14.07 uF    L2_H = 0.900 mH

Zobel network (parallel with woofer, before low-pass):
  Rz = 6.75 ohm  (1.25 * Re)
  Cz = 18.86 uF  (Le / Re^2)
```

**Tweeter L-pad** for 3 dB attenuation into 4 Ω nominal:

```
R₁ = 4 · (1 − 10^(−0.15)) = 1.17 Ω  ≈ 1.2 Ω
R₂ = 4 · 10^(−0.15) / (1 − 10^(−0.15)) = 9.43 Ω ≈ 10 Ω
```

These are starting values. Measure the in-baffle acoustic response of
each driver, then iterate filter component values in VituixCAD until
each driver's acoustic rolloff matches the LR4 target through and
beyond `fc`.

## Predicted impedance

The system will show:

- Two LF peaks bracketing Fb = 36 Hz, saddle minimum ≈ Re = 5.4 Ω at
  36 Hz. Peaks ~25 Ω at ~25 Hz and ~45 Hz.
- Smooth dip to Z_min ≈ 4.0 Ω between 200 Hz and 1 kHz (worst at the
  crossover region).
- Tweeter HF impedance ~4–6 Ω depending on L-pad and filter Q.
- Z_min target ≥ 3.5 Ω: meet by checking the simulation in
  VituixCAD's load plot. If lower, raise L-pad attenuation or rework
  the LR4 component values.

## Verification checklist

Before declaring done:

- [ ] Impedance sweep: two peaks bracketing 36 Hz, clean saddle at 36
      Hz dropping near Re. Off-tune saddle → trim or extend port.
- [ ] Free-air check (driver before installing): Fs and Qts match
      datasheet within 10 %.
- [ ] Gated quasi-anechoic FR (1 m, gate 4 ms → valid above 250 Hz):
      ±2 dB through midrange, smooth crossover transition.
- [ ] Nearfield woofer + port summed with diffraction correction:
      flat to ~32 Hz then 24 dB/oct rolloff.
- [ ] Distortion sweep at 96 dB SPL / 1 m: < 1 % above 100 Hz, < 3 %
      at 50 Hz.
- [ ] Polar measurements at 0°, 15°, 30°, 45° horizontal: smooth
      transition through crossover, no lobe nulls in listening
      window.
- [ ] Panel knock test: dull thunk, no ringing.

## What's likely to need adjustment

- Tweeter level: L-pad is a guess until you measure. Expect ±1.5 dB
  adjustment.
- Crossover frequency: 2 kHz may need to move ±200 Hz to clean up the
  acoustic blend. Re-derive filter values when you do.
- BSC depth: 3 dB is a guess. After listening at the actual placement,
  many builders end up wanting 1–2 dB less for a "lively" balance or
  1–2 dB more for a "polite" one.
- Port length: tuning often comes out 1–3 Hz different than predicted
  because the box stuffing changes effective volume. Re-trim the port
  after the impedance sweep.
