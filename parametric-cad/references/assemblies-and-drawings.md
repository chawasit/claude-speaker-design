# Assemblies and Drawings

The two CAD capabilities most commonly **missing** from community
MCP servers but **present** in the underlying CAD tool. When you
have access to them — through the official Fusion MCP, advanced
community servers, or by writing native code via an `execute_code`
tool — these patterns apply.

This file is shorter and more conditional than other CAD references
because the underlying tools vary widely. The principles are
universal; the syntax is per-MCP.

## 1. Bodies vs components vs parts vs assemblies

A loose hierarchy across CAD tools:

| Concept    | In Fusion 360       | In SolidWorks       | In FreeCAD         |
|------------|---------------------|---------------------|---------------------|
| Solid lump | Body                 | Body in a Part      | Solid              |
| Reusable group of bodies + features | Component | Part            | Body / Part        |
| Multiple components joined | Assembly       | Assembly            | Assembly           |

For a **single speaker cabinet**, work in **bodies inside one
component**. For a **stereo pair** or a **modular system** (driver +
sub + crossover module), use multiple components inside one assembly.

## 2. When to use an assembly

- The product has **multiple manufactured parts** that fit together
  (left + right speaker; main cabinet + removable back; speaker +
  stand).
- You want to **simulate motion** (which doesn't apply to passive
  speakers but does apply to driver mechanisms in CAD).
- You want **per-part BOM** with quantity counts.
- You want **mate** constraints (alignment between parts, gap
  tolerances) verified by the CAD.

For a single fixed-geometry bookshelf, you don't need an assembly —
a single component with multiple bodies (main shell, removable back,
brace) is sufficient.

## 3. Mate / joint types

The geometric constraints that hold parts together in an assembly:

| Constraint    | Geometry             | Use                                  |
|---------------|----------------------|---------------------------------------|
| Coincident    | Face-to-face         | Panel touching panel                  |
| Concentric    | Axis-to-axis         | Bolt in hole                         |
| Parallel      | Axis-axis or face-face | Brace parallel to bottom panel     |
| Perpendicular | Axis-axis or face-face | Brace perpendicular to side panels |
| Distance      | Two faces with gap   | Air gap between brace and floor       |
| Angle         | Two faces            | Tilted baffle, slanted front          |
| Tangent       | Cylinder-face        | Roundover-to-face                     |
| Rigid / fix   | All DOFs locked      | Bolt locked in place                  |

For a removable back-panel assembly: rigid constraint of the back
panel to the screws, concentric of each screw to its hole, coincident
of screw head to back panel face. The cabinet shell is the
**stationary** reference (fixed at origin).

## 4. Assembly best practices

### Use one origin

Every component should be created with **the same origin** as the
parent assembly. Don't drift origins between components — when you
later mate things, drift causes mysterious constraint failures.

### Build the master assembly top-down

For a cabinet + stand + speaker system:

1. Create the assembly (empty).
2. Define a **skeleton sketch** with key reference geometry (cabinet
   exterior dimensions, stand height, distance between cabinet and
   floor).
3. Create each component (cabinet, stand, top plate, …) **referenced
   to the skeleton** so changing the skeleton propagates to all
   components.

This is "**master-model**" or "**top-down**" design. Robust for
parametric edits, but more work to set up.

### Or work bottom-up for one-off projects

For a single-prototype build:

1. Design each component standalone.
2. Insert all components into an assembly.
3. Mate them together using their geometry.

Simpler; doesn't propagate parameter changes as cleanly.

### Naming and the BOM

Every component needs a name that means something in the BOM:

```
shell_main           material: 18 mm MDF       quantity: 1
shell_back           material: 18 mm MDF       quantity: 1
brace_horizontal     material: 18 mm MDF       quantity: 1
port_tube            material: 3D-printed PETG  quantity: 1
driver_woofer        manufacturer reference     quantity: 1
driver_tweeter       manufacturer reference     quantity: 1
hardware_M4_socket_cap material: A2 stainless    quantity: 8
```

The BOM tool of most CAD packages auto-generates from this. Fusion's
`get_bom` (when exposed via MCP) or SolidWorks' BOM table makes this
trivial.

## 5. Driver bodies in assemblies

You often want to **import** a manufacturer's driver STEP file into
the assembly, both to subtract its volume from the enclosure and to
visualize fit:

1. Import the driver STEP (`import_step` or `insert_component`).
2. Mate the driver's flange face **coincident** with the baffle face,
   and **concentric** with the driver cutout.
3. Use `cut_with_body` (boolean subtract) to remove the driver's
   back-side volume from the cabinet's internal volume — for
   accurate `V_b` measurement.

Most major manufacturers (Scan-Speak, SEAS, Faital Pro, Eminence)
publish STEP files. Smaller ones may not; for those, model a
simplified cylinder of approximate basket diameter and back-magnet
volume.

