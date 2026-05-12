# Materials

Every part of a loudspeaker exists to solve a structural problem the
physics imposes. The figures of merit are mostly:

- **Specific stiffness** `E / ρ` (m²/s² or equivalently Pa·m³/kg) —
  governs the speed of bending waves, and hence the frequency where
  modes appear. Higher = breakup pushed higher.
- **Loss factor** `tan δ` (dimensionless) — internal damping; how
  energetically resonances ring. Higher = quieter cabinet, smoother
  cone breakup.
- **Density** `ρ` — for cones, low is good (lighter moving mass, higher
  sensitivity); for cabinets, high is good (more inertia per surface
  area, less radiated sound).

These three rarely co-optimize. Cone design is an explicit Pareto
search between stiffness, mass, and damping.

## Cones and diaphragms

| Material              | E/ρ (Mm²/s²) | tan δ      | Notes                                          |
|-----------------------|--------------|------------|-----------------------------------------------|
| Paper / pulp          | 3–6          | 0.02–0.06  | classic; gentle, lossy breakup. Easy to dope.  |
| Polypropylene (PP)    | 1–2          | 0.05–0.10  | heavy but very lossy → smooth response.        |
| Doped paper / wool    | 4–8          | 0.04–0.08  | wider-band piston, tunable damping.            |
| Kevlar / aramid       | 6–10         | 0.02–0.04  | stiff, low mass; benign breakup if woven.      |
| Carbon fiber / weave  | 15–25        | 0.005–0.02 | very stiff; breakup peaks are sharp.           |
| Aluminum              | 26           | 0.0001     | piston band extends, but huge breakup peak.    |
| Magnesium             | 26           | 0.001      | similar to Al, slightly more damped.           |
| Beryllium             | 156          | 0.001      | tweeter domes; piston band to >40 kHz.         |
| Ceramic (Al₂O₃)       | 90–110       | 0.0005     | extreme stiffness; ceramic-coated Al common.   |
| Diamond (CVD)         | 280+         | 0.0001     | top-tier tweeter; ultrasonic breakup.          |
| Silk / fabric (dome)  | 1–3          | 0.05–0.15  | self-damped; smooth top end, lower extension.  |
| Sandwich (paper/foam) | 8–15         | 0.02–0.05  | "TPX" / Nomex / honeycomb; favorable trade.    |

**Cone breakup** appears near `f ≈ (1.8/πa²) · √(B/m'')` where `B` is
bending stiffness per unit width and `m''` is areal mass — i.e. driven
by specific stiffness. A 6.5" aluminum cone breaks up around 5 kHz with
a +10 dB peak; the same shape in polypropylene breaks up at 3 kHz but
with only +2 dB. The first material extends the piston band but
requires a 4th-order notch in the crossover; the second is a "just
roll it off" driver.

## Surround (roll)

The cone's outer suspension. Functions: seal the front-to-rear airflow,
guide axial motion, terminate cone bending waves.

| Material               | Compliance | Damping | Notes                                  |
|------------------------|------------|---------|----------------------------------------|
| Foam (urethane)        | high       | low     | excursive; UV/ozone life 10–15 years.  |
| Rubber (butyl, NBR)    | medium     | medium  | most common modern choice.             |
| Treated cloth (M-roll) | low        | high    | terminates cone modes well; less Xmax. |
| TPE / Santoprene       | medium     | medium  | rubber-like, better cold flow.         |

A poorly-terminated cone shows narrow ring modes 1–4 kHz on impedance
sweeps. A well-chosen rubber surround can put a useful resistive load
on cone bending waves and smooth this region by 3–5 dB.

## Spider (damper)

The inner suspension; corrugated phenolic-impregnated cotton (Nomex,
poly-cotton) in most modern drivers. Sets most of the suspension
compliance and almost all of the suspension nonlinearity.

- Linear spiders use "progressive" corrugation patterns to keep
  `K_ms(x)` flat near Xmax. Standard spiders stiffen sharply past
  Xmax → 3rd harmonic distortion at high level.
- Dual spiders (two stacked) constrain rocking modes and improve
  alignment at the cost of compliance.

## Voice coil

The motor's resistor + inductor + force generator.

| Coil wire           | ρ_e (nΩ·m) | Density g/cm³ | Comment                                 |
|---------------------|------------|---------------|------------------------------------------|
| Copper              | 17         | 8.96          | baseline; densest                        |
| Aluminum (Al)       | 28         | 2.70          | lighter, lower BL for same gap height    |
| CCAW (copper-clad Al)| 19–25     | ~3.0          | compromise; common in dome tweeters     |
| Silver              | 16         | 10.5          | marginal vs Cu, costly                   |

Coil former materials:

- **Kapton** (polyimide): low thermal mass, good to ~250 °C, low eddy
  losses. Tweeters and small mids.
- **Fiberglass**: cheap, moderate temp, slight eddy loss.
- **Aluminum**: high thermal mass (excellent power handling), but acts
  as a shorted turn → adds copper-cap-like high-frequency damping;
  reduces `L_e` and inductance modulation.
- **Titanium / Nomex**: high-end woofers needing both heat dissipation
  and low eddy.

