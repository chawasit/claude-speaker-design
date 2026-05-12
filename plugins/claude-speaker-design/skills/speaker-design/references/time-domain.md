# Time-Domain Analysis

The frequency-response view of a speaker — the magnitude plot
everyone shows — captures one half of the picture. The other half is
the **time domain**: how the speaker responds to a transient. Two
speakers with identical FR can sound very different if their time-
domain behavior differs.

This file covers impulse response, step response, group delay,
energy decay, and the audibility thresholds for time-domain errors.

## 1. The impulse response

The output `h(t)` of a system to an ideal Dirac impulse `δ(t)`.
Once you have `h(t)`, you have everything: the frequency response
is its FFT, the step response is its integral, the magnitude+phase
plot is its complex FFT.

Real measurements: use a **log-sweep** test signal, deconvolve to
obtain `h(t)`. REW, ARTA, and CLIO all do this automatically.

### What it looks like

A well-behaved direct-radiator speaker:

```
amplitude
   |
   |     ____
   |    /    \                _____
   | __/      \___       ____/      \___________ ringing tail (cone modes, room)
   |/             \___/
   +----+----+----+----+----+----+----+----+----  t (ms)
   0    0.5  1    1.5  2    2.5  3    3.5  4

   - 0-0.5 ms: pre-response (should be near-zero for minimum-phase)
   - 0.5-1.5 ms: main impulse (transient peak)
   - 1.5-2.5 ms: tweeter-to-woofer secondary impulse (if not time-aligned)
   - 3+ ms: room reflections, cabinet vibration tail, ringing
```

### Pre-ringing vs post-ringing

- **Pre-ringing**: oscillations **before** the main impulse.
  Caused by **linear-phase FIR filters** (especially aggressive
  brickwall filters). Audible as a "sucking-in" texture before
  transients on percussive material. ~1 ms of pre-ringing is the
  rough audibility threshold.
- **Post-ringing**: oscillations **after** the main impulse. Caused
  by resonances (cone, cabinet, room modes). Always present;
  becomes a problem when high-Q or low-frequency.

Minimum-phase filters and direct-radiator speakers have **no
pre-ringing**. This is one of the practical reasons to prefer
IIR (minimum-phase) over linear-phase FIR in critical listening
applications — see `dsp-and-active.md`.

## 2. The step response

The integral of the impulse response. The output to a sudden DC
shift (a unit step input).

```
amplitude
   |
   |        ___________________________________
   |       /                                    \
   |      /                                      \____
   |     /
   |    /
   |   /
   |--/
   |
   +-------- t

   - rise time: 0.35 / f_-3dB (Gaussian filter approx)
   - overshoot: depends on Q of the highest-frequency resonance
   - settling time: ~5 × rise time for typical Q
```

What to look for:

- **A smooth rise** (no pre-ringing, single dominant peak): well-
  aligned multi-way design.
- **Multiple peaks** on the rising edge: tweeter and woofer impulses
  are arriving at different times. Stepped/tilted baffle or DSP
  delay needed.
- **Overshoot before the plateau**: highest-frequency resonance has
  high Q. Cone breakup, often.
- **Slow droop** in the plateau: high-pass behavior (sealed/ported
  rolloff visible in the time domain).

The step response is the most intuitive single time-domain plot for
identifying timing/alignment issues.

## 3. Group delay

`τ_g(f) = -dφ(f)/dω`. The frequency-dependent delay of the signal
envelope as it passes through the system.

### Audibility

| Group delay        | Audible?                                                  |
|--------------------|-----------------------------------------------------------|
| < 1 ms             | inaudible                                                  |
| 1-5 ms             | inaudible for most music; audible on impulses (drums, plucked strings) |
| 5-20 ms            | audible as "softer transients"; common in heavily-EQd subs |
| > 20 ms            | starts to feel detached, especially below 100 Hz          |

Threshold for **change** in group delay across the band: ~1.5 cycles
at the lowest audible frequency in band. So `τ_g < 1.5/f` at every
frequency.

### Typical group delays

| System                  | Group delay characteristic                          |
|-------------------------|-----------------------------------------------------|
| Sealed sub, Qtc=0.7     | ~5 ms at Fc, dropping above                         |
| Ported sub at Fb        | ~15-25 ms (4th-order filter contributes)            |
| Sealed sub + Linkwitz transform | same as sealed (LT adds no group delay)     |
| FIR room correction     | half the filter length (e.g. 21 ms for 4096-tap @ 96 kHz) |
| Mains crossover (LR4 at 2 kHz) | ~0.5 ms at fc                                |

A speaker with no DSP, minimum-phase crossover, and sealed alignment
has group-delay variation < 5 ms across its full band — typically
inaudible. Add a Linkwitz transform to bass-extend and the variation
stays the same. Add FIR for room correction and you trade group-delay
flatness for added latency.

## 4. Energy decay (waterfall plot)

A 3D plot showing SPL vs frequency vs time. For each time slice
after the impulse, plot the residual response. Typical
visualization:

```
freq → 100 Hz                  1 kHz                  10 kHz
       |                        |                       |
   --- top of waterfall ---     (t = 0)
       |                        |                       |
       |   resonance ridge      |   clean decay         |
       |   at panel mode        |                       |
       |                        |                       |
   --- 10 ms below              ---
       |                        |                       |
       |   still ringing        |   gone                |
   --- 30 ms below              ---
```

