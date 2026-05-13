# Crossover Components: Tolerances, Types, and Topology

A passive crossover is built from three component types — capacitors,
inductors, resistors — with countless type/value/topology choices.
This file covers:

1. How **tolerance** on each component shifts the acoustic response.
2. How **dielectric and core type** add non-ideal behavior beyond
   nominal value.
3. How **series vs parallel topology** changes what each component
   does to the signal.

For filter slopes, summing behavior, and acoustic design targets see
`references/crossovers.md`. This file is about the components
themselves.

## 1. Capacitors

### Tolerance and acoustic effect

The crossover corner frequency depends on `√(LC)`:

```
f_c ∝ 1 / √(L · C)
```

A ±X % deviation on C shifts `f_c` by ≈ X/2 % (RSS, single component) or
up to X % (worst case if combined with same-direction L deviation).

| Capacitor tolerance | Crossover frequency shift (worst case) | Audibility |
|---------------------|----------------------------------------|------------|
| ±20 % (electrolytic) | ±20 %                                 | Audible    |
| ±10 % (standard film) | ±10 %                                | Audible at critical levels |
| ±5 % (premium film)   | ±5 %                                 | Marginal   |
| ±2 % (selected)       | ±2 %                                 | Inaudible  |
| ±1 % (measured)       | ±1 %                                 | Inaudible  |

For a 2 kHz LR4 crossover, ±10 % moves `f_c` from 1.8 to 2.2 kHz —
clearly audible as a tonal shift. For stereo pairs, the practical
target is ±2-3 % matched between left and right; **mismatch
between channels** moves the image more than absolute deviation
from nominal.

### Dielectric types

| Type | Quality in audio | ESR | Tolerance | Cost | Use |
|------|------------------|------|-----------|------|-----|
| Polypropylene film (PP) | excellent | < 0.01 Ω | ±5 % typical, ±2 % selected | $$$ | hi-fi crossover **default** |
| Metallized polypropylene | very good | low | ±5 % | $$$ | hi-fi alternative |
| Polyester (PET / Mylar) | good | low | ±10 % | $$ | budget crossover |
| Non-polar electrolytic | poor | 0.1-1 Ω | ±20 % | $ | tweeter HP only (small values) |
| Ceramic (class 2, X5R/X7R) | bad in audio | low | varies | $ | avoid (microphonic, voltage coefficient) |
| Ceramic (class 1, NP0/C0G) | OK below 1 nF | very low | ±2 % | $$ | rare in crossover (too small) |
| Paper-in-oil | excellent (vintage) | very low | ±10 % | $$$$ | audiophile niche |

**Polypropylene is the default** for any capacitor in the audio
signal path. Use electrolytic only if it's a large value (>50 µF)
on a tweeter HP where size and cost matter more than absolute fidelity
— and even there, prefer a film+electrolytic parallel hybrid (the
film bypasses the electrolytic at HF, where the electrolytic's ESR
becomes audible).

### Microphonics

Ceramic capacitors (and to a lesser extent electrolytics) convert
mechanical vibration into voltage via the piezoelectric and
electrostriction effects. Inside a speaker cabinet **vibrating at
high SPL**, this adds intermodulation noise to the signal — audible
on critical material. **Polypropylene is essentially immune.**

### ESR (Equivalent Series Resistance)

ESR adds an in-band loss and modifies filter Q:

| Type | ESR (typical for 10 µF) |
|------|---------------------------|
| PP film, 250 V | 0.005 Ω |
| Polyester | 0.05 Ω |
| Bipolar electrolytic | 0.5 Ω |
| Aluminum electrolytic | 0.1 Ω (large) to 5 Ω (small) |

For a 10 µF film cap in a tweeter crossover at 2 kHz, the cap's
reactance is ~8 Ω; an ESR of 0.005 Ω is irrelevant. For the same cap
as a bipolar electrolytic with 0.5 Ω ESR: that's 6 % of the cap's
impedance, contributing to passband loss and slightly reducing the
filter Q.

### Voltage rating

Rule of thumb: cap voltage rating ≥ 2 × the peak voltage that will
appear across it. For a tweeter HP cap in a 100 W system: peak
voltage ≈ 40 V, so use 100 V-rated film caps. Higher rating = larger
physical size + cost.

