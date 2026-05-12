# Cookbook: Bookshelf Cabinet CAD via MCP

End-to-end CAD walkthrough for the speaker designed in
`speaker-design/cookbooks/bookshelf-2way.md`. We turn the acoustic
spec into a parametric model with verification at each step.

The pseudocode below uses a granular Fusion 360-style MCP tool
naming convention (snake_case, name-based handles). Adapt to whatever
MCP is actually loaded — patterns are universal, exact tool names are
not.

## Inputs from the acoustic design

From the speaker-design cookbook (6.5" + 1" dome, ported, LR4):

| Parameter             | Value         | Source                                  |
|-----------------------|---------------|-----------------------------------------|
| Net `V_b`             | 12.3 L        | ported_box tool, B4 alignment           |
| Cabinet WxHxD ext.    | 200×350×280 mm| iterated to land 13 L gross internal     |
| Panel thickness       | 18 mm         | MDF default                             |
| Woofer cutout         | 152 mm dia    | driver datasheet                        |
| Woofer flange         | 178 × 5 mm    | driver datasheet                        |
| Tweeter cutout        | 86 mm dia     | driver datasheet                        |
| Tweeter flange        | 104 × 4 mm    | driver datasheet                        |
| Tweeter offset        | 15 mm from CL | diffraction smoothing                   |
| Port                  | 60 mm dia × 163 mm | port_length tool, 60 mm diameter   |
| Bracing               | 1 horizontal  | panel mode mitigation                   |
| Roundovers            | 25 mm radius  | edge diffraction reduction              |

## Phase 1: Plan

"Build a 200×350×280 mm bookshelf cabinet, 18 mm MDF panels, with a
rear-firing 60 mm port 163 mm long, woofer centered horizontally at
y=220 mm, tweeter offset 15 mm right of CL at y=295 mm, one
horizontal brace at mid-height with two 40 mm air-passage holes,
25 mm front-baffle vertical roundovers. Internal volume target
12.3 L net after driver displacement and brace. Removable rear
panel with M4 threaded inserts × 8."

## Phase 2: Discover available tools

```
# Inventory MCP tools (skip if you already know from the system prompt)
LIST: mcp__<server>__list_components
      mcp__<server>__create_parameter
      mcp__<server>__create_sketch
      mcp__<server>__draw_rectangle / draw_circle
      mcp__<server>__extrude / cut / shell
      mcp__<server>__fillet
      mcp__<server>__measure / get_volume
      mcp__<server>__screenshot / render_view
      mcp__<server>__export_step
```

If a critical tool is missing, plan a workaround now. Most likely
gaps for community Fusion MCPs: no `add_constraint`, no
`create_component` for separate panels, no `circular_pattern` —
each has the fallbacks listed in `references/mcp-conventions.md`.

## Phase 3: Build

### Step 1: Parameters (always first)

```python
create_parameter("baffle_w",       "200 mm")
create_parameter("baffle_h",       "350 mm")
create_parameter("depth",          "280 mm")
create_parameter("panel_t",        "18 mm")

create_parameter("woofer_cutout_d","152 mm")
create_parameter("woofer_flange_d","178 mm")
create_parameter("woofer_flange_t",  "5 mm")
create_parameter("woofer_y_center","220 mm")
create_parameter("woofer_x_offset",  "0 mm")

create_parameter("tweeter_cutout_d","86 mm")
create_parameter("tweeter_flange_d","104 mm")
create_parameter("tweeter_flange_t", "4 mm")
create_parameter("tweeter_y_center","295 mm")
create_parameter("tweeter_x_offset","15 mm")

create_parameter("port_dia",       "60 mm")
create_parameter("port_length",    "163 mm")
create_parameter("port_y_center",   "80 mm")
create_parameter("port_x_offset",   "0 mm")

create_parameter("brace_width",    "30 mm")
create_parameter("brace_thickness","18 mm")

create_parameter("front_roundover_r", "25 mm")
create_parameter("rear_chamfer",      "8 mm")

create_parameter("terminal_cup_w",  "90 mm")
create_parameter("terminal_cup_h",  "50 mm")
create_parameter("terminal_cup_inset","10 mm")
```

Verify:

```
list_parameters()  → expect 22 user parameters
```

### Step 2: Outer shell solid

```python
sketch_outer = create_sketch(plane="XY", name="sketch_outer_baffle")
draw_rectangle(
    sketch=sketch_outer,
    corner1=(-"baffle_w"/2, -"baffle_h"/2),
    corner2=("baffle_w"/2,  "baffle_h"/2),
)

extrude(
    profile=sketch_outer,
    distance="depth",
    direction="positive_z",
    name="extrude_outer_shell",
)
```

Verify:

```
render_view(view="isometric")
measure(body="extrude_outer_shell", property="volume")
  → expect 19.6 L (200 × 350 × 280 mm)
```

### Step 3: Shell to internal volume

```python
shell(
    body="extrude_outer_shell",
    thickness="panel_t",
    direction="inward",
    open_faces=[],          # closed shell — split off back panel later
    name="shell_main_body",
)
```

Verify:

