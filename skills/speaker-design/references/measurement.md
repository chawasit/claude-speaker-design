# Measurement

Without measurement, speaker design is theology. Every claim in this
skill ("LR4 sums flat", "Zobel flattens impedance") is only true to the
extent you can verify it at the listening position. The good news:
modern measurement is cheap (~$150 mic + free software) and accurate
to within ±1 dB anywhere it matters.

## The measurement chain

```
DUT ── air ── microphone ── preamp/ADC ── DAW/measurement software
                                   ↑
                                   reference signal
```

Each link has a calibration step. Skip one and you'll chase artifacts
for weeks.

## Hardware

| Microphone               | Use                          | Notes                          |
|--------------------------|------------------------------|--------------------------------|
| miniDSP UMIK-1           | room/in-situ, USB            | individual cal file; ~$80      |
| miniDSP UMIK-2           | room + higher SPL            | 24-bit, IEPE optional          |
| Dayton EMM-6             | DIY, XLR + interface         | needs phantom + cal file       |
| Behringer ECM-8000       | budget, XLR                  | mediocre cal, decent for relative measurements |
| Earthworks M30 / M50     | reference                    | factory-flat; ~$700+           |
| GRAS 46AE                | metrology                    | IEC 61094 standard mic         |
| Klippel KA3 / Klippel R&D| nonlinear analysis           | turnkey large-signal           |

Always use the **individual calibration file** for your specific mic
serial — generic cal is wrong above ~8 kHz.

For impedance, a USB DAC with both inputs in use (one for voltage
across the DUT, one for current via a sense resistor) works well; or a
dedicated jig like the Dayton DATS V3 / WT3.

## Software

- **REW (Room EQ Wizard)** — free, the de-facto standard. Sweeps,
  RTA, T/S extraction, impedance, filter design, EQ export.
- **HolmImpulse / ARTA / CLIO** — older but capable.
- **VituixCAD** — measurement merging + crossover design + simulation
  (the best free tool for two-way+ design as of 2026).
- **Klippel Distortion Analyzer (KDA)** — large-signal nonlinear
  parameters; not free.

REW with VituixCAD covers ~95 % of DIY needs.

## Quasi-anechoic measurement

A free-field measurement in a normal room, accomplished by **windowing**
the impulse response to keep only the direct sound. The first floor
or wall reflection sets the window length:

```
t_window ≤ (d_reflection − d_direct) / c
f_min   ≈ 1 / t_window
```

Typical living room: mic 1 m from speaker tweeter, both 1 m above
floor, far from walls → ~5 ms gate → valid above ~200 Hz. To get
deeper, raise mic+speaker higher or move outdoors.

Smoothing: 1/12-octave for engineering; 1/3-octave for "what it sounds
like" reports. Below the gate cutoff, the data is the room, not the
speaker — splice in nearfield (see below).

## Nearfield merge

For the bass region, place the mic ~5 mm from the dust cap of the
woofer. The mic now sees the direct cone radiation with ≥40 dB SNR vs.
the room. Valid up to:

```
f_max,nf ≈ 0.11 · c / a   (cone radius a)
```

For a 6.5" driver, ~860 Hz. Above that, the wavefront across the cone
develops phase variation and the on-axis nearfield response diverges
from the far-field anechoic response.

Combining nearfield + far field:

1. Apply **diffraction loss** correction to nearfield (use VituixCAD's
   baffle simulator or Edge software) — this converts the half-space
   nearfield level to the full-space level the far-field measurement
   sees.
2. For a ported box, sum the nearfield woofer and nearfield port
   responses, scaled by `√(S_port/S_d)`.
3. Splice the corrected nearfield to the gated far-field at a frequency
   well below the gate cutoff (e.g. 250 Hz if your gate is 200 Hz).

## Polar response

Measure on a turntable (or pivot the speaker manually) every 10° from
0° to 90° horizontal and vertical. Plot as:

- **Polar map** (frequency on one axis, angle on the other, dB by color).
- **Beamwidth plot** (-6 dB angle vs. frequency).
- **Directivity Index** (10·log₁₀ of on-axis vs. spherically averaged
  power).