## 6. Drawings (2D)

A drawing is a flat 2D dimensioned view derived from the 3D model.
Required for:

- Sending to a fabricator who works from paper or PDF.
- Documenting manufacturing intent and tolerances.
- Customer review / sign-off.

### Drawing essentials

A useful cabinet drawing includes:

1. **Three principal views** (front, side, top) of the assembled
   cabinet, dimensioned.
2. **Sectional view** through the cabinet's vertical center showing
   internal bracing and port.
3. **Exploded view** showing how panels assemble.
4. **Driver-cutout detail** (close-up, with dimensions for
   manufacturer's cutout pattern).
5. **BOM table** of all parts, materials, and quantities.
6. **Notes** on tolerances, finish, joinery method, special features.
7. **Title block**: project name, scale, date, author, revision.

Each view should be dimensioned to **only** the features that need
to be made or verified. Over-dimensioning creates conflicts when
parametric edits occur.

### Tolerances on drawings

A drawing-level **general note** sets default tolerances:

```
GENERAL TOLERANCES (UNLESS SPECIFIED):
  ±0.5 mm for all dimensions
  ±0.2 mm for hardware-mating features (driver cutouts, hinge holes)
  ±1 mm for cabinet edge dimensions
  R5 mm minimum on internal corners (tool-radius limit)
```

Manufacturers honor general notes; per-feature exceptions go on the
view next to the feature.

### Drawing standards

- **ASME Y14.5** (US): GD&T, the dominant standard for engineering
  drawings.
- **ISO 1101** (International): the equivalent ISO standard for
  GD&T.
- **First-angle vs third-angle projection**: orientation of the side
  views. First-angle = European; third-angle = American. Specify
  on the drawing.

For DIY work, drawings are usually less formal — a clean
dimensioned view in PDF/DXF is sufficient.

### Generating drawings via MCP

Many CAD MCPs **don't expose drawing tools**. The fallback:

1. Generate **section** or **projected** views using the MCP's
   `create_section`, `project_to_plane`, or equivalent.
2. Export each as a **DXF** (each face of the cabinet exported flat).
3. Compose the drawing manually in a 2D tool (Inkscape, LibreCAD,
   AutoCAD) using the DXFs.

For full drawing automation, work in the native CAD tool's UI for
the drawing creation step, then export the result. MCPs are still
catching up on drawing capabilities.

## 7. Tolerancing in the model

A robust parametric model bakes tolerance into the parameters:

```
# Driver flange recess
driver_flange_d         = 178 mm  # nominal
driver_flange_clearance = 2 mm    # for fit
driver_flange_d_actual  = driver_flange_d + driver_flange_clearance
```

Now the driver fits with 2 mm radial clearance, accommodating
manufacturing tolerance + the gasket thickness. To change clearance
globally, edit one parameter.

### GD&T (Geometric Dimensioning and Tolerancing)

For drawings: GD&T specifies **how** features may vary, not just by
how much. Examples relevant to cabinet design:

- **Parallelism**: panel faces parallel to each other within 0.5 mm.
- **Perpendicularity**: woofer cutout perpendicular to baffle face.
- **Concentricity**: driver cutout concentric with mounting bolt
  pattern.
- **Profile**: roundover radius profile within ±0.5 mm.
- **Surface finish**: visible faces Ra ≤ 1.6 µm; hidden faces
  uncontrolled.

GD&T is overkill for a single prototype; essential for production.

## 8. MCP-side support patterns

For granular MCPs:

- `create_assembly`, `add_component_to_assembly`, `mate_components`,
  `create_drawing`, `add_view_to_drawing`, `dimension_view`,
  `export_drawing_pdf`.

For execute-code MCPs:

- Native CAD API calls: `doc.assemblyManager.addComponent(...)`,
  `assembly.joints.add(...)` in Fusion's adsk API, or
  `Mod_Assembly.LinkXChildren` in FreeCAD.

For all: **rely on naming**. Mate operations reference parts by
name; if your parts aren't named meaningfully, mating becomes
ambiguous.

## 9. When the MCP can't do drawings

The pragmatic fallback for DIY:

1. Render isometric, front, top, side views via screenshots from
   the MCP.
2. Open the screenshots in a graphics tool.
3. Annotate dimensions manually.
4. Compose into a PDF with title block.

This is enough for sending to a CNC operator or for self-reference.
Customers wanting "engineering drawings" need the full GD&T treatment;
the MCP probably can't deliver that anyway.

## Cross-references

- `references/parametric-modeling.md` — bodies vs components.
- `references/mcp-conventions.md` — what tools to expect / look up.
- `references/manufacturability.md` — tolerances per process.
- `references/speaker-cabinet-cad.md` — how driver imports + cutouts
  interact in the assembly context.