```
measure(body="shell_main_body", property="material_volume")
  → expect ~7.0 L of MDF (the panels)
measure_void(body="shell_main_body")    # internal air volume
  → expect ~12.6 L gross internal (close to nominal 12.57 L)
```

### Step 4: Driver cutouts

```python
# Woofer flange recess (on outside of front baffle)
sketch_wf_flange = create_sketch(plane="front_baffle_outer", name="sketch_woofer_flange_recess")
draw_circle(sketch=sketch_wf_flange,
            center=("woofer_x_offset", "woofer_y_center" - "baffle_h"/2),
            diameter="woofer_flange_d")
cut(profile=sketch_wf_flange, depth="woofer_flange_t", direction="into_body",
    target="shell_main_body", name="cut_woofer_flange_recess")

# Woofer through-hole
sketch_wf_cutout = create_sketch(plane="front_baffle_outer", name="sketch_woofer_cutout")
draw_circle(sketch=sketch_wf_cutout,
            center=("woofer_x_offset", "woofer_y_center" - "baffle_h"/2),
            diameter="woofer_cutout_d")
cut(profile=sketch_wf_cutout, depth="panel_t", direction="into_body",
    target="shell_main_body", name="cut_woofer_through")

# Tweeter (same pattern with tweeter parameters)
sketch_tw_flange = create_sketch(plane="front_baffle_outer", name="sketch_tweeter_flange_recess")
draw_circle(sketch=sketch_tw_flange,
            center=("tweeter_x_offset", "tweeter_y_center" - "baffle_h"/2),
            diameter="tweeter_flange_d")
cut(profile=sketch_tw_flange, depth="tweeter_flange_t",
    target="shell_main_body", name="cut_tweeter_flange_recess")

sketch_tw_cutout = create_sketch(plane="front_baffle_outer", name="sketch_tweeter_cutout")
draw_circle(sketch=sketch_tw_cutout,
            center=("tweeter_x_offset", "tweeter_y_center" - "baffle_h"/2),
            diameter="tweeter_cutout_d")
cut(profile=sketch_tw_cutout, depth="panel_t",
    target="shell_main_body", name="cut_tweeter_through")
```

Verify:

```
render_view(view="front")
  → expect woofer cutout centered horizontally near bottom-middle,
    tweeter cutout offset 15 mm right of center near top
```

### Step 5: Port

```python
# Port hole through rear panel
sketch_port_hole = create_sketch(plane="rear_baffle_outer", name="sketch_port_hole")
draw_circle(sketch=sketch_port_hole,
            center=("port_x_offset", "port_y_center" - "baffle_h"/2),
            diameter="port_dia")
cut(profile=sketch_port_hole, depth="panel_t",
    target="shell_main_body", name="cut_port_through")

# Port tube (extends inward from inner surface of rear panel)
sketch_port_tube = create_sketch(plane="rear_baffle_inner", name="sketch_port_tube")
# Outer profile slightly larger than the port diameter
draw_circle(sketch=sketch_port_tube,
            center=("port_x_offset", "port_y_center" - "baffle_h"/2),
            diameter="port_dia" + "2 mm")
draw_circle(sketch=sketch_port_tube,
            center=("port_x_offset", "port_y_center" - "baffle_h"/2),
            diameter="port_dia")   # inner = the through hole
extrude(profile=sketch_port_tube,
        distance="port_length" - "panel_t",
        direction="inward",
        operation="add",
        target="shell_main_body",
        name="extrude_port_tube")
```

Verify:

```
render_view(view="section_horizontal_at_port_y")
  → expect tube extending into the cabinet, through the rear panel
measure(feature="port_tube_inner_diameter") → expect 60 mm
```

### Step 6: Brace

```python
sketch_brace = create_sketch(plane="XZ_at_y_175", name="sketch_brace")
draw_rectangle(sketch=sketch_brace,
               corner1=(-"baffle_w"/2 + "panel_t", -"depth"/2 + "panel_t"),
               corner2=( "baffle_w"/2 - "panel_t",  "depth"/2 - "panel_t"))

# Cutouts for wire/air passage
draw_circle(sketch=sketch_brace, center=(-50, 0), diameter=40)
draw_circle(sketch=sketch_brace, center=( 50, 0), diameter=40)

extrude(profile=sketch_brace, distance="brace_thickness", direction="symmetric",
        operation="add", target="shell_main_body", name="extrude_brace")
```

Verify:

```
render_view(view="section_vertical")
  → expect the brace spanning side-to-side at mid-height,
    with two clearance holes
```

### Step 7: Terminal cup recess

```python
sketch_tc = create_sketch(plane="rear_baffle_outer", name="sketch_terminal_cup")
draw_rectangle(sketch=sketch_tc,
               corner1=(-"terminal_cup_w"/2, -"terminal_cup_h"/2 - 50),
               corner2=( "terminal_cup_w"/2,  "terminal_cup_h"/2 - 50))
cut(profile=sketch_tc, depth="terminal_cup_inset",
    target="shell_main_body", name="cut_terminal_cup_recess")

# Binding post holes (2x ~10 mm)
sketch_posts = create_sketch(plane="rear_baffle_outer", name="sketch_binding_posts")
draw_circle(sketch=sketch_posts, center=(-20, -50), diameter=10)
draw_circle(sketch=sketch_posts, center=( 20, -50), diameter=10)
cut(profile=sketch_posts, depth="panel_t",
    target="shell_main_body", name="cut_binding_posts")
```

