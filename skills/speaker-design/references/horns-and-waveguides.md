# Horns and Waveguides

A horn (or waveguide) sits between a transducer and free air. It does
two jobs at once, with different emphasis depending on the design:

1. **Impedance matching** — couples the small, stiff diaphragm of a
   compression driver (or the small effective radius of a dome) to the
   large impedance of free air, raising efficiency by 10–20 dB.
2. **Directivity control** — shapes the radiation pattern so it is
   roughly constant with frequency, rather than collapsing from omni
   to a beam as wavelength shrinks.

Convention: "horn" emphasizes loading; "waveguide" emphasizes
directivity. The distinction is a continuum, not a category — every
horn has some directivity, every waveguide has some loading.

## 1. Webster's horn equation

For a duct whose cross-sectional area `S(x)` varies smoothly with
axial distance `x`, and whose flare is gradual compared to a
wavelength, the plane-wave assumption gives Webster's equation:

```
∂²p/∂t² = (c² / S) · ∂/∂x (S · ∂p/∂x)
```

Solutions depend on the flare profile `S(x)`. The equation is
**approximate**: it ignores radial wave propagation and assumes
quasi-plane wavefronts inside the horn. The approximation is best for
small flare angles and breaks down badly when the wavefront within the
horn is not flat (e.g. wide-mouth horns at HF, where radial modes
matter). Modern designs (OS waveguide, Le Cléac'h) start from this
limitation and try to fix it.

## 2. Flare profiles

### Conical

`S(x) = (S_t + α x)²` for a cone of half-angle θ. Wavefronts
inside the horn are nearly spherical; throat impedance is mostly
reactive at low frequency.

- Smooth high-frequency directivity (constant), ripply low-frequency
  loading.
- Easy to build (CNC lathe, layered plywood).
- The reference for "controlled-directivity" — directivity is set by
  the cone angle, frequency-independent above the diffraction limit.
- Compromised LF loading: a 60° conical horn doesn't load much below
  500 Hz unless very long.

### Exponential

`S(x) = S_t · e^(m x)`. Flare constant `m = 4π · f_c / c` defines the
cutoff frequency below which throat impedance becomes purely reactive:

```
f_c = m c / (4π)            Hz
```

Below `f_c`, the horn ceases to load — driver excursion goes up,
output drops. **Practical loading band starts at ~2 × f_c**, well
above the formal cutoff. Don't design a 100 Hz horn with f_c = 100 Hz;
design it with f_c ≈ 50 Hz so loading is firm by 100 Hz.

- Maximum LF loading per unit length of any profile.
- Mouth reflection (impedance mismatch at the mouth) gives ripples in
  passband; severity drops as mouth size grows.
- Pattern narrows with frequency (typical "honking" of cheap PA horns
  comes from poor exponentials + sharp throats).

### Hyperbolic (Salmon family)

`S(x) = S_t · (cosh(mx/2) + T·sinh(mx/2))²` with shape parameter T:

- T = 0: catenoidal
- T = 0.5: typical Salmon "hyperbolic"
- T = 1.0: exponential
- T → ∞: conical

Salmon's family lets you trade LF loading (lower T) for HF smoothness
(higher T). For PA midbass, T = 0.5–0.7 is the sweet spot.

### Tractrix

The tractrix is the curve a point traces when dragged on a string of
fixed length pulled along a line. Its key property: the wavefront
inside a tractrix horn is approximately a portion of a sphere of fixed
radius — the wavefront stays "in the same shape" as it propagates.

- Often praised for "naturalness" — no flare discontinuity to excite
  resonances; smooth time response.
- Wide directivity at LF, narrow at HF; not constant-directivity by
  default.
- Bulky for a given cutoff.

### Le Cléac'h / JMLC

Jean-Michel Le Cléac'h's iterative profile uses the Putland equation
to keep the wavefront spherical along the entire horn axis, with a
chosen wavefront-area progression. Tunable T parameter sets the
flare aggressiveness.

- Smoother passband response than tractrix or exponential.
- Wide LF pattern that gradually narrows; not strictly CD but better
  than exponential.
- Generated parametrically by ATH4 (Mabat), spreadsheets from
  audiohorn.com, and Hornresp.

### Oblate Spheroidal (OS) — Earl Geddes

The wave equation is separable in oblate spheroidal coordinates,
giving exact (not approximate) solutions for a specific class of
axisymmetric waveguides. The geometry: a hyperbolic flare into a
spherical mouth, parameterized by a single throat angle.

- Lowest higher-order mode excitation of any practical waveguide.
- True constant-directivity above ~`f_c × 2`, set by the chosen
  throat angle (typically 60°–100° full angle).
- Smooth time response; doesn't sound like a "horn".
- Compromised LF loading vs exponential — uses a compression driver's
  sensitivity advantage rather than further amplifying it.

Geddes' Summa speakers and the modern DIY OS-based designs (e.g.
JTRopp, ATH-generated waveguides) are the practical embodiments.

## 3. Cutoff and throat impedance

