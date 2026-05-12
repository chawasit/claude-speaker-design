# claude-speaker-design

A Claude skill for designing loudspeakers — from cone materials and motor
structures to enclosure acoustics and the underlying physics of sound.

The skill lives in [`speaker-design/`](./speaker-design/) and is loaded by
Claude when a conversation touches loudspeaker design, driver parameters,
enclosure tuning, crossover networks, room acoustics, or related topics.

## Layout

```
speaker-design/
├── SKILL.md                       # entry point, loaded first
├── references/
│   ├── physics-of-sound.md        # waves, SPL, room modes, radiation
│   ├── acoustic-properties.md     # frequency response, directivity, distortion
│   ├── thiele-small.md            # driver small-signal parameters
│   ├── enclosures.md              # sealed, ported, bandpass, horn, TL
│   ├── crossovers.md              # filter topologies, slopes, alignment
│   ├── materials.md               # cones, surrounds, magnets, cabinets
│   ├── driver-types.md            # dynamic, compression, ribbon, AMT, ESL...
│   ├── measurement.md             # REW, gating, T/S extraction, impedance
│   ├── subwoofers.md              # LF-specific design, multi-sub, integration
│   ├── dsp-and-active.md          # active speakers, FIR/IIR, room correction
│   ├── baffle-and-cabinet-acoustics.md  # baffle step, diffraction, panel modes
│   ├── closed-box-geometry.md     # how box geometry shapes the driver response
│   ├── room-response-simulation.md # modal sum, image, FEM/FDTD, multi-sub sim
│   └── horns-and-waveguides.md    # flare profiles, OS waveguide, CD, Hornresp
├── tools/                         # executable calculation helpers
│   ├── ts_from_added_mass.py
│   ├── sealed_box.py
│   ├── ported_box.py
│   ├── port_length.py
│   ├── crossover_lr.py
│   └── xmax_spl.py
└── cookbooks/                     # worked end-to-end design examples
```

## Install

Copy or symlink `speaker-design/` into a location Claude scans for skills
(e.g. `~/.claude/skills/` or a project's `.claude/skills/`).
