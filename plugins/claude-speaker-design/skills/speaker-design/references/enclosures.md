# Enclosures

The enclosure is the second-order acoustic filter that, in series with
the driver's own second-order behavior, determines low-frequency
response. Pick the alignment first, then verify with simulation
(WinISD, VituixCAD, Hornresp), then prototype.

## Why you need a box at all

A bare driver is a **dipole** — front and rear radiation cancel below
the frequency where the path length equals λ/2. For a 6.5" driver in
free air, that cancellation starts around 500 Hz, costing 6 dB/oct
below it. An enclosure either absorbs the rear wave (sealed, aperiodic),
re-uses it in phase (ported, horn, bandpass), or delays it long enough
to fall out of band (transmission line).

## Sealed (closed box, acoustic suspension)

Driver in a sealed volume `V_b`. The trapped air acts as an added
stiffness in parallel with the suspension.

```
F_c   = Fs · √(1 + Vas/V_b)      in-box resonance
Q_tc  = Q_ts · √(1 + Vas/V_b)    in-box total Q
```

Alignments by `Q_tc`:

- `Q_tc = 0.5` — critically damped, no peak, slowest transient (Bessel-like).
- `Q_tc = 0.577` — Bessel, maximally flat group delay.
- `Q_tc = 0.707` — Butterworth (B2), maximally flat amplitude.
  `f_-3 ≈ F_c`.
- `Q_tc = 1.0` — Chebyshev, ~1 dB ripple, more extension at the cost of
  group delay; "boomy" if pushed further.

Pros: smallest box, best transient response, 12 dB/oct rolloff means
excursion stays bounded below cutoff. Cons: lowest efficiency near
cutoff (3 dB down vs. ported); needs more power and Xmax.

Sizing: pick target `Q_tc`, solve `V_b = Vas / ((Q_tc/Q_ts)² − 1)`.

## Ported / bass-reflex (vented)

A Helmholtz resonator (port + box volume) hangs off the rear of the
driver and radiates in phase with the front at its tuning frequency
`Fb`. The system is now 4th order.

```
Fb = (c / 2π) · √(S_p / (V_b · L_p,eff))
```

with effective port length `L_p,eff = L_p + 0.85·√(S_p/π)` for a flanged
port (end correction).

Alignments (after Thiele):

- **QB3** (Quasi-Butterworth, `Qts ≈ 0.3–0.4`): tight, fast, slightly
  damped. `Fb ≈ Fs`, `V_b ≈ 0.7 · Vas`.
- **SBB4 / B4** (Butterworth, `Qts ≈ 0.35–0.42`): textbook flat,
  `Fb ≈ Fs`, `V_b ≈ Vas`, `f_-3 ≈ 0.9 · Fb`.
- **C4** (Chebyshev, `Qts ≈ 0.4–0.5`): ripple for extra extension,
  `f_-3` below `Fb`.
- **EBS / Extended Bass Shelf** (`Qts ≈ 0.3–0.4`, oversized box):
  trades 2–3 dB sensitivity near `Fb` for an extra half-octave of
  in-room bass after room gain.

Pros: ~3 dB more SPL near tuning vs. sealed of same volume; less cone
excursion at and above `Fb` (the port unloads the cone). Cons: 24 dB/
oct rolloff below `Fb`; cone excursion goes **up** below `Fb` because
the cone is now unloaded — sub-tuning content can wreck the driver. Use
a high-pass at ~0.5·Fb in active systems.

Port design rules of thumb:

- Air velocity at Fb at max SPL must stay below ~17 m/s (5 % of c) or
  port noise / chuffing appears. Larger port area = lower velocity but
  longer length.
- Flared ends (radius ≥ 0.5·port diameter) push chuffing threshold
  ~3 dB higher.
- Port resonance (organ-pipe mode) sits at `c/(2·L_p)`. Keep it well
  above crossover to avoid passband artifacts; or stuff lightly with
  long-fiber damping near the velocity maximum.

## Passive radiator (drone cone)

Equivalent to a port, with a moving mass instead of an air mass.
Tuning:

```
Fb = (1 / 2π) · √(S_d² · ρ₀ c² / (V_b · M_pr))
```

Use when the port for desired Fb would be impractically long, or when
the cabinet is too narrow to admit a port without chuffing. Passive
radiators have their own Xmax — usually rated for 2–3× the active
driver's displacement.

## Bandpass (4th- and 6th-order)

Driver mounted between two chambers, one sealed and one ported (4th
order single-tuned), or both ported (6th order).

- 4th order: 12 dB/oct slopes on both sides, narrow bandwidth, +3 dB
  passband gain. Used in car subs where one octave is enough.
- 6th order: wider bandwidth, steeper slopes; tricky to tune.

Bandpass hides the driver mechanically (it radiates only through ports),
so excursion-limited SPL is lower than a comparable ported box at
mid-bass frequencies. Phase response is also notoriously difficult to
integrate with mains.

## Horn

A horn transforms the high acoustic impedance at the throat (small
area) to a low impedance at the mouth (large area), better matching the
driver to free air. Throat impedance for an exponential horn of flare
constant `m`:

```
Z_t(ω) = ρ₀ c / S_t · [√(1 − (ω_c/ω)²) + j (ω_c/ω)]   for ω > ω_c
```

with cutoff `ω_c = m·c/2`, below which the horn ceases to load the
driver. Horn design rules:

- Mouth area must be at least `λ_c² / 4π` (ideally `λ_c²`) to avoid
  reflection back into the horn at the cutoff frequency.
- Length sets the mid-band loading; longer = lower passband ripple but
  bigger box.
- Flare profile (conical, exponential, tractrix, Le Cléac'h, JMLC)
  trades pattern control vs. loading uniformity. Tractrix and Le
  Cléac'h are popular for constant-directivity mid/high horns.

Pros: 105–115 dB/W/m sensitivity, low distortion at high SPL, controlled
directivity. Cons: enormous for low cutoffs (a 50 Hz tractrix mouth is
~3 m across), passband honkiness from internal reflections.

## Transmission line (TL)

A long, internally damped acoustic line behind the driver, terminated
at the line's quarter-wave resonance `f_tl = c / (4·L)`. Heavy damping
turns the rear wave into heat below `f_tl` and lets the line act in
phase with the cone above it.

Pros: smooth rolloff, no port chuffing, excellent below-tuning excursion
behavior. Cons: large cabinet, very sensitive to stuffing density;
"properly tuned" TLs are mostly the result of measurement-driven
iteration, not formulas.

## Aperiodic / acoustic-resistance enclosures

A sealed box with a heavily damped vent (e.g. ScanSpeak Variovent,
Dynaudio Compound). Behaves between sealed and ported: slightly larger
effective volume than sealed, no Fb peak, gentle rolloff. Good for
small boxes with stiff drivers (`Q_tc` would otherwise be too high).

## Picking an alignment quickly

```
                       Q_ts
            < 0.3    0.3–0.4    0.4–0.5    > 0.5
horn          ✓
ported        ✓        ✓✓         ✓
sealed                              ✓        ✓✓
TL            ✓        ✓          ✓
aperiodic                           ✓        ✓
```

Then check excursion at target SPL, port velocity, and box volume vs.
what you can actually build.
