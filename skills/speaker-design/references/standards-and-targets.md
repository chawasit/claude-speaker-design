# Standards and Target Curves

What "flat" means depends on context. Anechoic flat ≠ in-room flat ≠
preferred. This file collects the published standards, target
curves, and measurement protocols that the industry has converged on.

## 1. CEA/CTA-2034 (the "Spinorama")

Originally CEA-2034 (2013), now CTA-2034-A (2021). The de facto
standard for **anechoic loudspeaker measurement** in consumer audio.

Defines a **70-measurement scheme**: 36 horizontal + 36 vertical
positions around the speaker (10° increments), reduced to a set of
weighted-average curves:

| Curve                      | What it averages                          | What it tells you             |
|----------------------------|-------------------------------------------|-------------------------------|
| On-axis                    | 1 measurement at 0° / 0°                  | Direct-sound character        |
| Listening window           | ±30° H × ±10° V (9 measurements)         | What a seated listener hears  |
| Early reflections          | Floor / ceiling / front / rear / side    | First-bounce-weighted average |
| Sound power                | All 70 weighted by area                  | Total radiated power vs. f    |
| Predicted In-Room (PIR)    | 12% LW + 44% ER + 44% sound power        | Predicted in-room response    |
| Directivity Index (DI)     | On-axis − sound power                    | Pattern width vs. frequency   |
| Early-Reflection DI        | On-axis − early reflections              | Reflection vs. direct ratio   |

**Why spinorama matters**: Toole and Olive at the Canadian National
Research Council showed (1980s–1990s) that listener preference
correlates with **smooth, flat on-axis response + smooth gently-
declining sound power + matched DI through crossover**. The spinorama
is the dataset that quantifies all four.

**How to read one** (the typical 7-line plot):

- **On-axis**: should be flat ±2 dB from cutoff to 10 kHz.
- **Listening window**: should track on-axis within 1 dB.
- **Early reflections**: should tilt down 3–6 dB from 200 Hz to
  10 kHz (the natural pattern of a well-designed speaker).
- **Sound power**: should track early reflections within 1 dB.
- **Predicted in-room**: should match the Harman target slope (next).
- **DI**: should rise smoothly from ~0 dB at LF to ~10–15 dB at HF.
  Sudden DI changes = directivity discontinuity = bad.

Spinorama data published by Audio Science Review (ASR),
spinorama.org, manufacturers like Genelec and KEF.

## 2. Harman / Olive in-room target

In-room measured response that listeners (across blind tests) rated
most preferred. Sean Olive's research at Harman, ~2010–present.

The curve:

- **20 Hz to ~120 Hz**: rising +3 to +6 dB above midrange.
- **120 Hz to 1 kHz**: flat.
- **1 kHz to 10 kHz**: −1 dB/octave downward tilt.
- **Above 10 kHz**: −2 dB/octave.

Plotted at the listening seat with 1/6-octave smoothing.

The shape reflects:
- LF rise from room gain / boundary loading.
- Midrange flat for natural timbre.
- Treble tilt because room absorption and air absorption knock down
  HF more than LF; speakers should compensate to leave the **direct
  sound** balanced.

This target is for **measured-at-seat** response, not anechoic. An
anechoic-flat speaker placed in a typical room produces roughly this
curve, modulated by room modes — i.e., you don't have to design to
the Harman target; you design to flat anechoic, and the room does
this transformation.

## 3. ITU-R BS.1116 / BS.775 (broadcasting reference)

International Telecommunications Union references for surround-sound
critical listening rooms.

- **Listening room T_60 (500 Hz, 1 kHz)**: 0.25 s ± 0.05 s
- **Frequency response at listening point**: ±3 dB from 50 Hz to
  16 kHz (relaxed to ±6 dB at 30 Hz)
- **Background noise**: NR15 (≈25 dB(A))
- **Listener position**: equilateral triangle, listening distance =
  speaker spacing.

These are stricter than typical hi-fi targets — they're for content
review and quality control.

## 4. BBC RD reports (legacy reference designs)

The BBC's Research Department published influential acoustic
references in the 1970s–1980s:

- **RPB-coloration curve**: a "room-plus-speaker bidirectional"
  in-room response target. Similar to modern Harman target but
  derived earlier from BBC listening rooms.
- **LS3/5a target**: a famous studio monitor reference — became the
  template for "BBC-tradition" small monitors (Spendor, Harbeth,
  Rogers, Falcon).

The BBC tradition's emphasis on **low coloration, smooth midrange,
controlled HF** lines up well with modern listening preferences.

## 5. AES2-2012 (driver characterization)

AES recommended practice for **measuring transducer parameters**.
Specifies:

- T/S parameter measurement methods (free-air, added-mass, added-
  volume).
- Small-signal vs large-signal parameters.
- Klippel-style large-signal measurement (BL(x), Kms(x), Le(x, i)).
- Xmax defined by **10 % distortion** or **20 % BL drop** thresholds.

Use AES2 Xmax over manufacturer marketing-Xmax when the data is
available — the AES number is typically 30–50 % lower than the
marketing claim.

## 6. IEC 60268-5 (loudspeaker performance)

International standard for performance specifications. Defines:

- Rated sensitivity (2.83 V at 1 m, half-space).
- Rated power handling (continuous, peak, music).
- Distortion measurement procedures.
- Polar response.

Used in compliance / commercial specifications. Most consumer audio
ad copy doesn't strictly comply with IEC 60268-5; pro / commercial
specs do.

