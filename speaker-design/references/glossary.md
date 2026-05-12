# Glossary

Terms used throughout this skill, in one place. Brief definitions
with cross-references to deeper treatment.

## A

**Aperiodic enclosure** — A "between sealed and ported" alignment
where a heavily damped vent replaces a tuned port. See
`enclosures.md`.

**Acoustic center** — The point from which a speaker's radiation
appears to emanate, often offset from the geometric center.
Relevant for time alignment. See
`point-source-and-line-arrays.md`.

**Acoustic impedance** — Pressure / volume velocity ratio.
`Z_ac = p/U`. Different from specific acoustic impedance
(`Z_s = p/u`, particle velocity). See `physics-of-sound.md`.

**Acoustic suspension** — Air-spring-dominated sealed alignment (`α
= Vas/Vb > 3`). The trapped air provides most of the cone's
restoring force.

**Active speaker** — Amplifier(s) and crossover inside the cabinet,
typically with DSP. See `dsp-and-active.md`.

**Allison effect** — Acoustic dip at the frequency where floor or
wall reflection cancels direct sound. Same as SBIR.

**AMT (Air Motion Transformer)** — Pleated-diaphragm tweeter
(Heil). See `driver-types.md`.

**Anechoic** — Room with no reflections. The reference environment
for speaker frequency-response specs.

## B

**B&K curve** — In-room target similar to Harman/Olive, derived from
Brüel & Kjær listening-room research.

**B4 (Butterworth 4th order)** — Standard ported alignment. Maximally
flat frequency response in the bass. See `enclosures.md`.

**Baffle step** — Transition from half-space to full-space loading
as frequency rises through `f ≈ 115/W` (W in m). See
`baffle-and-cabinet-acoustics.md`.

**Bandpass enclosure** — Driver between two chambers; radiates only
through ports. 4th- or 6th-order. See `enclosures.md`.

**Beamwidth** — Angular width within which response is -6 dB or less
from on-axis. See `acoustic-properties.md`.

**Bending wave** — A diaphragm flexing in modes rather than acting
as a piston. NXT, Manger, Tectonic.

**Bessel** — Filter type with maximally flat group delay. Bessel-
aligned sealed has `Q_tc = 0.577`.

**BL** — Motor force factor (T·m or N/A). Force on the cone for a
given current; or equivalently, back-EMF for a given velocity. See
`thiele-small.md`.

**Break-in** — Initial mechanical "loosening" of a driver's
suspension. Small, settling within ~24 hours of use.

**Breakup** — Cone or diaphragm modal flexure. Visible as response
peaks; see `materials.md`.

**Butterworth** — Filter family with maximally flat amplitude. B2
(`Q = 0.707`) for sealed, B4 for ported.

**BSC (Baffle Step Compensation)** — EQ shelf or filter to
compensate for the +6 dB step. See `crossovers.md`.

## C

**CD (Constant Directivity)** — Speaker design where radiation
pattern doesn't change with frequency over the working band.

**Cabin gain** — Pressure rise inside a small (≈vehicle-sized) room
below its lowest mode. Related to room gain.

**CBT (Constant Beamwidth Transducer)** — Don Keele's circular-arc
array with cosine amplitude weighting. See
`point-source-and-line-arrays.md`.

**CEA-2034 / CTA-2034-A** — Standard for 70-measurement spinorama
loudspeaker characterization. See `standards-and-targets.md`.

**Chebyshev** — Filter family with ripple. C4 ported alignment trades
ripple for extension.

**Compliance** — Inverse of stiffness. `C_ms` (mechanical) and `V_as`
(acoustic equivalent). See `thiele-small.md`.

**Compression driver** — HF transducer with diaphragm compressing
sound through a phasing plug into a horn throat. See
`driver-types.md`.

**Coincident** — Two transducers radiating from approximately the
same acoustic center. Coaxial = a coincident design.

**Coil former** — The bobbin the voice-coil wire winds around.
Kapton, fiberglass, aluminum, titanium. See `materials.md`.

**Cone breakup** — Cone vibrating in non-piston modes. See
`materials.md`.

**Cooling** — Voice-coil thermal management. Powerful drivers use
vented motors, ferrofluid, or pole-piece heat sinks.

**Crossover** — Filter network splitting signal among drivers.
Passive (after the amp) or active (before per-driver amps). See
`crossovers.md`.

## D

**dB SPL** — Sound Pressure Level in decibels.
`20·log₁₀(p_rms / 20 µPa)`.

**dBA, dBC** — A-weighted, C-weighted SPL.

**Diffraction** — Wave bending around an obstacle smaller than λ.
Source of baffle step ripples. See
`baffle-and-cabinet-acoustics.md`.

