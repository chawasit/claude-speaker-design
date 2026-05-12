# Physics of Sound

The acoustic layer of speaker design sits on a small set of wave-equation
results. This file is the lowest layer of the skill — everything in the
other references reduces to these.

## 1. The acoustic wave equation

For small-signal pressure `p(x, t)` in an inviscid, lossless fluid:

```
∂²p/∂t² = c² ∇²p
```

with sound speed

```
c = √(γ p₀ / ρ₀)   ≈ 343 m/s in air at 20 °C, 1 atm
```

`γ ≈ 1.4` for diatomic gases, `p₀` is static pressure, `ρ₀` is the
ambient density. For a plane harmonic wave `p = P · e^{j(ωt − kx)}`:

- angular frequency `ω = 2πf`
- wavenumber `k = ω/c = 2π/λ`
- wavelength `λ = c/f`  → 17 m at 20 Hz, 17 mm at 20 kHz

Particle velocity in a plane wave:

```
u = p / (ρ₀ c)
```

The product `ρ₀ c` (~415 Pa·s/m in air) is the **specific acoustic
impedance** of the medium. It is the acoustic analog of free-space
impedance in EM and is the reason transducer–air coupling is so poor.

## 2. Sound pressure level (SPL)

Reference pressure `p_ref = 20 µPa` (threshold of hearing at 1 kHz):

```
L_p = 20 · log₁₀(p_rms / p_ref)   dB SPL
```

Useful anchors:

| Source                            | SPL (dB) |
|-----------------------------------|----------|
| Threshold of hearing              | 0        |
| Quiet room                        | 30       |
| Conversation @ 1 m                | 60       |
| Reference listening level         | 83       |
| Live rock concert FOH             | 105–115  |
| Threshold of pain                 | ~130     |

Doubling acoustic power adds **3 dB**. Doubling SPL (perceived "twice as
loud" — Stevens' law) takes roughly **+10 dB**, which is 10× the power.
Halving the distance in free field adds **6 dB** (inverse-square law).

## 3. Radiation from a piston

A rigid circular piston of radius `a` in an infinite baffle radiates with
on-axis pressure

```
p(r, ω) = j ω ρ₀ U₀ a² / (2 r)  · [2 J₁(ka sinθ)/(ka sinθ)]
```

where `U₀` is piston velocity amplitude, `J₁` is the Bessel function of
the first kind, and `ka = ωa/c`. Three regimes:

- `ka ≪ 1` (low frequency, long wavelength): omnidirectional, output
  rises with ω² for constant cone velocity → flat SPL for constant cone
  acceleration. This is why direct-radiator drivers need huge cone
  displacement at low frequencies.
- `ka ≈ 1`: directivity narrows; first null appears off-axis.
- `ka ≫ 1`: highly directional beam, narrow main lobe `θ ≈ 1.22 λ/(2a)`.

The transition `ka = 1` defines a driver's **directivity frequency**
`f_d = c/(2πa)`. A 6.5" (a ≈ 0.0825 m) cone starts beaming around
660 Hz; a 1" dome at ~4.3 kHz. This sets crossover ceilings for
constant-directivity designs.

## 4. Radiation impedance and efficiency

The acoustic load on the cone is complex. Real part (radiation
resistance, drives radiated power) and imaginary part (radiation mass,
adds to moving mass) are tabulated as `R_a` and `X_a` for piston-in-
baffle. Limits:

- `ka ≪ 1`: `R_a ≈ (ρ₀ c) · (ka)² / 2`  — radiation resistance ∝ ω².
- `ka ≫ 1`: `R_a → ρ₀ c · S_d` (matched to medium).

The low-frequency ω² dependence is the physical reason direct-radiator
electro-dynamic speakers have ~0.1–1 % efficiency: most of the electrical
input becomes heat in the voice coil, not sound. Horns improve this by
transforming the cone impedance toward `ρ₀ c` over a band.

## 5. Near field, far field, Fresnel distance

The transition from near field (complex interference pattern across the
cone) to far field (1/r decay, smooth directivity) sits near

```
r_ff ≈ S_d / λ          ≈ a²/λ for a circular source
```

For a 6.5" driver at 1 kHz, `r_ff ≈ 0.02 m` — far field starts almost
immediately. At 100 Hz it's ~2 mm. This justifies the **nearfield
measurement technique**: place a mic touching the dust cap to capture
the cone's piston-band response without room contamination, valid up to
roughly `f ≤ c/(2π a) · √(some margin)`; for a 6.5" driver, useful to
~500–800 Hz.

## 6. Reflection, diffraction, interference

- **Reflection at boundary** of acoustic impedance `Z₁ → Z₂`:
  `R = (Z₂ − Z₁) / (Z₂ + Z₁)`. The huge mismatch between solid surfaces
  and air (`Z_wood / Z_air` ~ 10⁴) means walls are near-perfect mirrors.
- **Diffraction** spreads sound around obstacles smaller than λ. Speaker
  cabinet edges diffract a secondary wavefront that recombines with the
  direct one — the cause of the **baffle step** (~6 dB rise from
  half-space to full-space loading as λ shrinks past the baffle width).
- **Interference** between direct sound and a reflection arriving with
  delay τ produces a comb filter with nulls every `1/τ` Hz. Floor and
  desk bounces are the usual culprits at the listening position.

## 7. Room interaction

Below the **Schroeder frequency**

```
f_S ≈ 2000 · √(T₆₀ / V)   Hz   (T₆₀ in s, V in m³)
```

room behavior is dominated by discrete modes; above it, statistical
(reverberant). For a typical living room (50 m³, T₆₀ ≈ 0.4 s),
`f_S ≈ 180 Hz`. Below that, axial mode frequencies are

```
f = (c/2) · √((nx/Lx)² + (ny/Ly)² + (nz/Lz)²)
```

These modes can add ±10 dB at the listening seat regardless of how good
the speaker is. Treatment (bass traps), placement, and EQ are the only
real tools below `f_S`.

## 8. Psychoacoustic anchors

- Equal-loudness contours (ISO 226): bass and treble need more SPL to
  match midrange loudness, especially at low playback levels — the
  reason "loudness compensation" exists.
- Minimum audible level differences: ~1 dB broadband, ~0.3 dB tonal.
- Pitch JND: ~0.1–0.5 % above 500 Hz.
- Localization: ITD dominates below ~1.5 kHz, ILD above.
- Pre-echo audibility: a reflection 1 ms before the direct sound is far
  more disturbing than 10 ms after.