## 2. Inductors

### Tolerance

| Inductor type | Tolerance | Notes |
|---------------|-----------|-------|
| Air-core | ±2-5 % | The audiophile reference |
| Iron-core (laminated steel) | ±5-10 % | Compact, low DCR |
| Ferrite-core | ±10-20 % | Smallest; can saturate |
| Litz-wire air-core | ±2 % | Lowest AC losses |

Effect on `f_c` is the same as for caps — ±5 % on L → ±2.5 % on `f_c`
(RSS) or up to ±5 % (worst case).

### Core types

| Core | DCR (per mH, typical 16 AWG) | Saturation | Physical size | Cost |
|------|--------------------------------|--------------|----------------|------|
| Air | 0.4-2.0 Ω | None (never saturates) | large | $-$$$ |
| Laminated iron / steel | 0.1-0.5 Ω | At ~1-2 T flux density | small | $$ |
| Ferrite | < 0.1 Ω | At ~0.3-0.5 T (low!) | very small | $ |
| Air-core Litz | 0.1-0.3 Ω (at audio AC) | None | larger | $$$$ |

### DCR (DC resistance) — the hidden tax

An air-core inductor's coil resistance shows up as a series resistor
between the amp and driver. For a woofer at low frequency where the
inductor's reactance is small, the DCR dominates.

Example: 6.5" woofer (Re = 5.4 Ω) with a 6 mH air-core inductor at
the LP corner of a 250 Hz crossover. Inductor DCR = 1.0 Ω. Total
series resistance in the passband: 1.0 Ω in series with the 5.4 Ω
voice coil = **6.4 Ω total**.

Effect:
- Sensitivity reduction: 20·log₁₀(5.4 / 6.4) ≈ **-1.4 dB**
- Power-handling reduction: 1 W dissipated in the inductor at full
  drive becomes heat, not SPL
- Damping factor reduction: the amp sees a higher source impedance,
  reducing the effective electrical damping on the cone

Mitigations:
- Use thicker-gauge wire (lower DCR per mH) → larger inductor
- Use iron-core (much lower DCR/mH) → accept saturation risk
- Use a smaller inductor value (move the crossover higher) → loses
  the protection of a lower crossover
- Bi-amp / go active → no passive inductor

The "should I bi-amp this design?" question often comes down to:
"is the woofer's series inductor DCR > 0.5 Ω?" If yes, active is
worth considering.

### Saturation

Iron and ferrite cores have a maximum flux density beyond which the
inductor's effective inductance drops sharply. The cause:

```
B = µ₀ · µ_r · N · I / l_core
```

At high current (high SPL), B approaches saturation, µ_r drops, L
drops. The drop is gradual at first (a few percent), then sharp.
Audible as **2nd-harmonic distortion** rising rapidly above ~10 %
of rated saturation current.

For high-power pro systems: air-core is preferred even at the cost
of size and DCR, because the saturation distortion of an
undersized iron inductor is worse than the DCR loss of an air-core.

For home hi-fi at < 100 W peak: iron-core inductors of appropriate
size don't saturate; the DCR benefit is real.

### Self-resonance

Every inductor has parasitic capacitance between turns. The L + C_par
forms a self-resonant frequency (SRF):

```
SRF = 1 / (2π · √(L · C_par))
```

Below SRF, inductor behaves inductively. Above SRF, capacitively.
For crossover inductors (1-10 mH), SRF is typically 50-200 kHz —
well above audio band. Not usually an issue.

## 3. Resistors

### Types

| Type | Tolerance | Power | Noise | Inductance | Use in crossover |
|------|-----------|--------|--------|--------------|--------------------|
| Metal film | ±1 % | 0.25-1 W | low | low | Low-power roles (L-pad arms) |
| Metal oxide film | ±5 % | 1-10 W | low | low | Medium-power Zobel, L-pad |
| **Wirewound, non-inductive** | ±5 % | 5-50 W | very low | very low | **High-power Zobel, L-pad** |
| Wirewound, standard | ±5 % | 5-50 W | very low | **high (1-10 µH)** | **AVOID in crossover** |
| Carbon composition | ±5-10 % | 0.25-1 W | high | low | Vintage; replace |
| Cermet | ±1 % | 0.5-2 W | low | low | OK for low-power |

