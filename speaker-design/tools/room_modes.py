#!/usr/bin/env python3
"""Enumerate rectangular-room acoustic modes from dimensions.

For a "shoebox" room L_x x L_y x L_z with rigid walls, the eigenmodes are:

    f(n_x, n_y, n_z) = (c/2) * sqrt((n_x/L_x)^2 + (n_y/L_y)^2 + (n_z/L_z)^2)

with indices n_i >= 0, at least one nonzero. Modes are classified by
how many indices are nonzero:

    axial:      1 index nonzero  (between two parallel walls)
    tangential: 2 indices nonzero (between four walls)
    oblique:    3 indices nonzero (between six walls)

Axial modes are loudest; tangential are ~3 dB weaker; oblique ~6 dB
weaker. This script prints all modes below a chosen frequency cutoff,
sorted ascending.
"""
from __future__ import annotations

import argparse
import math

C_SOUND = 343.0


def mode_freq(nx, ny, nz, Lx, Ly, Lz):
    return (C_SOUND / 2.0) * math.sqrt(
        (nx / Lx) ** 2 + (ny / Ly) ** 2 + (nz / Lz) ** 2
    )


def mode_class(nx, ny, nz):
    n_nonzero = sum(1 for n in (nx, ny, nz) if n > 0)
    return {1: "axial", 2: "tangential", 3: "oblique"}[n_nonzero]


def schroeder_freq(t60, vol):
    return 2000.0 * math.sqrt(t60 / vol)


def enumerate_modes(Lx, Ly, Lz, f_max):
    modes = []
    # Upper bound on each index
    nx_max = int(2 * f_max * Lx / C_SOUND) + 1
    ny_max = int(2 * f_max * Ly / C_SOUND) + 1
    nz_max = int(2 * f_max * Lz / C_SOUND) + 1
    for nx in range(nx_max + 1):
        for ny in range(ny_max + 1):
            for nz in range(nz_max + 1):
                if nx == ny == nz == 0:
                    continue
                f = mode_freq(nx, ny, nz, Lx, Ly, Lz)
                if f <= f_max:
                    modes.append((f, nx, ny, nz, mode_class(nx, ny, nz)))
    modes.sort()
    return modes


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--lx", type=float, required=True, help="Room length L_x (m)")
    p.add_argument("--ly", type=float, required=True, help="Room width L_y (m)")
    p.add_argument("--lz", type=float, required=True, help="Room height L_z (m)")
    p.add_argument("--fmax", type=float, default=300.0,
                   help="Upper frequency cutoff (Hz), default 300")
    p.add_argument("--t60", type=float, default=0.4,
                   help="Room T_60 in seconds, for Schroeder freq, default 0.4")
    p.add_argument("--filter-class", choices=["all", "axial", "tangential", "oblique"],
                   default="all", help="Restrict report to a mode class")
    args = p.parse_args(argv)

    vol = args.lx * args.ly * args.lz
    f_s = schroeder_freq(args.t60, vol)

    print(f"Room {args.lx:.2f} x {args.ly:.2f} x {args.lz:.2f} m "
          f"= {vol:.1f} m^3")
    print(f"Schroeder freq (T_60={args.t60:.2f}s): {f_s:.0f} Hz")
    print(f"Modes below {args.fmax:.0f} Hz")
    print(f"  (modes below Schroeder are individually audible;")
    print(f"   modes above merge into reverberant field)")
    print()
    print(f"  freq (Hz)   nx ny nz   class")
    print(f"  ---------   --------   -----------")

    modes = enumerate_modes(args.lx, args.ly, args.lz, args.fmax)
    if args.filter_class != "all":
        modes = [m for m in modes if m[4] == args.filter_class]

    for f, nx, ny, nz, klass in modes:
        marker = "  <-- below Schroeder" if f < f_s else ""
        print(f"  {f:7.1f}     {nx:2d} {ny:2d} {nz:2d}   {klass:11s}{marker}")

    print()
    print(f"Total: {len(modes)} modes <= {args.fmax:.0f} Hz")

    # Identify clustered modes (within 5% of each other) as risk
    clusters = []
    for i in range(len(modes) - 1):
        f1, *_ = modes[i]
        f2, *_ = modes[i + 1]
        if f2 / f1 < 1.05:
            clusters.append((f1, f2))
    if clusters:
        print()
        print("WARNING: clustered modes (within 5%) — louder bumps:")
        for f1, f2 in clusters:
            print(f"  {f1:.1f} Hz and {f2:.1f} Hz")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
