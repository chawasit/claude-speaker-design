# Listening Setup

A speaker's response at the listening position depends as much on
where it is in the room and where the listener is, as on how well
the speaker itself is engineered. This file is the practical
end-of-the-chain reference: geometry, placement, toe-in, height,
and reflection management to extract the speaker's potential.

## 1. The equilateral triangle (stereo)

The default for two-channel listening. The two speakers and the
listener form an **equilateral triangle**:

```
   L speaker -------- R speaker
       \              /
        \            /
         \          /
          listener
```

Side length: typically 2.0–3.5 m. Smaller for nearfield monitoring,
larger for "mid-field" home hi-fi.

Speaker spacing = listening distance = `D`. The angle subtended by
the speakers at the listener is exactly 60° — within the eye's
~30°-each-side comfortable image-width range, and a sweet spot for
stereo imaging.

### Deviations and consequences

- **Wider spacing** (`spacing > 1.2 × D`): "hole in the middle"; the
  stereo image collapses at the center.
- **Narrower spacing** (`spacing < 0.8 × D`): image compresses
  toward the center; loses width.
- **Asymmetric** (one speaker closer): the closer one dominates
  loudness and the image pulls toward it. Within ~3 dB / 10° of
  symmetry, the ear adapts; beyond, it doesn't.

The brain locks an image to "the loudest, earliest-arriving source"
(precedence effect, ~10 ms window). Asymmetric setups violate this
and the image becomes unstable.

## 2. Toe-in

The angle between each speaker's primary axis and the line to the
listener. Three regimes:

- **0° (parallel firing forward)**: maximum stage width but soft
  center image; works for omnidirectional speakers or those with
  wide horizontal pattern.
- **Toed-in to cross in front of listener (~10–30°)**: tightest
  center image; first-reflection sidewall is off-axis (helpful for
  rooms with reflective walls); narrower stage.
- **Toed-in to cross behind listener (extreme, ~30°+)**: rare;
  intentional to maximize sweet-spot precision at the cost of
  off-center listener experience.

### Picking toe-in

A pragmatic procedure:

1. Start with axes crossing **just in front of the listener's nose**.
2. Listen to a familiar voice-centered recording.
3. If the voice sounds disembodied or sibilant, **reduce toe-in**
   (point more parallel).
4. If the stage feels narrow or center-heavy, **reduce toe-in** also.
5. If the stage feels diffuse or center is "loose", **increase
   toe-in**.

Speakers with controlled directivity (waveguide HF, CD horns)
generally want **less toe-in** (their off-axis response is already
controlled). Wide-pattern speakers (small dome HF, omnidirectional)
want **more toe-in** (their off-axis is what excites the sidewall
reflections).

## 3. Listening height

The tweeter (or the acoustic-center axis of a multi-way speaker)
should sit at **listening ear height** — typically 95–110 cm for a
seated adult, 130–140 cm for standing.

### Vertical lobing tolerance

The polar pattern through crossover (between woofer and tweeter) is
typically **not** symmetric. For a typical bookshelf with the tweeter
above the woofer:

- **On tweeter axis**: best response.
- **+10° above tweeter axis**: response thinner (LR4 vertical lobe is
  on-axis; off-axis above sees one extreme of the lobe).
- **-10° below tweeter axis**: response also off; below sees the
  other extreme.

Ear height differs by 10–15 cm between sitting on a sofa vs sitting
upright in a chair. That's ±5° at typical distances — usually
tolerable. If you can hear the response shift when you change posture,
the tweeter is at the wrong height for both postures.

### Stand height calculation

```
stand_height = ear_height − distance_from_woofer_to_tweeter / 2
```

For 100 cm ear height and a tweeter 26 cm above the woofer center:
stand height ≈ 100 − 13 = 87 cm.

## 4. Distance from walls

Three boundary effects:

- **Front wall** (behind the speakers): boundary reinforcement
  +3 to +6 dB at LF; closer wall → more low-end gain. Sealed and
  small-cabinet designs handled.
- **Sidewall**: first reflection arrives within 1–3 ms of direct;
  comb-filters the response unless treated.
- **Floor**: similar to sidewall but worse (the listener's couch is
  usually closer to the floor than the side wall, and floor reflection
  carries different timbre cues).

### SBIR (Speaker–Boundary Interference Response)

When a speaker is `d` away from a wall, sound reflected off the wall
arrives at the speaker's own axis with delay `2d/c`. Where `2d/c` = a
half wavelength, the reflected wave **cancels** the direct radiation:

```
f_null = c · n / (4d),    n = 1, 3, 5, ...
```

For `d = 50 cm` from the front wall: nulls at 172 Hz, 514 Hz, …
For `d = 100 cm`: nulls at 86, 257, 429 Hz, …

The first null is the audible one — a 6–12 dB suckout. To control:

- **Move the speaker** toward or away from the wall to put the null
  outside the speaker's working band. Less than 30 cm from front
  wall pushes the null above 285 Hz where the room is taking over
  anyway; more than 1.5 m pushes the null below 60 Hz where the
  speaker can't reach.
- **Treat the wall** with broadband absorber (see
  `acoustic-treatment.md`). Reduces reflection amplitude → reduces
  null depth.
- **EQ** the null. Limited gain — adding 6 dB at 200 Hz needs careful
  excursion budget.

The "Allison effect" — the same phenomenon — gave its name to the
1970s loudspeaker design tradition of placing drivers at carefully
chosen heights/widths to spread SBIR nulls across frequency.

