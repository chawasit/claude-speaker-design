# Headphones

A loudspeaker is a transducer. A headphone is a loudspeaker coupled
directly to the ear via a small (~20 cm³ over-ear, ~1 cm³ IEM)
acoustic cavity. Much of the speaker-design skill applies — driver
T/S, materials, distortion — but the **coupling physics** is
fundamentally different, and so are the relevant target curves.

This file covers the differences and what they mean for design.

## 1. Coupling physics: why headphones are different

A speaker radiates into half-space (~`2π` sr). A headphone radiates
into a small sealed (or leaky) cavity bounded by the diaphragm on
one side and the ear canal on the other. Three regimes:

| Frequency band  | Behavior                                     |
|-----------------|----------------------------------------------|
| Below ~100 Hz   | Pressure chamber: SPL ∝ diaphragm displacement / cavity volume |
| 100 Hz – 1 kHz  | Mass-controlled cavity                       |
| > 1 kHz         | Distributed acoustics: ear-canal resonances, head/pinna diffraction |

In pressure-chamber mode, **excursion = SPL directly**. No box
loading, no room gain, no reflection — the diaphragm is the
source and the eardrum is the sink. This is why headphones can
produce 110 dB SPL from a 30 mm driver moving 0.5 mm.

The trade: every artifact in the diaphragm or the cavity reaches
the ear unmediated. There's no "room" to mask anything.

## 2. The HRTF and "natural" sound

A normal listener hearing a sound in free field experiences it
through the **Head-Related Transfer Function (HRTF)** — the
ear-and-head filtering that gives directional cues. The natural
HRTF has features:

- **Ear-canal resonance**: ~3–4 kHz peak, +10 to +15 dB.
- **Concha (outer ear) resonance**: ~5 kHz peak.
- **Pinna notches**: 8–12 kHz, source-direction-dependent.

A headphone playing back a recording **bypasses the HRTF**. Without
compensation, the playback would sound bass-heavy and treble-deficient
compared to listening to a real source at that level. Headphone EQ
("voicing") restores some of the missing HRTF, but never perfectly —
your HRTF is unique to your head shape.

## 3. Headphone target curves

The "what a headphone should measure like" question, finally
answered (somewhat) by Harman in the 2010s.

### Harman over-ear target (2018)

Measured on the Harman GRAS 43AG ear simulator. Looks like:

- 20 Hz: roughly flat with 200 Hz, +4 dB shelf rise below ~150 Hz.
- 200 Hz to 1 kHz: flat reference.
- 3 kHz: +10 to +12 dB peak (compensating for ear-canal resonance,
  inverted).
- 8–10 kHz: dip ~5 dB.
- 15 kHz: roll off.

The headphone is "neutral" by playing **the inverse of the average
HRTF** — flattening the difference between headphone playback and
free-field listening.

### Harman IEM target (2019)

For in-ear monitors. Different cavity → different target. Similar
shape but:
- Less ear-canal peak (the canal is partially bypassed by IEM tip
  position).
- Slightly different bass shelf.

### DF (diffuse-field) and FF (free-field) targets

Older targets from the 1980s, modeled on the average response of a
diffuse soundfield (DF) or free-field source (FF) at the eardrum.
DF is roughly Harman without the bass shelf; FF differs at HF
based on source direction.

Most "professional" headphones (Beyerdynamic, Sennheiser HD600
family) target DF; "consumer" ones target Harman.

## 4. Headphone types

### Over-ear (circumaural)

Large pads sealing around the entire ear. Cavity volume ~50–100 cm³;
ear pressure is largely sealed.

- Open-back (Sennheiser HD600, HiFiMan): rear of driver is open;
  diffraction relief but bass extension limited.
- Closed-back (Beyerdynamic DT770, Sennheiser HD25): sealed back;
  better bass + isolation, but acoustic-cavity reflections cause
  treble irregularity.

### On-ear (supra-aural)

Pads pressing on the ear, not around it. Sealing is poor; bass
response heavily dependent on fit.

### IEM (in-ear monitor)

Earpiece sealing in the ear canal (silicone, foam, or custom tips).
Direct coupling to the ear canal; very short acoustic path.

- Single-driver IEM (one dynamic, balanced armature, or planar
  magnetic): wide bandwidth but compromises.
- Multi-driver IEM (multiple balanced armatures with internal
  crossovers): each driver covers a band.
- Tribrid IEM (dynamic + BA + electrostatic): higher-end; covers
  bass/mid/treble with optimized transducers per band.

### Earbuds (non-sealing)

Sit in the outer ear, no canal seal. Heavy bass loss, room-
dependent. Not for critical listening.

### Bone-conduction

Vibrate the skull, bypass the eardrum. For accessibility and special
use; not for music quality.

## 5. Driver types in headphones

Same family as speaker drivers; design constraints differ:

| Type             | Pros                                  | Cons                                |
|------------------|---------------------------------------|--------------------------------------|
| Dynamic (moving-coil) | Cheap, broadband, low cost     | Distortion at LF/HF extremes; coil-form thermal limits |
| Planar magnetic  | Linear, low distortion, fast transient| Heavy, expensive, drive impedance varies |
| Balanced armature| Tiny, efficient, narrow band          | Bandwidth-per-driver limited; multi-driver designs needed |
| Electrostatic    | Lowest distortion, fastest transient  | Needs amp; large; expensive; STAX-only ecosystem |
| Bone-conduction  | Bypasses eardrum                      | Inefficient; not music-grade fidelity |

