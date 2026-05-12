# claude-speaker-design

A Claude Code plugin bundling two composable skills for loudspeaker
engineering — from cone materials and motor structures through
enclosure acoustics, room interaction, and the physics of sound, and
from acoustic specifications into manufacturable CAD via MCP servers.

## Install

### As a Claude Code plugin (recommended)

Add this repo as a plugin marketplace and install:

```
/plugin marketplace add https://github.com/chawasit/claude-speaker-design
/plugin install claude-speaker-design@claude-speaker-design
```

The plugin name and the marketplace name are both `claude-speaker-design`.

To verify it loaded:

```
/plugin list
```

Both skills (`speaker-design`, `parametric-cad`) become available.
Claude auto-loads them by topic relevance per the `description`
field in each skill's frontmatter.

### Alternative: install skills manually

If you'd rather not use the plugin layer, clone the repo and symlink
each skill folder into a directory Claude scans for skills:

```bash
git clone https://github.com/chawasit/claude-speaker-design.git
ln -s "$(pwd)/claude-speaker-design/skills/speaker-design"  ~/.claude/skills/speaker-design
ln -s "$(pwd)/claude-speaker-design/skills/parametric-cad"   ~/.claude/skills/parametric-cad
```

Either approach works; the plugin path is the canonical install.

## Layout

```
claude-speaker-design/
├── .claude-plugin/
│   ├── plugin.json                       # plugin manifest
│   └── marketplace.json                  # marketplace entry for git distribution
├── README.md
└── skills/
    ├── speaker-design/                   # acoustic engineering skill
    │   ├── SKILL.md
    │   ├── references/                   # 22 topical reference docs
    │   ├── tools/                        # 9 Python calculation helpers
    │   └── cookbooks/                    # 5 worked end-to-end designs
    └── parametric-cad/                   # CAD-via-MCP skill
        ├── SKILL.md
        ├── references/                   # 7 topical reference docs
        └── cookbooks/                    # 1 worked end-to-end CAD build
```

## What the skills cover

### `speaker-design`

Triggered when a conversation touches loudspeaker design, driver
parameters, enclosure tuning, crossover networks, room acoustics,
horns, measurement, DSP/active processing, listening setup, or
acoustic treatment.

References:
- **Physics & properties**: `physics-of-sound`, `acoustic-properties`,
  `thiele-small`, `time-domain`
- **Drivers & cabinets**: `driver-types`, `materials`, `phase-plugs`,
  `enclosures`, `closed-box-geometry`,
  `baffle-and-cabinet-acoustics`, `horns-and-waveguides`,
  `point-source-and-line-arrays`
- **Subsystems**: `crossovers`, `subwoofers`, `dsp-and-active`
- **Setup & measurement**: `measurement`, `listening-setup`,
  `acoustic-treatment`, `room-response-simulation`,
  `standards-and-targets`
- **Special**: `headphones`
- **Navigation**: `glossary`, `bibliography`

Tools (all CLI Python, runnable from the skill directory):
- T/S extraction from added-mass measurement
- Sealed and ported box alignment design (Small-tabulated)
- Port length with chuffing-velocity check
- Linkwitz-Riley crossover values + Zobel
- Displacement-limited SPL prediction
- Room mode enumeration with Schroeder frequency
- Group delay vs audibility threshold
- Baffle step + edge diffraction estimator

Cookbooks (end-to-end design walkthroughs):
- Ported 6.5" + 1" bookshelf, LR4
- 12" sealed subwoofer with Linkwitz transform
- 10" + 5" + 1" three-way tower
- Open-baffle H-frame dipole
- DSP-active studio monitor with waveguide

### `parametric-cad`

Triggered when a conversation involves driving a parametric CAD tool
through an MCP server — Fusion 360 (official Fusion MCP,
faust-machines, FusionMCP), FreeCAD (neka-nat), OnShape, SolidWorks,
OpenSCAD, CadQuery, or Build123d.

References:
- `parametric-modeling` (parameters, sketches, features, rebuilds)
- `mcp-conventions` (tool naming, annotations, server families)
- `speaker-cabinet-cad` (driver cutouts, ports, bracing, baffles)
- `manufacturability` (tolerances, joinery, kerf, DFM)
- `fasteners-and-finishing` (M-screws, inserts, glue, finishes)
- `assemblies-and-drawings` (assemblies, mates, drawings, GD&T)
- `sheet-goods-nesting` (panel layout, kerf, DXF export)

Cookbook:
- End-to-end CAD for the bookshelf design, consuming the acoustic
  spec from `speaker-design`

## How the skills compose

1. Use `speaker-design` to specify the speaker: driver T/S → alignment
   → port → crossover → baffle layout → cabinet dimensions.
2. Use `parametric-cad` to turn that spec into a CAD model via your
   loaded MCP server — produces STEP and DXF for fabrication.
3. Return to `speaker-design` for measurement verification, listening
   setup, and acoustic treatment of the finished room.

## License

MIT