## 7. IEC 60268-21 (in-situ measurement)

For installed sound systems in rooms — what they actually deliver,
not what they could in an anechoic chamber. Specifies:

- Microphone position averaging.
- Measurement signals (pink noise, sine sweep).
- Smoothing for reporting.

Cinema (SMPTE), large-venue (AES), and public address (NEC) systems
typically use this for commissioning.

## 8. ISO 226 (equal-loudness contours)

Defines the **equal-loudness contours** (the "Fletcher-Munson curves"
in their modern form). At 40 phons:

- 1 kHz reference: 40 dB SPL.
- 100 Hz: ~62 dB SPL.
- 10 kHz: ~50 dB SPL.

At 80 phons:
- 1 kHz: 80 dB SPL.
- 100 Hz: ~87 dB SPL.
- 10 kHz: ~85 dB SPL.

Implication: the bass-treble balance changes with playback level.
"Loudness compensation" knobs apply a level-dependent EQ to match
perception across listening levels.

For mixing engineers: working at variable levels means the relative
LF/HF balance drifts. Studios standardize at ~83 dB SPL (cinema dialog
reference) or 76 dB (Dolby small-room reference) for consistency.

## 9. Weighting curves

Frequency-dependent weighting applied to SPL measurements to better
approximate hearing perception:

| Curve | Defined in   | Use                                           |
|-------|--------------|------------------------------------------------|
| A     | IEC 61672    | Everyday environmental SPL; ear at low levels |
| C     | IEC 61672    | High-level / peak; closer to flat               |
| Z     | IEC 61672    | True flat (no weighting)                        |
| K     | ITU-R BS.1770| Broadcast loudness (LUFS), heavier HF weighting|

Audio measurements should typically use **C-weighting or no weighting**
for hi-fi work — A-weighting hides LF noise that affects subjective
listening.

LUFS (Loudness Units Full Scale) per BS.1770 is the modern broadcast
standard for loudness normalization. Apple, Spotify, YouTube, etc.
normalize to roughly −14 LUFS.

## 10. Tolerance budget for a "neutral" speaker

Different organizations propose different tolerances for "good"
loudspeaker behavior. A consensus:

| Metric                                            | Target                       |
|---------------------------------------------------|-------------------------------|
| On-axis FR (anechoic, 1/12-oct smoothed)          | ±1.5 dB, 100 Hz–10 kHz       |
| Listening window vs on-axis                       | ±1 dB                         |
| Sound power smoothness                            | no peak/dip > 3 dB / octave   |
| Directivity (DI) variation through crossover       | ≤ 2 dB                        |
| Harmonic distortion at 96 dB SPL / 1 m             | < 1 % above 200 Hz; < 3 % above 50 Hz |
| Impedance minimum                                 | ≥ 0.7 × nominal              |
| Phase deviation from minimum-phase                 | < 90° anywhere               |

A speaker meeting all of these is in the top decile of consumer
designs.

## 11. Studio monitor specific (CTA-CEDIA RP-22, EBU R128)

- **EBU R128**: defines −23 LUFS integrated loudness for European
  broadcast. Implies a known peak level so monitor calibration
  matters.
- **Dolby Atmos for Home**: calibration to 79 dB pink noise per
  channel at the listening position.
- **THX cinema**: 85 dB SPL pink noise per main channel from 20 Hz
  to 20 kHz.

If you're mixing for any of these, set the studio gain so −18 dBFS
on the meters → reference SPL on the meter.

## 12. Practical use of these targets

For a DIY or commercial design:

1. **Aim for spinorama-flat anechoic** in the design phase. Use
   gated quasi-anechoic + nearfield merge to approximate spinorama
   on-axis and listening window. Sound power needs the full 70-point
   scan; estimate from polar measurements at 0°, ±30°, ±60°, ±90°.
2. **Place the speaker** so the in-room response approximates the
   Harman / Olive target. If it doesn't, adjust placement and room
   treatment before EQ.
3. **EQ only if needed** to fix room modes below ~300 Hz and remove
   significant breakup peaks above. Never EQ to compensate for
   spinorama irregularities — they reveal directivity problems EQ
   can't fix.
4. **Validate** against a published "good" speaker: Genelec 8351,
   Revel F228Be, KEF Reference Meta. If yours behaves like theirs,
   you're done.

## 13. Where the standards disagree

- **Anechoic flat (CEA-2034 on-axis target)** vs **in-room flat
  (Harman target)**: the two differ by the room transfer function;
  both are valid in their respective domains.
- **A-weighting** (used by SPL meters) vs **flat** (what speakers
  actually measure): SPL meter A-weighted readings underweight bass
  by 16 dB at 60 Hz.
- **Marketing sensitivity** (typically 1 W into 8 Ω rather than 2.83 V)
  vs **IEC 60268-5 sensitivity** (2.83 V): differ for 4-Ω-nominal
  speakers by 3 dB.
- **Distortion measured at "rated power"** vs at **listening levels**:
  rated power testing tells you nothing about how the speaker sounds
  at 90 dB SPL / 1 m.

## Cross-references

- `references/measurement.md` — how to do the spinorama-style polar
  measurement at DIY scale.
- `references/listening-setup.md` — placement to match the target
  in-room curve.
- `references/acoustic-treatment.md` — when to treat the room to hit
  the target.
- `references/acoustic-properties.md` — definitions for sensitivity,
  THD, IMD, group delay.