**Always specify "non-inductive wirewound"** for power resistors in
a crossover. The standard wirewound type has 1-10 µH of inductance,
which adds reactance at HF and skews filter behavior.

### Power rating

The resistor in an L-pad or Zobel dissipates real power at full drive:

**L-pad:** for a 3 dB pad on a 4 Ω tweeter receiving 40 W peak:
- R1 ≈ 1.2 Ω in series → dissipates ~10 W peak, ~3 W RMS
- R2 ≈ 10 Ω in parallel → dissipates ~3 W peak
- Spec both at 10 W ratings

**Zobel:** for a Zobel network on a 5 Ω woofer, the Rz ≈ 6 Ω
dissipates ~5 W peak at full drive. Spec at 10 W.

Underrating → resistor heats, drifts, eventually fails. Often the
first crossover failure in a high-power system.

## 4. Tolerance budget for a crossover

Putting it together for a typical 2-way LR4 crossover at 2 kHz:

| Component | Nominal | Tolerance | Worst-case range |
|-----------|---------|------------|--------------------|
| Tweeter C (HP) | 14.07 µF | ±5 % | 13.37-14.77 µF |
| Tweeter L | 0.45 mH | ±5 % | 0.43-0.47 mH |
| Woofer L (LP) | 0.90 mH | ±5 % | 0.86-0.95 mH |
| Woofer C | 7.03 µF | ±5 % | 6.68-7.38 µF |

`f_c` of the HP section can range from 1.86 to 2.16 kHz worst-case.
The LP section similar. Filter slopes within ±5 % of LR4. Acoustic
sum within ±1 dB through crossover.

For a **stereo pair**, the L and R speakers should be **matched
within ±2 %** on every component. A 5 % L vs R mismatch on the
tweeter cap moves the right channel's crossover ~5 % higher than
the left → audible image asymmetry (the louder side around the
crossover pulls the image).

### Matching strategy

1. Buy components from one batch (same lot = similar deviations).
2. Measure each with an LCR meter; reject outliers > 3 % from
   nominal.
3. Sort matched pairs (L1-L = 0.443 mH, L1-R = 0.442 mH; etc.).
4. Build the two channels with matched pairs.

## 5. Series vs parallel topology

The same components in different positions produce different
filtering. The four basic crossover arrangements:

### LR4 low-pass (woofer side)

```
in ---L1--- L2 ---- out (to woofer)
            |
   +--C1--+ |
   |       ||
   gnd    gnd

   alternate format:

    in
     |
     L1
     +-- C1 -- gnd
     |
     L2
     +-- C2 -- gnd
     |
     out → woofer
```

- **Series L**: opposes high frequencies (`X_L = ω·L`); passes low.
- **Parallel C**: shunts high frequencies to ground; doesn't affect low.

### LR4 high-pass (tweeter side)

```
in ---C1--- C2 ---- out (to tweeter)
            |
            L1  L2
            |   |
           gnd gnd
```

Mirror image: series C blocks low, parallel L shunts low to ground.

### Series notch (parallel with driver)

```
   in
    |
    +--(driver)--out
    |
   L
    |
    C
    |
    R
    |
   gnd
```

R-L-C in series, in parallel with the driver. At the tank's
resonance frequency (`f₀ = 1/(2π√LC)`), the tank's impedance
**drops to R** (a low value), shorting that frequency to ground.
Off-resonance, the tank impedance is high, no effect.

