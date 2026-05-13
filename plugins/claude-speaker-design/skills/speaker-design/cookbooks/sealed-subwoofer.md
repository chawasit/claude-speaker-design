# Cookbook: 12" Sealed Subwoofer with Linkwitz Transform

A worked DSP-active sealed subwoofer. Sealed for transient response
and small box; Linkwitz transform to recover extension; PEQ for the
worst room mode at the listening seat.

## Targets

| Spec                              | Target                                    |
|-----------------------------------|--------------------------------------------|
| Bandwidth                         | 18 Hz to 80 Hz (-3 dB)                    |
| Max SPL at listening seat, 25 Hz  | 102 dB peak (with single driver); 108 dB with dual force-cancelling 12" |
| Group delay                       | < 30 ms below 60 Hz                       |
| Volume (external)                 | ≤ 55 L                                    |
| Crossover to mains                | 80 Hz, LR4                                 |

## Driver choice

For 102 dB peak at 25 Hz at the listening seat (≈ 4 m), with ~6 dB of
room gain in a typical 50 m³ living room, we need ~96 dB at 1 m
anechoic at 25 Hz.

```
$ python tools/xmax_spl.py --sd 510 --xmax 13 --f-min 20 --f-max 60 \
                           --steps 4 --target-spl 96
  f (Hz)   SPL_peak (dB)
   20.0      97.0      <-- target reached above 20 Hz
   26.3     101.8
   34.6     106.6
   45.6     111.3
   60.0     116.1
```

A single 12" driver with Sd ≈ 510 cm² and Xmax ≈ 13 mm reaches ~97 dB
at 20 Hz / ~102 dB at 26 Hz anechoic, matching industry benchmarks
for sealed home-theater subs (SVS SB-2000, Rythmik F12). For higher
SPL targets (110 dB+ peaks for HT reference), use a pair of opposed
12" drivers in one cabinet (+6 dB) or step up to a 15" with higher
Xmax.

Illustrative T/S parameters for a typical home-theater 12":

- Fs = 22 Hz, Qts = 0.45, Vas = 95 L
- Re = 3.4 Ω, Le = 1.2 mH
- BL = 18 T·m, Mms = 165 g
- Sd = 510 cm², Xmax = 13 mm
- Power: 500 W continuous, 1000 W peak

## Enclosure

Sealed box. Pick `Qtc = 0.7` for Butterworth alignment (good transient,
mild peak avoided):

```
$ python tools/sealed_box.py --fs 22 --qts 0.45 --vas 95 --qtc 0.707
Vb            = 64.9 L
alpha (Vas/Vb)= 1.46
Fc            = 34.6 Hz
Qtc           = 0.707  (Butterworth B2)
f-3dB         = 34.6 Hz
```

Vb = 65 L is too big for our 55 L external target. Increase Qtc
slightly:

```
$ python tools/sealed_box.py --fs 22 --qts 0.45 --vas 95 --qtc 0.80
Vb            = 46.0 L
alpha (Vas/Vb)= 2.07
Fc            = 38.6 Hz
Qtc           = 0.800  (non-standard)
f-3dB         = 36.7 Hz
```

Qtc = 0.80 gets us into a 46 L net box. With 25 mm MDF (heavy
construction is warranted at LF) plus driver displacement (~2 L) and
bracing (~1 L), external volume ~ 55 L. Mark up Fc, Qtc, and natural
f-3dB:

- Natural Fc = 38.6 Hz
- Natural Qtc = 0.80 (slight peak ~+0.7 dB)
- Natural -3 dB = 36.7 Hz

## Linkwitz transform

Target shape: Butterworth Q = 0.5, F = 18 Hz. The LT biquad shifts
the natural (Fc=38.6, Qtc=0.80) to the target (Fp=18, Qp=0.5).

Required boost at the limit (`f → 0`):

```
boost_dB = 40 · log₁₀(Fc / Fp) = 40 · log₁₀(38.6 / 18) = 13.2 dB
```

13 dB EQ boost at 18 Hz. At target SPL, this means the amplifier
must deliver 20× the unprocessed voltage at 18 Hz. Verify driver
displacement under LT:

```
displacement scaling factor = (Fc/Fp)² · (Qp/Qtc) at the LT corner
                            = (38.6/18)² · (0.5/0.8)
                            ≈ 2.87  (close to 3× more excursion)
```

