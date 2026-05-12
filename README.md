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
└── references/
    ├── physics-of-sound.md        # waves, SPL, room modes, radiation
    ├── acoustic-properties.md     # frequency response, directivity, distortion
    ├── thiele-small.md            # driver small-signal parameters
    ├── enclosures.md              # sealed, ported, bandpass, horn, TL
    ├── crossovers.md              # filter topologies, slopes, alignment
    └── materials.md               # cones, surrounds, magnets, cabinets
```

## Install

Copy or symlink `speaker-design/` into a location Claude scans for skills
(e.g. `~/.claude/skills/` or a project's `.claude/skills/`).
