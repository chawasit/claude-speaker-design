# Room Response Simulation

Predicting what a speaker will sound like in a room is one of the most
useful applications of acoustic computation. You can optimize speaker
and listener placement, evaluate subwoofer schemes, or check a treatment
plan before pouring concrete. None of it is a substitute for real
measurement — but a good simulation tells you where to look and what to
expect.

## Why simulate

| Problem                                    | Simulation gets you                              |
|--------------------------------------------|-------------------------------------------------|
| Single-sub placement                       | Modal SPL map, "least-bad-seat" search          |
| Multi-sub design (Welti / SFM)             | Per-sub gain/delay/PEQ to minimize seat variance|
| Speaker placement                          | Predicted in-room FR at the seat                |
| Treatment plan (panels, bass traps)        | Modal Q reduction; RT60 prediction              |
| New-room geometry decisions                | Mode pile-ups; dimensions to avoid              |
| Listener position optimization             | Sweet-spot mapping                              |

Simulation **does not** replace measurement at the listening position.
It predicts. The further the room is from a rectangular box with hard
walls, the larger the gap between prediction and reality.

## The frequency-dependent regime problem

A room behaves differently in three frequency regions; no single
simulation method covers them all efficiently.

```
LF modal           |  transition  |   statistical reverberant
                   |              |
                  f1              f_S (Schroeder)
0 Hz             ~30 Hz         ~150–300 Hz                 20 kHz
                   |              |
< 10 discrete      |  ~10–100     |   thousands of modes;
modes              |  modes       |   diffuse field
                   |              |
exact modal /      |  modal +     |   ray tracing / SEA
FEM solver         |  diffraction |
```

**Schroeder frequency** marks the boundary between modal and
statistical behavior:

```
f_S ≈ 2000 · √(T_60 / V)     (Hz, T_60 in s, V in m³)
```

Typical living room (50 m³, `T_60` ≈ 0.4 s): `f_S` ≈ 180 Hz. Below
this, your simulation must capture discrete modes. Above it,
statistical averages are fine.

## Method 1: Modal summation (rectangular rooms, < `f_S`)

For a rectangular ("shoebox") room of dimensions `L_x × L_y × L_z`
with rigid walls, the eigenmodes have:

```
f(n_x, n_y, n_z) = (c/2) · √((n_x/L_x)² + (n_y/L_y)² + (n_z/L_z)²)
```

Pressure at receiver `(x_r, y_r, z_r)` for a source at `(x_s, y_s, z_s)`
radiating volume velocity `U(ω)`:

```
p(r, ω) = (ρ₀ c² / V) · Σ_{n_x,n_y,n_z} ψ_n(s) · ψ_n(r) ·
                                          U(ω) / (k_n² − k² − jωD_n/c²)

ψ_n(p) = cos(n_x π x_p / L_x) · cos(n_y π y_p / L_y) · cos(n_z π z_p / L_z)
```

where `k_n = ω_n/c`, `D_n` is the modal damping (related to wall
absorption), and the sum runs over all `(n_x, n_y, n_z)` modes you care
to include. In practice include modes up to ~2 × `f_S`.

Strengths: exact for the assumed geometry, fast (sums of cosines),
gives explicit pressure at every receiver. Tells you immediately
where modal nulls and antinodes sit and how to move sources/receivers
to avoid them.

Weaknesses: assumes rigid rectangular walls (real rooms have absorption,
doors, windows, drywall flex). Treat results as ±2 dB.

REW's "Room Sim" panel implements exactly this for shoebox geometry —
you give it dimensions, wall absorption, and source/listener positions,
and it returns the predicted SPL response at the listener.

## Method 2: Image source method (Allen & Berkley 1979)

Replace reflections by virtual "image sources" at mirror positions
across each wall. For a rectangular room, the image of a source at
`(x_s, y_s, z_s)` across the `x = L_x` wall sits at `(2L_x − x_s, y_s,
z_s)`. Reflections of reflections produce a 3D infinite lattice of
images.

For receiver at position `r`, total impulse response is:

```
h(t) = Σ_{i} (α^{n_i} / d_i) · δ(t − d_i/c)
```

where `d_i` is the distance from image `i` to the receiver, `n_i` is
the number of reflections to reach that image, and `α` is the wall
amplitude reflection coefficient (`α = √(1 − absorption)`).

Truncate the lattice at a delay corresponding to the desired impulse
response length (e.g. 500 ms → first-order images out to ~170 m).

Strengths: produces a full impulse response usable for **auralization**
(convolve with anechoic music to listen to a simulated room). Captures
discrete early reflections precisely.

Weaknesses: rigid rectangular geometry only; constant absorption per
surface (no frequency dependence in the basic form); reflection
"sharpness" misrepresented at LF (real walls diffract, image method
treats them as perfect mirrors).

