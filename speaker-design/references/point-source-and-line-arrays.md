# Point Source vs Line Array

The system-architecture choice that shapes a speaker's behavior more
than driver selection: should the speaker radiate from approximately
one point (spherical waves, 6 dB/distance-doubling) or from a vertical
line (cylindrical waves, 3 dB/distance-doubling, controlled vertical
pattern)?

This file covers the physics, the design criteria, the variants
(coincident point sources; constant-curvature, progressive-splay,
and CBT line arrays), and when each fits.

## 1. The radiation regimes

A loudspeaker's far-field radiation can be characterized by how its
sound pressure falls with distance:

| Geometry          | Pressure with distance | Power with distance | Reason                          |
|-------------------|------------------------|---------------------|----------------------------------|
| Point source      | 1/r (6 dB / doubling)  | 1/r²                | Spherical-wave expansion        |
| Line source (infinite) | 1/√r (3 dB / doubling) | 1/r            | Cylindrical-wave expansion      |
| Plane wave (no expansion) | constant         | constant            | No expansion (impractical)      |

Real line sources (finite length) act as cylindrical sources within
their **near field** and transition to spherical (point-source-like)
in their **far field**. The transition distance:

```
r_transition ≈ L² · f / c
```

where `L` is the array length. For a 2 m array at 1 kHz: r ≈ 5.8 m;
at 10 kHz: r ≈ 58 m. So small line arrays "behave like lines"
within useful listener distances at HF, but transition to point-
source behavior in the bass.

## 2. Point source

All drivers radiate from approximately the same acoustic center.
Approximations:

- **True coincident**: a single driver, or a coaxial design where HF
  and LF emanate from the same axis (KEF Uni-Q, Tannoy DC, Genelec
  coaxial, Cabasse). See `phase-plugs.md` for how phase plugs make
  this possible.
- **Close-spaced multi-way**: a two-way with center-to-center driver
  spacing ≤ λ at the crossover frequency behaves approximately as a
  point source through the listening band. Most studio nearfield
  monitors aim for this.
- **D'Appolito MTM** (midrange-tweeter-midrange): two midrange drivers
  flanking a tweeter; on-axis they sum coherently, off-axis vertical
  has nulls. Not strictly a point source — has vertical lobing — but
  presents as one in the horizontal plane.

### Strengths

- **Smooth power response** at all angles (sphere has same DI in all
  directions).
- **Predictable in-room behavior**: 6 dB/doubling matches what every
  intuition expects.
- **Tight imaging** when listening on-axis.
- **No complex array tuning**: one box, point it at the listener.

### Weaknesses

- **Coverage area limited**: SPL falls fast with distance. A point
  source mixed at 100 dB at 2 m delivers 88 dB at 8 m and 70 dB at
  64 m — useless in arenas.
- **Floor and ceiling reflections**: at concert/PA distances, the
  floor and ceiling are within the same range as the listener.
  Reflections sum with direct at varying delays, comb-filtering the
  response.
- **Vertical pattern uncontrolled**: a point source radiates upward
  as much as forward at LF. Wastes energy.

### When to use

- Studio nearfield (≤ 2 m).
- Living-room hi-fi (≤ 4 m).
- Conferencing where listeners are seated around a table.
- Atmos overhead channels.
- Cinema surround.

## 3. Coaxial point sources

The most disciplined point source is a true coaxial design:
- KEF Uni-Q (since 1988, refined 12+ generations).
- Tannoy Dual Concentric (since 1947).
- Genelec coaxial 8341/8351 etc.
- Cabasse "Murano" line.

Engineering challenges:

- **Doppler modulation**: the tweeter is mounted on the woofer's
  motor structure; woofer cone excursion at LF moves the tweeter
  axially. Modulates HF by ~0.1 % per 1 mm of LF excursion → 3rd-
  order IMD at high levels. KEF mitigates this with a stationary
  tweeter on the pole piece (not the cone).
- **Woofer cone acts as horn for tweeter**: the curved cone defines
  the HF radiation pattern. Phase plug + cone profile must be co-
  designed.
- **Voice-coil overlap**: tweeter motor inside woofer motor needs
  flux clearance; difficult to make low-distortion woofers in this
  geometry.

Done well, coaxial designs achieve **near-textbook point-source
behavior** — single FR vs angle, no vertical lobing, no
crossover-region collapse. Live recordings on coaxials are notably
"believable" in spatial cues.