**Diffuser** — Surface that scatters specular reflections (Schroeder
QRD, PRD, skyline). See `acoustic-treatment.md`.

**Dipole** — Open-baffle radiation; front and rear of cone radiate
out of phase. Figure-8 pattern.

**Directivity Index (DI)** — On-axis SPL minus spatial-average
(power) SPL, in dB. See `acoustic-properties.md`.

**DOSC** — L-Acoustics' wavefront-sculpting technology for line
arrays. Patent expired ~2018.

**Doppler distortion** — Modulation of HF by LF cone motion in a
single driver covering both. ~0.1 % per mm of LF excursion at HF.

## E

**EBP (Efficiency Bandwidth Product)** — `Fs / Qes`. Predicts
whether a driver suits sealed (low) or ported (high). Rule: EBP
< 50 → sealed; > 100 → ported; in between → either.

**EBS (Extended Bass Shelf)** — Oversized ported box that trades
sensitivity near tuning for extra extension.

**Edge diffraction** — Cabinet-edge wave re-radiation creating comb
filtering. See `baffle-and-cabinet-acoustics.md`.

**Electrostatic (ESL)** — Mylar diaphragm in electrostatic field
between perforated stators. See `driver-types.md`.

**Excursion** — Cone displacement. Xmax is the linear limit, Xmech
the absolute limit. See `thiele-small.md`.

## F

**Fb** — Tuning frequency of a ported box (the port + cabinet
Helmholtz resonance).

**Fc** — Resonance frequency of a sealed driver in a closed box.
`F_c = F_s · √(1 + V_as/V_b)`.

**FEM (Finite Element Method)** — Numerical method to solve the wave
equation in arbitrary geometry. See `room-response-simulation.md`.

**FFT** — Fast Fourier Transform; the workhorse of audio
measurement.

**FIR / IIR filter** — Finite/Infinite Impulse Response. FIR has
linear phase but latency; IIR is minimum phase but compact. See
`dsp-and-active.md`.

**First-reflection point** — Wall or floor location where the first
specular reflection of direct sound originates. Located by the
mirror trick.

**Flow resistivity** — Pressure-per-thickness needed to push air at
a given velocity through a porous material. Determines absorber
performance. See `acoustic-treatment.md`.

**Force cancellation** — Mounting two identical drivers facing
opposite directions in one cabinet so reaction forces cancel.

**Free air** — Driver mounted with no enclosure (in a stand or on a
large IEC baffle). The condition T/S parameters refer to.

**Fs** — Driver free-air resonance frequency.

## G

**Gain (acoustic)** — Increase in SPL from one configuration to
another. Boundary loading gain, horn gain, room gain.

**Group delay** — `τ_g = -dφ/dω`; the envelope delay of a
narrowband signal. Audibility threshold ~1.5 cycles.

## H

**Harman target** — Olive's preferred in-room curve. See
`standards-and-targets.md`.

**Helmholtz resonator** — Cavity-and-port acoustic resonator.
Forms a ported speaker's tuning, or a tuned-trap room treatment.

**HOM (Higher-Order Modes)** — Non-plane-wave acoustic modes
inside a duct, horn, or phase plug. Source of "horn coloration."

**Horn cutoff** — Frequency `f_c = m·c/(4π)` for exponential horns
below which the horn ceases to load. See
`horns-and-waveguides.md`.

## I

**Impedance** — Electrical: `Z(f) = V/I`. Acoustic: `Z = p/U`. See
the relevant references.

**Impulse response** — Time-domain output of a system to a δ(t)
input. Source of FR (via FFT), step response, energy decay.

**In-phase / out-of-phase** — Signals aligned (0° offset) or
inverted (180° offset).

**Isobaric** — Two drivers in series sharing a chamber; doubles
effective Vas, allowing half the cabinet.

**ITD / ILD** — Interaural Time / Level Difference. The cues used by
the ear for horizontal localization.

## K

**Klippel** — German company / large-signal analyzer name. The
gold standard for nonlinear driver characterization.

**Kerf** — Width of material removed by a cutting tool (laser, saw,
router). See `parametric-cad/references/manufacturability.md`.

## L

**LEDE (Live End Dead End)** — Studio room layout: absorbent at the
speaker end, reflective/diffuse at the listener end.

**Le** — Voice-coil inductance.

**Line array** — Vertical column of drivers behaving as a cylindrical
source.

**Linkwitz transform** — Biquad that shifts a sealed driver's
natural rolloff to a new target. Adds nothing to group delay.

**LR2 / LR4** — Linkwitz-Riley 2nd / 4th order crossover. The
standard acoustic targets.

