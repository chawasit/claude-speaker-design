# Driver Types

The Thiele/Small framework and most of this skill assume a moving-coil
dynamic driver. That covers ~95 % of speakers but not all. This file
catalogs the major transducer topologies, their physics, and what they
are good at.

## Moving-coil dynamic

The default. Voice coil in a permanent-magnet gap, glued to a cone or
dome that radiates. Linear over a wide bandwidth, high power handling,
cheap, well-understood.

- **Cone drivers** (woofer, midrange): paper/poly/metal/composite cone
  with surround and spider. Optimal range: ~30 Hz – 4 kHz depending on
  size. See `materials.md` for cone trade-offs.
- **Dome tweeters**: 1" or 25 mm convex diaphragm (silk, aluminum,
  beryllium, ceramic, diamond). Optimal range: 1.5 kHz – 30 kHz.
- **Cone tweeters**: small (≤2") paper cones; common in vintage and
  pro PA two-ways. Better off-axis at the top than domes due to
  smaller effective radiating area.
- **Subwoofers**: 8"–21" overhung-coil cones with massive motors.
  Excursion-limited, not breakup-limited. See `subwoofers.md`.

Strengths: linear, high power, well-modeled, inexpensive, easy to
match. Weaknesses: low efficiency (0.1–1 %), cone breakup at HF,
limited displacement.

## Compression driver + horn

A small diaphragm (titanium, polyester, beryllium, aluminum) drives a
small chamber through a phasing plug into a horn throat. Geometry:

```
diaphragm → phasing plug → throat (typically 1" or 1.4") → horn
```

The compression ratio (diaphragm area / throat area, ~5–10:1) raises
acoustic impedance toward `ρ₀ c`, drastically increasing efficiency.

- **Frequency range**: 500 Hz – 18 kHz, depending on diaphragm size.
- **Sensitivity**: 105–115 dB SPL/W/m. Decades higher than direct
  radiators.
- **Distortion**: very low above ~1 kHz at moderate drive; very high
  at the cutoff (air nonlinearity in the throat).
- **Crossover**: typically at 2× the horn's flare cutoff, never below.

Trade-offs: pattern is set by the horn flare; honkiness from internal
reflections; large size for low cutoffs; can't reproduce true high
top-end without supertweeter assist (1" diaphragms roll off above
~16 kHz).

## Ribbon tweeter

A corrugated metal foil (aluminum, ~5 µm) suspended in a magnetic gap,
carrying current end-to-end. The foil itself is the conductor, the
diaphragm, and the entire moving mass.

- **Pros**: vanishingly low moving mass → response to >40 kHz; minimal
  ringing; horizontal dispersion excellent (foil width sets ka).
- **Cons**: extremely low impedance (~0.1 Ω) needs a transformer;
  low sensitivity unless horn-loaded; cannot cross below ~3 kHz
  (foil tears under air load); fragile to physical contact and dust.

True ribbons (no diaphragm membrane) are open-baffle by nature — both
sides radiate. Most "ribbons" in consumer products are pseudo-ribbons:
a printed conductor on a Kapton or Mylar substrate (planar magnetic;
see below).

## Air Motion Transformer (AMT / Heil)

Pleated diaphragm in a transverse magnetic field. Current flowing in
the pleat conductors pushes adjacent pleats together and apart, like
a squeezing accordion. Result: diaphragm velocity is ~5× the velocity
of any single fold — high acoustic velocity from low foil velocity.

- **Range**: 800 Hz – 30 kHz, can cross lower than most domes.
- **Sensitivity**: ~94–96 dB SPL/W/m.
- **Power handling**: high, since the foil itself dissipates heat
  across a large area.
- **Dispersion**: narrow vertically (tall pleats), wide horizontally.

AMTs feel "fast" and "clean" because of low ringing and low mass.
Modern designs (Mundorf, ESS) are robust and cost-effective.

## Planar magnetic / printed-trace

A thin Mylar/Kapton film with a printed serpentine conductor, suspended
between two arrays of bar magnets. Like a flattened ribbon, but with
its own membrane and a much higher impedance (4–8 Ω, no transformer).

- **Range**: 200 Hz – 25 kHz depending on size.
- **Headphones**: most premium open-back headphones (HiFiMan, Audeze,
  Dan Clark) are planar magnetic — the form factor scales perfectly.
- **Speakers**: large panels (Magnepan) act as line sources at LF and
  dipoles overall, producing huge soundstages but poor room
  integration and modest max SPL.

## Electrostatic (ESL)

A thin, conductive Mylar diaphragm (~10 µm) charged to several
kilovolts DC, suspended between two perforated stators. Audio voltage
on the stators (1–10 kV peak) creates electrostatic force across the
gap.

- **Pros**: lowest-distortion diaphragm in audio (no breakup,
  pistonic over full range); extremely low moving mass; full-range
  ESLs cover 50 Hz – 20 kHz.
- **Cons**: needs step-up transformer (1:50 to 1:150); dipole
  radiation (big sweet spot, poor LF in small rooms); high impedance
  at LF, very low impedance at HF (a 1:1 transform of a capacitor —
  most amps struggle); requires AC mains for the bias supply; can
  arc in humid environments.

Notable: Quad ESL-57, Martin Logan hybrid (ESL panel + dynamic woofer),
KingSound, Sanders.

## Bending-wave / distributed-mode (NXT, Tectonic, Manger)

Instead of trying to keep the diaphragm pistonic, drive it
deliberately into bending modes that produce a statistically
distributed wavefront. The Manger MSW uses a flat disc damped at the
rim to absorb bending waves once they've radiated, avoiding standing
waves.

- **Pros**: dispersion almost omnidirectional; impulse-like time
  domain (Manger).
- **Cons**: irregular frequency response, low sensitivity, hard to
  integrate with conventional drivers.
- Used in: laptop speakers (NXT licensees), public address with
  controlled coverage (Tectonic BMR), niche high-end (Manger).

## Whizzer cones and full-range

A small auxiliary cone attached to the voice-coil former or dust cap of
a larger cone. The whizzer takes over above the main cone's breakup
frequency, decoupling its mass via the surround glue compliance.

Typical full-range driver: 4"–8" main cone + whizzer covering up to
~16 kHz. Used in single-driver designs (Lowther, Fostex, Mark Audio).

- **Pros**: no crossover, time-coherent, simple.
- **Cons**: limited SPL, rough on-axis response, narrow polar pattern
  at HF, modest bass without horn loading.

## Coaxial / concentric

Two drivers sharing one axis: tweeter mounted inside a hole through
the woofer's pole piece, or on a phase plug at the center of the cone.

- **Pros**: point-source behavior, identical horizontal and vertical
  polar response, eliminates lobing in crossover region.
- **Cons**: tweeter sees the woofer cone as a horn (Doppler modulation,
  midrange honk); woofer cone vibration moves the tweeter (IMD); both
  drivers compete for motor real estate.
- Notable: KEF Uni-Q, Tannoy Dual Concentric, Genelec coax, Cabasse,
  Seas T-series.

## Open baffle (dipole)

A driver mounted on a flat or open-back baffle with no enclosure. Both
sides radiate; rear wave is out of phase with the front. Below the
baffle's effective half-wavelength cutoff, the two waves partially
cancel; output rolls off 6 dB/oct relative to closed-baffle response.

- **Pros**: no enclosure resonances; rear radiation excites the room
  diffusely (spacious sound); zero cabinet diffraction.
- **Cons**: requires huge drivers + EQ + lots of amp power to reach
  reasonable LF; figure-8 polar means sidewall first-reflection is
  null (a feature, not a bug, if you place correctly); ≥1 m clearance
  from rear wall.
- See Linkwitz's LX521 / Pluto for canonical open-baffle dipole and
  cardioid designs.

## Selecting a driver type per role

| Frequency      | Default                              | Premium                                 |
|----------------|--------------------------------------|------------------------------------------|
| 20–80 Hz       | 10–18" dynamic in sealed/ported sub  | dual opposed force-cancel; servo         |
| 80–500 Hz      | 6.5–10" dynamic woofer in box        | midbass coupler; isobaric                |
| 500 Hz–3 kHz   | 4–6.5" dynamic midrange              | compression driver in horn; full-range   |
| 3–12 kHz       | 1" soft/metal dome tweeter           | beryllium/diamond dome; AMT; ribbon      |
| 12–25 kHz      | covered by above                     | dedicated supertweeter (ribbon, AMT)     |

## Mixing types in one speaker

The headache is matching directivity across the crossover. A 1" dome
hands off to a 6.5" cone naturally because both are nearly omni up to
their working bands. A 90×40° horn handing off to a 6.5" cone has a
mismatch around the crossover — the cone is widening (omni at 1 kHz)
while the horn is narrowing (controlled at ~1 kHz). Common solutions:

- Choose a smaller cone (e.g. 4" or 5") that beams sooner so its
  directivity at fc matches the horn.
- Use a waveguide on the dome/tweeter to narrow its dispersion to
  match the woofer.
- Cross higher so the cone is beaming where the horn loses pattern
  control.

Constant-directivity through crossover ≈ smooth in-room timbre.
Directivity discontinuities ≈ characteristic "monitor sound."