A single 12" with Xmax = 13 mm reaches ~97 dB anechoic at 20 Hz; with
the LT extending to 18 Hz at Qp = 0.5, the excursion at 18 Hz scales
up by ~2.9× over the unprocessed driver, capping practical clean SPL
at ~94 dB anechoic at 18 Hz (limited by Xmax). Add ~10 dB room gain
at the seat and you have ~104 dB peak at 18 Hz in-room — close to the
limit for a single sealed 12". Set the excursion limiter at 12 mm
(10 % Xmax margin). For higher reference levels, dual opposed 12"
drivers add +6 dB at the same excursion.

## Amplifier and DSP

| Function                    | Setting                                |
|-----------------------------|----------------------------------------|
| Subsonic high-pass          | 12 Hz, BW 24 dB/oct (LT cannot reach DC) |
| Linkwitz transform biquad   | Source (Fc=38.6, Q=0.80), Target (Fp=18, Q=0.5) |
| Room-mode PEQ #1            | Set after measurement (see below)      |
| Low-pass to mains           | 80 Hz, LR4                              |
| Excursion limiter           | Predict displacement from filter chain; limit at 12 mm |
| Thermal limiter             | Reduce gain when modeled coil temp ≥ 200 °C |
| Amplifier                   | ≥ 600 W RMS into 4 Ω; Class D plate amp typical |

A 600 W amp + 13 dB of LT boost dictates: peak voltage at 18 Hz =
√(600·4) · 10^(13/20) = 49 V · 4.5 = ~220 V peak. **This exceeds most
plate amps' rails.** Solutions: reduce LT extension to 22 Hz (saves
~5 dB headroom), use a higher-power amp, or accept lower max SPL at
the very bottom octave.

For this design we'll back off LT to Fp = 22 Hz, Qp = 0.5 — a still
useful half-octave of extension below natural Fc, with only ~7 dB of
boost and reasonable excursion at max output.

## Room mode correction

Measure at the listening seat. The first axial mode in a typical
5 × 4 × 2.4 m room sits at:

```
f = (c/2) / L_long = 343 / (2·5) = 34 Hz
```

Often shows up as a +8 to +12 dB peak at the seat. Add a parametric:

- f = 34 Hz, Q = 5, gain = -10 dB

Re-measure. If a second axial mode (length, n=2) at 68 Hz is still
boosted, add another PEQ. Be conservative with PEQ cuts (small Q)
and ruthless with cuts you can verify by measurement; do not cut
peaks you have not measured.

**Do not** PEQ a null (cancellation dip). Boosting cancellation can
only make it deeper somewhere else; the proper fix is to move the sub
or add a second sub.

## Multi-sub consideration

If the room is asymmetric or seat-to-seat consistency matters, two
subs placed at the side-wall midpoints (Welti's "mid-wall" position)
cancel the lowest length mode and reduce seat-to-seat variance by
~6 dB. For this single-sub cookbook we'll skip; if you have the
opportunity, add a second sub and re-EQ together.

## Verification checklist

- [ ] Impedance: single peak at Fc ≈ 38–39 Hz, height ≥ 40 Ω
      (low Qms drivers will be less). No second peak (sealed).
- [ ] Nearfield SPL with LT engaged: flat to ~22 Hz, 12 dB/oct
      rolloff below.
- [ ] In-room SPL at seat: after PEQ, ±4 dB from 25 to 80 Hz at the
      listening position.
- [ ] Distortion at 100 dB SPL / seat: < 10 % below 30 Hz, < 3 %
      above. If higher, you are running out of Xmax — verify
      excursion limiter is engaging.
- [ ] Group delay: < 30 ms at 25 Hz (sealed + LT typically gives
      18–25 ms; mostly the LT delay, not the box).
- [ ] Crossover to mains: sweep both, summed response within ±2 dB
      of mains' on-axis response above 80 Hz; delay-aligned so
      polarity flip degrades response (proof of alignment).

## What's likely to need adjustment

- **Sub position**: a 1 m move can shift the room mode by 3–5 dB. Run
  REW's "Best Subwoofer Position" tool if you can experiment.
- **LT corner frequency**: trade extension vs. excursion vs. amp
  headroom. Common pattern: design for 18 Hz, listen, decide if 22 Hz
  is enough.
- **PEQ count**: 1–3 PEQs should handle the worst modes. Beyond that,
  the room (not the sub) is the limit; consider treatment or more
  subs.
- **Crossover slope to mains**: LR4 (24 dB/oct) is standard. If the
  mains have weak excursion, raise their HP to LR4 at 100 Hz; some
  bass response loss but huge gain in main-driver headroom.
