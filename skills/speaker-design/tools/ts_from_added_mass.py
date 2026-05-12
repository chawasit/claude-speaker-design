#!/usr/bin/env python3
"""Compute Thiele/Small parameters from free-air + added-mass impedance sweeps.

Inputs: Fs (Hz), Fs' after added mass (Hz), added mass dm (g), Re (ohm),
        Qms, Qes, cone effective radius a (mm) for Sd.

Refs: Small (1972), Thiele (1971). Valid in the small-signal piston band.
"""
from __future__ import annotations

import argparse
import math
import sys

RHO0 = 1.204     # kg/m^3, air at 20 C
C_SOUND = 343.0  # m/s


def ts_added_mass(fs, fs_prime, dm_g, re, qms, qes, a_mm):
    if fs_prime >= fs:
        raise ValueError("Fs' must be lower than Fs after adding mass.")
    dm = dm_g * 1e-3
    a = a_mm * 1e-3
    sd = math.pi * a * a

    m_ms = dm / ((fs / fs_prime) ** 2 - 1.0)         # kg
    c_ms = 1.0 / ((2 * math.pi * fs) ** 2 * m_ms)    # m/N
    qts = (qms * qes) / (qms + qes)
    vas = RHO0 * C_SOUND ** 2 * sd ** 2 * c_ms       # m^3
    bl = math.sqrt(2 * math.pi * fs * m_ms * re / qes)  # T*m
    r_ms = (2 * math.pi * fs * m_ms) / qms            # N*s/m
    eta0 = (4 * math.pi ** 2 / C_SOUND ** 3) * (fs ** 3 * vas) / qes
    spl_2_83v_1m = 112.0 + 10.0 * math.log10(max(eta0 * 8.0 / re, 1e-12))

    return {
        "Sd_cm2": sd * 1e4,
        "Mms_g": m_ms * 1e3,
        "Cms_mm_per_N": c_ms * 1e3,
        "Kms_N_per_mm": 1.0 / (c_ms * 1e3),
        "Rms_Ns_per_m": r_ms,
        "Qts": qts,
        "Vas_L": vas * 1e3,
        "BL_Tm": bl,
        "eta0_pct": eta0 * 100.0,
        "SPL_2.83V_1m_dB": spl_2_83v_1m,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--fs", type=float, required=True, help="Free-air resonance (Hz)")
    p.add_argument("--fs-prime", type=float, required=True, help="Resonance with added mass (Hz)")
    p.add_argument("--dm", type=float, required=True, help="Added mass (grams)")
    p.add_argument("--re", type=float, required=True, help="DC voice-coil resistance (ohm)")
    p.add_argument("--qms", type=float, required=True, help="Mechanical Q at Fs")
    p.add_argument("--qes", type=float, required=True, help="Electrical Q at Fs")
    p.add_argument("--cone-radius-mm", type=float, required=True,
                   help="Effective cone radius (mm); ~0.4 * frame OD for a typical driver")
    args = p.parse_args(argv)

    try:
        result = ts_added_mass(args.fs, args.fs_prime, args.dm, args.re,
                               args.qms, args.qes, args.cone_radius_mm)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    print(f"Sd            = {result['Sd_cm2']:.1f} cm^2")
    print(f"Mms           = {result['Mms_g']:.2f} g")
    print(f"Cms           = {result['Cms_mm_per_N']:.3f} mm/N")
    print(f"Kms           = {result['Kms_N_per_mm']:.3f} N/mm")
    print(f"Rms           = {result['Rms_Ns_per_m']:.3f} N*s/m")
    print(f"Qts           = {result['Qts']:.3f}")
    print(f"Vas           = {result['Vas_L']:.2f} L")
    print(f"BL            = {result['BL_Tm']:.2f} T*m")
    print(f"eta0          = {result['eta0_pct']:.3f} %")
    print(f"SPL @ 2.83V/1m= {result['SPL_2.83V_1m_dB']:.1f} dB (half-space)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
