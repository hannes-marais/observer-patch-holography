#!/usr/bin/env python3
"""Two-defect interaction in the OPH patch-net: do 'dark masses' interact, and how?

Extends oph_darkmatter_sim.py to TWO topological defects (vortices) separated by d.
Interaction energy  E_int(d) = Phi_min(pair) - Phi_min(A alone) - Phi_min(B alone).

Prediction (2D frustrated-consensus / vortex physics): E_int ~ C * q_A q_B * ln(d)
-- a LOGARITHMIC potential, i.e. a 1/d force. A log potential is exactly the
deep-MOND regime (it yields flat rotation curves). So this tests whether OPH's
repair-defect 'dark matter' interacts MOND-like.

HONEST caveat baked in: 2D Green's function is intrinsically ~ln(r), so a log law
here is partly a DIMENSIONAL artifact, not proof of 3D MOND. We measure and say so.
"""
import numpy as np

def build(L):
    idx = lambda r, c: r*L + c
    edges = []
    for r in range(L):
        for c in range(L):
            if c+1 < L: edges.append((idx(r, c), idx(r, c+1)))
            if r+1 < L: edges.append((idx(r, c), idx(r+1, c)))
    B = np.zeros((len(edges), L*L))
    for e, (i, j) in enumerate(edges):
        B[e, i] = 1.0; B[e, j] = -1.0
    return B, edges

def wrap(a): return (a + np.pi) % (2*np.pi) - np.pi

def offsets(edges, L, cores):
    # sum of vortex phases from each (core, charge); b = wrapped phase diff per edge
    coord = lambda k: (k % L, k // L)
    b = np.zeros(len(edges))
    for e, (i, j) in enumerate(edges):
        ci, ri = coord(i); cj, rj = coord(j)
        ti = sum(q*np.arctan2(ri - cy, ci - cx) for (cx, cy, q) in cores)
        tj = sum(q*np.arctan2(rj - cy, cj - cx) for (cx, cy, q) in cores)
        b[e] = wrap(tj - ti)
    return b

L = 31
B, edges = build(L)
Lap = B.T @ B
Lpinv = np.linalg.pinv(Lap)          # compute once; reuse for every configuration
def phi_min(b):
    x = Lpinv @ (B.T @ b)
    r = B @ x - b
    return 0.5 * r @ r

cx0 = cy0 = L/2 - 0.5
print("=== Two-defect interaction: do OPH 'dark masses' interact, and how? ===\n")
for label, qB in [("same charge (+,+)", +1), ("opposite charge (+,-)", -1)]:
    print(f"--- {label} ---")
    print(f"{'sep d':>6} {'Phi_pair':>10} {'E_int':>10}")
    ds, Es = [], []
    for d in [3, 4, 5, 6, 8, 10, 12, 14]:
        A = (cx0 - d/2, cy0, +1); Bc = (cx0 + d/2, cy0, qB)
        pair = phi_min(offsets(edges, L, [A, Bc]))
        sa = phi_min(offsets(edges, L, [A]))
        sb = phi_min(offsets(edges, L, [Bc]))
        Eint = pair - sa - sb
        ds.append(d); Es.append(Eint)
        print(f"{d:>6} {pair:>10.3f} {Eint:>10.3f}")
    ds, Es = np.array(ds), np.array(Es)
    slope = np.polyfit(np.log(ds), Es, 1)[0]
    # force F = -dE/dd; energy RISES with separation (slope>0) => attractive (bound),
    # energy DROPS with separation (slope<0) => repulsive.
    force = "attractive" if slope > 0 else "repulsive"
    print(f"  fit: E_int = {slope:.2f} * ln(d) + const   ({force}: energy "
          f"{'rises' if slope>0 else 'drops'} with separation)\n")

print("Reading: E_int linear in ln(d) => a 1/d force = LOGARITHMIC potential = the")
print("deep-MOND / flat-rotation-curve force law. Same-charge repel, opposite attract,")
print("like 2D charges. CAVEAT: 2D Green's function is ~ln(r) intrinsically, so the log")
print("law is partly dimensional; it is MOND-SHAPED, not a derivation of 3D MOND.")