Use for: killing cone breakup peaks (parallel-trap a frequency
the driver shouldn't reproduce); flattening Fs of a woofer.

### Parallel notch (in series with driver)

```
in --(R || L || C all parallel)-- driver -- out
```

R-L-C in parallel, in series with the signal path. At the tank's
resonance, parallel tank impedance is **very high**, blocking that
frequency from reaching the driver. Off-resonance, impedance is
low, no effect.

Less common than series notch because:
- Components in series with the driver carry full driver current
- Power dissipation is in the components, not bypassed
- More expensive (higher-power L and C needed)

### Zobel network

```
in --- driver --- out
        |
        R_z
        |
        C_z
        |
       gnd
```

R-C in series, in **parallel with the driver**. Flattens the driver's
voice-coil-inductance-induced impedance rise above ~1 kHz.

`R_z = 1.25 · R_e`
`C_z = L_e / R_e²`

For a driver with R_e = 5.4 Ω, L_e = 0.7 mH:
`R_z = 6.75 Ω`, `C_z = 24 µF`

Always **before** the crossover (the crossover then sees a flat
impedance and the textbook filter math actually applies).

## 6. Why parallel topology dominates

A standard LR4 uses parallel C and series L for LP (mirror for HP).
**Pure series topology** (everything in series) doesn't make a useful
filter — you'd have N components in series with the signal, dropping
the same voltage across all → insertion loss without selectivity.

**Pure parallel topology** (everything in parallel) doesn't make a
filter either — every component sees the same voltage; no slope.

The standard topology alternates: series element + shunt element,
each contributing to the slope. 2nd-order section: 1 series + 1 shunt.
4th-order section: 2 series + 2 shunt. 8th-order section: 4 series +
4 shunt.

**For notches**, the topology choice (series vs parallel trap) maps
to where the energy goes:

| Topology | Resonance behavior | Energy at resonance | Use case |
|----------|---------------------|------------------------|----------|
| Series trap (R-L-C in series, in parallel with driver) | Z drops to R | Diverted to ground through R | Driver-side breakup notch (common) |
| Parallel trap (R-L-C in parallel, in series with driver) | Z rises high | Blocked from reaching driver | Less common; high-power applications |

For DIY crossover work, **series traps** are the default. Easier to
build, less power dissipation in critical components, more familiar
formulas.

## 7. The L-pad in detail

For attenuating a too-loud driver (typically tweeter):

```
in --R1-- driver -- out
         |
         R2
         |
         gnd
```

R1 in series, R2 to ground after R1. Combination presents the same
load impedance to the upstream circuit as the driver alone — so the
crossover filter still sees the design impedance.

```
R1 = Z · (1 - 10^(-A/20))
R2 = Z · 10^(-A/20) / (1 - 10^(-A/20))
```

For A = 3 dB on a 4 Ω tweeter:
- R1 = 1.17 Ω
- R2 = 9.43 Ω

For A = 6 dB on a 4 Ω tweeter:
- R1 = 2.00 Ω
- R2 = 4.00 Ω

**Power dissipation** in R1 and R2 at full drive — see § 3 above.
Spec power ratings to handle the **peak** drive, not just continuous.

## 8. Component quality and audibility

What actually affects sound (in rough order of impact):

| Issue | Audibility | Mitigation |
|-------|-------------|--------------|
| Acoustic target mismatch | very audible | Measure and design properly |
| Tweeter sensitivity mismatch (L-pad) | very audible | Measure on-axis SPL, set L-pad |
| Inductor DCR loss on woofer | audible | Air-core thick wire, or active |
| Stereo channel matching (>3 % off) | audible | Hand-match components |
| Tolerance > 5 % on filter components | marginal-audible | Use ±2-3 % parts |
| Electrolytic vs film capacitor | audible on HP | Use film |
| Iron-core saturation at high SPL | audible | Air-core for pro, OK iron for home |
| Inductive vs non-inductive resistor | marginal | Spec non-inductive |
| Brand of film capacitor | marginal | Trust the spec, not marketing |
| Magic cables and capacitors | mostly inaudible | Spend the money elsewhere |

Spend the **biggest budget on capacitors and inductors** that
matter (signal path, high-current sections). Cheap on the rest.

## 9. Practical sourcing

For DIY:
- **Parts Express, Madisound, Solen** (US/international) — broad
  selection of film caps and air-core inductors.
- **Mundorf, Jantzen, Clarity Cap** — premium brands with
  audiophile reputation.
- **Erse, Dayton** — budget options that work fine.

For matched pairs:
- Buy 4 of each value (for L+R + 2 spares for matching).
- Use a Dayton DATS V3 or LCR meter to measure.
- Build the two channels with the closest pairs; keep spares.

## Cross-references

- `references/crossovers.md` — filter design and acoustic targets
- `references/measurement.md` — verifying real component values
  in-circuit via impedance sweep
- `references/dsp-and-active.md` — when component choice stops
  mattering (active/DSP eliminates passive components)
- `tools/crossover_lr.py` — calculates nominal LR2/LR4 component
  values + Zobel; assumes ideal components