Ridges that persist beyond ~10 ms = resonances. Look for:

- **Vertical ridges below ~300 Hz**: panel resonances and room
  modes.
- **Vertical ridges 1–5 kHz**: cone breakup, tweeter dome modes.
- **Vertical ridge at port tuning frequency**: ringing from the
  Helmholtz resonator (always present; should die within 1.5–2
  cycles).

The waterfall is the single most useful plot for distinguishing
"sounds clean" from "sounds colored" speakers when FR alone doesn't
tell you the answer.

## 5. Cumulative spectral decay (CSD)

A waterfall plot computed with **logarithmic time** axis (showing
decay over 100 ms in detail near zero, less detail at the end).
Common in REW, more useful for spotting LF resonances than
linear-time waterfalls.

## 6. Phase response

`φ(f)` accompanies magnitude in a full FR plot. Two flavors:

- **Minimum-phase**: phase is uniquely determined by magnitude.
  Computable via Hilbert transform of `log|H(f)|`. The "expected"
  phase for a given magnitude curve.
- **Excess phase**: the difference between measured phase and
  minimum-phase. Reveals true delay (acoustic-center offset,
  diffraction-induced delay).

For diagnosis: plot **excess group delay**. A speaker that is
well-time-aligned has near-zero excess phase across its band. Excess
phase shows up as a non-flat excess group delay vs frequency.

### Phase across a crossover

At an LR4 crossover frequency, both drivers experience 180° phase
shift through the filter. They sum to 0° (same phase as the input)
because their relative phases cancel. **This is normal** and is
not a defect.

At an LR2 crossover, the two drivers are 180° apart at fc; you
invert one driver to make them sum coherently.

Phase rotation through a 2nd-order filter is 180° over the full
transition; through a 4th-order, 360°. Audibility of this rotation:
generally inaudible for music (per Lipshitz, Pocock, Vanderkooy
1982), unless the rotation is concentrated at very low frequencies
(< 100 Hz) and the music has strong transients.

## 7. Audibility thresholds (summary)

| Time-domain feature             | Audibility threshold                            |
|---------------------------------|--------------------------------------------------|
| Group delay (constant offset)   | not audible at any value (just a time shift)    |
| Group delay variation across band | ~1.5 cycles at lowest frequency              |
| Pre-ringing                     | ~1 ms broadband; less at HF                     |
| Post-ringing                    | depends on Q; high-Q LF resonances most audible |
| ITD between L and R speakers    | ~10 μs (with headphones); ~50 μs (loudspeakers) |
| Step-response misalignment      | ~100 μs audible on critical transients          |
| Reflection (early, ≤10 ms)      | audible as spaciousness, not echo                |
| Reflection (late, >50 ms)       | audible as discrete echo                        |
| Pre-arrival reflection          | always audible above ~-20 dB relative to direct |

## 8. Time-domain in design

Practical implications for speaker design:

### Crossovers

LR4 is the default not just for its summing behavior but because its
time-domain step response — while not "ideal" — is **predictable**
and consistent. Bessel crossovers (BS4) have better step shape but
worse magnitude flatness.

### Active vs passive

DSP-active speakers can use FIR linear-phase crossovers for "perfect"
step response at the cost of pre-ringing and latency. Passive
speakers cannot. Whether this matters subjectively is a long-running
debate; published research suggests it doesn't, for music — but
listeners differ.

### Drivers

A driver with severe cone breakup will ring even when its breakup
peaks are filtered out — the time-domain ringing extends below the
crossover frequency at reduced amplitude. Hard-cone drivers
(aluminum, beryllium, ceramic) need notch filters AND careful
crossover frequency selection to keep time-domain artifacts buried.

### Cabinets

Panel resonances and internal modes ring at 100–500 Hz for tens of
ms. Bracing + damping kill the Q; the resonance frequency is what
the energy is at, the Q is what makes it ring.

### Subwoofers

Sealed subs have lower group delay than ported (~10 ms vs ~20 ms at
typical tuning frequencies). For music with prominent kick drum,
this is audible. The Linkwitz-transform-on-sealed approach combines
sealed's transient response with ported-like extension — at the cost
of amplifier headroom.

## 9. Measuring time-domain behavior

REW workflow (free, the standard):

1. Run a swept-sine measurement.
2. View the **impulse response** tab; this is your raw data.
3. **Frequency response** tab: FFT.
4. **Step response** tab: integral of impulse.
5. **Group delay** tab: `-dφ/dω`.
6. **Waterfall / CSD** tab: time-frequency-amplitude 3D.
7. **Excess group delay** tab: deviation from minimum-phase.

Gate the impulse to ~5 ms for in-room speaker measurements to remove
room reflections from the time-domain analysis; this limits the
lowest valid frequency to ~200 Hz. Below that, near-field measurement.

## Cross-references

- `references/measurement.md` — REW measurement workflow.
- `references/crossovers.md` — how crossover topology shapes the
  time-domain.
- `references/dsp-and-active.md` — FIR vs IIR time-domain trade-off.
- `references/baffle-and-cabinet-acoustics.md` — panel and internal
  modes as the source of time-domain coloration.
- `references/subwoofers.md` — group delay budgets for LF.
- `references/standards-and-targets.md` — Lipshitz/Pocock/Vanderkooy
  on phase audibility.
