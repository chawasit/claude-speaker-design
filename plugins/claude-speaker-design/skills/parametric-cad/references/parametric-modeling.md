# Parametric Modeling

The discipline that separates "an LLM that draws boxes in CAD" from
"an LLM that delivers a manufacturable design that can be edited at
3am the day before fabrication."

## The first commandment: parameters before geometry

A parametric model is one where every dimension that **could change**
is named and referenced from a parameter, not embedded as a literal.
This is the single highest-leverage practice in CAD-via-LLM workflows
because:

- An LLM that hard-codes dimensions has to **rebuild from scratch**
  when the user says "make it 5 mm taller". An LLM that uses
  parameters changes one line.
- A parametric model is **legible**: a human or another agent can
  read the parameter table and understand the design intent without
  parsing the feature tree.
- A parametric model is **testable**: change a parameter, regenerate,
  measure — if the model rebuilds correctly and the measurement
  matches, the model is robust.

### Naming convention

Use descriptive, snake_case parameter names with units in the value,
not the name:

```
# Good
baffle_w        = 200 mm
panel_thickness = 18 mm
driver_cutout_d = 152 mm
port_dia        = 60 mm
internal_vb     = 12.3 L

# Bad
W = 200             # what is W?
thickness18 = 18    # unit in the name
diam2 = 152         # no semantics
```

Group related parameters with a common prefix so they sort together
in the parameter table (`driver_*`, `port_*`, `panel_*`, `internal_*`).

### Derived parameters

Compute downstream values from upstream ones, don't duplicate:

```
# Upstream (user inputs)
baffle_w         = 200 mm
baffle_h         = 350 mm
depth            = 280 mm
panel_thickness  = 18 mm

# Derived (formulas)
internal_w       = baffle_w - 2 * panel_thickness     # 164 mm
internal_h       = baffle_h - 2 * panel_thickness     # 314 mm
internal_d       = depth - 2 * panel_thickness        # 244 mm
internal_vol     = internal_w * internal_h * internal_d  # 12.57 L gross
```

Now the user can change `panel_thickness` from 18 to 25 mm and the
internal volume updates automatically — no manual recompute, no
hidden references to "18 mm" buried five features deep.

In MCPs without a parameter system (rare but real — some early
servers only have geometry tools), achieve the same effect by keeping
parameters in Python locals at the top of an `execute_code` call.

## Sketches: fully constrained, named, minimal

A sketch is **fully constrained** when every entity's position and
size is unambiguously determined by dimensions and geometric
constraints. Most CAD packages indicate this visually (black lines
for constrained, blue for free in Fusion 360; green vs other-color
in SolidWorks). Always finish in the fully-constrained state.

**Why it matters**: a partially constrained sketch contains "free
play" — when a parameter changes upstream, the sketch may rebuild
with the unconstrained entity in an arbitrary new position. The
model regenerates without error but produces wrong geometry.

### MCPs without exposed constraints

Several community CAD MCPs (as of 2026) lack sketch constraint tools.
They give you `draw_line`, `draw_circle`, `draw_rectangle`, but no
`add_constraint` or `add_dimension`. In that case:

- Use **construction geometry** at the origin to anchor everything
  (centerline, center point).
- Specify coordinates as **expressions of parameters**, not literals.
  Even without formal constraints, parameter-driven coordinates
  preserve design intent: if a downstream feature uses the same
  parameter expression, it stays aligned.
- Prefer rectangles defined by two corner parameters (corner1, corner2)
  to rectangles defined by center + width + height — fewer chances
  for a sign flip.

### Sketch naming

Name every sketch after **its purpose**, not its content:

```
sketch_baffle_profile
sketch_driver_cutouts
sketch_port_centerline
sketch_internal_brace
```

Not `Sketch1`, `Sketch2`. Many MCPs return entity handles by name; if
all sketches are `Sketch1`/`Sketch2`/etc., subsequent calls are
ambiguous and rebuilds become impossible.

### Sketch minimalism

One sketch = one purpose. Don't combine the baffle profile, driver
cutouts, and port location into one sketch — they have different
edit lifecycles and different parameters. If the user wants to swap
to a different driver, you should only need to edit
`sketch_driver_cutouts`, leaving the baffle profile alone.

## Feature ordering: parents before children

The CAD timeline (or feature tree) is a directed acyclic graph.
Every feature has parents (the entities it references) and children
(the features that reference it). When a parent regenerates, all
children rebuild against the new parent geometry.

### Order of operations

1. **Sketches that define datum geometry** (centerlines, reference
   points).