**LUFS** — Loudness Units Full Scale (BS.1770). Modern broadcast
loudness standard.

## M

**MDF (Medium Density Fiberboard)** — Wood-fiber engineered panel.
Default cabinet stock for DIY.

**Mms** — Driver moving mass (cone + coil + air load).

**Modal density** — Number of acoustic modes per unit frequency in
a room. Rises with `f²` for 3D space.

**Moving-coil** — The default loudspeaker transducer type: coil in
magnet gap, glued to cone/dome.

## N

**Nearfield** — Within ~`Sd/λ` of the source. Used for low-room-
contamination measurement of LF.

**Neodymium / Ferrite / Alnico** — Magnet materials. Strongest /
cheapest / most thermally stable, respectively.

**Notch filter** — Narrow-band band-stop filter. Used to kill cone-
breakup peaks. See `crossovers.md`.

## O

**Open baffle** — Driver on a flat baffle with no enclosure;
naturally dipole.

**OS waveguide** — Earl Geddes' oblate-spheroidal waveguide. Low HOM,
constant directivity.

## P

**Passive radiator** — Replacement for a port: a moving cone with no
motor, tuned by its mass.

**Phase plug** — Structure between diaphragm and air/throat that
equalizes path lengths. See `phase-plugs.md`.

**Polar response** — SPL vs angle, plotted at each frequency.

**Ported / vented / bass-reflex** — Synonyms for Helmholtz-tuned
enclosure with a port.

**Power compression** — SPL output falling below linear-extrapolated
input due to voice-coil heating.

**Precedence effect** — Ear locks an image to the earliest-
arriving sound within ~10 ms. Foundation of stereo imaging.

## Q

**Q (quality factor)** — Sharpness of a resonance, `Q = f_0 / Δf`.
The dimensionless damping factor.

- `Qes` — Electrical Q at Fs.
- `Qms` — Mechanical Q at Fs.
- `Qts` — Total Q at Fs (driver alone).
- `Qtc` — Total Q at Fc (driver in sealed box).
- `Q_filter` — Q of an electrical filter.

## R

**Re** — Voice-coil DC resistance.

**Reverberation time (T_60)** — Time for SPL to fall 60 dB after
the source stops.

**RFZ (Reflection-Free Zone)** — Listening area free of early
reflections within 15–20 ms of direct.

**Room gain** — Pressure boost below the room's lowest mode,
~12 dB/octave indoors.

## S

**Sd** — Effective cone radiating area, m².

**Sealed (closed box)** — Enclosure with no port; 12 dB/oct rolloff.

**Sensitivity** — SPL at 1 m for 2.83 V input; not the same as
efficiency.

**Schroeder frequency** — `f_S = 2000 · √(T_60 / V)`. Boundary between
modal LF and statistical HF in a room.

**Schroeder QRD diffuser** — Quadratic-residue-sequence diffuser
with mathematically optimized scattering.

**SBIR (Speaker-Boundary Interference Response)** — Comb-filter
pattern from speaker-to-wall reflection back to the speaker.

**Sound power** — Total acoustic power radiated, summed over all
angles. The "in-room average" indicator.

**Spinorama** — CEA/CTA-2034 70-measurement scheme.

**Spider** — Inner suspension of a driver (corrugated cloth).

**SPL** — Sound Pressure Level (in dB).

## T

**T/S (Thiele/Small)** — The small-signal parameter set for
moving-coil drivers. See `thiele-small.md`.

**Tractrix** — Horn flare profile preserving spherical wavefront
inside the horn.

**Transmission line (TL)** — Long, damped acoustic line behind the
driver. See `enclosures.md`.

**THD** — Total Harmonic Distortion.

**Time alignment** — Adjustment of per-driver delay so acoustic
arrivals at the listener are simultaneous.

## V

**Vas** — Equivalent compliance volume of a driver. The air volume
whose stiffness matches the driver suspension stiffness.

**Vb** — Net internal volume of the speaker enclosure.

**Voice coil** — Coil of wire in the magnet gap; the "motor" of a
moving-coil driver.

## W

**Waveguide** — Horn-like structure emphasizing directivity control
over loading.

**Wavelength** — `λ = c / f`. 17 m at 20 Hz; 17 mm at 20 kHz.

**Welti** — Todd Welti, primary author of multi-sub placement
papers (JAES 2003).

## X

**Xmax** — Linear excursion limit (typically 10 % BL or Kms drop).

**Xmech** — Mechanical excursion limit (the driver bottoms out).

## Z

**Z (impedance)** — See "Impedance" above.

**Zobel network** — Series RC across a driver to flatten its rising
inductive impedance for crossover design.

---

**See also**: `bibliography.md` for the original papers behind these
terms.