Extensions handle frequency-dependent absorption (filter each reflected
path through the surface's absorption spectrum), but you've now
crossed into FDTD / hybrid-method territory.

## Method 3: Finite Element Method (FEM)

Mesh the room volume into ~`(λ/6)³` tetrahedra; solve the Helmholtz
equation `∇²p + k²p = 0` with boundary conditions on each surface
(impedance, velocity, pressure-release). At each frequency, solve a
sparse linear system for `p` at all mesh nodes.

Pros: handles any geometry, frequency-dependent surface impedance,
sound-rigid and locally-reacting boundaries. Captures diffraction and
finite-impedance effects that modal summation misses.

Cons: cost scales like `f³` (mesh resolution × `f²`, frequencies × `f`).
A 50 m³ room is tractable to ~500 Hz on a workstation in COMSOL or
FEniCS; pushing to 2 kHz is feasible but expensive; above 2 kHz, switch
to a high-frequency method.

Best fit: LF and lower-mid simulation when room shape isn't rectangular
(slanted ceilings, soffits, openings). For a normal shoebox, modal
summation gives equivalent answers at 1 % of the cost.

## Method 4: Finite-Difference Time-Domain (FDTD)

Discretize the wave equation in **time and space**:

```
p_{n+1}(i,j,k) = 2·p_n(i,j,k) − p_{n−1}(i,j,k)
                 + (cΔt/Δx)² · (p_n(i±1,j,k) + p_n(i,j±1,k) + p_n(i,j,k±1) − 6·p_n(i,j,k))
```

with boundary conditions enforced by either rigid (Neumann),
absorptive (PML / impedance), or transparent boundaries.

Pros: produces the **complete time-domain impulse response** in one
shot. Naturally handles arbitrary geometry, moving sources, and
nonlinear effects. Excellent for transient acoustic visualization.

Cons: voxel grid must satisfy `Δx < λ_min / 10` and `Δt < Δx / (c√3)`
(Courant). A 50 m³ room at 2 kHz needs ~10⁸ voxels and ~10⁵ time
steps — large but tractable on GPU.

Free / open implementations: k-Wave (Matlab/Python, GPU), parallelFDTD,
i-simpa (with hybrid options).

Best fit: research and high-end auralization, not everyday speaker
design.

## Method 5: Geometrical / ray tracing (above `f_S`)

Treat sound as rays from each source, reflecting specularly (or with
diffuse scattering) off surfaces. Each ray's intensity decays per
inverse-square + per-reflection absorption. Histogram receiver-arriving
rays into a temporal energy decay curve → reverberation behavior.

Pros: cheap (each ray is independent); scales to large spaces well;
handles complex geometry naturally; well-suited to architectural
acoustics.

Cons: wavelength-blind below `f_S`; misses diffraction and modal
behavior; assumes ergodic sound field.

Best fit: large rooms above 500 Hz, concert halls, classrooms.
Speaker-in-living-room is in the borderline regime — works for HF, but
LF needs a wave-based method.

Tools: Odeon, EASE, CATT-Acoustic (commercial); pyroomacoustics (free,
Python, image source + ray tracing).

## Method 6: Hybrid (the practical default)

Real simulation packages combine methods:

```
0 Hz ─────── f1 ─────── f_S ─────── 1 kHz ─────── 20 kHz
   |        |         |          |          |
   modal    modal     hybrid     ray        ray + diffusion
   summation FEM      LF + HF    tracing    (statistical)
```

A typical hybrid pipeline:

1. Modal solver below `f_S` (or FEM/FDTD if geometry is non-rectangular).
2. Image-source method up to ~`5·f_S`, with frequency-dependent
   reflection filters.
3. Ray tracing above that.
4. Crossover bands blended in the frequency domain.

This is what Treble, Odeon-V, and the newer cloud-based room acoustics
tools (some using DiffNet-style ML acceleration) do under the hood.

## What an in-room speaker simulation needs as input

To predict the response at a listener position for a real speaker in
a real room, you need:

- **Room geometry**: dimensions, openings, large furniture treated as
  acoustic obstacles.
- **Surface absorption** per surface, per octave band. Default
  "average residential" tables exist; for accuracy below 100 Hz,
  measure with a Sabine reverberation test or estimate from material
  + thickness tables.
- **Source position and directivity**: not just a point source — a real
  speaker radiates with a frequency-dependent polar pattern. For
  accurate simulation, import the speaker's measured polar response
  (CLF, SPK, ANSYS, or CSV) and place it with its actual orientation.
  REW Room Sim treats sources as point omnidirectional, which is fine
  for subs and rough enough for full-range LF, but misses HF directivity.
- **Receiver position**.

## Practical workflows

### Single subwoofer placement (modal sum or REW Room Sim)

1. Model the room. Place the sub at 8–12 candidate positions
   (corners, mid-walls, off-corner, mid-room).
2. For each sub position, compute the predicted SPL response at each
   of 5–9 candidate listener positions.
3. Pick the (sub, listener) combination with the smallest mean
   absolute deviation from a flat target across 20–80 Hz.
4. Verify by measurement at the chosen position. Expect ±3 dB
   agreement.

### Multi-sub optimization (MSO or REW)

1. Model the room. Define multiple sub positions, each as a separate
   source with adjustable gain, delay, and PEQ.
2. Define a target curve and a list of seat positions to optimize for.
3. Run the solver. It will return per-sub gain/delay/PEQ that
   minimizes the seat-region variance.
4. Build, measure, refine.

This is the workflow that makes 2-sub and 4-sub home systems sound
dramatically better than the best single sub. Andrew Jones, Earl
Geddes, and Floyd Toole all published on it; Welti & Devantier (JAES
2003) is the canonical reference.

### Speaker placement (modal + image, full-range)

1. Model the room with the speaker as a directional source (load the
   measured polar response if you have it).
2. Compute predicted FR at 3–5 candidate listener positions for each
   of 5–9 speaker positions.
3. Identify the position that minimizes the worst-case LF mode +
   keeps the early-reflection arrival times above a threshold (10 ms
   first arrival window for stereo imaging clarity).
4. Verify; iterate.

### Treatment design

1. Simulate the bare room. Identify problem modes from the modal sum,
   problem early reflections from the image method.
2. Place candidate absorber/bass-trap geometries in the model; assign
   each its measured absorption coefficient α(f).
3. Re-simulate. Compare predicted decay times and FR.
4. Build a minimum-viable treatment, measure, expand if needed.

## What simulation predicts well vs. poorly

| Phenomenon                                      | Sim accuracy            |
|-------------------------------------------------|--------------------------|
| Modal peak frequencies (rectangular room)       | ±2 % (very good)         |
| Modal peak amplitudes                           | ±3 dB                    |
| Cancellation null depth                         | poor — depends on geometry detail; real null depth ±10 dB |
| Listening position SPL > 200 Hz                 | ±3 dB on average; large local deviation |
| Reverberation time `T_60` per band              | ±20 % with reasonable α inputs |
| Early-reflection arrival times                  | within 1 ms for the first few |
| Effect of moving a sub 30 cm                    | direction correct, magnitude approximate |
| Effect of adding bass traps                     | qualitative; magnitudes optimistic |
| Effect of removing furniture                    | poorly modeled by most tools |
| Above 2 kHz at any seat                         | best treated statistically; not point predictions |

A useful framing: simulation tells you **where to place** speakers and
treatment, but **measurement tells you whether it worked**.

## Tools, free and paid

| Tool                       | Method                        | Cost     | Best for                       |
|----------------------------|-------------------------------|----------|--------------------------------|
| REW Room Sim               | modal summation               | free     | shoebox rooms < 500 Hz         |
| AmCoustics calculator      | analytical modes              | free     | quick mode-frequency lookup    |
| Hunecke room mode calc     | analytical                    | free     | new-room dimension picking     |
| MSO (Multi-Sub Optimizer)  | measurement-based, per-sub FIR| free     | multi-sub gain/delay/PEQ       |
| pyroomacoustics (Python)   | image + ray                   | free     | scripted simulation, research  |
| k-Wave                     | FDTD                          | free     | LF transient research          |
| ABEC                       | BEM + modes                   | free     | acoustic radiation problems    |
| COMSOL Acoustics           | FEM                           | $$$$     | non-rectangular geometry       |
| ANSYS                      | FEM/BEM                       | $$$$     | engineering CAE                |
| Odeon                      | image + ray + diffraction     | $$       | large-space architectural      |
| EASE                       | image + ray                   | $$       | PA system design               |
| CATT-Acoustic              | ray tracing                   | $$       | architectural                  |
| Treble                     | hybrid (cloud)                | $        | residential + studio rooms     |

For DIY speaker work in a normal room, the practical stack is **REW
Room Sim + MSO**, validated by measurement. Step up to FEM or hybrid
only when geometry is unusual or stakes are high (mastering room,
recording studio, dedicated theater).

## Auralization (listening to the simulation)

Once you have a simulated impulse response from any of the wave-based
methods, you can:

```
y(t) = x(t) ⋆ h_sim(t)
```

i.e. convolve a dry anechoic recording `x` with the simulated room
impulse response `h_sim`. Playback through neutral headphones (binaural
rendering with HRTFs) lets you "hear" the predicted room without
building it.

The auralization is convincing within its bandwidth — the modal LF
behavior sounds correct, early reflections sound correct, late decay
sounds right. The headphone-vs-speakers transfer is the dominant
remaining error; binaural rendering improves with individualized
HRTFs.

Tools: any DAW with convolution + a head-tracking binauralizer. The
SOFA file format is the standard for HRTF data. Sennheiser AMBEO
Orbit and Waves Nx are typical playback chains.
