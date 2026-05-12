#!/usr/bin/env python3
"""Simple baffle-step and diffraction estimator.

Implements two approximations:

1. Baffle step transition center frequency for a rectangular baffle of
   width W: f_bs ~= 115 / W (W in m). Below f_bs the speaker radiates
   into 4*pi (full space, -6 dB relative to half-space); above, into
   2*pi (half-space, 0 dB). Transition centered at f_bs with smooth
   shoulder roughly +/- 1 octave.

2. Edge diffraction comb-filter: a driver at offset (xo, yo) from
   baffle center sees four edge "secondary sources" at distances
   d1, d2, d3, d4. Combined interference at large axial distance has
   nulls where 2*d_i*cos(theta=0) = lambda*(2k+1)/2, i.e.

       f_null,i,k = c * (2k+1) / (4*d_i)

For a flat rectangular baffle, this is the Olson 1969 model's
first-order approximation. Higher-order modes and cabinet-depth
effects are ignored — the result captures the dominant pattern, not
the exact response.

Output: predicted on-axis response (dB) vs frequency.
"""
from __future__ import annotations

import argparse
import math

C_SOUND = 343.0


def baffle_step_response_db(f, w_baffle_m):
    """Smooth shelf from -6 dB at LF to 0 dB at HF, centered at 115/W."""
    fc = 115.0 / w_baffle_m
    # Logistic transition over ~2 octaves
    t = math.log2(max(f, 0.1) / fc)
    shelf = 6.0 / (1.0 + math.exp(-2.0 * t)) - 6.0
    return shelf


def edge_distances(baffle_w, baffle_h, driver_xo, driver_yo):
    """Driver at (xo, yo) from baffle center; baffle has corners.

    Returns the distances from driver to the four edges.
    """
    d_left   = baffle_w / 2 + driver_xo  # offset right is positive
    d_right  = baffle_w / 2 - driver_xo
    d_top    = baffle_h / 2 - driver_yo  # offset up is positive
    d_bottom = baffle_h / 2 + driver_yo
    return [d_left, d_right, d_top, d_bottom]


def diffraction_ripple_db(f, edges, edge_amp=0.1):
    """Sum direct + four delayed edge contributions; return ripple in dB.

    edge_amp ~ 0.1 corresponds to a sharp rectangular baffle edge. A
    rounded edge would use 0.05 or less; the result is a smaller ripple.
    """
    total = 1.0  # direct
    for d in edges:
        delay = 2 * d / C_SOUND
        phase = 2 * math.pi * f * delay
        total += edge_amp * math.cos(phase)
    return 20 * math.log10(max(abs(total), 1e-6))


def baffle_response(f, baffle_w, baffle_h, driver_xo, driver_yo):
    bs = baffle_step_response_db(f, baffle_w)
    edges = edge_distances(baffle_w, baffle_h, driver_xo, driver_yo)
    ripple = diffraction_ripple_db(f, edges)
    return bs + ripple


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--w", type=float, required=True, help="Baffle width (mm)")
    p.add_argument("--h", type=float, required=True, help="Baffle height (mm)")
    p.add_argument("--xo", type=float, default=0.0,
                   help="Driver x offset from baffle center (mm); +right")
    p.add_argument("--yo", type=float, default=0.0,
                   help="Driver y offset from baffle center (mm); +up")
    p.add_argument("--f-min", type=float, default=80.0)
    p.add_argument("--f-max", type=float, default=5000.0)
    p.add_argument("--steps", type=int, default=20)
    args = p.parse_args(argv)

    w_m = args.w * 1e-3
    h_m = args.h * 1e-3
    xo_m = args.xo * 1e-3
    yo_m = args.yo * 1e-3

    fc = 115.0 / w_m
    print(f"Baffle: {args.w:.0f} x {args.h:.0f} mm")
    print(f"Driver offset from center: ({args.xo:+.0f}, {args.yo:+.0f}) mm")
    print(f"Baffle step center frequency: {fc:.0f} Hz")
    print()
    print(f"  f (Hz)    BS (dB)   Diff (dB)   Total (dB)")
    print(f"  -------   -------   ---------   ----------")

    log_min = math.log10(args.f_min)
    log_max = math.log10(args.f_max)
    max_ripple = 0.0
    min_ripple = 0.0
    for i in range(args.steps + 1):
        f = 10 ** (log_min + (log_max - log_min) * i / args.steps)
        bs = baffle_step_response_db(f, w_m)
        edges = edge_distances(w_m, h_m, xo_m, yo_m)
        diff = diffraction_ripple_db(f, edges)
        total = bs + diff
        print(f"  {f:6.0f}     {bs:+5.1f}    {diff:+5.2f}     {total:+5.2f}")
        max_ripple = max(max_ripple, diff)
        min_ripple = min(min_ripple, diff)

    print()
    print(f"Diffraction ripple range: {min_ripple:+.2f} to {max_ripple:+.2f} dB "
          f"({max_ripple - min_ripple:.2f} dB peak-to-peak)")

    if args.xo == 0.0 and args.yo == 0.0:
        print()
        print("note: driver is centered. Try --xo 15 --yo 60 for "
              "asymmetric placement (diffraction-smoothing).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
