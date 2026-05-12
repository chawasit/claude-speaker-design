# Baffle and Cabinet Acoustics

The box around a driver is not acoustically neutral. Two effects
dominate audibility in the 200 Hz – 3 kHz region where the ear is most
sensitive:

1. **Baffle step and edge diffraction** — what the front baffle does
   to radiated sound, on and off axis.
2. **In-cabinet resonance** — what the enclosed air and the panels
   themselves do, coupling back through the cone and through the
   walls.

Get these right and a mediocre driver sounds good. Get them wrong and
the best driver in the world sounds like a clock radio.

## 1. Baffle step

A driver on an infinite baffle radiates into a half-space ("2π
loading"). A driver in free air, or on a baffle small compared to the
wavelength, radiates into the full space ("4π loading"). The
transition between the two is the **baffle step**: an upward shelf of
~6 dB as frequency rises through `f_bs` where the wavelength becomes
comparable to the baffle width.

Approximate center frequency for a flat rectangular baffle of width W:

```
f_bs ≈ 115 / W   (Hz, W in meters)
      ≈ 4500 / W (Hz, W in inches)
```

So a typical 200 mm (8") bookshelf baffle has its step centered around
575 Hz. The full transition spans roughly ±1.5 octaves around `f_bs`.

**Why it matters**: take a driver with a flat anechoic response on a
baffle. Listen far-field in a room (≥2 m): the response will appear
to droop 4–6 dB below `f_bs` relative to above it. Listen nearfield
or wall-mount it and the step disappears (because near a wall, the
baffle is effectively continuous with the wall — restored 2π loading).

### Off-axis variation

The baffle step is partly a directivity effect, partly a diffraction
effect. The two-step picture (half-space below `f_bs`, full-space
above) is exactly correct only on-axis. Off-axis, the geometry of the
edges relative to the driver changes the cancellation pattern:

- 30° horizontal off-axis: the step shifts down ~10 % in frequency
  and develops a 1–2 dB ripple from the now-asymmetric edge distances.
- Below the baffle (cabinet on a stand, listener looking down): the
  shelf is shallower because the floor restores partial 2π loading.

This is why measurements at one angle are misleading and full polar
sweeps matter.

### Baffle step compensation (BSC)

The fix depends on where the speaker lives:

| Placement                    | Compensation needed              |
|------------------------------|----------------------------------|
| Free-standing, room center   | Full BSC: −3 to −6 dB shelf above `f_bs` |
| ≤30 cm from rear wall        | Half BSC: −3 dB shelf            |
| Wall-mounted (in-wall)       | None (the wall is the baffle)    |
| Corner-loaded subwoofer      | None (corner = 1/8 space)        |

Passive BSC: a series inductor + parallel resistor across the woofer
input. Sizing:

```
L_bsc ≈ R / (2 π · f_bs)
R_par ≈ R · 10^(−A/20) / (1 − 10^(−A/20))    (A = dB step)
```

In active/DSP designs, BSC is a low-shelf EQ — much cheaper, easier
to tweak after listening.

## 2. Edge diffraction

Every cabinet edge re-radiates a delayed copy of the driver's wave.
The interference between the direct wavefront and these edge waves
produces a comb-filter pattern in the on-axis response.

Path difference from driver to edge and back to a far-field
microphone is approximately:

```
Δd ≈ d_edge − d_direct ≈ d_edge   (far field)
```

For a driver at the center of a 200 mm wide baffle, `d_edge = 100 mm`.
First cancellation at frequency where `2·d_edge = λ/2`:

```
f_null,1 ≈ c / (4 · d_edge)   = 343 / (4·0.1) ≈ 860 Hz
f_peak,1 ≈ c / (2 · d_edge)   ≈ 1720 Hz
```

The classic **Olson (1969) curves** measured this directly for stock
shapes. Severity ranking (worst to best):

1. **Cube with driver on one face** — 6+ dB ripples through midrange.
2. **Rectangular box with sharp corners** — 3–6 dB ripples.
3. **Cube with rounded corners** — 2–4 dB ripples.
4. **Cylinder** — 1–2 dB ripples, smooth.
5. **Sphere** — <1 dB ripple; the theoretical optimum.

### Mitigation strategies

**Driver offset on baffle**: place the tweeter asymmetrically (e.g.
30 mm left of centerline, 80 mm down from top). Each edge now has a
different distance to the driver, so each contributes a comb at a
different frequency. The sum is smoother by 2–4 dB. Use a "1.0 : 0.6 :
0.4" or Pythagorean-derived ratio of distances; avoid equal distances
to any two edges.

**Rounded edges**: a roundover of radius ≥ 20 mm (ideally 25–40 mm)
turns the sharp edge into a continuous curve, reducing edge wave
amplitude. Spheres are the limit; full 25 mm roundovers on a normal
box get you 80 % of the way there.

**Felt or foam strips** around the tweeter, ~10 mm thick × 30 mm wide,
absorb the wave before it reaches the edge. Particularly effective
above 2 kHz where felt becomes a good absorber.

**Waveguide loading**: a waveguide on the tweeter narrows its
radiation pattern at the bottom of its band; the energy that would
have diffracted off the cabinet edges is simply not radiated to those
angles. The waveguide itself becomes the diffraction-relevant
geometry, and its smooth flare is much better than a hard cabinet
edge.

**Bevels (chamfers)** are intermediate between sharp and rounded —
better than sharp, not as good as a full roundover, but easier to
cut. A 45° chamfer of depth ≥ ¼ wavelength at the highest frequency
of concern is the rule of thumb.

### Diffraction simulation

Software tools (Edge by Tolvan Data, VituixCAD's diffraction sim,
Akabak) accept baffle outline + driver positions and compute the
diffraction-modified frequency response and polar pattern. Run this
before cutting wood — moving the tweeter 20 mm can save 3 dB of
midrange ripple.

## 3. In-cabinet acoustic resonance (internal standing waves)

The air inside the cabinet supports its own standing-wave modes,
just like a small room. Mode frequencies for a rectangular box of
internal dimensions `L_x, L_y, L_z`:

```
f(n_x, n_y, n_z) = (c/2) · √((n_x/L_x)² + (n_y/L_y)² + (n_z/L_z)²)
```

Indices `n_i ≥ 0`, with at least one nonzero. The lowest mode is
along the longest internal dimension.

Example: a 300×500×250 mm internal cabinet (typical 8" two-way):

- (1,0,0): 343 / (2·0.5) = 343 Hz
- (0,1,0): 343 / (2·0.3) = 572 Hz
- (0,0,1): 343 / (2·0.25) = 686 Hz
- (1,1,0): 670 Hz; (1,0,1): 769 Hz; etc.

These modes couple back through the driver cone — the cone is one
boundary of the resonator. The result is narrow peaks and dips in
the on-axis SPL response, typically 2–5 dB, at the modal
frequencies. They also drive panel resonances from the inside.

### Mitigation

**Stuffing** (absorber, see `materials.md` for material choices):
broadband porous absorption that converts modal energy to heat. Stuff
the cabinet rear walls and away from the driver, not packed against
the cone (which would couple mechanical load to it).

- Long-fiber wool or polyester batting, ~0.5 kg/m³ for ~3 dB
  reduction at modal frequencies; ~1.0 kg/m³ for ~6 dB.
- Over-stuffing increases effective Vb by 5–15 % (isothermal vs
  adiabatic compression) — re-compute `Fc` after stuffing.
- Stuff a sealed box; lightly stuff a ported box (only the rear half,
  not the port path); never stuff a port itself unless deliberately
  reducing its Q.

**Non-parallel internal walls** prevent simple `c/(2L)` modes. A
small angle (3–5°) between facing walls smears modes across a band
rather than concentrating them at one frequency. Common in audiophile
cabinet design (B&W, Sonus Faber).

**Irrational length ratios** for cabinet dimensions: avoid 1:1:1
(cube — modes all align) and 1:2:4 (modes pile up at the same
frequencies). Use ratios like 1 : 1.27 : 1.62 (golden) or 1 : 1.4 :
1.9 to spread modes.

**Internal partitions / Helmholtz absorbers** tuned to specific
problem modes can suck out 6–10 dB at one frequency — useful for
the lowest, longest mode where stuffing alone is weak.

### Diagnosing internal modes

- **Impedance sweep**: narrow wiggles superimposed on the smooth
  curve in the 200 Hz – 1 kHz region typically indicate strong
  internal modes coupling to the cone.
- **Nearfield SPL at the cone**: a clean piston response with no
  ripples is good; small peaks/dips at calculated mode frequencies
  confirm internal coupling.
- **Microphone inside the cabinet** (carefully — leakage through the
  mic port spoils things): mic at a corner picks up all modes;
  comparing pre- and post-stuffing shows how effective the absorber is.

## 4. Panel resonance (cabinet wall modes)

Each cabinet wall is a thin plate that flexes in response to internal
pressure. Its bending modes radiate to the outside, adding a delayed,
colored copy of the music. Audibility is highest in the 100–500 Hz
range — exactly where vocals and bass guitar live.

### Plate bending modes

For a thin rectangular plate of dimensions `a × b`, thickness `h`,
Young's modulus `E`, density `ρ_p`, Poisson's ratio `ν`, with simply-
supported (typical glued-joint) edges:

```
f(m, n) = (π/2) · √(E h² / (12 ρ_p (1−ν²))) · ((m/a)² + (n/b)²)
```

For 18 mm MDF (`E ≈ 4 GPa`, `ρ_p ≈ 750 kg/m³`, `ν ≈ 0.25`) panel of
200 × 300 mm (a typical bookshelf side):

- (1,1): ~ 280 Hz
- (2,1): ~ 450 Hz
- (1,2): ~ 670 Hz

Panel modal frequency scales:

- `∝ h` (thickness): doubling stock thickness doubles mode frequency.
- `∝ 1/a²` (length): halving panel span quadruples mode frequency.
- `∝ √(E/ρ)` (specific stiffness): stiffer/lighter materials raise it.

### Mitigation

**Bracing** is the highest leverage move. A single transverse brace
at the panel midpoint halves the effective length → quadruples the
mode frequency, often pushing it above the speaker's working band.
Two perpendicular braces partition the panel into four sub-panels,
each with much higher modes. Standard practice: brace every
unsupported panel span > 200 mm.

Brace types:

- **Spreaders** (wood dowels or rectangles between opposite walls) —
  cheap, very effective.
- **Window braces** (a hollow rectangle inset on each wall) — light
  but strong, popular in PMC and B&W designs.
- **Matrix bracing** — multiple intersecting braces forming a 3D
  lattice; expensive to build but eliminates panel modes nearly
  completely (Wilson Audio, large monitor cabinets).

**Constrained-layer damping (CLD)**: two stiff layers sandwiching a
viscoelastic core. Bending of the panel shears the core, dissipating
energy as heat. Adds 5–15 dB of damping (`tan δ → 0.1–0.3`) at the
fundamental mode for a few mm of core thickness. Materials: Green
Glue, butyl rubber sheet, bituminous panels.

**Mass loading**: stick-on bitumen pads add mass without much
stiffness, lowering mode frequencies (sometimes useful — pushes them
into the bass where the room dominates anyway) and adding modest
damping. Less effective than CLD for the same mass.

**Material choice**: see `materials.md`. MDF is the default for a
reason — moderate damping is built in. Plywood is stiffer but rings
more. Aluminum needs CLD or it sings like a bell.

### Diagnosing panel resonance

- **Accelerometer (or contact mic) on the outside of each panel
  during a sweep** is the gold standard. Look for peaks 100–600 Hz.
- **"Knock test"**: rap each panel with a knuckle; well-damped
  cabinets sound dull, undamped ones ring. Crude but instructive.
- **Comparing FR with the cabinet sealed vs. open**: if removing one
  panel changes the response above 100 Hz audibly, that panel was
  contributing radiated noise.

## 5. Putting it together

The audible severity ranking for a typical bookshelf:

1. **Internal acoustic modes 200–800 Hz** unstuffed: 2–5 dB peaks,
   muddy midrange.
2. **Edge diffraction 800 Hz – 3 kHz** without driver offset or
   roundovers: ±2–3 dB on axis, worse off axis.
3. **Panel resonance 200–600 Hz** without bracing on >200 mm panels:
   audible ~−15 to −25 dB below direct sound — characteristic "boxy"
   coloration.
4. **Baffle step** uncompensated for free-standing speakers: 4–6 dB
   "thin" presentation, fixable in EQ but obvious if ignored.

A speaker that gets all four right will sound noticeably better than
a much more expensive driver in a poorly-designed cabinet. Spend the
first few hours of any new design on enclosure geometry — driver
choice comes later.
