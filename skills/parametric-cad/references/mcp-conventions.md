# MCP Conventions for Parametric CAD

What a Claude-driving-CAD session actually looks like at the protocol
layer, and how to write code that works across the heterogeneous set
of CAD MCP servers that exist in the wild (as of 2026).

## Two server families

CAD MCPs fall into two architectural schools. The skill applies to
both; the tactics differ.

### A. Granular per-operation tools (the dominant pattern)

One MCP tool per CAD operation. Tool names are dominantly
**snake_case**, occasionally PascalCase (ArchimedesCrypto's
fusion360-mcp-server). Typical surface area for a Fusion 360 server:

```
# Scene / Query
list_components, list_bodies, list_sketches, list_parameters,
get_view, screenshot, get_bounding_box, get_volume, get_mass,
get_origin

# Parameters
create_parameter, change_parameter, list_parameters, delete_parameter

# Sketches
create_sketch, draw_line, draw_arc, draw_circle, draw_rectangle,
draw_polygon, draw_spline, add_constraint, add_dimension,
project_geometry

# Features (additive)
extrude, revolve, sweep, loft

# Features (subtractive)
cut, hole, shell

# Modify
fillet, chamfer, draft, scale, move_face

# Patterns
rectangular_pattern, circular_pattern, mirror

# Boolean
combine, intersect, subtract

# Components / Bodies
create_component, copy_body, rename_body, delete_body

# Construction geometry
create_plane, create_axis, create_point

# Export
export_step, export_stl, export_iges, export_obj, export_dxf,
save_file

# History
undo, redo, save_snapshot, restore_snapshot
```

faust-machines/fusion360-mcp-server is the most complete current
reference (~84 tools at last count) and the closest thing to a
de-facto convention.

### B. Execute-code wrappers

A small number of tools that accept code (Python typically):

```
create_document, execute_code, get_view, get_objects,
edit_object, delete_object, insert_part_from_library
```

The LLM writes Python that runs in-process against the CAD's API
(adsk.fusion, FreeCAD.ActiveDocument, cadquery.Workplane,
build123d.BuildPart). neka-nat/freecad-mcp, cadquery-mcp-server, and
pzfreo/build123d-mcp follow this pattern.

**Tactically**: write self-contained Python that declares parameters
at the top, builds the model, and returns. Don't rely on session
state — many execute-code MCPs scope the session per call.

## Tool discovery

Before relying on a specific tool, **list what the server exposes**.
The CAD MCP's tool list is visible in the system prompt at session
start. Look for the namespace prefix the server uses:

- Official Fusion MCP: `mcp__fusion__*`
- faust-machines: `mcp__fusion360-mcp__*`
- neka-nat FreeCAD: `mcp__freecad-mcp__*`
- Build123d: `mcp__build123d__*`

If you don't see the expected prefix, the MCP isn't loaded; tell the
user and stop. Don't fabricate tool calls — they'll error and confuse
the conversation.

If the MCP is loaded but a critical tool you expected is missing,
adapt:

| Want                  | Common fallback                                    |
|-----------------------|----------------------------------------------------|
| `create_parameter`    | put parameters inline in `execute_code`            |
| `add_constraint`      | drive sketch geometry from parameter math directly |
| `circular_pattern`    | loop in `execute_code`; or manual repeated cuts    |
| `fillet`              | model with sketch-level radii on lines             |
| `create_component`    | work with multiple bodies in one component         |
| `export_step`         | export STL, accept the precision loss              |

## MCP annotations: read the hints

The Model Context Protocol exposes three boolean hints per tool that
matter for CAD work:

- `readOnlyHint: true` — tool doesn't mutate the document.
  Examples: `list_*`, `get_*`, `screenshot`.
- `destructiveHint: true` — tool deletes geometry or makes an
  irreversible change.
  Examples: `cut`, `delete_body`, `shell`.
- `idempotentHint: true` — calling twice produces the same result as
  calling once.

If the MCP marks a tool `destructiveHint`, snapshot first or be
certain. Most server implementations are correct about these
annotations; trust them as primary signals.

## Entity references: by name, not opaque ID

CAD MCPs almost universally return **named handles** to created
entities, not opaque numeric IDs:

```
result = create_sketch(plane="XY", name="sketch_baffle_profile")
# result.name == "sketch_baffle_profile"

result = extrude(profile="sketch_baffle_profile", distance=350,
                 name="extrude_main_shell")
# result.body_name == "extrude_main_shell"
```

If you don't name the entity, the server typically auto-names it
(`Sketch1`, `Body1`, `Extrude1`). Subsequent references to those
auto-names work, but they're unstable: any reorder or rename breaks
downstream calls.

**Always pass a meaningful `name=` argument when the tool supports
it.** Use the same names you'd use in the parameter table — this is
the design intent surfacing through the entity tree.

## Sync, async, and the UI thread

Fusion 360, FreeCAD, and most desktop CAD apps execute their API
calls on the **UI thread**. CAD MCPs typically:

1. Receive an MCP call (background thread).
2. Post a task to the UI thread.
3. Wait for the task to complete (with a timeout, usually 30 s).
4. Return the result.

