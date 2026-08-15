# Observer Patch Holography — An Independent Investigation

*A verification-and-extension study of the OPH framework (FloatingPragma/observer-patch-holography).*
*Dated 2026-07-13. Methods: independent symbolic recomputation, controlled source-code experiments, and machine-checked proofs — no reliance on OPH's own scripts for any headline claim.*

---

## Executive summary

Observer Patch Holography (OPH), by Bernhard Mueller, is a proposed "observer-consistency theory of everything": no observer sees the whole world; each holds a local patch; **physics is the public fixed point that survives agreement across overlapping patches.** It claims to recover General Relativity and the Standard Model from a handful of axioms plus one number.

After independently checking its headline numbers, auditing the source code behind them, examining the formal proofs, and stress-testing the boldest applications, the verdict is:

> **OPH is neither crank numerology nor the "true theory of everything" it advertises. It is a serious framework with one genuinely impressive physics result (the cosmological-constant magnitude), a logically sound consensus core (which this study completes and extends past the authors' own proofs), and a presentation layer that systematically oversells conditional results as parameter-free — with the applications layer containing an outright internal contradiction.**

Crucially, the honesty is not uniform. There is a clear **gradient**: OPH's technical corpus (papers, claim registry, theorem gates, negative-control lists) is scrupulous about what is *not* derived; the README slightly oversells; and the popular/applications layer is the boldest and least evidenced.

This study also makes **constructive contributions**: five machine-checked proofs that complete and generalize OPH's `sorry`-bearing formal core across three layers (algebraic, multi-observer, dynamical), plus a new sharp falsifier the framework does not state.

---

## Method

Every headline claim was re-derived from authoritative inputs (PDG/NIST/Planck) rather than trusted from OPH's outputs. Three independent instruments were used:

- **`symbolicaql`** — a symbolic-math engine, for recomputing OPH's algebraic identities and closed forms from scratch.
- **OPH's own solver, run as a controlled experiment** — the α/electroweak chain (`code/P_derivation/`, pure-`Decimal` stdlib) was executed with single constants swapped, isolating one assumption at a time.
- **`spleanql`** — a dependent-type-theory proof kernel (no tactics, explicit recursors), for machine-checking the formal claims and building extensions.

Findings were tracked as hypotheses with confidence "mass" in a `labbookql` notebook (domain `oph`), each with a concluded experiment and committed evidence. The full ledger appears at the end.

---

## Part I — What OPH is

OPH reconstructs physics from finite observer patches whose descriptions must agree where they overlap. Its four operational pillars: **Boundary** (each observer has limited local access), **Readback** (records become objective when comparable across boundaries), **Repair** (conflicting records generate pressure to update), **Continuation** (records determine where observers can stably exist).

Quantitatively, everything hangs on two fixed points:
- a local **pixel fixed point** `P⋆ ≈ 1.6310`, solving `P = φ + √π / A_T(P)` (φ = golden ratio), which feeds α, gauge structure, and particle rows;
- a global **record-capacity fixed point** `N_CRC ≈ 10¹²²`, feeding cosmology.

The repository is large and actively developed (≈1,190 commits, 878 Python files, 19 Lean files, six papers, a book, a claim registry, runnable verification code).

---

## Part II — Independent numerical verification

Recomputed from authoritative inputs on `symbolicaql`:

| Quantity | OPH formula | Independent result | vs. experiment | Verdict |
|---|---|---|---|---|
| Spectral tilt | n_s = 1 − P⋆/48 | 0.9660215 | **0.27σ** from Planck | ✓ clean |
| Cosmological constant | N_CRC = π·exp(6π/(P·α_U)) | log₁₀ = 122.55 | **7%** from observed dS entropy | ✓ striking |
| MOND scale | a₀ = (15/8π²)c²√(Λ/3) | 1.03×10⁻¹⁰ m/s² | ratio 0.86 to empirical | ✓ within 15% |
| Proton spin | C_F/(C_F+C_A) = 4/13 | 0.3077 | 0.59σ from 0.29±0.03 | ✓ |
| Koide phase | δ = 2/9 | 0.22222 | see below | ~ oversold precision |
| Baryon ratio | (1/6)¹² | 4.59×10⁻¹⁰ | factor 1.33 low | ~ order-of-magnitude |
| Fine structure α⁻¹ | √π/(P−φ) | 136.9948 (source) | needs +0.041 hadron closure | ✗ see Part III |

**Koide caveat (new finding).** Recomputing the phase from raw PDG lepton masses gives δ = 0.222221 (electron anchor) to 0.222270 (τ anchor), because Koide's Q = 0.6666605 is not *exactly* 2/3. So δ ≈ 2/9 holds to ~4 significant figures, but the advertised "match to 4 ppm (0.2222248 ± 6.3e-6)" is convention-dependent and overstates the robustness.

---

## Part III — The α crux: a SUSY-conditional knife-edge

OPH's flagship claim is deriving α ("from one number"). Reading the actual solver (`code/P_derivation/paper_math.py`) shows the fixed point is **genuine** — A_T(P) is built from P via group theory and RG running with **no measured coupling, mass, or angle used as a target.** So α is *not* a naive fit. But two things the marketing omits are load-bearing:

**1. It structurally assumes supersymmetry.** The running uses `b_mssm = (33/5, 1, −3)` — the *MSSM* beta coefficients. A controlled experiment (OPH's own solver, only the betas swapped to the Standard Model values (41/10, −19/6, −7)):

| Betas | α⁻¹ | closure |
|---|---|---|
| MSSM (OPH) | **136.99483** (reproduces documented value) | ✓ |
| SM (physical) | — | **fails: no valid m_Z fixed point** |

The SM's negative b₂, b₃ drive the inverse couplings through zero inside the solver's running range (α₂⁻¹ = −0.20), so α goes negative and the construction produces *no α at all*. With the physically-correct Standard Model spectrum, the result does not merely change — it ceases to exist.

**2. α = 137 is a knife-edge in particle-content space.** Mapping α⁻¹ over the beta coefficients (a scan OPH never publishes):

| b₂ (b₃=−3) | 2.0 | 1.5 | **1.0 (MSSM)** | 0.7 | 0.4 | 0.0 |
|---|---|---|---|---|---|---|
| α⁻¹ | 123.3 | 129.7 | **137.0** | 141.9 | 147.2 | 155.0 |

Sensitivity dα⁻¹/db₂ ≈ −16, dα⁻¹/db₃ ≈ −12 per unit; the measured value is hit *only* at the MSSM integers, and the construction fails outside a narrow band. **α = 137 is inherited from the assumed MSSM spectrum on a steep slope — the α prediction is exactly as strong as OPH's (unproven) claim to derive supersymmetry, no stronger.**

**3. The "exact" α is empirically closed.** The strict source-only value is 136.9948 (~0.03% off); reaching 137.036 requires adding empirical e⁺e⁻→hadrons data. OPH's own `SOURCE_SPECTRAL_THEOREM.md` concedes the needed hadronic spectral measure is "absent from the current corpus."

**A new falsifier (constructive).** Because α = 137 ⟺ MSSM betas, OPH gains a sharp test it does not state: *if collider data establishes SM-like (non-MSSM) running of the couplings, OPH's α prediction is falsified.* This turns the SUSY-dependence critique into a Popperian virtue.

**Electroweak masses.** The same chain's "0.02–0.08% agreement" for W/Z/Higgs masks that, at real measurement precision, Z is **−34.5σ**, the strict Higgs **+5.8σ**, and W **−2.95σ** from data. Only the top (+0.10σ) and Λ_QCD (−0.27σ) are genuine precision matches.

---

## Part IV — The cosmological constant: OPH's strongest result

OPH's capacity fixed point is `N_CRC = π·exp(6π/(P·α_U))`, built from the same source quantities as α. Independently:

- OPH: **log₁₀ N_CRC = 122.55** (~3.5×10¹²²)
- Observed de Sitter entropy S = 3π/(Λℓ_P²): **log₁₀ S = 122.52** (~3.3×10¹²²)

They agree to **7%**. OPH reproduces the *magnitude* of the cosmological constant — the notorious 120-orders-of-magnitude problem — from the α fixed point. That is more than most theories achieve.

The result is hyper-sensitive to the integer "6" (≈20 orders of magnitude per unit; the value needed to hit Λ exactly is 5.9986, and OPH uses 6). Auditing that integer's provenance largely vindicates it: **6 = m_rep/β_EW = 24/4**, where **24 = 2·dim(su(3)⊕su(2)⊕u(1)) = 2·(8+3+1)** (twice the SM gauge-algebra dimension) and **4 = n_c+1**. OPH documents seven *rejected* alternative integers (including "24-from-SU(5)," rejected despite giving the same value) and a no-empirical-input ledger. So the integer is structurally derived, not tuned to Λ. Residual caveats: the ×2 orientation-doubling axiom is the softest link, and the result inherits α_U's MSSM-conditionality.

---

## Part V — Formal-proof status, and a completed replacement

**What OPH actually proves.** Its Lean (`Lean/ObserverPatchHolography/`) does *not* machine-check its central Proposition 4.2. The repair operator itself is literally `sorry`:
- `localRepair` (Primitives.lean:129), `Repair` (:133), and `repair_respects_gauge` are `sorry`.
- What *is* sorry-free: generic Newman's-lemma abstract rewriting over an *opaque* relation (self-labeled "a skeleton, not a Prop 4.2 statement"), boundary reconstruction over one concrete demo carrier, and a two-bit example. The authors state this explicitly (Primitives.lean:1027–1032).

So the "Lean-verified consensus core" reduces to standard textbook rewriting plus a demo, with the dynamical heart deliberately unproven.

**What this study proves instead.** Five `spleanql` artifacts (all axiom-free modulo the carrier) complete and generalize the core across three layers:

| Layer | File | Content |
|---|---|---|
| Toy | `oph_consensus_core.splean` | 2-state consensus: convergence, idempotence, overlap agreement |
| Concrete fill | `oph_repair_prop42.splean` | a concrete (non-`sorry`) repair on a two-patch net discharges consistency, faithfulness, idempotence, and the **gauge congruence OPH leaves `sorry`** |
| Algebraic (general) | `oph_repair_general.splean` | Prop 4.2 for **any** carrier from one read-after-write law `r(w v)=v`; concrete witness proves non-vacuity |
| Multi-observer | `oph_consensus_extended.splean` | overlap consensus, universal agreement on public states, transitive propagation → the public world is **globally** well-defined |
| Dynamical | `oph_repair_dynamical.splean` | **bounded Lyapunov convergence**: from any state, Φ(s) repair steps reach consensus (Φ=0), by induction on the potential |

Two structural insights fall out of the `#axioms` receipts, neither stated by OPH:
- **Two-layer decomposition.** Gauge-invariance and consensus (`repair_respects_gauge`, `overlap_consensus`, `consensus_transitive`) need *no* coherence law — they are pure congruence. Only convergence/faithfulness use read-after-write. This mirrors physics (gauge symmetry exact; equilibration conditional) and suggests a cleaner OPH axiomatization.
- The dynamical convergence — the piece OPH leaves `sorry` and earlier work modeled only as a one-shot retraction — is genuinely provable from a single descent law.

Together these constitute a machine-checked OPH consensus/repair theory that **strictly exceeds OPH's own (sorry-bearing, single-carrier) Lean.**

---

## Part VI — The applications layer (OMEGA)

The website (`omega.floatingpragma.io`) and `APPLICATIONS.md` claim tabletop fusion, anti-gravity hoverbikes, AGI, and compute. All are honestly labeled *Draft / pre-hardware / "not measured evidence."* Two observations:

- **Internal contradiction.** `APPLICATIONS.md:58` claims a ~$1,000 build "would likely mine a Bitcoin block in milliseconds." That requires candidate enrichment of **~10¹³** even at an absurdly optimistic 10¹² optical evals/s — i.e., *solving* the proof-of-work search. But the README insists the compute lift is modest and "the classical complexity-class problem remains untouched." The boldest OMEGA claim contradicts OPH's own stated limitation (and SHA-256d has no exploitable pre-evaluation structure to enable it).
- **No hardware evidence.** The one place OPH ran real hardware, the IBM Quantum Cloud archive (frozen 2026-07-11), states plainly: *"No experiment in this bundle distinguishes OPH from standard quantum mechanics."*

---

## Part VII — The meta-pattern

The single most useful finding for a reader deciding how to weigh OPH:

> **The honesty runs corpus → README → applications.** The technical papers are rigorous and self-critical — they explicitly disclaim neutrinos (a "rejected target-informed candidate" from a "hand-written template" that NuFIT rejects), baryogenesis/sphaleron ("no baryogenesis theorem package"), quark masses (proven non-identifiability), and the Yang-Mills gap (conditional). The misleading impression comes from popular headlines and isolated close-looking numbers, not the documents. The two places even the README oversteps are the α "zero-input" framing and the "matches the W/Z/Higgs" phrasing.

The right critique target is the marketing, not the corpus.

---

## Part VIII — Simulation, and the accommodation pattern

The analytical study was followed by **four independent simulations** and a native **3D app**, so the mechanism could be *run*, not just read.

- **Consensus dynamics** (`oph_consensus_sim.py`): OPH's repair reaches the public fixed point on every topology, and the convergence **rate = the patch-net's spectral gap** (algebraic connectivity) — classical Laplacian-consensus theory. This *measures* the dynamical-rate law OPH leaves abstract (the "form"), while the cosmological *value* still needs the physical screen graph.
- **Dark matter, 2D** (`oph_darkmatter_sim.py`, `..._interaction.py`): a topological defect leaves an **unrepairable residual** only where repair fails, with an extended ~1/r² (isothermal-halo) profile and a logarithmic (deep-MOND) two-defect interaction. Qualitatively supportive of OPH's "dark stress = imperfect repair."
- **Dark matter, genuine 3D** ([oph-sim-macos](../../oph-sim-macos), an interactive SwiftUI/SceneKit app): the decisive dimensional-lift test. A vortex **line** (2D-symmetric) reproduces the isothermal halo (p ≈ −2.4); a **localized vortex loop** gives **p ≈ −6.5** — a compact, Newtonian (dipole) knot, *not* a dark-matter halo. **The MOND-shaped halo was a 2D/line-symmetry artifact; it does not survive to a localized 3D defect.** This *revised the earlier supportive finding downward* — the discipline held even against OPH.

### How OPH explains a result it did not predict

That 3D result is the sharpest single example of the pattern the whole study found. *Can OPH explain it?* Yes — and grounded in its own text: OPH's dark stress is a **"collar remainder"** built on **extended, codimension-1 structures** (collars, quotient-edges, finite-thickness bands — 84 "collar" mentions in the dark-matter paper, with a thickness hierarchy `ℓ_UV ≪ δ_collar ≪ ℓ`). That *is* the extended defect the 3D sim shows produces an isothermal halo; the localized loop that came out Newtonian is simply not OPH's object.

But the explanation is **accommodation, not prediction**:
1. OPH *assumed* the extended collar; it never stated that *localized* defects fail. The simulation supplies the missing "why."
2. OPH is holographic — everything lives on 2D screens — so codimension-1 is *baked in*. Consistency with an extended-defect result is partly structural inevitability, not a risky bet. **The machinery is rich enough to accommodate the outcome, which is exactly why OPH is hard to falsify.**

The constructive flip: this sharpens into one genuine, falsifiable claim OPH should adopt explicitly — *the dark stress is codimension-1, so dark matter traces extended, web-like structure (filaments and sheets), not isolated point clumps* — which loosely matches the observed cosmic web. A negative simulation result thus becomes the flip side of a real OPH-flavored prediction.

**This is the framework in miniature:** OPH explains, by a construction flexible enough that "explains" means "was built to accommodate" more than "forecast" — while still yielding one crisp, checkable commitment.

## Evidence ledger

Eighteen hypotheses (labbookql, domain `oph`), each with a concluded experiment and committed evidence. Confidence "mass" reflects the weight of evidence after this study.

| Mass | Hypothesis |
|---|---|
| 0.90 | α/EW chain uses no measured target **but is conditional on assumed MSSM/SUSY betas** |
| 0.90 | Prop 4.2 `sorry`-gap is fillable (concrete repair, gauge congruence proved) |
| 0.85 | Dynamical Prop 4.2 (iterated repair → consensus) machine-provable via Lyapunov descent |
| 0.80 | α⁻¹ ≈ 137 is a knife-edge selecting the MSSM integers |
| 0.80 | Multi-observer thesis machine-checkable, extending the single-carrier core |
| 0.70 | Spectral tilt n_s = 1 − P⋆/48 matches Planck (0.27σ) |
| 0.70 | Consensus/repair core is a consistent machine-checkable structure |
| 0.70 | Cosmological-constant magnitude (~10¹²²) is a genuine structural prediction |
| 0.65 | MOND scale a₀ matches empirical (within 15%) |
| 0.60 | Proton-spin fraction 4/13 matches (0.59σ) |
| 0.55 | Koide phase δ = 2/9 (real, but ppm precision is convention-dependent) |
| 0.45 | Baryon ratio (1/6)¹² (order-of-magnitude only, factor 1.33 low) |
| 0.40 | α⁻¹ is a **zero-input** prediction (genuine fixed point, but MSSM-conditional + hadron-incomplete) |
| 0.25 | Strict W/Z/H masses match **at measurement precision** (no — tens of σ) |
| 0.25 | Central consensus dynamics is machine-checked **in OPH's Lean** (no — it's `sorry`) |
| 0.25 | OPH predicts neutrino masses/mixing from source (no — rejected template) |
| 0.20 | OPH derives the sphaleron/baryogenesis value (no — disavowed in the corpus) |
| 0.20 | Bitcoin-in-ms compute claim is consistent with OPH's complexity limitation (no — contradiction) |

---

## Limitations of this study

- The dynamical convergence theorem is proved for an *abstract* potential and descent law; it does not construct a concrete non-trivial repair operator over general finite patch-nets with an *async schedule* and a derived potential — that fuller mechanization remains open (as it is in OPH).
- The α controlled experiment used reduced group-theory cutoffs (applied equally to both branches); it reproduces the documented MSSM value to 5+ digits, so the MSSM-vs-SM contrast is faithful, but the absolute reduced-cutoff numbers are not the full-precision values.
- The cosmological-constant provenance audit vindicates the integer 6 up to the orientation-doubling axiom, which was not independently re-derived here.
- No independent physical experiment was performed; "verification" here means recomputation, code audit, and proof, not laboratory test.

---

## Reproducibility

- **OPH repo:** `FloatingPragma/observer-patch-holography` (cloned into this working tree).
- **Proof artifacts (this study):** `verification/*.splean` (five files), checked with `spleanql <file>`.
- **Controlled experiments:** `sm_vs_mssm.py`, `beta_scan.py` (patch `paper_math.PaperMathContext.b_mssm`; pure stdlib, no venv needed).
- **Symbolic checks:** `symbolicaql eval` (fine structure, Koide, N_CRC, MOND, σ-distances).
- **Logbook:** `labbookql query "SELECT mass,label FROM hypotheses WHERE domain='oph' ORDER BY mass DESC"`.

---

## Conclusion

OPH deserves to be taken more seriously than a typical "theory of everything" and less literally than its marketing. Its consensus/repair core is a coherent, now fully machine-checked idea; its cosmological-constant result is genuinely impressive and survives provenance scrutiny; and its papers are honest about their many open gaps. But its flagship α claim is a supersymmetry-conditional knife-edge dressed as parameter-free, its electroweak "agreements" are many-sigma at real precision, and its applications layer overreaches to the point of self-contradiction.

The most durable output of this study is not the verdict but the **method and the extensions**: independent recomputation over trust, controlled single-variable experiments on the authors' own code, and a completed formal core that carries OPH's central thesis further than its authors did — including a concrete, testable falsifier they can adopt.