## 4. Time alignment in point sources

For a two-way with physically separated drivers (typical bookshelf or
tower), the **acoustic centers** of the two drivers are at different
distances from the listener:

```
acoustic center ≈ voice-coil center + small correction
```

For a 6.5" woofer + 1" dome, the dome sits ~10 mm forward of the
woofer's voice coil. At a 2 kHz crossover, that 10 mm represents 17°
of phase rotation — enough to shift the crossover lobe a few degrees
off-axis.

Mitigation strategies:

1. **Tilted / stepped baffle**: physically recess the tweeter so the
   acoustic centers align at the listening axis. Common in
   high-end designs (Wilson, Vandersteen, KEF).
2. **DSP delay** to one driver. Trivial in active speakers; impossible
   in passive.
3. **Crossover phase compensation**: select a crossover topology
   (e.g. LR4) whose phase rotation at the crossover frequency
   compensates for the spatial offset. Requires per-design tuning.
4. **Accept the misalignment**: many commercial speakers do, with the
   sweet spot a few degrees below the geometric center.

The lobing pattern from imperfect alignment is most visible in vertical
polars — measure off-axis vertical to verify.

## 5. Line array

A vertical column of drivers (woofers, mid-tweeters, or full-range
boxes), spaced closely enough that they act collectively as a long
source.

### Two regimes

For a line of length `L` with element spacing `d`:

- **Long-line regime** (`λ < 2L`): array behaves as a cylindrical
  source. Vertical pattern controlled, 3 dB/distance-doubling decay.
- **Short-line regime** (`λ > 2L`): array behaves as a sum of point
  sources at LF — back to spherical decay.

For drivers crossing over at frequency `f_x`, **element spacing
must satisfy `d < c/(2 f_x) ≈ λ_x/2`** to avoid spatial-aliasing
lobes above `f_x`. Spacing too wide creates comb-filtering at
extreme off-axis angles and "fingers" in the vertical pattern.

### Straight column

All elements coaxial, vertically aligned. Used by:
- Bose 901 (vintage; reflective-walls concept).
- Karlson and Voigt line arrays.
- Small in-wall or soundbar designs.

Limited HF performance: at frequencies where adjacent elements are
more than λ/2 apart, comb-filtering appears off-axis. A standard
50 mm element spacing limits the array to ~3.4 kHz before
significant lobing.

### Constant-curvature (J-array)

Elements arranged on a circular arc; vertical pattern is
approximately constant across the band. Used in vintage L-Acoustics
V-DOSC, EAW KF series.

- Throws far at the center of the arc.
- Lobing at the bottom of the array (where geometry deviates from
  ideal).

### Progressive-splay (modern variable-curvature)

Each box's tilt angle from its neighbor is **individually adjustable**.
The user chooses the splay per box to match the venue geometry
(audience position vs array height). Tools (L-Acoustics Soundvision,
d&b ArrayCalc, Meyer MAPP) predict coverage from box angles.

Examples:
- L-Acoustics K-series, Kara, KS28
- d&b audiotechnik J-series, Y-series, GSL
- Meyer Sound LEO, LEOPARD, PANTHER
- JBL VTX, KSL
- RCF HDL

This is the dominant pro-touring topology since ~2005. Mixing has
shifted from "find the sweet spot" to "deliver uniform SPL across the
listening area."

### Wavefront sculpting (DOSC)

L-Acoustics' patented technique: each line array element has a
waveguide that shapes its output into a specific wavefront curvature,
so that adjacent boxes combine into a continuous cylindrical
wavefront over a wide band. Replaces the simple "tighter spacing =
higher cutoff" rule with explicit wavefront design.

### CBT (Constant Beamwidth Transducer)

A circular-arc section of an array with **cosine amplitude weighting**
across the elements produces a constant beamwidth over a wide range
of frequencies. Theory by Don Keele Jr. (2003); used in:

- JBL CBT public-address line.
- Some Bose conference systems.
- DIY designs with 4–12 element sections.

Why CBT matters:

- **Wide working range**: a single CBT array delivers ~50° vertical
  pattern from ~100 Hz to ~16 kHz, no per-frequency splay tuning
  required.
- **No floor / ceiling reflection issues**: the narrow vertical
  pattern doesn't excite floor/ceiling modes.
