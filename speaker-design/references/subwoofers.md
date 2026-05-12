# Subwoofers

Low-frequency reproduction has its own physics: the wavelengths are
large compared to the room, so the room is part of the speaker.
Designing a sub without thinking about the room is like designing a
midrange driver without thinking about the cone — you can do it, but
the result will be poor.

## What's different below ~200 Hz

- **Wavelengths exceed room dimensions** → modal interference is the
  dominant SPL determinant at the listening seat. Speaker quality
  alone cannot fix a bad seat.
- **Localization is weak** → one mono sub is acoustically fine for
  music below ~80 Hz; stereo subs are about smoothing room response,
  not stereo imaging.
- **The ear is less sensitive** → +10 dB at 30 Hz to match the
  apparent loudness of midrange. So peak power demands and excursion
  needs are huge.
- **Group delay tolerance is loose** → 20 ms at 30 Hz (about 0.6
  cycles) is still inaudible. This is why ported and bandpass subs
  remain popular despite their phase character.
- **Room gain** ("cabin gain"): below the room's lowest mode, pressure
  rises ~12 dB/oct in a sealed room. Effective indoors below ~30 Hz in
  living spaces; below ~80 Hz in cars.

## Excursion-limited SPL

Below the enclosure's tuning, output is displacement-limited:

```
SPL(f) = 20·log₁₀(2π² ρ₀ f² S_d x_peak / (p_ref · √2 · r))
```

Per-driver target for "reference level home theater" (THX): 105 dB SPL
at the listening seat, 25 Hz, with 10 dB headroom → ~115 dB at the
seat. With ~10 dB room gain, the sub needs to put out ~105 dB anechoic
at 25 Hz at the seat distance. A single 12" with Xmax = 10 mm just
barely makes it; a 15" gets there comfortably.

The `tools/xmax_spl.py` script computes this directly.

## Sealed vs ported vs bandpass for subs

- **Sealed**: gentle 12 dB/oct rolloff naturally meets the +12 dB/oct
  room gain → flat to ~20 Hz in many rooms. Lowest group delay. Best
  transient response. Largest amplifier requirement: 6–10 dB more
  than ported for same SPL at port tune.
- **Ported (4th-order)**: highest output efficiency at and just above
  Fb. 24 dB/oct rolloff below Fb adds to room gain unpredictably.
  Cone unloads below Fb → must high-pass below tuning, ideally with
  a 24 dB/oct or steeper filter at ~0.5×Fb.
- **6th-order bandpass**: maximum SPL in a defined band; ugly time
  response. Common in car audio "SPL competitions"; rare elsewhere.
- **Tapped horn / 6th-order TH**: very high efficiency (105+ dB SPL/W)
  over an octave; large; popular in pro touring and cinema.
- **Passive radiator**: equivalent to ported but cabinet-only, with
  the PR's own Xmax limiting LF output instead of port chuffing.

Common DIY default: **sealed with Linkwitz transform** — get textbook
sealed transient + EQ the rolloff to whatever the room and amp can
support. See `cookbooks/sealed-subwoofer.md`.

## Multiple subwoofers

The case for ≥2 subs is **not** stereo or SPL — it's mode smoothing.
Different sub positions excite room modes differently; the seat
position sums multiple sources differently from each. With 2 subs at
modal nulls and antinodes, seat-to-seat variance drops dramatically.

Established configurations (Welti & Devantier, JAES 2003):

- **Two subs, mid-wall opposites** (one front-center, one rear-center
  or mid-side-walls) — symmetric, cancels odd-order length modes.
- **Four subs at room midpoints** of each wall — cancels all odd modes
  along both axes; gold standard for symmetric rooms.
- **Four subs at corners** — flips a few modes but excites others; not
  as clean as midpoints.

For asymmetric rooms or where placement is constrained, optimize with
measurement: place sub, measure 5–9 seat-region positions, average,
move sub, repeat. The MSO (Multi-Sub Optimizer) tool does this
automatically with PEQ and per-sub level/delay.

## Time alignment with mains

The sub should arrive at the listening seat with the same timing as
the mains in the crossover band.

```
delay = (d_sub − d_main) / c
```

A sub 1 m further than the mains needs ~3 ms delay applied to the
mains (not the sub — adding delay to the sub doesn't help because
it's already physically later). Most AVRs do this in their setup.

For active two-way + sub systems, set the crossover slope/order to
match between mains and sub (e.g. LR4 high-pass on the mains at 80 Hz
+ LR4 low-pass on the sub at 80 Hz). Polarity flip on one device may
be required if their internal latencies differ.

## Crossover to mains

- **80 Hz / LR4 (24 dB/oct)** is the THX home cinema standard for a
  reason: by 80 Hz the mains have negligible directional cues, by
  40 Hz the sub is doing all the work, and the 4th-order slopes keep
  excursion bounded on both sides.
- **Music systems** can go lower (50–60 Hz) if the mains are large,
  giving the sub less work and the mains more room dependence. Avoid
  going above 100 Hz unless the mains are very small; localization
  cues from the sub become audible above ~120 Hz.

## Group delay budgets

Audibility threshold for added group delay (worst case, electronic
music with tight kick drums): ~1.5 cycles. So:

```
τ_g,audible ≈ 1.5 / f
```

At 30 Hz: 50 ms. At 80 Hz: 19 ms. A ported sub at Fb = 30 Hz has
~30 ms group delay — close to but generally below threshold for music
content. A 6th-order bandpass with Fb = 35 Hz can hit 50 ms group
delay at 30 Hz: audible on percussive material.

Linkwitz transform on a sealed sub adds no group delay above its
unprocessed cutoff — pure pole-shift in the s-plane. This is the main
reason audiophiles prefer sealed + LT.

## Servo subs

A second sensor (accelerometer or velocity coil) measures cone motion
and feeds back into the amplifier in real time. Result: distortion
reduced by 10–20 dB, excursion linearized.

- Velodyne, Rythmik, Earthquake make commercial servo subs.
- DIY-able with a Kanji-Bose-style accelerometer on the dust cap and
  a power amp with a feedback summing junction.
- Best with sealed enclosures (port air motion confuses the sensor).

## Open-baffle (dipole) subs

Two or four large drivers on an open H- or U-frame baffle. Naturally
high-passed by the dipole rolloff (~ω) below the baffle's λ/4 cutoff;
needs steep EQ boost or natural room gain to flatten.

- **Pros**: no enclosure → no enclosure resonance, no port chuffing,
  no panel modes. Cancels the room's modal excitation along the dipole
  null axis → smoother in-room bass.
- **Cons**: very large; needs ~4× the displacement of a sealed sub for
  the same SPL at 30 Hz; ≥1 m of clearance from the rear wall.
- Linkwitz LXmini-sub and SLOB are canonical references.

## Things to verify in a sub design

- **Cone excursion** at target SPL, in band, with EQ applied — must
  stay below Xmax with 3 dB margin.
- **Port air velocity** below 17 m/s peak at max SPL at Fb.
- **Amplifier headroom** — peak power demand can be 4× continuous;
  Class D amps hit current limits before voltage limits.
- **High-pass below port tuning** (subsonic filter) on ported designs.
  24 dB/oct minimum at ~0.5 × Fb.
- **Cabinet bracing** — bass cabinets are most sensitive to panel
  flexure since the driver pushes them hard. Brace every 12" of
  unsupported panel span.
- **Seat measurement, not 1 m measurement** — a sub's job is in-room
  performance, not anechoic.
