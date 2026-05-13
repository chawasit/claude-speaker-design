#!/usr/bin/env python3
"""Sealed (closed-box) alignment design from Thiele/Small parameters.

Given Fs, Qts, Vas, computes in-box resonance Fc, total Q (Qtc), and
the -3 dB cutoff (which only equals Fc for the Butterworth Qtc=0.707).

Equations (Small, 1972):
    alpha = Vas/Vb
    Fc    = Fs * sqrt(1 + alpha)
    Qtc   = Qts * sqrt(1 + alpha)
    f-3dB = Fc * sqrt((1 - 1/(2*Qtc^2)) + sqrt((1 - 1/(2*Qtc^2))^2 + 1))^(1/2)
"""
from __future__ import annotations

import argparse
import math


def sealed(fs, qts, vas_L, vb_L=None, qtc_target=None):
    if (vb_L is None) == (qtc_target is None):
        raise ValueError("Provide exactly one of --vb or --qtc.")

    if qtc_target is not None:
        if qtc_target <= qts:
            raise ValueError(f"Qtc target ({qtc_target}) must exceed driver Qts ({qts}).")
        alpha = (qtc_target / qts) ** 2 - 1.0
        vb_L = vas_L / alpha
    else:
        alpha = vas_L / vb_L

    fc = fs * math.sqrt(1.0 + alpha)
    qtc = qts * math.sqrt(1.0 + alpha)

    # -3 dB frequency of the resulting 2nd-order high-pass
    # -3 dB frequency of the resulting 2nd-order high-pass (Small 1972).
    # Solving |H(jw)|^2 = 0.5 for w gives:
    #   (w/wc)^2 = b + sqrt(b^2 + 1),  where b = 1/(2*Qtc^2) - 1
    b = 1.0 / (2.0 * qtc ** 2) - 1.0
    f_minus_3 = fc * math.sqrt(b + math.sqrt(b * b + 1.0))

    # Qualitative alignment label
    label = "non-standard"
    for qtag, name in [(0.5, "critically damped"), (0.577, "Bessel"),
                       (0.707, "Butterworth B2"), (1.0, "Chebyshev (peaked)")]:
        if abs(qtc - qtag) < 0.03:
            label = name
            break

    return {
        "Vb_L": vb_L,
        "alpha": alpha,
        "Fc_Hz": fc,
        "Qtc": qtc,
        "f_minus_3dB_Hz": f_minus_3,
        "alignment": label,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--fs", type=float, required=True, help="Driver free-air Fs (Hz)")
    p.add_argument("--qts", type=float, required=True, help="Driver total Q at Fs")
    p.add_argument("--vas", type=float, required=True, help="Driver Vas (L)")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--vb", type=float, help="Box net internal volume (L)")
    g.add_argument("--qtc", type=float, help="Target system Qtc (e.g. 0.707)")
    args = p.parse_args(argv)

    if args.qts < 0.18 and args.qtc and args.qtc < 0.707:
        print("warning: very low Qts; sealed alignment will be over-damped.")
    if args.qts > 0.7:
        print("warning: high Qts; sealed alignment will be peaky unless Vb is huge.")

    r = sealed(args.fs, args.qts, args.vas, args.vb, args.qtc)
    print(f"Vb            = {r['Vb_L']:.2f} L")
    print(f"alpha (Vas/Vb)= {r['alpha']:.2f}")
    print(f"Fc            = {r['Fc_Hz']:.1f} Hz")
    print(f"Qtc           = {r['Qtc']:.3f}  ({r['alignment']})")
    print(f"f-3dB         = {r['f_minus_3dB_Hz']:.1f} Hz")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
