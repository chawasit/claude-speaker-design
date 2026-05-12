# DSP and Active Speakers

Active speakers (amplifier + crossover + drivers in one box) and
DSP-based processing have become the default for studio monitors and
the dominant trend in consumer audio. The benefits are large and not
purely marketing: tighter driver-amp coupling, no passive component
losses, freedom to use steep slopes without expensive inductors, and
the ability to undo cone, motor, and enclosure imperfections in
software.

## Active vs. passive: where the differences matter

| Aspect                        | Passive                                  | Active / DSP                            |
|-------------------------------|------------------------------------------|------------------------------------------|
| Crossover position            | After power amp                          | Before power amps (per driver)          |
| Steep slopes (LR4+, LR8)      | Heavy, expensive inductors/caps          | Trivial in software                      |
| Driver-amp coupling           | Filter parts in path → damping factor ↓  | Direct amp-to-driver → max damping       |
| Driver protection             | None (PTC, fuses are crude)              | Limiters, voltage clamps, thermal models |
| Pair matching                 | Components vary ±5–10 %                  | Identical bits for every unit            |
| Response correction           | Possible but expensive (LCR notches)     | Trivial PEQ in software                  |
| Linkwitz transform            | Approximate (Linkwitz-Reilly EQ amp)     | Exact pole-shift in IIR                  |
| Linear-phase / FIR crossovers | Impossible                               | Available with latency cost              |
| Latency                       | ~µs (electrical only)                    | 0.5–30 ms depending on FIR length        |
| Bi-/tri-amping flexibility    | Hard to retrofit                         | Native                                   |
| Field updates                 | Hardware-only                            | Firmware updates change behavior         |

The trade is mostly cost + complexity + latency vs. precision + control.

## IIR vs. FIR filters

**IIR (Infinite Impulse Response)**: digital implementation of analog
biquads (1st and 2nd order sections). Behaves like analog: minimum
phase, low latency (sample-level), efficient on DSP MIPS. The default
for crossovers and PEQ. Standard filter types: low/high-pass
(Butterworth, LR, Bessel), peaking, shelving, all-pass.

**FIR (Finite Impulse Response)**: filter defined by a tap-by-tap
convolution kernel. Can have arbitrary magnitude + arbitrary phase,
including **linear phase** (constant group delay across band). Cost:
latency equal to half the tap count.

```
latency_FIR = N_taps / (2 · f_sample)
```

At 96 kHz, 8192 taps = 43 ms latency. Long FIRs are needed only for
low-frequency phase correction; for HF, 256 taps at 48 kHz (3 ms) is
plenty.

Use FIR when:
- You want linear phase through crossover for a critical monitor.
- You need to invert a driver's measured phase response (driver
  linearization, full-band group-delay flattening).
- You're correcting a horn or waveguide's group-delay departure.

