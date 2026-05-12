#!/usr/bin/env python3
"""Compute group delay for standard crossover filters.

Group delay tau_g(f) = -d(phase)/d(omega) [seconds]. For a 2nd-order
filter (Q, fc), the magnitude and phase at frequency f are:

    H(s) = wc^2 / (s^2 + (wc/Q)*s + wc^2)
    s = j*omega

Differentiating gives a closed form for tau_g(f) in terms of (f, fc, Q).
Cascading two equal Butterworth-Q=0.707 sections gives LR4.

This script computes group delay vs frequency for a single filter
(LP or HP) or for an LR4 (cascaded). It also computes the maximum
delay across a band and compares to the audibility threshold
(~1.5 cycles at the lowest frequency in band).
"""
from __future__ import annotations

import argparse
import math


def group_delay_2nd_order(f, fc, Q, kind="LP"):
    """Group delay of a 2nd-order biquad at frequency f.

    kind: "LP" (low-pass) or "HP" (high-pass). For an analog biquad
    the group delay shape is the same; here we use the LP form.
    """
    omega = 2 * math.pi * f
    wc = 2 * math.pi * fc
    # Closed-form derivative of arctan(...) for the analog biquad phase:
    # phi(omega) = -arctan((wc/Q * omega) / (wc^2 - omega^2))
    # d phi / d omega = -[ (wc/Q) * (wc^2 + omega^2) ] /
    #                    [ (wc^2 - omega^2)^2 + (wc*omega/Q)^2 ]
    numerator = (wc / Q) * (wc ** 2 + omega ** 2)
    denominator = (wc ** 2 - omega ** 2) ** 2 + (wc * omega / Q) ** 2
    return numerator / denominator   # seconds


def group_delay_LR4(f, fc):
    """LR4 = two cascaded Butterworth-Q=0.707 filters at the same fc."""
    return 2 * group_delay_2nd_order(f, fc, 0.7071, "LP")


def group_delay_sealed(f, fc, qtc):
    """A sealed-box LF system is a 2nd-order high-pass.

    Group delay shape is the same as a 2nd-order LP (just shifted)
    so we reuse the formula.
    """
    return group_delay_2nd_order(f, fc, qtc, "HP")


def audibility_threshold(f):
    """Approximate audibility threshold for added group delay at frequency f."""
    return 1.5 / f   # 1.5 cycles


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--type", choices=["B2", "LR2", "LR4", "sealed", "ported"],
                   default="LR4", help="Filter type")
    p.add_argument("--fc", type=float, required=True,
                   help="Cutoff frequency (Hz). For sealed box, F_c.")
    p.add_argument("--q", type=float, default=0.707,
                   help="Q factor (Butterworth = 0.707, Bessel = 0.577)")
    p.add_argument("--f-min", type=float, default=20.0)
    p.add_argument("--f-max", type=float, default=200.0)
    p.add_argument("--steps", type=int, default=12)
    args = p.parse_args(argv)

    print(f"Group delay for {args.type} filter at f_c = {args.fc:.0f} Hz")
    if args.type in ("LR2", "B2", "sealed", "ported"):
        print(f"Q = {args.q:.3f}")
    print()
    print("  f (Hz)    tau_g (ms)   threshold (ms)   audible?")
    print("  -------   -----------  ---------------  --------")

    log_min = math.log10(args.f_min)
    log_max = math.log10(args.f_max)
    max_tg = 0.0
    for i in range(args.steps + 1):
        f = 10 ** (log_min + (log_max - log_min) * i / args.steps)
        if args.type == "LR4":
            tg = group_delay_LR4(f, args.fc)
        elif args.type in ("LR2", "B2"):
            tg = group_delay_2nd_order(f, args.fc, args.q)
        elif args.type == "sealed":
            tg = group_delay_sealed(f, args.fc, args.q)
        elif args.type == "ported":
            # Approximate a B4-aligned ported box as cascaded biquads:
            # one at Fc=Fb with Q=Qts*sqrt(1+alpha), one at Fb itself.
            # Use 2x sealed approximation as a first-order estimate.
            tg = 2 * group_delay_sealed(f, args.fc, args.q)
        threshold = audibility_threshold(f)
        audible = "YES" if tg > threshold else "no"
        print(f"  {f:6.1f}     {tg * 1000:7.2f}      {threshold * 1000:6.1f}        {audible}")
        max_tg = max(max_tg, tg)

    print()
    print(f"Peak group delay: {max_tg * 1000:.2f} ms")
    threshold_lowest = audibility_threshold(args.f_min)
    print(f"Threshold at f_min ({args.f_min:.0f} Hz): {threshold_lowest * 1000:.1f} ms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
