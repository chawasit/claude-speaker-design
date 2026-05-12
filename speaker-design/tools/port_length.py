#!/usr/bin/env python3
"""Compute physical port length for a target tuning Fb.

Helmholtz resonance with end correction k * sqrt(Sp/pi):
    Fb = (c / 2*pi) * sqrt(Sp / (Vb * Lp_eff))
    Lp_eff = Lp_physical + k * sqrt(Sp/pi)

For a flush (one-end-flanged, one-end-free) port: k_total = 0.732
For both-flanged port:                            k_total = 0.85
For a free (both-end-free) port:                  k_total = 0.613

Also reports air velocity at Fb at a target peak displacement, so you
can check chuffing before building.
"""
from __future__ import annotations

import argparse
import math

C_SOUND = 343.0  # m/s


def port_length(fb, vb_L, dia_mm, both_flanged=True, sd_cm2=None, x_peak_mm=None):
    sp = math.pi * (dia_mm * 1e-3 / 2.0) ** 2
    vb = vb_L * 1e-3
    k = 0.85 if both_flanged else 0.732

    lp_eff = (C_SOUND / (2 * math.pi * fb)) ** 2 * sp / vb
    lp_physical = lp_eff - k * math.sqrt(sp / math.pi)

    if lp_physical <= 0:
        raise ValueError(
            "Port diameter is too large for this Fb / Vb — physical length "
            "is negative. Use a smaller diameter or passive radiator.")

    result = {
        "Sp_cm2": sp * 1e4,
        "Lp_physical_mm": lp_physical * 1e3,
        "Lp_effective_mm": lp_eff * 1e3,
        "end_correction_mm": k * math.sqrt(sp / math.pi) * 1e3,
    }

    if sd_cm2 is not None and x_peak_mm is not None:
        # Volume velocity from cone == volume velocity through port at Fb
        sd = sd_cm2 * 1e-4
        x_peak = x_peak_mm * 1e-3
        omega = 2 * math.pi * fb
        v_port_peak = (sd / sp) * omega * x_peak
        result["v_port_peak_m_per_s"] = v_port_peak
        result["chuffing_risk"] = (
            "OK" if v_port_peak < 17.0 else
            "WARN — exceeds 17 m/s; expect audible chuffing")

    return result


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--fb", type=float, required=True, help="Target tuning Fb (Hz)")
    p.add_argument("--vb", type=float, required=True, help="Net box volume (L)")
    p.add_argument("--dia", type=float, required=True, help="Port diameter (mm)")
    p.add_argument("--one-end-free", action="store_true",
                   help="Port flanged on one end only (default: both ends flanged)")
    p.add_argument("--sd", type=float, help="Cone Sd (cm^2) for velocity check")
    p.add_argument("--xpeak", type=float,
                   help="Peak cone excursion at Fb (mm) for velocity check")
    args = p.parse_args(argv)

    r = port_length(args.fb, args.vb, args.dia,
                    both_flanged=not args.one_end_free,
                    sd_cm2=args.sd, x_peak_mm=args.xpeak)

    print(f"Port area     = {r['Sp_cm2']:.1f} cm^2  (dia {args.dia:.0f} mm)")
    print(f"End correction= {r['end_correction_mm']:.1f} mm")
    print(f"Effective Lp  = {r['Lp_effective_mm']:.1f} mm")
    print(f"Physical Lp   = {r['Lp_physical_mm']:.1f} mm  <-- cut this length")
    if "v_port_peak_m_per_s" in r:
        print(f"Port velocity = {r['v_port_peak_m_per_s']:.1f} m/s peak  "
              f"({r['chuffing_risk']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