- **Reasonable DIY**: a 4-element CBT (small bookshelf-sized elements
  on a curve) is buildable and well-documented; Don Keele has
  published DIY guides.

CBT design parameters:
- Arc radius `R`: sets the LF onset (longer arc = lower freq).
- Total arc angle `Θ`: sets the vertical beamwidth.
- Element spacing: must be < λ/2 at the highest frequency.
- Cosine amplitude weighting: per-element gain ∝ cos(angle from center).

### J-shaped vs straight vs J-with-CBT hybrid

Modern arena PA stacks combine philosophies: a CBT-shaded section at
the top (covers far throw, narrow pattern), a progressive-splay
section in the middle (covers main audience), and downfill boxes
(near-field at the front). DSP delays per box align the wavefront.

## 6. Selection guide

| Scenario                          | Topology                          |
|-----------------------------------|------------------------------------|
| Studio nearfield, ≤ 2 m           | Coaxial point source              |
| Living room hi-fi, ≤ 5 m          | Close-spaced point source          |
| Conference room, 12 listeners     | CBT array or point source         |
| Cinema (mid-size)                 | 3-way point source per channel    |
| Small club PA, 20×15 m            | 2-3 element line array per side   |
| Mid-size venue, 50×30 m           | Variable-splay line array         |
| Arena, 80×60 m                    | Long progressive-splay line array  |
| Atmos overhead                    | Compact point source              |
| Soundbar (left+right virtualized) | Horizontal line array              |
| In-wall hi-fi                     | Point source with shallow waveguide|

## 7. Practical pitfalls

- **"Mini line array" sized between regimes** — too short to be a
  cylindrical source at LF, too long to be a point source at HF.
  Result: confused vertical pattern, comb-filtering across the
  midrange. Either make the array longer or use a coaxial point
  source.
- **Line array + subwoofer integration**: the array is cylindrical
  above its lower limit; the sub is a point source. They don't sum
  cleanly across the crossover — the sum varies with listener
  position in a way single-source systems don't show. Tune the
  crossover with measurement at multiple listening positions, not
  just one.
- **Floor / ceiling reflections for line arrays**: a line array within
  a room treats the floor and ceiling as virtual extensions of the
  array (image sources). At low frequencies this gains 3–6 dB of
  output; at high frequencies it creates lobing depending on array
  height relative to the boundaries.
- **Imaging in a line array**: localization cues are weakened — there
  is no single source to localize. Acceptable for PA, problematic
  for stereo hi-fi.
- **Element spacing chosen by aesthetics**: must be chosen by the
  highest-frequency-of-use λ/2 criterion. Cosmetic spacing creates
  cosmetic-only line arrays.

## 8. Measurement

- **Polar response at multiple heights**: a line array's coverage
  changes with listener vertical position. Sweep at ear height,
  +30 cm, -30 cm at minimum.
- **SPL vs distance**: confirms cylindrical/spherical transition
  point. Important for verifying the system "throws" as designed.
- **Predicted vs measured coverage**: prediction tools (Soundvision,
  ArrayCalc) match measured response within 2-3 dB at most listener
  positions. Where they don't, the array's geometry is mis-modeled.

## 9. DIY notes

- A **small CBT** (4-element vertical curve, ~600 mm tall) is the
  most tractable DIY line array project. Don Keele has published
  step-by-step designs.
- **Straight in-wall arrays** with full-range drivers (5 × 4" Fostex
  in a 1.2 m baffle) work in the 200 Hz – 8 kHz range and pair well
  with a sub.
- **Mini line array** for atmos (3 × 2" drivers on a tilted panel)
  is realistic — short enough to behave as point source in the
  cylindrical-wave's far field, long enough to give acceptable HF
  dispersion control.

## Cross-references

- `references/phase-plugs.md` — phase plugs make point sources
  acoustically coincident.
- `references/horns-and-waveguides.md` — variable-splay line array
  elements typically use compression-driver-on-waveguide HF.
- `references/dsp-and-active.md` — modern line arrays rely on DSP for
  per-box delay and EQ.
- `references/baffle-and-cabinet-acoustics.md` — diffraction and
  baffle considerations apply per-element.
- `references/room-response-simulation.md` — array coverage prediction
  tools and ray-tracing for the venue.
