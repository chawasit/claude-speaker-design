# Crossovers

A crossover splits the input signal into bands that each driver can
handle. The crossover lives in the **acoustic** domain — what matters
is the SPL each driver radiates after the filter, not the electrical
voltage at its terminals. Driver response and the filter combine to
form the acoustic target.

## Target acoustic slopes

Named by their summed response when both drivers play in phase and the
filter is symmetric around `fc`.

| Topology              | Order | Slope (dB/oct) | Sum response   | Phase shift | Notes                              |
|-----------------------|-------|----------------|----------------|-------------|------------------------------------|
| Butterworth 1st (B1)  | 1     | 6              | flat power     | 90°         | minimum phase, lobing upward       |
| Linkwitz–Riley 2 (LR2)| 2     | 12             | flat amp       | 180°        | invert one driver; tilted lobe     |
| Bessel 3 (BS3)        | 3     | 18             | flat-ish       | 270°        | rarely used                        |
| Linkwitz–Riley 4 (LR4)| 4     | 24             | flat amp       | 360°        | on-axis lobe, well-controlled      |
| LR8                   | 8     | 48             | flat amp       | 720°        | DSP/active only; minimal overlap   |

**LR4 is the default** for two-way passive home speakers because (a)
acoustic slopes are steep enough that drivers operate well inside their
piston ranges, (b) phase shift through crossover is a full cycle so
both drivers stay in phase across the overlap region (lobe on-axis),
(c) drivers see less out-of-band content.

For active/DSP designs, FIR linear-phase crossovers are an option —
zero phase distortion at the cost of latency and pre-ringing.

## Picking the crossover frequency

Constraints:

- **Tweeter:** `fc ≥ 1.5–2 × Fs_tweeter` for power handling. A tweeter
  with Fs = 700 Hz wants `fc ≥ 1.5 kHz` for LR4, higher for shallower
  slopes.
- **Woofer:** `fc ≤ f_breakup / 2` to keep modal peaks well outside the
  passband. Aluminum and metal cones break up violently; paper and
  pulp roll off gently.
- **Directivity match:** woofer beamwidth at `fc` should equal tweeter
  beamwidth at `fc`. For a 6.5" woofer, `ka = 1` is around 660 Hz; you
  generally cross to a 1" dome between 1.5–2.5 kHz to keep the polar
  pattern continuous.
- **Vertical lobing (LR4):** the listening axis sits between the
  drivers; off-axis vertical response has a null at one side and a
  lobe at the other. Keep driver center-to-center spacing ≤ λ at `fc`
  (ideally ≤ 0.75 λ) to push the null outside the listening window.

## Compensating real driver impedance

Textbook filter values assume a flat resistive load. Real drivers are
not. Two common corrections:

**Zobel network** (impedance equalization) flattens the rise of
`Z_e(f)` due to voice-coil inductance `L_e`:

```
R_z = 1.25 · R_e
C_z = L_e / R_e²
```

Place in parallel with the driver. After Zobel, the driver looks ≈
resistive (`R_e`) through the crossover passband, so textbook filter
values land in the right place.

**LCR notch** flattens the Fs peak of a woofer in a passive crossover,
or kills a specific cone breakup peak:

```
L_n = 1 / (4π²·f_peak²·C_n)
R_n = Q_peak · √(L_n/C_n)
```

Place in series with the driver for series notch, parallel for parallel
notch.

## Baffle step compensation (BSC)

The transition from `2π` (half-space) to `4π` (full-space) radiation as
λ shrinks past the baffle width gives a +6 dB shelf around

```
f_bs ≈ 115 / W_baffle (m)   Hz
```

A passive BSC network is a parallel L||R across the woofer that shelves
high frequencies down by ~3–6 dB. Active EQ does the same. Skip BSC if
the speaker is wall-mounted (half-space loading restored by the wall).

## Tweeter level matching (L-pad)

Tweeters are usually 3–6 dB more sensitive than the woofer. Attenuate
with an L-pad that preserves the load impedance:

```
R₁ = Z · (1 − 10^(−A/20))
R₂ = Z · 10^(−A/20) / (1 − 10^(−A/20))
```

where `A` is the desired attenuation in dB and `Z` is the nominal
tweeter impedance. `R₁` in series, `R₂` in parallel with the tweeter
**after** R₁. An L-pad ahead of a filter changes the filter loading —
put it between filter and driver, or recompute.

## Polarity and lobing

For LR2 (180° offset at fc), wire one driver inverted so they sum in
phase. LR4 (360°) needs both in phase. If you can measure, sweep
polarity at the crossover frequency and pick the wiring that maximizes
on-axis SPL through the overlap band.

## Workflow

1. Measure each driver in the actual baffle, at the actual listening
   distance and angle.
2. Apply Zobel/LCR to make the load look reasonable. Re-measure.
3. Design filters in software (XSim, VituixCAD) against the acoustic
   target (e.g. LR4 acoustic, not LR4 electrical). The electrical
   filter shape will not look like a textbook LR4.
4. Listen. Then measure again at off-axis angles. Adjust slopes/levels
   to maintain power response and DI through crossover.
5. Final pass: distortion sweeps at target SPL, harmonic + IMD, with
   the crossover loaded.
