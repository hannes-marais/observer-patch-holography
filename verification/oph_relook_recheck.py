#!/usr/bin/env python3
"""Independent recomputation for Part IX of OPH_INVESTIGATION_REPORT.md (November 2026 re-look).

Uses no OPH code. Needs mpmath and numpy.

  1. Charged-lepton ratios at the exact Koide point (rho = sqrt 2, delta = 2/9).
  2. The Wissner-Gross fine-structure formula (79 + 48 sqrt2 + 42 sqrt3 + 3 sqrt6) / 31104.
  3. The scalar tilt n_s = 1 - P/48 with P = phi + sqrt(pi) * alpha.
  4. A chance-hit count for formulas of the form (a + b sqrt2 + c sqrt3 + d sqrt6) / 31104.

Reference values: CODATA 2022 (alpha^-1, m_mu/m_e, m_e), PDG m_tau = 1776.93(9) MeV,
electron g-2 (Fan et al. 2023), Rb recoil (Morel et al. 2020), Cs recoil (Parker et al. 2018),
Planck 2018 and ACT DR6 P-ACT-LB for n_s.
"""
import math

import mpmath as mp
import numpy as np

mp.mp.dps = 40


def koide_ratios(rho, delta):
    """sqrt(m_k) proportional to 1 + rho*cos(delta + 2*pi*k/3)."""
    m = sorted((1 + rho * mp.cos(delta + 2 * mp.pi * k / 3)) ** 2 for k in range(3))
    q = sum(m) / sum(mp.sqrt(x) for x in m) ** 2
    return m[1] / m[0], m[2] / m[0], q


# --- 1. lepton ratios -------------------------------------------------------
mu_e, tau_e, q = koide_ratios(mp.sqrt(2), mp.mpf(2) / 9)
mu_meas, mu_unc = mp.mpf("206.7682827"), mp.mpf("0.0000046")
m_e = mp.mpf("0.51099895069")
tau_meas, tau_unc = mp.mpf("1776.93") / m_e, mp.mpf("0.09") / m_e
print("Koide (sqrt2, 2/9):  mu/e =", mp.nstr(mu_e, 12), "  tau/e =", mp.nstr(tau_e, 12), "  Q =", mp.nstr(q, 10))
print("  mu/e  residual:", mp.nstr((mu_e / mu_meas - 1) * 1e6, 5), "ppm =", mp.nstr((mu_e - mu_meas) / mu_unc, 5), "sigma")
print("  tau/e measured:", mp.nstr(tau_meas, 8), "+/-", mp.nstr(tau_unc, 3), " pull =", mp.nstr((tau_e - tau_meas) / tau_unc, 3), "sigma")
d_need = mp.findroot(lambda d: koide_ratios(mp.sqrt(2), d)[0] - mu_meas, mp.mpf(2) / 9)
print("  delta that reproduces measured mu/e:", mp.nstr(d_need, 12), " (shift", mp.nstr(d_need - mp.mpf(2) / 9, 4), ")")
p, r = mp.mpf(1) / 12, mp.mpf(1) / 6
print("  XOR probability of events 1/12 and 1/6:", mp.nstr(p + r - 2 * p * r, 12), " (2/9 =", mp.nstr(mp.mpf(2) / 9, 12), ")")

# --- 2. fine-structure formula ----------------------------------------------
alpha = (79 + 48 * mp.sqrt(2) + 42 * mp.sqrt(3) + 3 * mp.sqrt(6)) / 31104
inv = 1 / alpha
codata, codata_unc = mp.mpf("137.035999177"), mp.mpf("0.000000021")
print("\nalpha^-1 from the formula:", mp.nstr(inv, 18))
for name, val, unc in [
    ("CODATA 2022", "137.035999177", "0.000000021"),
    ("electron g-2 (2023)", "137.035999166", "0.000000015"),
    ("Rb recoil (2020)", "137.035999206", "0.000000011"),
    ("Cs recoil (2018)", "137.035999046", "0.000000027"),
]:
    print(f"  vs {name:22s} pull = {mp.nstr((inv - mp.mpf(val)) / mp.mpf(unc), 3)} sigma")

# --- 3. scalar tilt ---------------------------------------------------------
P = (1 + mp.sqrt(5)) / 2 + mp.sqrt(mp.pi) * alpha
ns = 1 - P / 48
print("\nP =", mp.nstr(P, 14), "  n_s = 1 - P/48 =", mp.nstr(ns, 10))
for name, val, unc in [("Planck 2018", 0.9649, 0.0042), ("ACT DR6 P-ACT-LB", 0.9743, 0.0034)]:
    print(f"  vs {name:18s} pull = {(float(ns) - val) / unc:+.2f} sigma")

# --- 4. chance-hit count ----------------------------------------------------
s2, s3, s6 = math.sqrt(2), math.sqrt(3), math.sqrt(6)
target = 31104 / float(codata)                      # numerator that reproduces CODATA
win = 31104 * float(codata_unc) / float(codata) ** 2  # one sigma, in numerator units
A, B, C = np.meshgrid(np.arange(173), np.arange(173), np.arange(173), indexing="ij")
keep = (A + B + C) <= 172
A, B, C = A[keep], B[keep], C[keep]
D = 172 - A - B - C
val = A + B * s2 + C * s3 + D * s6
dist = np.abs(val - target) / win
print(f"\nSplits of 172 records into four non-negative counts: {val.size}")
for k in (1, 10, 1000):
    print(f"  within {k:>4} sigma of CODATA: {(dist < k).sum()}")
wide = 1.0e5
print(f"  local density: {(dist < wide).sum()} within {wide:.0e} sigma"
      f" -> expected chance hits within 1 sigma = {(dist < wide).sum() / wide:.2e}")
best = np.argsort(dist)[:2]
for i in best:
    print("  closest:", (int(A[i]), int(B[i]), int(C[i]), int(D[i])), f"at {dist[i]:.2f} sigma")