Wire cross-section: round vs. flat (rectangular ribbon). Flat wire
gives ~20–30 % more copper per unit gap height → higher BL for same
`R_e`, at higher cost.

## Magnet structure

Generates the static gap flux B that, multiplied by gap-length
intersected by the coil, gives BL.

| Material              | BHmax (MGOe) | Curie T (°C) | Notes                                   |
|-----------------------|--------------|--------------|-----------------------------------------|
| Ferrite (ceramic Y30) | 3–4          | 450          | bulky, cheap, thermally rock-solid.     |
| Alnico (5/8)          | 5–8          | 850          | excellent thermal stability, expensive; |
|                       |              |              | can demagnetize at high drive.          |
| Neodymium (N42–N52)   | 42–52        | 310–350      | tiny, strong; care for thermal limit.   |
| Samarium cobalt       | 16–32        | 750          | aerospace; high-temp Nd alternative.    |

Gap geometry features:

- **T-pole, copper sleeve, or copper cap** on the pole piece shorts
  high-frequency eddy currents → flattens `L_e(i, x)` modulation,
  cutting IMD by 5–15 dB above 1 kHz.
- **Underhung** (coil shorter than gap) and **overhung** (coil longer
  than gap) trade Xmax for efficiency. Pro compression drivers are
  underhung; subwoofers are deeply overhung.
- **Shorted ring at the bottom of the gap** ("Faraday ring") does the
  same job as a copper cap, for the bottom-half stroke.

## Cabinet stock

Goal: high density, high internal damping, high panel stiffness — so
that radiated cabinet noise is 15–20 dB below the driver in the bass
and inaudible above 200 Hz.

| Stock                 | Density (kg/m³) | tan δ | Notes                            |
|-----------------------|------------------|--------|----------------------------------|
| MDF                   | 700–800          | 0.02–0.04 | flat, machinable, default DIY.   |
| HDF                   | 850–1000         | 0.02   | denser MDF; better but pricey.   |
| Plywood (Baltic birch)| 600–750          | 0.01   | stiffer than MDF; rings more.    |
| Particleboard         | 600–700          | 0.03   | cheap; not as stiff/uniform.     |
| Solid hardwood        | 600–900          | 0.005  | varies with grain; can sing.     |
| Aluminum (cast)       | 2700             | 0.0001 | very stiff/dense; needs damping. |
| Concrete / mineral    | 2200–2400        | 0.01   | extreme inertia; heavy.          |

Damping strategies for panels:

- **Constrained-layer damping (CLD):** two stiff layers (MDF, aluminum)
  with a viscoelastic core (Green Glue, butyl). Adds 10–20 dB at the
  fundamental panel mode for ~3 mm extra thickness.
- **Bracing** at 1/3 + 1/2 panel divisions raises modal frequencies
  out of the audio band or above driver passband.
- **Mass loading** (bitumen pads) lowers mode amplitude by inertia.
- **Internal damping** (long-fiber wool, polyester batting, Dacron)
  absorbs internal standing waves above ~200 Hz. Stuff loosely;
  packed stuffing kills cabinet volume estimates by 10–20 %.

## Damping/absorber materials inside the cabinet

| Material                  | f range (effective) | Notes                                     |
|---------------------------|---------------------|-------------------------------------------|
| Long-fiber wool           | 200 Hz – 20 kHz     | classic ported-box stuffing.              |
| Polyester batting / Dacron| 300 Hz – 20 kHz     | hypoallergenic, dimensionally stable.     |
| Acoustic foam (open cell) | 500 Hz – 20 kHz     | wall-mount; little effect at low freq.    |
| Fiberglass (rigid)        | 100 Hz – 20 kHz     | best per cm thickness; itchy.             |
| Activated carbon          | extends effective Vb| adsorbs/desorbs gas — virtually larger box.|

## Adhesives and finishes

Easy to overlook, frequently the failure mode after a decade.

- Cone-to-surround / surround-to-frame: PVA or contact cement; flexible
  variants (Hennecke E2010, 3M Hi-Strength 90).
- Voice-coil winding: thermally-cured polyimide enamel + epoxy.
- Cabinet joinery: PVA wood glue + biscuits/dominos; sufficient if
  joinery is tight. Polyurethane glues foam and shift dimensions.
- Cabinet finish: thick lacquer adds stiffness (good); cheap veneer
  rings (bad). For DIY, BIN primer + several coats of waterborne
  polyurethane is a robust default.

## Picking materials by goal

- **Maximum SPL per dollar:** paper cone, ferrite motor, MDF cabinet,
  ported alignment. (Most pro PA.)
- **Minimum distortion:** hard cone (Be / ceramic) with notch filter,
  copper-capped motor, large-Xmax overhung coil, sealed alignment.
- **Smallest cabinet:** stiff aluminum cone + sealed + DSP EQ; ceramic
  or treated MDF panel + heavy bracing to keep panel modes well above
  the driver passband.
- **Best timbre / smooth response:** doped paper or polypropylene cone,
  soft-dome tweeter, well-damped cabinet, gentle slopes.
- **Reference monitor:** measure-and-iterate philosophy beats material
  dogma. Any of the above can be excellent if executed carefully.