## 5. Listening position in the room

The listening **chair** sits where the modal pattern is least bad
for the chosen seat — usually:

- **Not in the geometric center** of the room: axial modes have
  pressure null in the center for odd modes, antinode at the walls
  for all. Mid-room is hit-or-miss; off-center is more predictable.
- **Not against the rear wall**: pressure antinodes at every mode
  pile up at the boundary.
- **Roughly 0.4 × room length from rear wall** is a starting point
  for a typical room.
- **Roughly the same distance from each sidewall** (symmetric):
  preserves stereo image.

If the room is rectangular, **39%** of the room length from one end
is the classic "Cardas position" — claimed to minimize modal
problems based on golden-ratio reasoning. It often does work; the
underlying explanation (modes pile up at specific room fractions)
is reasonable.

### Sweet-spot size

The "sweet spot" (where stereo image is stable) is typically the
volume within ~50 cm of the equilateral-triangle apex, at the
correct height. A second listener 1 m to the side perceives an
asymmetric image biased toward the near speaker.

For multi-listener setups (couch, conference room), accept that the
image will not be symmetric for off-axis listeners; concentrate on
SPL uniformity instead.

## 6. First reflections

Reflections from sidewalls, floor, and ceiling arriving within
~50 ms of the direct sound integrate with it perceptually but can
also smear localization cues.

### The "mirror trick" for sidewall first reflection

Place a small mirror flat on the sidewall. Slide it along the wall
while looking at it from the listening position. The point on the
wall where you can see the speaker's tweeter in the mirror is the
first-reflection point.

Treat this point (~50×50 cm absorber panel) for cleaner stereo
imaging. Or do not treat it, leaving the sidewall reflection live,
for a more open / spacious presentation — there are valid
preferences in either direction.

### Floor reflection

Always present, hardest to treat. A rug between speakers and listener
absorbs ~3 dB above 500 Hz; doesn't help in the bass region (which is
modal anyway). Stand-mounted speakers with the tweeter at ear height
minimize the difference between direct and floor-reflected sound
paths, lessening the SPL of the floor bounce relative to direct.

### Ceiling reflection

Same principle as floor; harder to treat (most living rooms aren't
willing to host a ceiling cloud). A clamped-cloud absorber or even a
deep ceiling rosette reduces it.

## 7. Multi-channel and surround

For 5.1 / 7.1 / Atmos setups:

- **Center channel**: ideally same model as L/R; placed on the same
  acoustic-center axis (height). When mounted below or above the
  screen, tilt or aim it at the listener.
- **Surround channels**: locate at +110° / −110° from center for 5.1,
  ±100° + ±150° for 7.1. Direct radiating dynamic speakers preferred
  over dipoles for modern object-based audio (Atmos).
- **Atmos heights**: ceiling-mounted at +30° to +55° elevation. Each
  speaker should "fire down" at the seating area. Tight pattern
  control (small waveguide on HF) reduces sidewall and floor
  reflections.
- **Subwoofer(s)**: see `subwoofers.md`. Multi-sub placement (Welti
  config) preferred over single sub.

## 8. The "tuning" procedure

After installing speakers, before declaring done:

1. **Set toe-in** by ear with familiar voice / center-image content.
2. **Set listening height** so tweeter is at ear height when seated
   in the listening posture.
3. **Sweep mic measurement** at the listening seat. Reveal modal
   peaks and SBIR nulls.
4. **Move speakers** to minimize the worst peak/null in the
   80–300 Hz region. Often a 10–20 cm move pays back 5–8 dB.
5. **Add broadband absorber at first reflections** if the room is
   reverberant. Re-measure.
6. **Add bass traps** in corners (see `acoustic-treatment.md`).
   Re-measure.
7. **Apply minimal PEQ** to remaining peaks, never to nulls.
8. **Listen** to familiar program material. If something still sounds
   wrong, the speaker — not the setup — may be the limit. Or the room
   is uncorrectable without serious treatment.

## 9. Common pitfalls

- **Speakers in corners** (intended for "more bass") → severe modal
  excitation, lumpy LF. Pull out 30–60 cm.
- **Coffee table between speakers and listener** → diffraction +
  early-reflection comb-filtering. Remove or treat.
- **Asymmetric room** (window on one side, bookshelf on the other) →
  asymmetric reflections; the stereo image leans. Treat the
  bare-wall side with diffuser or absorber to match the bookshelf.
- **Speakers on the wrong end of a rectangular room** (firing along
  the short axis instead of the long axis) → modes are denser, less
  separated; treatment is harder. Try the long-axis configuration.
- **Tilting the speaker for "vertical aim"** without re-measuring →
  often makes off-axis vertical worse than it was on-axis. Use
  stand height, not tilt, when possible.
- **Fixating on a "best chair" centered between speakers** in a sofa
  setup → no one else can sit there. Aim for the best **average**
  across the seating area, not the optimum at one specific point.

## Cross-references

- `references/baffle-and-cabinet-acoustics.md` — boundary loading
  effects share physics with SBIR.
- `references/acoustic-treatment.md` — what to put on the walls.
- `references/room-response-simulation.md` — predict before moving
  speakers and treatment.
- `references/standards-and-targets.md` — what "correct" in-room
  response looks like.
- `references/subwoofers.md` — sub placement is a special case of
  speaker placement, treated separately.