Practical consequences:

- **Don't fire many tool calls in parallel.** Even if you can, the
  server will serialize them. Sequential is the only correct mental
  model.
- **Long operations time out.** Generative design, large patterns,
  or simulation calls may exceed the timeout. If a call hangs,
  assume the operation is still running on the host; don't retry.
- **The host UI may freeze briefly** during each tool call. This is
  normal.

In execute-code MCPs (CadQuery, Build123d), the script runs in-
process and can be much faster — no UI hop. They're a good choice
for batch parametric exploration.

## Errors

Modern servers return errors with the MCP `isError=true` flag and a
structured payload. Older or simpler servers raise an exception that
ends up in the tool result as a stack trace.

When a tool errors, common causes (rank-ordered):

1. **Reference to nonexistent entity** — typo in a name, or the
   entity was renamed/deleted upstream.
2. **Sketch is open / unfinished** — many features require the
   sketch to be closed first; some MCPs expose `finish_sketch` or
   `close_sketch`.
3. **Geometry is degenerate** — fillet radius too large for the
   edge, hole bigger than the face, etc.
4. **Parameter not yet defined** — referencing a user parameter the
   server hasn't ingested.
5. **Out-of-band: server is busy** — host CAD has a modal dialog
   open, or a previous tool call is still rendering.

Don't paper over errors. Read the message, fix the cause, retry. If
the error message is uninformative, **render the current state** —
seeing the model often makes the issue obvious.

## Verification: render → measure → snapshot

The render-measure-iterate loop is the closest thing to a community
convention for LLM-driven CAD. The Build123d MCP's `default_prompt.md`
makes it explicit; most other servers leave it to the LLM.

### Rendering

Tools to use (any of, depending on server):
- `screenshot`, `render_view`, `get_view`, `take_picture`
- `export_image`

Render after:
- Each major feature group (not every tool call — too noisy).
- Before exporting.
- When the user asks "what does it look like now?".
- After any error, to inspect the partially-built state.

What to render:
- **Isometric** is the workhorse — shows depth + all three principal
  views in one image.
- **Front / right / top** for verifying flat-face geometry like
  driver cutouts on a baffle.
- **Section / cross-section** for verifying internal geometry like
  bracing, port channels, internal volume.

### Measuring

Tools to use:
- `measure`, `get_volume`, `get_mass`, `get_bounding_box`,
  `get_surface_area`, `inspect`
- `get_distance_between` if available; otherwise compute from
  bounding boxes.

Measure after:
- A feature whose dimensions you care about numerically (e.g. cabinet
  internal volume matches `V_b`).
- A pattern (count + spacing).
- An export (file size sanity check).

### Snapshots

Tools to use:
- `save_snapshot`, `checkpoint`, `save_file` with a versioned name.

Snapshot before:
- Any `destructiveHint` operation.
- Any pattern over more than 4 instances.
- Any boolean operation that combines bodies.

Why: `undo` is **not** universally implemented in CAD MCPs. The
Build123d MCP exposes `save_snapshot`/`restore_snapshot`/`diff_snapshot`
as the recommended idiom; treat it as the gold standard and emulate
when other servers offer equivalents.

## Common server-specific notes

### Autodesk Fusion (official)

- Two MCPs: **Fusion MCP** (local, drives Fusion) and **Fusion Data
  MCP** (remote, queries APS data).
- Covers a broader surface than community servers; most likely to
  have parameters, components, and proper export.
- Documents-level operations require Fusion to be open and logged in.

### faust-machines/fusion360-mcp-server

- Best community reference for the granular per-operation pattern.
- snake_case, MCP annotations, prebuilt prompt scaffolds.
- TCP socket bridge to a Fusion add-in; 30 s tool timeout.

### neka-nat/freecad-mcp

- Execute-code style (Python against FreeCAD.ActiveDocument).
- Most popular FreeCAD MCP (~600-900 stars).
- Document state is persistent across calls in a session.

### pzfreo/build123d-mcp

- Execute-code style + verification loop tooling.
- 11 tools including `execute`, `render_view`, `measure`, `export`,
  `save_snapshot`, `restore_snapshot`, `diff_snapshot`.
- The most LLM-friendly design currently in the CAD MCP space.

### CadQuery MCP servers

- Execute-code style. Code is Python with the CadQuery DSL.
- Some servers only generate-and-verify, not execute; check whether
  the loaded one runs the code or just lints it.

### OpenSCAD MCP

- Generate OpenSCAD source; the server renders to STL.
- No interactive editing — every change is a script regeneration.
- Good for procedural parts, awkward for assemblies.

## A working tool-call template

For granular MCPs, your first three calls should typically be:

```
1. list_parameters()           # see what already exists
2. create_parameter("baffle_w", "200 mm")   # add design parameters
3. create_parameter(...)        # one per dimension
```

Then sketches, then features, then verification. Resist starting
with `extrude` — without parameters and named sketches first, you're
modeling by accident.

For execute-code MCPs, your first call is `execute_code` with the
full parametric script. Verify with `render_view` and `measure`,
then iterate by editing the script — not by issuing edit commands
against the model state.