Throat acoustic impedance `Z_t(ω)` is a complex function of frequency
and profile. For an exponential horn:

```
Z_t(ω) = (ρ₀ c / S_t) · [ √(1 − (ω_c/ω)²) + j (ω_c/ω) ]
         for ω > ω_c

       = (ρ₀ c / S_t) · j · [(ω_c/ω) ± j·√((ω_c/ω)² − 1)]
         for ω < ω_c (purely reactive)
```

Above cutoff, `Re(Z_t) > 0` and the horn radiates real power. Just
above cutoff, the reactive part is large and the driver wastes energy
moving air without radiating. By `f ≈ 2 f_c`, `Re(Z_t)` approaches the
high-frequency asymptote `ρ₀ c / S_t` and the horn is fully loading.

Compression-driver datasheets typically quote efficiency at the
"practical loading frequency" — usually 1.5–2× the formal cutoff.

## 4. Compression ratio

For a compression driver feeding a horn, the **compression ratio** is:

```
CR = S_d / S_t           (diaphragm area / throat area)
```

Typical values: 5:1 to 10:1. Higher CR means more efficiency (the
horn impedance is transformed back to the diaphragm by the inverse
ratio), but:

- More HF distortion in the throat (air nonlinearity at high
  particle velocity).
- Earlier diaphragm breakup as the throat unloads at HF.
- Phasing plug becomes critical to maintain plane-wavefront entry.

Modern HF compression drivers (BMS, B&C, JBL) use CR ≈ 6:1; bass
horns use lower (3:1) since LF particle velocities are tolerable.

## 5. Mouth termination

A horn's mouth is an impedance mismatch from the horn's throat-area
characteristic impedance to free air's `ρ₀ c`. The mismatch reflects
some energy back into the horn, producing mouth-resonance ripples in
the response.

Minimum mouth area to avoid serious mouth reflection at cutoff:

```
A_mouth ≥ (λ_c / 2)² / π    (theoretical minimum)
A_mouth ≥ λ_c²              (engineering rule of thumb)
```

For a 100 Hz horn (`λ = 3.43 m`), `λ²` = 11.8 m². This is why
free-standing bass horns are huge — and why folded horns (Klipschorn,
Lowther, Voigt pipe) and corner-loading (using room walls as horn
extensions) became popular for domestic LF horns.

Mouth shape matters too:

- **Round (axisymmetric)** mouth radiates as a piston; smoothest
  pattern.
- **Square** mouth introduces small diffraction asymmetry; tolerable.
- **Rectangular** mouth (typical PA) creates asymmetric vertical
  vs. horizontal pattern, often desired.
- **Wedge / radial flare at mouth** softens the impedance transition,
  reducing reflection ripples by 2–4 dB.

## 6. Directivity control

The directivity of a horn at any frequency is dominated by which
limit applies:

- **Below diffraction limit** (`λ > mouth dimension`): horn loses
  pattern control; radiates near-omni from the mouth.
- **At the diffraction limit** (`λ ≈ mouth dimension`): narrowest
  pattern; some "flip-flop" lobes form.
- **Above diffraction limit** (`λ << mouth dimension`): pattern is
  set by **the walls of the horn**, not by mouth diffraction.

Constant-directivity (CD) design ensures the third regime kicks in
above the lowest design frequency. Typical CD horns achieve flat
beamwidth from ~`2 × f_c` to ~10 kHz. Pattern is set by the included
wall angle: a 60° × 40° horn has 60° horizontal beamwidth and 40°
vertical, regardless of frequency in band.

Beamwidth vs. frequency plot is the standard CD figure of merit. A
flat plot from `f_c` to 8 kHz means a CD horn is working as designed.

### Diffraction slot horns

A different approach (JBL Smart): use a narrow diffraction slot at
the throat that radiates with controlled pattern, then expand the
horn to size. The diffraction slot, not the horn walls, sets the
pattern.

Pros: very controlled pattern over wide band. Cons: HOM-prone, "horn
honk" character if not carefully designed.

## 7. Higher-order modes (HOM)

When the throat or mid-horn cross-section is larger than half a
wavelength, the plane-wave assumption fails and radial wave modes
propagate inside the horn. Each radial mode has its own propagation
velocity (slower than the plane wave above cutoff), producing time
smear and frequency-response ripples.

HOM are the dominant source of "horn coloration" — the harsh, papery,
nasal quality of bad horns. Mitigation:

- Smooth flare with no kinks (avoid section transitions in
  CNC-routed laminated horns).
- Low throat angle and gentle flare initiation.
- OS waveguide geometry specifically minimizes HOM excitation.
- Felt or foam at the throat entrance (kills HOM but kills HF too;
  trade-off).

## 8. Bass horns

LF horns are physically enormous because mouth size scales with
wavelength. Practical strategies:

- **Folded horn** (Klipschorn, La Scala, Voigt pipe): wrap the horn
  inside a cabinet. Lossy in the folds; useful 80–300 Hz.
