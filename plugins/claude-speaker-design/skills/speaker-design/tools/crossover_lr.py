#!/usr/bin/env python3
"""Linkwitz-Riley passive crossover component values for textbook resistive loads.

Computes L and C for LR2 and LR4 high-pass and low-pass filters at a given
crossover frequency fc into a load impedance Z.

These are starting points only. Real drivers are not resistive, so:
  1. Add a Zobel network to flatten the rising L_e of the woofer.
  2. Add an L-pad to attenuate the tweeter.
  3. Then measure and adjust — the acoustic slope is what matters,
     not the electrical filter.

LR2 (12 dB/oct): cascade of two equal Butterworth 1st-order, but realized
   as a 2nd-order section with Q = 0.5. Component values come from
   solving for Q=0.5 at fc.

LR4 (24 dB/oct): cascade of two Butterworth 2nd-order at the same fc,
   each with Q = 0.707.
"""
from __future__ import annotations

import argparse
import math


def lr2_values(fc, z):
    # 2nd-order Butterworth with Q=0.707 has C1=1/(omega*Z*sqrt(2))
    # but LR2 is Q=0.5 -> different coefficient.
    # LR2 LP:  L = Z / (pi * fc),   C = 1 / (4 * pi * fc * Z)
    # LR2 HP:  L = Z / (4 * pi * fc),  C = 1 / (pi * fc * Z)
    lp_L = z / (math.pi * fc)
    lp_C = 1.0 / (4 * math.pi * fc * z)
    hp_L = z / (4 * math.pi * fc)
    hp_C = 1.0 / (math.pi * fc * z)
    return {"LP": {"L_H": lp_L, "C_F": lp_C}, "HP": {"L_H": hp_L, "C_F": hp_C}}


def lr4_values(fc, z):
    # LR4 = two cascaded Butterworth-Q0.707 sections at same fc.
    # Standard 4th-order LR component values (resistive load):
    # LP: L1 = Z*sqrt(2)/(2*pi*fc),   C1 = 1/(2*pi*fc*Z*sqrt(2))
    #     L2 = Z*sqrt(2)/(4*pi*fc),   C2 = 1/(pi*fc*Z*sqrt(2))
    # HP: C1 = 1/(2*pi*fc*Z*sqrt(2)), L1 = Z*sqrt(2)/(2*pi*fc) ... but mirrored
    sqrt2 = math.sqrt(2.0)
    omega = 2 * math.pi * fc
    lp = {
        "L1_H": (sqrt2 * z) / omega,
        "C1_F": 1.0 / (sqrt2 * z * omega),
        "L2_H": z / (sqrt2 * omega),
        "C2_F": sqrt2 / (z * omega),
    }
    hp = {
        "C1_F": 1.0 / (sqrt2 * z * omega),
        "L1_H": z / (sqrt2 * omega),
        "C2_F": sqrt2 / (z * omega),
        "L2_H": (sqrt2 * z) / omega,
    }
    return {"LP": lp, "HP": hp}


def zobel(re, le_mH):
    le = le_mH * 1e-3
    rz = 1.25 * re
    cz = le / (re * re)
    return {"Rz_ohm": rz, "Cz_uF": cz * 1e6}


def fmt_L(h):
    return f"{h * 1e3:.3f} mH"


def fmt_C(f):
    return f"{f * 1e6:.2f} uF"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--fc", type=float, required=True, help="Crossover frequency (Hz)")
    p.add_argument("--z", type=float, default=8.0, help="Load impedance (ohm), default 8")
    p.add_argument("--order", choices=["LR2", "LR4"], default="LR4")
    p.add_argument("--re", type=float, help="Woofer Re for optional Zobel calc")
    p.add_argument("--le", type=float, help="Woofer Le in mH for optional Zobel calc")
    args = p.parse_args(argv)

    fn = lr2_values if args.order == "LR2" else lr4_values
    vals = fn(args.fc, args.z)

    print(f"{args.order} crossover at {args.fc:.0f} Hz into {args.z:.1f} ohm "
          "(resistive-load idealization)\n")
    print("Low-pass section (to woofer):")
    for k, v in vals["LP"].items():
        print(f"  {k} = {fmt_L(v) if k.startswith('L') else fmt_C(v)}")
    print("\nHigh-pass section (to tweeter):")
    for k, v in vals["HP"].items():
        print(f"  {k} = {fmt_L(v) if k.startswith('L') else fmt_C(v)}")

    if args.re is not None and args.le is not None:
        z = zobel(args.re, args.le)
        print("\nZobel network (parallel with woofer, before low-pass):")
        print(f"  Rz = {z['Rz_ohm']:.2f} ohm  (1.25 * Re)")
        print(f"  Cz = {z['Cz_uF']:.2f} uF  (Le / Re^2)")

    print()
    print("CAVEAT: real drivers are NOT resistive. Measure the in-baffle "
          "acoustic response, then adjust filter values to hit the LR target.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
