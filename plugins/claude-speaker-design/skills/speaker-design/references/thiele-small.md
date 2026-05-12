# Thiele/Small Parameters

The small-signal lumped-element model of a moving-coil driver,
formalized by Thiele (1971) and Small (1972). Valid up to the first cone
breakup, for displacements within Xmax, and at one drive level (it
ignores compression and large-signal nonlinearity).

## Equivalent circuit

A driver is two coupled second-order systems:

```
                 BL : 1
   amp ── R_e ── L_e ──┤├──── M_ms, R_ms, C_ms ──── radiation impedance
   (electrical)          (mechanical)               (acoustical)
```

The motor `BL` is the gyrator that couples electrical force to
mechanical force: `F = BL · i`, and the back-EMF is `e = BL · v`.

## Core parameters

| Symbol  | Name                              | Units    | Typical 6.5" woofer |
|---------|-----------------------------------|----------|----------------------|
| `R_e`   | DC voice-coil resistance          | Ω        | 5–7                  |
| `L_e`   | Voice-coil inductance (@ 1 kHz)   | mH       | 0.5–1.5              |
| `Sd`    | Effective cone area               | m²       | ~0.013 (130 cm²)     |
| `M_md`  | Cone+coil mass (no air load)      | g        | 10–18                |
| `M_ms`  | M_md + radiation mass             | g        | 12–22                |
| `C_ms`  | Suspension compliance             | mm/N     | 0.5–2                |
| `K_ms`  | Suspension stiffness = 1/C_ms     | N/mm     | 0.5–2                |
| `R_ms`  | Mechanical damping                | N·s/m    | 0.5–1.5              |
| `BL`    | Motor force factor                | T·m (N/A)| 5–10                 |
| `Xmax`  | Linear one-way excursion          | mm       | 3–6                  |

## Derived parameters

These are what you actually use for enclosure design — they are
algebraic combinations of the above and what every datasheet lists.

**Resonance frequency** of the driver in free air:

```
Fs = 1 / (2π · √(M_ms · C_ms))
```

**Electrical Q at Fs** (energy lost to amplifier source impedance):

```
Q_es = (2π · Fs · M_ms · R_e) / (BL)²
```

**Mechanical Q at Fs** (energy lost to suspension friction):

```
Q_ms = 2π · Fs · M_ms / R_ms
```

**Total Q at Fs:**

```
Q_ts = (Q_es · Q_ms) / (Q_es + Q_ms)
```

`Q_ts` is the single most useful number for picking an alignment:

- `Q_ts < 0.3`: needs a horn or ported alignment to compensate for
  low cone compliance; sealed will be over-damped.
- `Q_ts ≈ 0.35–0.5`: ideal for ported (vented) alignments.
- `Q_ts ≈ 0.5–0.7`: ideal for sealed alignments (Bessel to Butterworth).
- `Q_ts > 0.7`: needs a large sealed box or transmission line;
  the driver is essentially self-tuning.

**Equivalent compliance volume:**

```
Vas = ρ₀ · c² · Sd² · C_ms       ≈ 1.4·10⁵ · Sd² · C_ms (m³)
```

`Vas` is the air volume whose stiffness equals the driver suspension's
stiffness. A box of volume `V_b = Vas` doubles total stiffness, raising
the in-box resonance to `√2 · Fs`. This is the single most useful
intuition for sealed-box sizing.

**Reference efficiency** (anechoic half-space):

```
η₀ = (4 π² / c³) · (Fs³ · Vas) / Qes
```

Sensitivity (at 2.83 V, 1 m, half-space) is then

```
SPL = 112 + 10·log₁₀(η₀ · 8 / R_e)
```

## Measuring T/S parameters

1. Measure `R_e` with a DMM (correct for lead resistance).
2. Sweep driver in free air with a current-sense rig; find Fs (impedance
   peak) and the half-power points to extract Q_ms, Q_es.
3. Add a known mass `Δm` to the cone (modeling clay, 5–10 g) or load
   with a sealed test box of known volume, re-measure Fs:
   - **Added-mass method:** `M_ms = Δm / ((Fs/Fs')² − 1)`
   - **Added-volume method:** `Vas = V_b · ((Fs_box/Fs)² − 1)`
4. Compute the rest algebraically.

Use signal level low enough that excursion stays well under Xmax
(≤ 0.1 V drive on a typical woofer). T/S is by definition a
small-signal model.

## Large-signal departures

Real drivers diverge from the T/S model at higher drive. Klippel-style
analyzers fit nonlinear functions:

- `BL(x)`: motor strength as function of displacement. Decreases as the
  coil leaves the gap → 2nd and 3rd harmonic distortion.
- `K_ms(x)`: suspension stiffness vs. displacement. Always increases at
  large excursion ("progressive" suspension) — adds 3rd harmonic and
  asymmetric distortion.
- `L_e(i, x)`: inductance varies with current (flux modulation) and
  displacement (coil moving through pole). Causes intermodulation
  distortion at higher frequencies.

When the user is past Xmax, T/S is not the right tool — switch to
displacement-limited SPL calculations and consider equalization, more
drivers, or a bigger driver.
