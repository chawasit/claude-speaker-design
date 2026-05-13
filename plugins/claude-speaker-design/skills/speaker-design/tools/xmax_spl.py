#!/usr/bin/env python3
"""Displacement-limited SPL of a direct-radiator driver vs. frequency.

For a piston in an infinite baffle (half-space, ka<<1), the far-field
on-axis peak pressure is (Beranek / Olson):

    p_peak = rho0 * S_d * omega^2 * x_peak * n / (2 * pi * r)

Converting to RMS and to dB SPL:

    SPL(f) = 20*log10(rho0 * S_d * omega^2 * x_peak * n / (sqrt(2) * 2*pi * p_ref * r))

This is the anechoic ceiling. Below the enclosure's tuning frequency
(Fb or Fc), this is the actual cap on output. Above tuning, port air
or amplifier voltage usually limits first.

Outputs a table from 20 Hz to 200 Hz by default; use --f-min/--f-max
to override.
"""
from __future__ import annotations

import argparse
import math

RHO0 = 1.204
P_REF = 20e-6   # Pa


def spl_at(f, sd_m2, xmax_m, r_m=1.0, n_drivers=1):
    # Piston in infinite baffle, half-space, far-field, on-axis:
    #   p_peak = rho0 * Sd * omega^2 * x_peak * n / (2*pi*r)
    # The 2*pi divisor is the half-space radiation geometry (4*pi for free space).
    p_peak = RHO0 * sd_m2 * (2 * math.pi * f) ** 2 * xmax_m * n_drivers \
             / (2 * math.pi * r_m)
    p_rms = p_peak / math.sqrt(2.0)
    return 20.0 * math.log10(p_rms / P_REF)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--sd", type=float, required=True, help="Cone Sd (cm^2)")
    p.add_argument("--xmax", type=float, required=True,
                   help="Linear one-way excursion (mm); use measured Klippel value")
    p.add_argument("--r", type=float, default=1.0, help="Measurement distance (m)")
    p.add_argument("--n", type=int, default=1, help="Number of drivers (in phase)")
    p.add_argument("--f-min", type=float, default=20.0)
    p.add_argument("--f-max", type=float, default=200.0)
    p.add_argument("--steps", type=int, default=12)
    p.add_argument("--target-spl", type=float,
                   help="If set, prints the lowest frequency where this SPL is reached")
    args = p.parse_args(argv)

    sd = args.sd * 1e-4
    xmax = args.xmax * 1e-3

    print(f"Half-space displacement-limited SPL (Xmax = {args.xmax} mm, "
          f"Sd = {args.sd} cm^2, n = {args.n}, r = {args.r} m)\n")
    print("  f (Hz)   SPL_peak (dB)")
    print("  -------  -------------")

    log_min = math.log10(args.f_min)
    log_max = math.log10(args.f_max)
    crossing = None
    n_steps = max(args.steps, 1)
    for i in range(n_steps + 1):
        f = 10 ** (log_min + (log_max - log_min) * i / n_steps)
        spl = spl_at(f, sd, xmax, args.r, args.n)
        print(f"  {f:6.1f}    {spl:6.1f}")
        if args.target_spl is not None and crossing is None and spl >= args.target_spl:
            crossing = f

    if args.target_spl is not None:
        if crossing is None:
            print(f"\nTarget {args.target_spl:.0f} dB SPL NOT reached above {args.f_min:.0f} Hz.")
            print("Need more Sd, more Xmax, more drivers, or higher cutoff.")
        else:
            print(f"\nReaches {args.target_spl:.0f} dB SPL at ~{crossing:.1f} Hz.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
