# claude-speaker-design

Claude skills for designing loudspeakers — from cone materials and
motor structures through enclosure acoustics, room interaction, and
the physics of sound, and from acoustic specifications into
manufacturable CAD via MCP servers.

Two skills live here, designed to work together:

## `speaker-design/` — the acoustic & engineering knowledge

Triggered when a conversation touches loudspeaker design, driver
parameters, enclosure tuning, crossover networks, room acoustics,
horns, measurement, DSP/active processing, listening setup, or
acoustic treatment.

```
speaker-design/
├── SKILL.md                              # entry: routing + workflow + pitfalls
├── references/
│   ├── physics-of-sound.md               # waves, SPL, room modes, radiation
│   ├── acoustic-properties.md            # FR, directivity, distortion, excursion
│   ├── thiele-small.md                   # driver small-signal parameters
│   ├── enclosures.md                     # sealed, ported, bandpass, horn, TL
│   ├── crossovers.md                     # filter topologies, slopes, alignment
│   ├── materials.md                      # cones, surrounds, magnets, cabinets
│   ├── driver-types.md                   # dynamic, compression, ribbon, AMT, ESL...
│   ├── measurement.md                    # REW, gating, T/S extraction, impedance
│   ├── subwoofers.md                     # LF-specific design, multi-sub, integration
│   ├── dsp-and-active.md                 # active speakers, FIR/IIR, room correction
│   ├── baffle-and-cabinet-acoustics.md   # baffle step, diffraction, panel modes
│   ├── closed-box-geometry.md            # how box geometry shapes driver response
│   ├── room-response-simulation.md       # modal sum, image, FEM/FDTD, multi-sub sim
│   ├── horns-and-waveguides.md           # flare profiles, OS waveguide, CD, Hornresp
│   ├── phase-plugs.md                    # compression driver + cone phase plugs
│   ├── point-source-and-line-arrays.md   # coaxial, line array, CBT, splay
│   ├── listening-setup.md                # placement, toe-in, height, first reflections
│   ├── acoustic-treatment.md             # absorbers, bass traps, diffusers, T_60
│   ├── standards-and-targets.md          # CTA-2034 spinorama, Harman target, IEC
│   ├── time-domain.md                    # impulse / step response, group delay
│   ├── headphones.md                     # over-ear, IEM, planar, Harman target
│   ├── glossary.md                       # terms across both skills, indexed
│   └── bibliography.md                   # foundational papers, books, web resources
├── tools/                                # executable calculation helpers
│   ├── ts_from_added_mass.py             # T/S from impedance + added-mass
│   ├── sealed_box.py                     # sealed-box alignment from T/S
│   ├── ported_box.py                     # ported alignment (B4/QB3/C4 tabulated)
│   ├── port_length.py                    # port length + chuffing-velocity check
│   ├── crossover_lr.py                   # LR2 / LR4 component values + Zobel
│   ├── xmax_spl.py                       # displacement-limited SPL vs frequency
│   ├── room_modes.py                     # axial / tangential / oblique room modes
│   ├── group_delay.py                    # filter group delay vs audibility threshold
│   └── diffraction_olson.py              # baffle step + edge diffraction estimator
└── cookbooks/
    ├── bookshelf-2way.md                 # ported 6.5"+1" LR4 two-way
    ├── sealed-subwoofer.md               # 12" sealed sub + Linkwitz transform
    ├── three-way-tower.md                # 10"+5"+1" floor-stander
    ├── open-baffle-dipole.md             # H-frame dipole + boxed LF
    └── active-studio-monitor.md          # DSP-active 6.5"+1" with waveguide
```

## `parametric-cad/` — drives CAD MCP servers (Fusion 360, FreeCAD, Build123d, ...)

Triggered when a conversation involves driving a parametric CAD tool
through an MCP server. Covers the disciplined render→measure→iterate
workflow, parameter-driven modeling philosophy, MCP tool-discovery
patterns, common gaps in CAD MCPs, speaker-cabinet CAD patterns,
hardware/finishing, assemblies/drawings, and sheet-goods nesting.

```
parametric-cad/
├── SKILL.md                              # entry: when-to-use, workflow, pitfalls
├── references/
│   ├── parametric-modeling.md            # parameters, sketches, features, rebuilds
│   ├── mcp-conventions.md                # tool naming, annotations, server families
│   ├── speaker-cabinet-cad.md            # driver cutouts, ports, bracing, baffles
│   ├── manufacturability.md              # tolerances, joinery, kerf, DFM
│   ├── fasteners-and-finishing.md        # M-screws, inserts, glue, finishing
│   ├── assemblies-and-drawings.md        # assemblies, mates, drawings, GD&T
│   └── sheet-goods-nesting.md            # panel layout, kerf, DXF export
└── cookbooks/
    └── speaker-cabinet-2way.md           # end-to-end CAD for the bookshelf design
```

## How they compose

The two skills compose naturally:

1. Use `speaker-design` to specify the speaker (driver T/S → alignment
   → port → crossover → baffle layout → cabinet dimensions). Many
   cookbooks walk this end-to-end.
2. Use `parametric-cad` to turn that specification into a CAD model
   via whatever Fusion 360 / FreeCAD / Build123d MCP is loaded. The
   bookshelf CAD cookbook consumes the same spec and produces the
   parametric model + DXF/STEP exports.
3. After the build, return to `speaker-design` for measurement
   verification, listening setup, and acoustic treatment.

## Install

Copy or symlink either or both skill folders into a location Claude
scans for skills (e.g. `~/.claude/skills/` or a project's
`.claude/skills/`). The skills are independent — you can use either
one without the other — but used together is the typical workflow
for a complete design.