For a stereo pair in a room, the angles that matter most are 0° (direct),
±10° (toe-in adjustment), ±30° (first sidewall bounce), and 90° (sets
sidewall reflection timbre).

## Impedance measurement

Two-channel method:

```
DAC out ── R_sense (10 Ω, 1 % wirewound) ── DUT ── GND
                  ↑                    ↑
                  ch A (reference)      ch B
```

Sweep at low level (≤ 50 mV across DUT) so the driver stays in
small-signal regime. Compute:

```
Z(f) = R_sense · V_B(f) / (V_A(f) − V_B(f))
```

Impedance is the most diagnostic single measurement of a loudspeaker:
the curve's shape encodes the driver's resonance, the enclosure's
loading, internal damping, port tuning, and any air leaks. Always
sweep impedance first, before chasing frequency-response anomalies.

## Free-air ("open-field") vs in-cabinet measurement

The same driver produces three very different impedance and frequency
responses depending on how it is mounted. Knowing which is which is
the foundation of T/S extraction and enclosure verification.

### Free-air (open field, unbaffled)

Driver suspended in space (clamped at the frame, held in a stand, or
on a small "IEC half-baffle" that does not significantly load the
cone). No enclosure on either side. This is what datasheet T/S numbers
refer to.

**Impedance signature**: a single Lorentzian peak at the driver's
free-air resonance `Fs`, with height `Z_max` and -3 dB half-power
points `f1`, `f2`:

```
Qms = Fs · √(Z_max / R_e) / (f2 − f1)
Qes = Qms · R_e / (Z_max − R_e)
Qts = Qms · Qes / (Qms + Qes)
```

Above the peak, impedance falls back near `R_e` then rises slowly with
voice-coil inductance `L_e`.

**Frequency response**: dominated by dipole cancellation. Below the
frequency where front-to-rear path length equals λ/2 (~λ ≈ 4× driver
diameter), output falls 6 dB/oct because the rear wave wraps around
and partially cancels the front. Useless for piston-band measurement.

**Why use it**: this is the **only** configuration where the standard
T/S model applies cleanly — no air load from a cabinet, no Helmholtz
resonator, just the driver's own moving system. T/S extraction (added
mass or added volume) starts from a free-air impedance sweep.

**Practical setup**:

- Clamp the driver vertically by its frame in a stable stand.
- Keep ≥ 1 m from large reflective surfaces.
- Drive at ≤ 50–100 mV peak. Higher levels exceed small-signal regime
  and `Qms` will rise spuriously (suspension softens under exercise).
- Let the driver "exercise" for ~30 s at moderate level before
  measuring — Fs and Qms drift ~1–3 % between cold and warm
  suspensions.
- Free-air on the floor or on a soft surface couples the moving mass
  to the surface and shifts results; suspend it.

### Sealed in-cabinet

Driver mounted in its final sealed enclosure of volume `V_b`.

**Impedance signature**: still a **single** peak, but moved up from
`Fs` to the in-box resonance:

```
F_c  = Fs · √(1 + Vas/V_b)
Q_tc = Qts · √(1 + Vas/V_b)
```

The peak gets both higher in frequency and taller (because Q rises
with stiffness when damping is unchanged).

What the curve diagnoses:

- **F_c far below predicted** → box leaks. A sealed box that "fakes"
  a larger volume has lower stiffness than its geometry suggests.
  Check gasket, terminal cup seal, joinery.
- **F_c at predicted, peak much lower than expected** → too much
  damping material. The mechanical Q is being killed by stuffing;
  efficiency near Fc drops with it.
- **Two small peaks where one is expected** → significant internal
  panel resonance coupling to the cone. Add bracing or CLD.
- **Wide, broad peak instead of sharp** → driver is bottoming or the
  spider is damaged; or the test signal is too loud.

The added-volume T/S method exploits this shift directly:

```
Vas = V_b · ((F_c / Fs)² − 1)
```

The same equation says: if you measure `Fs` and `F_c` of a finished
sealed speaker and know `V_b`, you can back-compute `Vas` to verify
the driver matches its datasheet.

