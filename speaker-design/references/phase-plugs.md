# Phase Plugs

A phase plug is a physical structure between a transducer's
diaphragm and the air (or horn throat) it loads into, designed to
control **path-length differences** across the diaphragm so that
contributions from different cone/dome regions arrive in phase at a
common exit. Without one — or with a badly designed one — the high
end develops comb-filtering, narrow nulls, and rapid pattern
collapse.

Two distinct applications:

1. **Compression drivers** — phase plug sits behind the diaphragm,
   inside the compression chamber, equalizing path lengths to the
   horn throat.
2. **Cone drivers (coaxial, full-range, midbass)** — phase plug
   replaces or augments the dust cap, controlling the cone's
   own radiation pattern at HF.

## 1. The path-length problem

A flat or domed diaphragm has finite area. If radiation from the
**edge** of the diaphragm takes a longer path to the listener than
radiation from the **center**, the two arrive out of phase at high
frequencies. For a 25 mm dome:

```
Δd (edge vs center) ≈ a − a·cos(θ)
                    = 12.5 mm − 12.5·cos(half-dome) ≈ 4 mm

f_null,1 = c / (2 · Δd) ≈ 43 kHz   (for 4 mm)
```

So a bare 25 mm dome sees its first cancellation around 43 kHz, well
above the audible band — no phase plug needed. But for a **50 mm
compression driver diaphragm** (typical for 1" exit), Δd grows to ~12
mm and the first null lands around 14 kHz — squarely audible. Hence
the phase plug.

For an 8" cone driver radiating up to ~3 kHz on its own, Δd from
center to surround is ~50 mm, giving the first axial null around
3.4 kHz — exactly where cone breakup is. A phase plug on the dust
cap can push this transition higher or smooth it out.

## 2. Compression driver phase plugs

The compression chamber is the small volume between the diaphragm
and the phase plug face. The plug body contains **slits or channels**
that route the radiated sound through equal-length paths to the
throat exit.

### Slit / channel topologies

**Radial slits** (Western Electric 555, Altec, JBL 2440 derivatives):
straight radial channels from outer edge to center, all the same
length within manufacturing tolerance. Simple to machine; adequate
to ~12 kHz with a 2" exit driver.

**Annular slits** (B&C, Faital, BMS): concentric circular slits at
matched radii, each communicating with the throat through equal-
length back channels. More slits = better phase matching; modern
drivers use 3-5 annular slits.

**Helical / spiral** (TAD TD-4001): single continuous spiral
channel. Excellent path-length equalization at the cost of complex
machining.

**Eccentric multi-port** (BMS coaxial compression drivers): separate
phase plug regions for HF and midrange diaphragms, sharing one
throat. Allows a 2-way compression driver from a single chassis.

### Equivalent transmission-line model

Each channel is a short acoustic transmission line:

```
Z_ch(f) = (ρ₀ c / S_ch) · tan(k L_ch + φ_end)
```

where `S_ch` is the channel cross-section, `L_ch` is its length, `k =
ω/c`. Channels combine in **parallel at the throat**. For the result
to be phase-coherent, every channel must have the same `L_ch` —
this is the design constraint.

A useful sanity check: at the highest frequency of intended use,
the **largest difference** between channel lengths should be < λ/8.
For a 16 kHz upper limit: λ = 21 mm; max ΔL = 2.6 mm. Mass-production
compression drivers hold this within ±0.5 mm.

### Compression ratio at the phase plug

The phase plug also performs the **area transition** from the
diaphragm to the throat:

```
CR = S_d / S_t = 5:1 to 10:1 (typical)
```

The channels' aggregate area at the diaphragm-facing end is roughly
`S_d / CR` (matching the throat); they expand or contract from there
according to the chosen profile. Channels narrowing as they
approach the throat is the most common pattern; helps maintain plane-
wave behavior all the way to the exit.

### What goes wrong

- **Path-length mismatch** → high-frequency response shows narrow
  nulls; on-axis pattern dives at specific frequencies.
- **Sharp internal corners** → higher-order acoustic modes (HOMs)
  generated; ripples in response above ~3 kHz; nasal "horn honk"
  character.
- **Diaphragm-to-plug gap too small** → diaphragm contacts plug at
  high excursion (rare in compression drivers, but possible).
- **Diaphragm-to-plug gap too large** → useful diaphragm area in
  the compression chamber is reduced; efficiency drops, distortion
  rises (excessive cone velocity in the chamber).

The diaphragm-to-plug gap is typically 0.3–0.5 mm. Production
drivers ship within ±0.1 mm; the spec is critical for distortion and
HF extension.

## 3. Cone driver phase plugs

A phase plug replaces the dust cap on a cone driver. Two
purposes:

1. **Eliminate the cone's central null** — the cone radiates from a
   ring, not a center; a stationary plug projects a smaller
   effective radiator at the center, improving on-axis HF response.
2. **Modify HF radiation pattern** — a tapered plug acts as a small
   waveguide for the very top of the driver's range, controlling
   off-axis behavior.

### Bullet (cone-pointed) phase plugs

The simplest design: a tapered cone (often aluminum or brass) at the
center of the woofer, stationary, attached to the pole piece. The
cone radiates around it; the plug surface itself contributes
nothing acoustically.

- Modest improvement (1–2 dB at 5 kHz on a 6.5" driver).
- Aesthetics: prized in full-range and vintage designs.
- Thermal: pole-piece-mounted aluminum plug dumps heat from the
  pole, lowering voice-coil temperature rise.

### Tangerine / segmented phase plugs (KEF Uni-Q lineage)

Segmented profile with circumferential ridges; alternates protruding
ridges with troughs. Each ring acts as a small ring-radiator at
slightly offset radii, breaking up the strong on-axis cancellation
of a bare-cone driver.

- KEF Uni-Q tweeters use a tangerine plug as both diffuser for the
  midrange (which radiates through the woofer cone) and as a small
  waveguide for the tweeter.
- Improves on-axis HF balance by 3–5 dB; smooths off-axis transition
  by ~2 dB.

### Coaxial concentric drivers

Tweeter mounted **inside** the hole through the woofer's pole piece,
with a phase plug that doubles as the tweeter's waveguide and the
woofer's dust-cap replacement.

- Acoustic center of HF and LF is coincident → near-true point source.
- The woofer cone, however, acts as a horn for the tweeter — its
  geometry colors the HF radiation pattern.
- Doppler modulation: woofer excursion at LF moves the tweeter
  axially. Audible above ~5 mm cone displacement during high
  bass+treble passages.

Modern coaxial designs (KEF Uni-Q latest generation, Tannoy Dual
Concentric Mark VI+, SEAS T-series) carefully shape the phase plug
to control both effects.

## 4. Phase-plug design rules of thumb

For DIY cone driver phase plugs (compression-driver phase plugs are
not realistically DIY — leave them to the manufacturer):

1. **Match plug height to cone neck depth** — protruding plug
   shouldn't extend much past the front of the cone, else it
   becomes a separate scatterer.
2. **Tapered or domed profile preferred** — sharp cones create
   diffraction.
3. **Plug diameter ≈ 0.25 × cone diameter** for the most pronounced
   effect.
4. **Don't seal the dust-cap area** if the driver was designed with a
   ventilated pole — that ventilation is part of the motor's thermal
   path.
5. **Mount rigidly to the pole piece**, not to the cone. A
   cone-mounted plug moves with the diaphragm and behaves like
   added moving mass (worse on-axis response, lower Fs).

### Materials

- Aluminum: light, conducts heat, easy to machine. The default.
- Brass: heavy but pretty; can dampen the plug's own vibrations.
- Plastic / 3D-printed: cheap, easy to prototype; check thermal
  stability above the driver's operating temperature.

## 5. Higher-order modes (HOMs)

Once the diaphragm-to-throat path exceeds about half a wavelength in
any transverse direction, radial modes propagate inside the phase
plug structure. Each mode has its own velocity and decay, smearing
the time response and adding response ripples.

HOM symptoms:
- Ripples 1–3 dB across 2–8 kHz that don't correspond to driver
  resonance.
- "Horn coloration" / nasal character (the classical PA-horn sound).
- Worse on-axis than off-axis (off-axis attenuation lowers HOM
  contribution faster than direct).

HOM mitigation:
- More channels (smaller transverse dimension).
- Smooth derivative of channel cross-section (no kinks).
- Oblate-spheroidal waveguide geometry minimizes HOM excitation —
  but that's a waveguide topic, see `horns-and-waveguides.md`.

## 6. Modern design tools

Compression driver phase plugs are designed in COMSOL Acoustics or
similar FEM packages, with iterative loops:

1. Generate candidate phase plug geometry (CAD).
2. Compute throat impedance and on-axis SPL vs frequency.
3. Compute polar response.
4. Optimize geometry parameters for flat response + minimum
   distortion.

For cone drivers, simpler 1D Webster-equation calculations + a
diffraction sim are adequate. The cone-plus-plug system can be
modeled as a piston with a non-uniform radiation impedance, fitted
to measured response.

## 7. Practical implications

- **Don't replace** a manufacturer's compression-driver phase plug.
  The compression chamber, plug, and diaphragm are co-optimized at
  fractions of a millimeter; any swap will degrade performance.
- **Do experiment** with bullet phase plugs on cone drivers — they're
  bolt-on and reversible. Measure before/after; expect modest gains.
- **Tangerine plugs** in DIY full-range drivers are tractable to
  3D-print and test. Iterate by measurement.
- **In coaxial designs**, the phase plug is half the design; never
  treat it as a passive component.

## Cross-references

- `references/horns-and-waveguides.md` — compression drivers feed
  horns; phase plug + horn co-design.
- `references/driver-types.md` — coaxial and full-range driver
  topologies.
- `references/closed-box-geometry.md` — driver mounting and dust-cap
  context.
- `references/measurement.md` — verifying phase-plug behavior with
  on-axis and polar sweeps.
