---
name: parametric-cad
description: Use when driving a parametric CAD tool through an MCP server to design, model, or fabricate physical parts — primarily speaker cabinets and enclosures, also general flat-pack furniture and solid-modeled assemblies. Works with Autodesk Fusion 360 (official Fusion MCP, faust-machines/fusion360-mcp-server, FusionMCP), FreeCAD (neka-nat/freecad-mcp), OnShape, SolidWorks, OpenSCAD, CadQuery, and Build123d-MCP. Covers parameter-driven modeling, sketch constraints, named feature trees, the render→measure→iterate workflow, MCP tool-discovery conventions, common gaps in CAD MCPs (sketch constraints, components / assemblies, 2D drawings, simulation, undo); CAD patterns for speaker cabinets (driver cutouts and flange recesses, port tubes, bracing, baffle layout, roundovers, removable back panels, terminal cup recesses, internal-volume verification); manufacturability and DFM (tolerances per process, kerf compensation, internal corner radii, tool diameter, dog-bone reliefs); process-specific joint design (CNC plywood / MDF joinery — butt / rabbet / dado / miter / domino / lock-miter / finger / pocket-screw; FDM 3D-print joints — snap-fit, captive-nut pocket, heat-set boss, press-fit; SLA threaded posts; laser-cut tab-and-slot, T-slot, finger joints, living hinge; sheet-metal tab-and-bend, PEM nuts; multi-material joints with CTE compensation); manufacturing offsets and as-designed-vs-as-built compensation (kerf, tool radius, finish buildup, FDM shrinkage and first-layer compression, SLA cure, sheet-metal K-factor and spring-back, tolerance stack-up RSS vs worst-case, process-aware parameter pattern); fasteners (M2–M10 metric screws, heat-set and screw-in threaded inserts, wood screws #4–#12, pilot and clearance hole tables); glue (PVA, polyurethane, epoxy, CA), sanding (grit progression), finishing (lacquer, polyurethane, oil, conversion varnish, automotive 2K), neutral-cure silicone for sealing; assemblies, mates and joints, 2D engineering drawings, GD&T, BOM generation; sheet-goods nesting (panel layout, grain orientation, kerf accounting, Deepnest / SVG-Nest workflow); and exports to STEP, STL, IGES, DXF, F3D for CNC routing, laser cutting, waterjet, 3D printing (FDM/SLA/SLS).
---

# Parametric CAD via MCP

Reference for using Claude to drive parametric CAD tools — Fusion 360,
FreeCAD, OnShape, SolidWorks, OpenSCAD, CadQuery, Build123d — through
their Model Context Protocol servers.

The goal of this skill is to **make CAD-by-LLM reliable**. The
failure mode is well-documented: an LLM eagerly fires twenty tool
calls, half of them silently produce wrong geometry, the model is
inscrutable to edit, and the user can't recover. The cure is a tight
loop: plan in words, build with parameters, **verify by rendering or
measuring after every non-trivial step**, and structure the model so
any value can be changed without re-doing the work.

## When this skill applies

Load this skill if any of:

- The user mentions Fusion 360, FreeCAD, OnShape, SolidWorks,
  OpenSCAD, CadQuery, or Build123d.
- MCP tools with names like `create_sketch`, `extrude`, `fillet`,
  `create_parameter`, `export_step` are visible in the conversation.
- The user asks to "design", "model", or "CAD" any 3D part or
  assembly.
- The user is moving from a speaker-design (or other engineering)
  spec into manufacturable geometry.

When combined with the `speaker-design` skill, use the cookbook
`cookbooks/speaker-cabinet-2way.md` as the worked example.

## Routing table

| Topic                                              | Load                                       |
|----------------------------------------------------|--------------------------------------------|
| parameters, sketches, features, naming, rebuilds   | `references/parametric-modeling.md`        |
| MCP tool names, annotations, entity refs, gaps     | `references/mcp-conventions.md`            |
| driver cutouts, ports, bracing, baffle layout      | `references/speaker-cabinet-cad.md`        |
| tolerances, joinery, CNC/laser/3D-print DFM        | `references/manufacturability.md`          |
| M-screws, inserts, pilot holes, glue, sanding, finish | `references/fasteners-and-finishing.md` |
| process-specific joints (FDM, SLA, CNC, laser, metal, snap-fit, tab-and-slot, press-fit, T-slot, multi-material, CTE) | `references/joints-by-process.md` |
| kerf comp, finish buildup, shrinkage, stack-up, as-built offsets | `references/manufacturing-offsets.md` |
| dadoes / rabbets / grooves as assembly guides, self-aligning joinery | `references/assembly-locating-features.md` |
| assemblies, mates, drawings, GD&T, BOM             | `references/assemblies-and-drawings.md`    |
| sheet nesting, kerf, DXF export, grain orientation | `references/sheet-goods-nesting.md`        |
| worked: bookshelf cabinet for the 2-way design     | `cookbooks/speaker-cabinet-2way.md`        |

## Workflow

A reliable CAD-via-MCP session follows a four-phase loop. Don't
short-circuit it — every shortcut costs more time later debugging
geometry you can no longer reason about.

### Phase 1: Plan (in words, before any tool call)

State, in user-facing text:

1. What you're building (one sentence).
2. What parameters drive it (list with values and units).
3. What the build order will be: parameters first, sketches by
   plane, features in dependency order, exports last.
4. What you'll render or measure to verify each step.

Don't call tools yet. If the plan is wrong, fix the plan; tool calls
are expensive (UI thread, slow rebuild, potential corruption).

### Phase 2: Discover available tools

The MCP server is the source of truth for what you can do. Before
calling anything, inventory the tools that are actually loaded — see
`references/mcp-conventions.md` for the discovery pattern. Don't
assume `extrude` exists; the server might call it `extrude_profile`
or expose only `execute_code` and want you to write Python.

If a critical capability is missing (e.g. no `fillet`, no
constraints, no parameters, no assemblies), name it explicitly to the
user and choose a fallback strategy before continuing.

### Phase 3: Build, one feature at a time

For each feature:

1. **Restate the goal** in one sentence ("creating the 12 mm driver
   cutout on the front baffle, located at offset_x, offset_y").
2. **Call the tool(s)** with explicit parameter values, not literals
   wherever the value should be parameter-driven.
3. **Render or measure** to verify (see Phase 4).
4. **Name the result** in code/notes — body name, sketch name —
   because the MCP returns entity handles by **name**, not by opaque
   ID, in most servers.

Resist batching. Five fast tool calls without verification will hide
one wrong feature that's painful to find later.

### Phase 4: Verify (render, measure, snapshot)

Use whatever the MCP exposes for visual + numeric verification:

- `render_view`, `screenshot`, `get_view`, or an equivalent → ensure
  the model looks like what you described.
- `measure`, `inspect`, `get_volume`, `get_bounding_box` → confirm
  numeric properties match the design spec (e.g. internal volume
  matches `V_b`; cabinet OD matches the design dimensions).
- `save_snapshot` / `checkpoint` if the MCP offers it → cheaper than
  relying on `undo`, which **is not guaranteed** to be implemented.

If the verification fails, fix it now. Geometry errors compound:
every downstream feature built on a wrong reference inherits it.

## What's likely missing

CAD MCPs cover a fraction of the host application. Across community
servers (as of 2026), expect these gaps:

| Capability                  | Coverage in typical MCP            |
|-----------------------------|------------------------------------|
| Sketches + primitives        | well covered                       |
| Extrude / revolve / cut      | well covered                       |
| Fillet / chamfer             | usually covered                    |
| Patterns (linear / circular) | hit-or-miss                        |
| **Sketch constraints**       | **often absent or partial**        |
| **User parameters**          | partial — sometimes via separate tool, sometimes only via execute_code |
| **Components and assemblies**| **rarely covered**; no joints/mates |
| **Drawings (2D)**            | **almost never covered**           |
| **Rendering / appearance**   | screenshot only; no PBR materials   |
| **Simulation (FEA/CFD)**     | not covered                        |
| **CAM / toolpaths**          | not covered                        |
| **Undo / redo**              | unreliable — snapshot if available |
| Export STEP / STL            | universally covered                |
| Export F3D / native          | rare                               |

The official Autodesk Fusion MCP closes more of these gaps than
community servers, but treat any single capability as "verify before
relying on it" until proven.

## Pitfalls and red flags

- **Building without parameters.** Hard-coded dimensions guarantee a
  rebuild from scratch when the spec changes by 1 mm. Always declare
  parameters first.
- **Free-hand sketching without constraints.** A sketch with even one
  unconstrained dimension is a time bomb on the next regenerate.
  Fully define every sketch (when constraints are available).
- **Trusting the LLM's spatial intuition.** Always render after a
  feature that adds non-trivial geometry. The LLM cannot see what
  you didn't show it.
- **Re-creating geometry instead of patterning it.** If you find
  yourself drawing two of the same hole, that's a missing pattern
  feature, not work. Use circular/rectangular pattern (or, in
  Python-style MCPs, a `for` loop with parameters).
- **Mixing units silently.** Most MCPs default to mm; some accept
  inches in tool args; some honor a document-level unit. State your
  units in every tool call.
- **Assuming undo works.** Build snapshots into the workflow before
  destructive operations.
- **Asking the LLM to "fix" a broken model.** Often easier to rebuild
  from parameters than to debug a corrupted feature tree. The
  parametric structure is the safety net — use it.

## Output discipline

- Tool calls should pass values from user-named parameters wherever
  possible, not from inline literals.
- After each tool call, say in one sentence what the result was and
  what you'll verify next.
- Render after groups of features, not after every single tool call —
  but always before exporting or finalizing.
- When exporting, state the format, the units, and the intended
  downstream use (CNC, laser, 3D print, FEA).