### Ported (vented) in-cabinet

Driver mounted in a vented enclosure tuned to `Fb`.

**Impedance signature**: a **two-peak "double hump"** with a saddle
in between. The saddle's minimum sits exactly at `Fb` — this is the
single most useful number on the curve.

```
        |\               /\
        | \    saddle   /  \
        |  \   at Fb   /    \
   |Z|  |   \  ___    /      \____
        |    \/   \__/             \___
        +-------------------------------- f
              FL    Fb    FH

   FL = lower peak (cone + port air resonance, low side)
   FH = upper peak (cone resonating with port acting closed)
   Fb = saddle minimum (port radiating; cone motion is minimized)
```

Relative peak heights:

- **Equal-height peaks**: typical of a properly damped B4/SBB4
  alignment.
- **Lower peak taller than upper**: box is over-damped or alignment
  is QB3-like.
- **Upper peak taller**: under-damped, or driver Qts is too high for
  this alignment.

What the curve diagnoses:

- **Saddle minimum off-target Fb** → port length wrong. Saddle higher
  than designed → port too short. Lower → port too long. Tune by
  trimming/extending the port and re-measuring.
- **Saddle "filled in" (shallow, no clean dip)** → port leak (poor
  seal at the port flange), excessive damping in the port path, or
  significant cabinet leakage. A clean saddle should drop almost to
  `R_e`.
- **Asymmetric peaks well outside textbook ratio** → wrong driver Qts
  for the alignment, or significant Vas mismatch with the box volume.
  Re-measure the driver's free-air T/S and reconsider the alignment.
- **Ragged ripples between or above the peaks** → internal box modes
  exciting the cone. Add stuffing to the rear wall opposite the
  driver, or improve bracing.
- **A third small peak well above FH** → port resonance (organ-pipe
  mode at `c / 2 L_p_eff`). Move it out of band by changing port
  geometry, or lightly stuff the port at the velocity-maximum mid-
  point.

This is why impedance is run first on any prototype: a 60-second sweep
tells you whether the box is sealed, whether the port tunes where you
intended, whether internal damping is right, and whether the driver
matches its datasheet — all before you ever measure SPL.

### Passive-radiator in-cabinet

Looks like a ported box impedance, but `Fb` is set by the passive
radiator's compliance + added mass instead of port air. The two-peak
shape is the same; the saddle still marks `Fb`. Additionally:

- The PR has its own Fs (with no air load); below the system's lower
  impedance peak you may see a tiny extra wiggle at the PR's free
  resonance.
- If the PR is over-driven, the saddle widens and shifts upward as
  the PR's suspension stiffens at large excursion — a sign you are
  past PR Xmax.

### Open-baffle / dipole in operation

Driver on an open baffle, both sides radiating. Impedance is close to
free-air (no enclosure stiffness), with small ripples from the baffle's
diffraction pattern coupling back to the cone — usually within ±0.5 Ω
of the free-air curve.

### Quick reference: impedance peak count

| Mounting / alignment            | Peaks | Where does Fb / Fc sit?           |
|---------------------------------|-------|-----------------------------------|
| Free-air                        | 1     | Peak = Fs                         |
| Sealed                          | 1     | Peak = Fc > Fs                    |
| Ported / passive-radiator       | 2     | Saddle min = Fb                   |
| Bandpass (4th-order)            | 2     | Both peaks set by chambers + port |
| Open baffle                     | 1     | Peak ≈ Fs (slightly lower)        |
| Horn (loaded driver)            | 1 (low Q) | Peak heavily damped by horn load |

When the count doesn't match what you expect, something physical is
wrong with the build — not your math.

### Frequency response: free-field vs in-room vs in-cabinet

A parallel story for SPL measurement:

| Where                | Captures              | Valid frequency range          |
|----------------------|-----------------------|--------------------------------|
| Anechoic / outdoor   | speaker only          | full bandwidth                 |
| Quasi-anechoic (gated) | speaker only        | above ~1/gate_ms × 1000 Hz     |
| Nearfield (mic at cone) | direct radiation   | up to ~0.11 c / cone radius    |
| In-room (1 m)        | speaker + early refl. | above Schroeder freq (informative only) |
| Listening position   | speaker + room        | what the listener hears        |

