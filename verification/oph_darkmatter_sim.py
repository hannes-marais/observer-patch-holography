#!/usr/bin/env python3
"""Independent test of OPH's dark-matter mechanism: 'dark/anomaly stress is imperfect
observer-patch repair bookkeeping' (oph_dark_matter_paper).

Setup: an L x L grid of observer patches. Each overlap (edge) carries a required
offset b_ij (the patches should agree up to b_ij: x_i - x_j = b_ij). With b = 0
everywhere, repair reaches perfect consensus (Phi = 0). A DEFECT is a loop with
nonzero HOLONOMY -- a plaquette where the offsets don't close (curvature the repair
cannot gauge away). We inject a unit vortex: b_ij = wrap(theta_j - theta_i) around a
core, so the holonomy around the core is 2*pi and zero elsewhere.

Repair minimizes  Phi(x) = 1/2 * ||B x - b||^2   (B = incidence matrix).
Residual per edge  r = B x - b;  Phi_min = 1/2 ||r||^2  is the UNREPAIRABLE remainder.

OPH's claim, made checkable:
  (1) Phi_min > 0 ONLY when a defect is present (no defect -> perfect repair, no dark stress).
  (2) the residual 'stress' localizes at the defect,
  (3) with an EXTENDED tail (halo-like), not a point -- residual energy density ~ dist^-p.
"""
import numpy as np

def build(L):
    idx = lambda r, c: r*L + c
    edges = []
    for r in range(L):
        for c in range(L):
            if c+1 < L: edges.append((idx(r, c), idx(r, c+1)))
            if r+1 < L: edges.append((idx(r, c), idx(r+1, c)))
    n, m = L*L, len(edges)
    B = np.zeros((m, n))
    for e, (i, j) in enumerate(edges):
        B[e, i] = 1.0; B[e, j] = -1.0
    return B, np.array(edges), n, m

def wrap(a):
    return (a + np.pi) % (2*np.pi) - np.pi

def vortex_offsets(edges, L, charge, core):
    # ideal phase of a charge-q vortex at `core`; b on edge = wrapped phase difference
    cx, cy = core
    coord = lambda k: (k % L, k // L)   # (c, r)
    th = {}
    b = np.zeros(len(edges))
    for e, (i, j) in enumerate(edges):
        ci, ri = coord(i); cj, rj = coord(j)
        ti = charge*np.arctan2(ri - cy, ci - cx)
        tj = charge*np.arctan2(rj - cy, cj - cx)
        b[e] = wrap(tj - ti)
    return b

def repair(B, b):
    L = B.T @ B                      # graph Laplacian (singular: constant null space)
    x, *_ = np.linalg.lstsq(L, B.T @ b, rcond=None)
    r = B @ x - b                    # residual per edge (the unrepairable remainder)
    return x, r

L = 25
B, edges, n, m = build(L)
core = (L/2 - 0.5, L/2 - 0.5)        # vortex core at the central plaquette
coord = lambda k: (k % L, k // L)

print("=== OPH dark stress = imperfect repair? Test on a defective patch-net ===\n")

# (1) no defect vs defect
b0 = np.zeros(m)
_, r0 = repair(B, b0)
bd = vortex_offsets(edges, L, 1, core)
xd, rd = repair(B, bd)
print(f"no defect : Phi_min = {0.5*(r0@r0):.3e}   (perfect repair, no dark stress)")
print(f"1 defect  : Phi_min = {0.5*(rd@rd):.3e}   (UNrepairable residual = dark stress)")

# (2) response vs number of defects (charge)
print("\ncharge q :  Phi_min      ratio to q^2")
base = None
for q in [1, 2, 3, 4]:
    bq = vortex_offsets(edges, L, q, core)
    _, rq = repair(B, bq)
    P = 0.5*(rq@rq)
    if base is None: base = P
    print(f"   q={q}   :  {P:.3e}    {P/(base*q*q):.3f}")

# (3) radial profile of residual energy density around the defect (halo tail?)
edge_mid = np.array([[ (coord(i)[0]+coord(j)[0])/2, (coord(i)[1]+coord(j)[1])/2 ]
                     for (i, j) in edges])
dist = np.sqrt((edge_mid[:,0]-core[0])**2 + (edge_mid[:,1]-core[1])**2)
energy = rd**2
print("\nradial profile of residual energy density (charge-1 defect):")
print(f"{'dist bin':>10} {'<r^2>':>12} {'count':>6}")
bins = [(0.5,1.5),(1.5,2.5),(2.5,3.5),(3.5,5),(5,7),(7,9),(9,12)]
centers, dens = [], []
for lo, hi in bins:
    mask = (dist >= lo) & (dist < hi)
    if mask.sum() == 0: continue
    d = energy[mask].mean(); c = 0.5*(lo+hi)
    centers.append(c); dens.append(d)
    print(f"{lo:>4.1f}-{hi:<4.1f} {d:>12.3e} {mask.sum():>6}")
# fit power law density ~ dist^p on the tail
c = np.array(centers); dq = np.array(dens); good = dq > 0
p = np.polyfit(np.log(c[good]), np.log(dq[good]), 1)[0]
print(f"\nresidual energy density falloff exponent p (density ~ dist^p): {p:.2f}")
print("(a pure vortex field ~ 1/dist gives energy density ~ dist^-2; p near -2 => extended halo-like tail)")