2. **Bulk solid features**: extrude the main body, the cabinet shell.
3. **Subtractive features**: driver cutouts, port hole, terminal cup
   cutout.
4. **Reinforcement / additive features**: bracing, mounting bosses.
5. **Cosmetic features**: fillets, chamfers, roundovers.
6. **Component splits**: separate the back panel from the main shell
   if you need a removable back.
7. **Exports**.

Cosmetic features come **last** so they don't interfere with
subtractive ones — a fillet on an edge that's about to be removed by
a later cut wastes computation and may fail to regenerate.

### When the order is wrong, the symptom is "rebuild fails"

If a parameter change causes a regenerate error, the cause is almost
always feature ordering: a child references a parent's edge that
moved or vanished. The fix is to reorder, not to fix the child.

## Bodies vs components

- **Body**: a solid lump of geometry inside a single component. Live
  inside one part file or document.
- **Component**: a self-contained part with its own coordinate system
  and feature tree. Components can be reused in assemblies.

For a single-cabinet model, work in **bodies inside one component**.
For multi-cabinet or multi-driver products (a stereo pair, a
multi-driver setup, modular speaker line), use components.

Most CAD MCPs handle bodies cleanly but stumble on components — be
aware that switching contexts may silently fail and check via
verification render.

## Naming the timeline

Every feature deserves a name that reflects what it does:

```
extrude_main_shell
shell_inset_internal_volume
cut_driver_woofer
cut_driver_tweeter
cut_port_through_back
extrude_brace_horizontal
fillet_outer_vertical_edges
split_back_panel
```

Many MCPs return numeric IDs by default (Extrude1, Cut2) — rename
them post-creation if the MCP exposes a `rename` tool. The
investment pays back the first time you debug a failed rebuild.

## Rebuild safety

A robust parametric model should **rebuild from a blank document**
given the parameter list and the script. If you can't reproduce it
from a clean state, the model has hidden dependencies on entities
created out of sequence.

Test: change three parameters by ±10 % each. The model should
regenerate cleanly. If any rebuild fails, the model is fragile;
investigate the failing feature's parent references and lock them
down (use the parameter, not the screen-picked edge).

## When the MCP only has `execute_code`

A handful of MCPs (CadQuery, FreeCAD's neka-nat in code-mode,
Build123d) accept Python source code rather than per-operation tool
calls. The principles are the same, just expressed in language:

```python
# === Parameters (always at the top) ===
baffle_w        = 200
baffle_h        = 350
depth           = 280
panel_thickness = 18
driver_cutout_d = 152

# === Derived ===
internal_w = baffle_w - 2 * panel_thickness
internal_h = baffle_h - 2 * panel_thickness
internal_d = depth   - 2 * panel_thickness

# === Geometry ===
shell = (Workplane("XY")
         .box(baffle_w, baffle_h, depth)
         .faces(">X").shell(-panel_thickness)
         .faces(">Z").workplane()
         .center(0, baffle_h * 0.1)
         .circle(driver_cutout_d / 2)
         .cutThruAll())
```

In execute-code MCPs, the script **is** the parametric model. Save
it; the user can re-run with different parameters at will.

## Anti-patterns to avoid

- **Magic numbers**: `move(38.7, 0, 0)` — what is 38.7? Replace with
  `move(tweeter_offset_x, 0, 0)`.
- **Implicit unit conversions**: passing inches to a millimeter-mode
  document. State the unit in every tool call.
- **Reusing one sketch for multiple features**: the second feature
  that consumes the sketch will fail when the first one consumes the
  profile. Re-create the sketch or use a copy.
- **Hidden references**: drawing a sketch on a face whose orientation
  depends on a fillet that hasn't been added yet. Anchor sketches to
  origin planes, not feature faces, when possible.
- **Mixing global and component parameters**: a parameter defined
  inside a component is invisible from outside it. Decide on the
  scope and keep it consistent.

## A checklist for "is this a real parametric model"

Before declaring the model done, verify:

- [ ] Every dimension in the model traces back to a named parameter
      or a formula on named parameters.
- [ ] Every sketch is named after its purpose.
- [ ] Every feature is named after its purpose.
- [ ] No sketch has unconstrained entities (if the MCP supports
      constraints).
- [ ] Changing each top-level parameter by ±10 % causes a clean
      rebuild.
- [ ] The model regenerates from a blank document via the saved
      script.
- [ ] Internal/cabinet volume is verified by measurement against the
      design `V_b`.
- [ ] Exports (STEP, STL) open in a downstream tool without warnings.

If any box is unchecked, the model is fragile; don't ship it.