Real workflow combines them: gated quasi-anechoic above ~200 Hz,
nearfield with diffraction-loss correction below, listening-position
sweep for in-room verification (not anechoic claims).

## T/S parameter extraction

Two flavors:

- **Added mass:** put 5–10 g of modeling clay on the dust cap. Measure
  Fs again. Solve `M_ms = Δm / ((Fs/Fs')² − 1)`. Then `C_ms = 1/((2π
  Fs)² M_ms)`, `Vas = ρ₀ c² S_d² C_ms`, etc.
- **Added volume:** seal the driver into a test box of known volume
  `V_b`. New resonance `Fs_b` gives `Vas = V_b · ((Fs_b/Fs)² − 1)`.
  Volume must be measured accurately (not "approximately Vas/4").

Use whichever is more practical. Mass method requires no test box;
volume method is less sensitive to mass measurement error on small
drivers.

## Klippel large-signal parameters

For drivers pushed past 30 % of Xmax, T/S no longer predicts behavior.
Klippel extracts:

- `BL(x)` — motor strength vs. displacement; should be symmetric and
  flat ±10 % through Xmax. Asymmetry → even-order distortion (2nd
  harmonic). Curvature → odd-order.
- `K_ms(x)` or `C_ms(x)` — suspension stiffness/compliance vs.
  displacement; always stiffens past Xmax, ideally symmetrically.
- `L_e(x, i)` — inductance vs. displacement and current; flux
  modulation source. A copper cap on the pole flattens this.

Report `Xmax` per the AES2-2012 / Klippel "10 % distortion" criterion
or "20 % BL drop" criterion, not the manufacturer's marketing number.

## Distortion measurement

Two test signals, two regimes:

- **Single-tone sweep at constant SPL**, harmonics 2nd, 3rd, 5th
  extracted. Tells you what cone/motor nonlinearity dominates.
- **Multitone or two-tone (SMPTE 60 + 7 kHz at 4:1)** for intermodulation.
  Audibly more relevant than THD for music content.

Spec your distortion at the **target listening SPL** (e.g. 96 dB SPL
at 1 m), not at 1 W or 90 dB — distortion rises faster than fundamental
as drive increases, so the curve at 90 dB is misleading.

## Standard test signals

| Signal             | What it's for                                  |
|--------------------|------------------------------------------------|
| Log-sweep (chirp)  | FR + impulse + harmonic distortion in one shot |
| Pink noise         | RTA, sound-pressure calibration                |
| MLS                | impulse response in noisy environments         |
| Two-tone           | IMD (SMPTE, CCIF, ITU-R)                       |
| Multitone (MOL)    | full-spectrum distortion under realistic load  |
| EIA-426B noise     | program-material-like spectrum for max SPL     |

Use log-sweep by default; modern PCs handle it and you get the impulse
response (so you can window/gate later) for free.

## Common gotchas

- **Mic position**: 1 mm shift = phase rotation at HF. Use a tripod and
  laser distance gauge if comparing tweets and woofs.
- **Speaker orientation**: tweeter axis = reference. Document the
  vertical position too.
- **SPL calibration**: REW's SPL meter is only accurate if you cross-
  check against a calibrated SPL meter at some level — there's an
  arbitrary digital level offset otherwise.
- **Ground loops**: a 60 Hz hum at -60 dB can hide LF distortion. Use
  a balanced interface or ground-lift on one device.
- **Speaker break-in**: real, but small (~1–2 % shift in Fs and Qms
  over 24 hours, plateauing within a week). Re-measure once after
  break-in if you care about ±0.5 dB precision.
- **Cold drivers**: voice-coil DC resistance varies with temperature;
  match Re measurements to ambient.
- **Stuffing settling**: TS-by-test-box methods drift if you keep
  re-stuffing the box. Stuff once, glue in place, re-measure.