Modern flagship over-ear designs use:
- Planar magnetic (HiFiMan Susvara, Dan Clark Stealth, Audeze LCD-5).
- Electrostatic (STAX SR-X9000, HiFiMan Jade).
- Dynamic with very large diaphragms (Focal Utopia, Sennheiser HD800).

## 6. Headphone impedance and amp drive

Headphone impedance varies enormously: 8 Ω IEMs to 600 Ω over-ear.
Two consequences:

- **Low impedance** (< 32 Ω): needs current capability; output
  impedance of source must be low to avoid frequency-response
  variation (e.g. < 1 Ω for an 8 Ω headphone).
- **High impedance** (> 250 Ω): needs voltage swing; can sound dull
  from a phone or laptop output but excellent on a desktop amp.

The 1/8 rule: source output impedance ≤ ⅛ × headphone impedance for
flat response. Most modern DACs/amps satisfy this for 16–600 Ω
headphones; integrated phone outputs often don't.

### Sensitivity

Quoted in dB SPL / V or dB SPL / mW. To compute drive voltage for
target SPL:

```
V_rms_for_target_SPL = 10^((target_SPL − sensitivity_dB_per_V) / 20)
```

For a 105 dB / 1 V headphone, 110 dB peak needs `10^(5/20) ≈ 1.78
V_rms`, well within any decent source.

## 7. Distortion in headphones

Headphones can achieve **lower distortion** than speakers in
absolute terms — small diaphragm, small excursion, no enclosure
modes. But:

- **Driver design matters more**: large excursion at LF (for bass
  extension) and high acceleration at HF stress the diaphragm.
- **Pad seal matters**: a leaky pad seal turns the pressure chamber
  into a vented box, drastically altering LF response and adding
  pad-induced ringing at 100–300 Hz.
- **Cable microphonics**: cable vibration coupling to the driver
  via stiffness. Audible as bass thumps when the wearer moves.

Target: < 1 % THD at 100 dB SPL across the band. Top-tier headphones
(Susvara, Utopia, Stealth) hit < 0.3 %.

## 8. Measurement of headphones

Different from speakers; requires a **head simulator** or **ear
simulator**:

- **GRAS 43AG / 45CA**: industry-standard occluded-ear simulator with
  pinna and ear-canal-equivalent volume. ~$8000.
- **MiniDSP EARS**: $500 DIY-level rig; less accurate at HF.
- **APR-25 / WD9000**: in-ear measurement microphones for IEMs.

Each fit / pad-seating / cup orientation gives a different reading.
Average ≥ 3 fits for a stable headphone curve. Published headphone
measurements (Crinacle, Rtings, Resolve Reviews) follow this
discipline.

### What to measure

| Metric                              | Target / interpretation                                |
|-------------------------------------|--------------------------------------------------------|
| Frequency response vs Harman target | ±3 dB from 20 Hz to 10 kHz                            |
| Channel matching                    | < 1 dB difference L vs R                              |
| THD at 100 dB SPL                   | < 1 %                                                  |
| Group delay variation               | < 2 ms across 100 Hz – 10 kHz                         |
| Impedance vs frequency              | If varies ± 50% from nominal, source matters more     |

## 9. Headphone listening: pros, cons, and use cases

Pros:
- **Bypasses room modes**: no LF boundary problem.
- **High SPL from low power**: 110 dB from 100 mW.
- **Privacy and portability**.
- **Lower distortion ceiling** than speakers.

Cons:
- **Bypasses HRTF**: spatial cues are wrong unless compensated.
- **Crossfeed required** for accurate stereo (L→R and R→L bleeding,
  with HRTF-correct delays).
- **Comfort over hours**: weight, clamp pressure, heat.
- **No tactile bass**: the body doesn't feel a kick drum at 40 Hz
  the way it does with a sub.

When to use headphones for mixing:
- Late at night.
- For checking spatial precision (panning, reverb tails).
- For verifying detail (cymbal decay, vocal sibilance).
- **NOT** as the sole reference for tonal balance — always cross-
  check on speakers.

When to use speakers (despite a great headphone setup):
- Verifying tonal balance.
- Checking bass tonality and weight.
- Listening with others.
- Long sessions where comfort matters.

## 10. DIY headphone considerations

Headphone DIY is a smaller community than speaker DIY but exists:

- **Driver modding**: pad swaps, damping changes inside the cup.
  Surprisingly large effects on FR (±3-6 dB in critical regions).
- **Cable making**: marginal at best on FR; can change microphonics.
- **Custom IEM**: requires ear-molds and BA driver knowledge;
  reachable for an experienced builder.
- **Open-baffle / planar magnetic DIY**: a few projects exist
  (large surface area diaphragms with magnet arrays).

The community's resources:
- `head-fi.org` (large forum).
- `Crinacle.com` (graphs and measurements).
- `Resolve Reviews` YouTube (technical reviews).
- `oratory1990` Reddit profile (Harman-compensated headphone
  measurements).

## Cross-references

- `references/driver-types.md` — planar magnetic, electrostatic,
  balanced armature.
- `references/measurement.md` — extended for headphone ear-simulator
  measurement.
- `references/standards-and-targets.md` — Olive's Harman headphone
  target.
- `references/time-domain.md` — distortion and ringing in headphone
  drivers.
- `references/dsp-and-active.md` — Crossfeed and HRTF-correction
  DSP for headphone playback.
