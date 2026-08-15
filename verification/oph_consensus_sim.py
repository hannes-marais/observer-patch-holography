#!/usr/bin/env python3
"""Independent OPH observer-patch consensus simulator.

Faithful minimal model of OPH's core loop: N observer patches on a graph (edges =
overlaps), each holding a local record x_i; the mismatch potential is
    Phi(x) = 1/2 * sum_{(i,j) in E} (x_i - x_j)^2   [Reality Def 2].
Repair drives overlapping patches toward agreement. Consensus (all equal, Phi=0)
is the public fixed point.

Two repair modes:
  * synchronous Laplacian descent   x <- x - dt * L x        (gradient flow on Phi)
  * asynchronous pairwise gossip     pick a random edge, average its endpoints
                                      (OPH's "local recovery move")

Questions:
  1. Does repair actually reach the consensus fixed point on a NON-trivial network?
     (my splean proofs show it must for the abstract model; this tests a concrete one)
  2. What sets the RATE? (the frontier I could not derive abstractly)
Prediction from classical consensus theory: Phi decays as exp(-2*lambda2*t), where
lambda2 = the second-smallest Laplacian eigenvalue = algebraic connectivity (spectral
gap). If the sim confirms this, the "dynamical law" OPH lacks is: rate = spectral gap.
"""
import numpy as np

rng = np.random.default_rng(7)

def laplacian(A):
    D = np.diag(A.sum(1))
    return D - A

def graph(kind, n):
    A = np.zeros((n, n))
    if kind == "path":
        for i in range(n-1): A[i, i+1] = A[i+1, i] = 1
    elif kind == "cycle":
        for i in range(n): A[i, (i+1) % n] = A[(i+1) % n, i] = 1
    elif kind == "complete":
        A = np.ones((n, n)) - np.eye(n)
    elif kind == "grid":
        s = int(round(n**0.5)); n = s*s; A = np.zeros((n, n))
        for r in range(s):
            for c in range(s):
                i = r*s+c
                if c+1 < s: j=i+1; A[i,j]=A[j,i]=1
                if r+1 < s: j=i+s; A[i,j]=A[j,i]=1
    elif kind == "random":
        while True:
            A = (rng.random((n, n)) < 0.15).astype(float); A = np.triu(A,1); A = A+A.T
            if np.all(laplacian(A).sum(1) >= 0) and connected(A): break
    return A

def connected(A):
    lam = np.linalg.eigvalsh(laplacian(A))
    return lam[1] > 1e-9

def phi(A, x):
    L = laplacian(A); return 0.5 * x @ L @ x

def sync_run(A, x0, dt, T):
    L = laplacian(A); x = x0.copy(); hist = [phi(A, x)]
    for _ in range(T):
        x = x - dt * (L @ x); hist.append(phi(A, x))
    return x, np.array(hist)

def gossip_run(A, x0, steps):
    edges = np.argwhere(np.triu(A) > 0); x = x0.copy(); hist = [phi(A, x)]
    rec = max(1, len(edges))
    for k in range(steps):
        i, j = edges[rng.integers(len(edges))]
        m = 0.5*(x[i]+x[j]); x[i] = x[j] = m
        if k % rec == 0: hist.append(phi(A, x))
    return x, np.array(hist)

def measured_rate(hist):
    # fit log(Phi) ~ -rate * t over the CLEAN exponential band only:
    # Phi between 1e-9 and 1e-1 of its start (above roundoff floor, past the transient).
    h0 = hist[0]
    t = np.arange(len(hist))
    mask = (hist > h0*1e-9) & (hist < h0*1e-1) & (hist > 0)
    if mask.sum() < 3:                      # converges too fast to fit (e.g. complete graph)
        return None
    slope = np.polyfit(t[mask], np.log(hist[mask]), 1)[0]
    return -slope

print("=== OPH patch-net consensus: does repair reach the fixed point, and what sets the rate? ===\n")
print(f"{'graph':10} {'N':>4} {'lambda2':>9} {'Phi_final':>12} {'converged':>10} {'meas.rate':>10} {'2*lambda2':>10} {'ratio':>7}")
for kind, n in [("path",20),("cycle",20),("grid",25),("random",30),("complete",20)]:
    A = graph(kind, n); N = A.shape[0]
    L = laplacian(A); lam = np.linalg.eigvalsh(L); lam2 = lam[1]
    x0 = rng.standard_normal(N); x0 -= x0.mean()
    dt = min(0.9/lam.max(), 0.05/lam2)         # stable AND dt*lambda2 << 1 (continuous regime)
    xf, hist = sync_run(A, x0, dt, 8000)
    conv = phi(A, xf) < 1e-9
    # measured decay per unit time (dt-scaled): Phi ~ exp(-2*lambda2 * (dt*step))
    rps = measured_rate(hist)
    if rps is None:
        print(f"{kind:10} {N:>4} {lam2:>9.4f} {phi(A,xf):>12.2e} {str(conv):>10} {'too-fast':>10} {2*lam2:>10.4f} {'--':>7}")
    else:
        rate_per_time = rps/dt; ratio = rate_per_time/(2*lam2)
        print(f"{kind:10} {N:>4} {lam2:>9.4f} {phi(A,xf):>12.2e} {str(conv):>10} {rate_per_time:>10.4f} {2*lam2:>10.4f} {ratio:>7.3f}")

print("\n=== asynchronous pairwise gossip (OPH's local recovery move) ===")
print(f"{'graph':10} {'N':>4} {'Phi_final':>12} {'converged':>10}")
for kind, n in [("path",20),("cycle",20),("grid",25),("random",30),("complete",20)]:
    A = graph(kind, n); N = A.shape[0]
    x0 = rng.standard_normal(N); x0 -= x0.mean()
    xf, hist = gossip_run(A, x0, 40000)
    print(f"{kind:10} {N:>4} {phi(A,xf):>12.2e} {str(phi(A,xf) < 1e-6):>10}")