### Step 8: Front roundovers (last)

```python
fillet(edges=["front_top", "front_bottom",
              "front_left", "front_right"],   # the 4 vertical front-baffle edges
       radius="front_roundover_r",
       name="fillet_front_baffle")
```

Verify:

```
render_view(view="isometric")
  → expect smooth 25 mm front edges, sharp rear edges
```

### Step 9: Split back panel for access

```python
sketch_split = create_sketch(plane="XY_offset_-panel_t_from_rear", name="sketch_back_split")
draw_rectangle(sketch=sketch_split, corner1=..., corner2=...)
split_body(body="shell_main_body", tool=sketch_split,
           names=["shell_main", "shell_back"])

# Screw holes for back attachment (8 around perimeter)
sketch_back_screws = create_sketch(plane="rear_baffle_outer", name="sketch_back_screws")
# ... 8 × dia 4.5 mm holes around the perimeter
cut(...)
```

## Phase 4: Verification

```
# Render full set
render_view(view="isometric")
render_view(view="front")
render_view(view="rear")
render_view(view="section_vertical")
render_view(view="section_horizontal")

# Measure final net volume
measure_void(body="shell_main")
  → target: ~12.0 L (gross 12.6 L, minus driver displacement
    ~0.5 L, minus brace ~0.15 L, minus port volume inside
    ~0.4 L) ≈ 11.5 L net

# Adjust depth if net Vb is < 11.7 L (allow 5% margin)
change_parameter("depth", "285 mm")
```

The internal volume measurement is the **single most important
verification step** for a speaker cabinet. If it doesn't match,
adjust `depth` (cheapest parameter to grow) and re-measure.

## Phase 5: Export

```python
# Full assembled cabinet for visualization / customer review
export_step(file="bookshelf_2way_v1.step", body=["shell_main", "shell_back"])

# Per-panel DXF for CNC routing on sheet stock
export_dxf(face="front_baffle_outer",  file="panel_front.dxf",  kerf=0.0)
export_dxf(face="rear_baffle_outer",   file="panel_rear.dxf",   kerf=0.0)
export_dxf(face="left_panel_outer",    file="panel_left.dxf",   kerf=0.0)
export_dxf(face="right_panel_outer",   file="panel_right.dxf",  kerf=0.0)
export_dxf(face="top_panel_outer",     file="panel_top.dxf",    kerf=0.0)
export_dxf(face="bottom_panel_outer",  file="panel_bot.dxf",    kerf=0.0)
export_dxf(body="extrude_brace",        file="panel_brace.dxf",  kerf=0.0)

# Snapshot for reproducibility
save_snapshot(name="v1.0_pre_finish")
```

CNC operator will compensate kerf in CAM. STL for the port tube
(if 3D-printed) is exported separately.

## Verifying after changes

The whole point of parametric CAD: when the spec changes, change the
parameter.

```python
# Example: user wants 25 mm panels instead of 18 mm
change_parameter("panel_t", "25 mm")
# Internal dimensions automatically reduce by 14 mm in each axis.
# Internal volume drops accordingly; if net Vb falls below target,
# grow `depth`:
change_parameter("depth", "300 mm")

# Re-verify
measure_void(body="shell_main")
render_view(view="isometric")
```

If any feature fails to rebuild on a parameter change, the model has
a hidden literal somewhere. Fix it (replace with the parameter
reference) — don't work around it.

## What can go wrong

| Symptom                                | Diagnose / fix                                 |
|----------------------------------------|------------------------------------------------|
| Internal volume measurement ≠ design   | Forgot to subtract brace / port / driver       |
| Port tube extends outside the cabinet  | `port_length` longer than depth available; reduce port_length (and re-tune Fb) or pick smaller port_dia |
| Roundovers fail to apply               | Edge selection ambiguous; specify edges by adjacent face name |
| Driver cutout shows wrong location     | Sketch plane orientation wrong; verify with render before cutting |
| Back panel doesn't separate            | Split sketch boundary didn't reach all faces; use a plane, not a rectangle |
| Parameter change breaks rebuild        | A downstream feature was screen-picked rather than parameter-driven; rebuild that feature with explicit parameter references |
| STEP export is huge / slow             | Roundovers approximated with too many faces; reduce facet count in export options |

## Cross-references

- `speaker-design/cookbooks/bookshelf-2way.md` — the acoustic spec
- `speaker-design/references/baffle-and-cabinet-acoustics.md` —
  why tweeter offset, roundovers, brace matter
- `speaker-design/references/closed-box-geometry.md` — why the
  internal-volume verification step is the most important one
- `references/parametric-modeling.md` — the philosophy here applied
- `references/mcp-conventions.md` — translating these pseudocode
  calls to whatever real MCP is loaded
- `references/manufacturability.md` — tolerances, joinery, kerf,
  driver-cutout sizing for CNC and laser fabrication