- **Front-loaded horn (FLH)**: horn radiates the front of the driver;
  rear in a sealed/ported chamber. Most efficient.
- **Back-loaded horn (BLH)**: horn radiates the rear of the driver;
  driver front in free air or small box. Lower efficiency but
  smoother midbass.
- **Tapped horn (TH)**: both sides of the driver feed the same horn,
  one near the throat and one further along. Wide passband (~1.5
  octaves), very high efficiency. Popular in modern pro touring subs
  and cinema.
- **Corner loading**: use the room corner as a horn extension.
  Klipschorn was designed for corner placement; works only there.

## 9. Compression driver matching

A compression driver's natural rolloff (set by diaphragm mass and
suspension) and the horn's loading characteristic combine into the
system response. Two issues:

- **High-frequency**: diaphragm + voice-coil mass produces 6 dB/oct
  rolloff above the diaphragm's first breakup; horn loading
  contributes another 6 dB/oct above its `f_c` × few. Combined, the
  system can need a HF EQ shelf of 6–12 dB above 5 kHz.
- **Low-frequency**: passive electrical EQ (CD horn equalization
  network) is common — a series cap + parallel inductor circuit that
  boosts the LF end of the compression driver's pass band to match
  the horn's rising loading.

Modern active systems do this with DSP shelving filters.

## 10. Designing a horn

A reasonable workflow:

1. **Pick the target coverage pattern** — e.g. 90° × 40°, 60° × 60°.
   For a domestic stereo, 90°×40° is common; for a near-field studio,
   60°×60°; for a cinema sweep array, 100°×60° per box.

2. **Pick `f_c`** — typically half the desired crossover frequency.
   For a 1.5 kHz crossover, `f_c = 750 Hz`; for a 250 Hz midbass,
   `f_c = 125 Hz`.

3. **Pick the flare family**:
   - Want max LF loading per length → exponential.
   - Want best directivity control → conical or OS.
   - Want best time response → tractrix or Le Cléac'h.
   - Want all of the above → OS waveguide (Geddes).

4. **Size the mouth** for `A_mouth ≥ λ_c²` (full pattern control) or
   accept some loading rolloff for `A_mouth ≥ (λ_c/2)²/π`.

5. **Pick the throat geometry** to match your compression driver
   exit (1", 1.4", or 2") or your direct radiator's effective radius.

6. **Simulate in Hornresp / ATH4 / Akabak** before cutting wood:
   - Predict on-axis SPL with driver T/S parameters.
   - Predict directivity at 0°, 15°, 30°, 45° off-axis.
   - Check that passband ripple is < 3 dB at the design level.
   - Predict cone excursion at max SPL to verify the driver's
     limits.

7. **Build a prototype**: CNC-routed laminated MDF or plywood is
   standard; 3D printing handles tweeter waveguides up to ~150 mm
   throat-to-mouth. Verify with measurement and revise.

## 11. Modern tools

| Tool                    | Method / scope                            | Notes                          |
|-------------------------|-------------------------------------------|--------------------------------|
| Hornresp (David McBean) | 1D Webster + lumped, predicts SPL + Z     | free, Windows; the workhorse   |
| ATH4 (Mabat)            | Parametric horn generator (OSWG, JMLC, …) | free; outputs STL for printing |
| Akabak                  | Lumped + BEM hybrid                       | paid; assemblies & coupling    |
| ABEC                    | BEM acoustic solver                       | free; rigorous polar response  |
| COMSOL Acoustics        | FEM                                       | $$$$; research-grade           |
| Le Cléac'h spreadsheet  | Generates JMLC profile point cloud        | free                           |
| GuitarHornCalc          | Voigt/tapered pipe                        | niche, BLH design              |

For a DIY HF waveguide, the modern stack is **ATH4 → STL → 3D print**.
For midbass horns, **Hornresp → CNC plywood laminations**. Bass horns
are mostly Hornresp + Akabak + heavy carpentry.

## 12. Common pitfalls

- **Designing for theoretical cutoff, not practical loading frequency**
  — system unloads in the bottom octave of intended use. Design `f_c`
  ≤ ½ of the crossover frequency.
- **Mouth too small** — passband ripples and lost directivity at the
  low end. Build to `A ≥ λ_c²` if you can; accept `(λ_c/2)²/π` if you
  can't.
- **Sharp throat transition** — excites HOMs. Smooth from compression
  driver exit into horn throat with a fillet ≥ 5 mm.
- **Picking exponential because "it's the most efficient"** — without
  checking mouth termination. The mouth-reflection ripple often
  wastes the efficiency advantage.
- **Treating waveguide as just a small horn** — different design
  philosophy. Geddes-style waveguides aim at minimum HOM and constant
  directivity, not maximum loading.
- **Ignoring HOM in the throat-to-mouth transition** — smooth flare
  derivatives matter more than the precise profile equation.
- **Putting EQ before measurement** — most "horn coloration" is HOM
  and mouth diffraction, not frequency response; EQ can't fix them.