Use IIR (and don't agonize) when:
- Latency matters (live sound, instruments, video lipsync).
- Phase character is acceptable (it usually is for a well-designed
  minimum-phase system).
- DSP resources are limited.

## Linkwitz transform (LT)

Pole-shift biquad that converts a sealed driver's natural high-pass
behavior into any new target high-pass shape. Given a measured
(`Fc`, `Qc`) and target (`Fp`, `Qp`):

```
H_LT(s) = (s² + (2π Fc)s/Qc + (2π Fc)²) / (s² + (2π Fp)s/Qp + (2π Fp)²)
```

Implemented as a single biquad. The transform is **exact in
amplitude and phase** through the working band — no group-delay
penalty above the new cutoff. The cost is excursion: driving the
driver to a lower Fp at the same SPL means more cone travel.

Typical use: convert a sealed sub from natural F_c = 50 Hz, Q_c = 0.7
to Fp = 25 Hz, Qp = 0.5 — gains a full octave of usable bass, costs
~20 dB of EQ boost at 20 Hz and corresponding excursion increase.

## Crossover targets in DSP

Same acoustic targets as passive (LR2, LR4, LR8 — see `crossovers.md`),
but the **filter** you apply is the **target acoustic** minus the
measured **driver** response. Workflow:

1. Measure each driver in the actual baffle with the actual mic
   position. Save complex (magnitude + phase) data.
2. In VituixCAD / rePhase / Acourate, set the target as e.g. LR4
   acoustic at 2 kHz.
3. Software derives the IIR or FIR filter chain that, in series with
   each driver's measured response, hits the target.
4. Apply driver-specific PEQ for breakup notches.
5. Apply system-wide tilt/shelves for room compensation if desired.

Critical: derive filters from the **acoustic** response, not the
electrical filter math. Real drivers' rolloffs alter the effective
crossover order — a 4 kHz natural rolloff on a tweeter changes a 2 kHz
LR4 low-pass into something steeper.

## Room correction

Two philosophies:

**Modal / below-Schroeder correction**: PEQ the room modes that cause
peaks at the listening position. Effective and uncontroversial below
~200 Hz. Pulling down a 12 dB peak at 45 Hz with a Q = 5 PEQ recovers
a clean bass region with no audible side effects.

**Full-range automatic correction** (Dirac, Audyssey, ARC, Trinnov,
RoomPerfect): software measures multiple positions and synthesizes an
inverse FIR filter. Effective with caveats:

- Phase issues from reflections **cannot** be EQ'd away — they're not
  minimum phase. Trying to flatten a comb-filter null adds boost
  energy that just makes the null deeper somewhere else.
- Above ~500 Hz, target curves matter more than corrections — most
  systems aim for a falling response ("Harman target", ~ -1 dB/oct
  above 1 kHz).
- More mic positions averaged = smoother result + less precision at
  any single seat. 5–9 positions in a stereo triangle is the standard.

Do **not** apply room correction to mids/highs without verifying with
measurement. The cure is often worse than the disease.

## Limiter and protection chain

A well-designed active speaker uses several limiters in series:

1. **Input clip limiter** — prevents the ADC from clipping.
2. **Per-driver excursion limiter** — uses a model of `Xmax(f)` from
   T/S parameters to predict cone displacement from instantaneous
   filter output, attenuates input when displacement would exceed
   limit. Lookahead 5–20 ms.
3. **Per-driver thermal limiter** — models voice-coil temperature
   from filtered RMS power, attenuates as `T_VC` approaches `T_max`.
4. **Amplifier limiter** — prevents clipping the output stage.
5. **DC offset / subsonic** — high-pass below working band to keep
   DC and infrasonic content from eating displacement.

Klippel's "Controlled Sound" or PowerSoft's "DSP-PFC" implement
these formally. DIY active systems often use only #1, #4, #5 — but
adding the model-based excursion limiter prevents the most common
field failure (cone bottoming on infrasonic content).

## Latency budget

Audible thresholds:

- **Lipsync (audio relative to video)**: ITU-R BT.1359 allows
  -125 ms (audio late) to +45 ms (audio early). Beyond this is
  visibly mismatched.
- **Live monitoring**: musicians notice >10 ms; uncomfortable >20 ms.
- **Crossfeed between left/right speakers**: irrelevant if both have
  the same latency.

So FIR + room correction is fine for movies and music. For live sound
or studio tracking, stay with IIR (sub-ms latency).

## DSP platforms

| Platform                    | DSP    | Crossovers          | Notes                          |
|-----------------------------|--------|---------------------|--------------------------------|
| miniDSP 2x4 HD / Flex       | SHARC  | IIR + 4096-tap FIR  | $200–600; DIY workhorse        |
| Hypex Fusion FA series      | ADAU   | IIR                 | Plate amps with built-in DSP   |
| Purifi Eigentakt + DSP front| varies | varies              | Class D + DSP modules          |
| Genelec GLM                 | proprietary | IIR + FIR     | Pro monitor ecosystem          |
| Dirac Live (PC/AVR plug-in) | host   | mixed-phase FIR     | Whole-system room correction   |
| Acourate (PC convolver)     | host   | linear-phase FIR    | DIY/audiophile FIR generation  |
| rePhase + JRiver/HQPlayer   | host   | FIR                 | Convolution at playback time   |

## Practical workflow for an active two-way design

1. Choose drivers; measure T/S; build trial enclosure.
2. Measure each driver in-baffle (gated quasi-anechoic + nearfield
   merged) at the design listening axis. Save magnitude + phase.
3. Apply a baseline LR4 acoustic target in VituixCAD at the chosen
   crossover frequency.
4. Add per-driver PEQ to flatten major response irregularities
   (breakup notch on the woofer, response ripple on the tweeter).
5. Apply BSC shelf if listening more than ~1 m from the speaker.
6. Verify on/off-axis response — adjust slopes or fc if directivity
   mismatches at the crossover.
7. Set excursion + thermal limiters from driver T/S + power rating.
8. Compile filters to the DSP platform's format (REW exports for
   most miniDSP/Hypex/JRiver targets).
9. Verify end-to-end with the speaker playing: measure FR, compare
   to target; sweep distortion at target SPL; check polar.
10. Listen on familiar program material. Iterate the target curve
    (not the filters) until the speaker sounds neutral on known
    material.
