#!/usr/bin/env python3
"""Vented (bass-reflex) alignment design from Thiele/Small parameters.

Uses tabulated standard alignments after Small (1973) and Margolis/Small
(1974), interpolated by Qts. Three families supported:

  - QB3: Quasi-Butterworth 3rd order, low-Qts drivers, small Vb, peaked.
  - B4 (SBB4): Butterworth 4th order, the canonical maximally-flat align.
  - C4: Chebyshev 4th order, ~1 dB ripple, extended bass.

Each table maps Qts -> (alpha = Vas/Vb, h = Fb/Fs, f3 = f-3dB/Fb).
"""
from __future__ import annotations

import argparse
import bisect

# (Qts, alpha, h, f3_over_Fb)
B4 = [
    (0.30, 1.92, 1.20, 0.83),
    (0.32, 1.69, 1.13, 0.86),
    (0.35, 1.55, 1.05, 0.89),
    (0.383, 1.414, 1.00, 0.91),
    (0.40, 1.34, 0.99, 0.92),
    (0.45, 1.23, 0.95, 0.94),
    (0.50, 1.20, 0.90, 0.96),
]

QB3 = [
    (0.20, 0.36, 1.84, 1.71),
    (0.25, 0.62, 1.55, 1.41),
    (0.30, 0.94, 1.34, 1.20),
    (0.35, 1.34, 1.20, 1.06),
    (0.38, 1.61, 1.13, 1.00),
]

C4 = [
    (0.40, 2.21, 1.06, 0.81),
    (0.45, 1.86, 0.99, 0.85),
    (0.50, 1.66, 0.93, 0.87),
    (0.55, 1.52, 0.87, 0.89),
    (0.60, 1.43, 0.83, 0.91),
]


def _interp(table, qts):
    """Linear interpolation of (alpha, h, f3) for a given Qts. Clamps at ends."""
    qs = [row[0] for row in table]
    if qts <= qs[0]:
        return table[0][1], table[0][2], table[0][3]
    if qts >= qs[-1]:
        return table[-1][1], table[-1][2], table[-1][3]
    i = bisect.bisect_left(qs, qts)
    q1, a1, h1, f1 = table[i - 1]
    q2, a2, h2, f2 = table[i]
    t = (qts - q1) / (q2 - q1)
    return (a1 + t * (a2 - a1),
            h1 + t * (h2 - h1),
            f1 + t * (f2 - f1))


def _pick_alignment(qts):
    if qts < 0.32:
        return "QB3", QB3
    if qts < 0.42:
        return "B4", B4
    return "C4", C4


def ported(fs, qts, vas_L, alignment="auto"):
    if alignment == "auto":
        name, table = _pick_alignment(qts)
    elif alignment == "QB3":
        name, table = "QB3", QB3
    elif alignment == "B4":
        name, table = "B4", B4
    elif alignment == "C4":
        name, table = "C4", C4
    else:
        raise ValueError(f"unknown alignment: {alignment}")

    alpha, h, f3_ratio = _interp(table, qts)
    vb_L = vas_L / alpha
    fb = fs * h
    f_minus_3 = fb * f3_ratio

    return {
        "alignment": name,
        "Vb_L": vb_L,
        "Fb_Hz": fb,
        "f_minus_3dB_Hz": f_minus_3,
        "alpha": alpha,
        "h": h,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--fs", type=float, required=True)
    p.add_argument("--qts", type=float, required=True)
    p.add_argument("--vas", type=float, required=True, help="Vas (L)")
    p.add_argument("--alignment", choices=["auto", "B4", "QB3", "C4"], default="auto")
    args = p.parse_args(argv)

    if args.qts < 0.20:
        print("warning: very low Qts; consider a horn or large EBS box.")
    if args.qts > 0.60:
        print("warning: high Qts; ported alignments will be over-damped. "
              "Consider sealed instead.")

    r = ported(args.fs, args.qts, args.vas, args.alignment)
    print(f"alignment     = {r['alignment']}")
    print(f"Vb            = {r['Vb_L']:.2f} L  (alpha = Vas/Vb = {r['alpha']:.2f})")
    print(f"Fb            = {r['Fb_Hz']:.1f} Hz  (h = Fb/Fs = {r['h']:.2f})")
    print(f"f-3dB         = {r['f_minus_3dB_Hz']:.1f} Hz")
    print()
    print(f"reminder: high-pass below {0.5 * r['Fb_Hz']:.0f} Hz at 24 dB/oct "
          "to protect from cone unloading.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
