# Observer Patch Holography — An Independent Investigation

*A verification-and-extension study of the OPH framework (FloatingPragma/observer-patch-holography).*
*Dated 2026-07-13. Updated 2026-11-10. Methods: independent symbolic recomputation, controlled source-code experiments, and machine-checked proofs — no reliance on OPH's own scripts for any headline claim.*

---

> **Revision note (2026-11-10).** Parts I–VIII record OPH as examined on 2026-07-13. Two things have changed. First, Part V has been wrong since 2026-07-18: five days after this study, upstream replaced the `sorry` placeholders for the repair operator with a construction and proofs (commit `d007c5e61`). The statements made here about OPH's Lean, and the claim that this study's proofs exceeded it, no longer hold; Part V, the ledger and the limitations are corrected in place. Second, by November 2026 upstream had changed direction and withdrawn most of the quantitative claims audited here. Part IX records a re-look at upstream as of 2026-11-11 and says which earlier findings stand.

---

## Executive summary

Observer Patch Holography (OPH), by Bernhard Mueller, is a proposed "observer-consistency theory of everything": no observer sees the whole world; each holds a local patch; **physics is the public fixed point that survives agreement across overlapping patches.** It claims to recover General Relativity and the Standard Model from a handful of axioms plus one number.

After independently checking its headline numbers, auditing the source code behind them, examining the formal proofs, and stress-testing the boldest applications, the verdict is:

> **OPH is neither crank numerology nor the "true theory of everything" it advertises. It is a serious framework with one genuinely impressive physics result (the cosmological-constant magnitude), a logically sound consensus core (which this study formalizes independently), and a presentation layer that systematically oversells conditional results as parameter-free — with the applications layer containing an outright internal contradiction.**

Crucially, the honesty is not uniform. There is a clear **gradient**: OPH's technical corpus (papers, claim registry, theorem gates, negative-control lists) is scrupulous about what is *not* derived; the README slightly oversells; and the popular/applications layer is the boldest and least evidenced.

This study also makes **constructive contributions**: five machine-checked proofs that formalize the consensus core independently across three layers (algebraic, multi-observer, dynamical), written while the repair operator in OPH's own Lean was still `sorry`, plus a sharp falsifier the framework did not state.

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

## Part V — Formal-proof status, and an independent formalization

**What OPH's Lean proved on 2026-07-13.** At that date its Lean (`Lean/ObserverPatchHolography/`) did *not* machine-check its central Proposition 4.2. The repair operator itself was literally `sorry`:
- `localRepair` (Primitives.lean:129), `Repair` (:133), and `repair_respects_gauge` were `sorry`.
- What *was* sorry-free: generic Newman's-lemma abstract rewriting over an *opaque* relation (self-labeled "a skeleton, not a Prop 4.2 statement"), boundary reconstruction over one concrete demo carrier, and a two-bit example. The authors stated this explicitly (Primitives.lean:1027–1032).

**Corrected status (from 2026-07-18).** Upstream commit `d007c5e61` replaced those placeholders, and the change is in this repository's own tree. `localRepair` is a constructed single-site move, `Repair` is an asynchronous schedule run to a normal form, and `repair_respects_gauge` is proved for any finite carrier, together with `lyapunovDescent_holds`, `termination_holds`, `Repair_normalForm` and `Repair_reachable`. The file reports that these depend only on the standard Lean/Mathlib axioms. It also states its own limits: completeness is proved only under stated local repair laws (frustration-free dynamics), and confluence is false in general (`demoCarrier_not_confluent`). A static scan of all 681 Lean files at upstream `6529d3ce7`, with comments and strings stripped, finds no `sorry`, no `admit`, no `axiom` declaration and 13 uses of `native_decide`. The library was not built for this check.

The July conclusion that the "Lean-verified consensus core" reduced to textbook rewriting plus a demo is therefore withdrawn.

**What this study proved.** Five `spleanql` artifacts (all axiom-free modulo the carrier) formalize the core independently, in a different proof kernel, across three layers:

| Layer | File | Content |
|---|---|---|
| Toy | `oph_consensus_core.splean` | 2-state consensus: convergence, idempotence, overlap agreement |
| Concrete fill | `oph_repair_prop42.splean` | a concrete (non-`sorry`) repair on a two-patch net discharges consistency, faithfulness, idempotence, and the **gauge congruence that OPH's Lean left `sorry` at the time** |
| Algebraic (general) | `oph_repair_general.splean` | Prop 4.2 for **any** carrier from one read-after-write law `r(w v)=v`; concrete witness proves non-vacuity |
| Multi-observer | `oph_consensus_extended.splean` | overlap consensus, universal agreement on public states, transitive propagation → the public world is **globally** well-defined |
| Dynamical | `oph_repair_dynamical.splean` | **bounded Lyapunov convergence**: from any state, Φ(s) repair steps reach consensus (Φ=0), by induction on the potential |

Two structural observations fall out of the `#axioms` receipts:
- **Two-layer decomposition.** Gauge-invariance and consensus (`repair_respects_gauge`, `overlap_consensus`, `consensus_transitive`) need *no* coherence law — they are pure congruence. Only convergence/faithfulness use read-after-write. This mirrors physics (gauge symmetry exact; equilibration conditional) and suggests a cleaner OPH axiomatization. Upstream's own proof of `repair_respects_gauge` rests on the same fact: everything the repair consults is a function of the declared overlap data.
- The dynamical convergence, which earlier work here modeled only as a one-shot retraction, is provable from a single descent law. Upstream proves descent and termination for a concrete asynchronous operator, which goes further than the abstract descent law assumed here.

On 2026-07-13 these proofs went beyond OPH's own Lean. **That comparison no longer holds.** Upstream's constructed operator over general finite carriers is the stronger mechanization of the single-carrier theory. Whether upstream also covers the multi-observer theorems (`overlap_consensus`, `consensus_transitive`) was not checked.

---

## Part VI — The applications layer (OMEGA)

The website (`omega.floatingpragma.io`) and `APPLICATIONS.md` claim tabletop fusion, anti-gravity hoverbikes, AGI, and compute. All are honestly labeled *Draft / pre-hardware / "not measured evidence."* Two observations:

- **Internal contradiction.** `APPLICATIONS.md:58` claims a ~$1,000 build "would likely mine a Bitcoin block in milliseconds." That requires candidate enrichment of **~10¹³** even at an absurdly optimistic 10¹² optical evals/s — i.e., *solving* the proof-of-work search. But the README insists the compute lift is modest and "the classical complexity-class problem remains untouched." The boldest OMEGA claim contradicts OPH's own stated limitation (and SHA-256d has no exploitable pre-evaluation structure to enable it).
- **No hardware evidence.** The one place OPH ran real hardware, the IBM Quantum Cloud archive (frozen 2026-07-11), states plainly: *"No experiment in this bundle distinguishes OPH from standard quantum mechanics."*

*Status, November 2026:* `APPLICATIONS.md` and the Bitcoin claim are no longer in the upstream repository, and its falsification programme lists the hardware and anti-gravity continuations as ineligible. The website was not re-checked.

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

---

## Part IX — November 2026 re-look

*Added 2026-11-10. Scope: a read-only review of upstream `main` at commit `6529d3ce7` (2026-11-11), 2,505 commits after this fork's branch point. Numbers were recomputed with standalone `mpmath` (`oph_relook_recheck.py`). The Lean library was scanned statically, not built. Upstream's model code was not run.*

### What changed upstream

- **A different programme.** From the October releases (r2050 onward) OPH is no longer presented as deriving the Standard Model from the pixel constant P. The stated aim is an executable observer model whose shared records should reproduce observed physics, with the design choices declared instead of derived. A new `model/` tree holds it.
- **Its own withdrawal of the numbers.** `docs/OPH_FALSIFICATION_PROGRAM.md` lists as ineligible all cosmology (capacity, scalar tilt, acceleration scale), the quantitative fine-structure, W/Z, Higgs/top, quark, charged-lepton and neutrino mass results, black-hole claims, and the anti-gravity and hardware continuations. `docs/EMPIRICAL_STATUS.md` opens by saying that no retained laboratory comparison selects a native record law, and the README's quantitative table is suppressed while the count of physically established results is zero.
- **More contributors.** The project is no longer one author's. A web search still found no independent peer review or external technical critique.

### Earlier findings, re-checked

| Finding (July) | Status (November) |
|---|---|
| Repair operator `sorry` in Lean (Part V) | Wrong since 2026-07-18; corrected in Part V. |
| α is MSSM-conditional and hadron-incomplete (Part III) | Stands, and upstream now says so. Measured α is treated as an input on every path that uses P, the running is labelled a supersymmetric proxy, and with the measured hadronic contribution upstream's own map returns α⁻¹ = 136.38, which it records as excluding the measured value. The fine-structure root has diagnostic status. |
| W/Z/Higgs agreement is many σ off (Part III) | Stands. Upstream's current twelve-mass table reports every value outside its interval: W −0.63%, Z −0.66%, H −0.23%, quarks +23% to +209%. |
| Spectral tilt matches Planck at 0.27σ (Part II) | Weakened. n_s = 0.96602 is still +0.27σ from Planck 2018 but −2.4σ from ACT DR6 (P-ACT-LB, 0.9743 ± 0.0034). Upstream reports a lower-tail posterior mass of 0.0061. |
| Cosmological-constant magnitude (Part IV) | Not recomputed. Upstream now classes all capacity results as ineligible, and by its own account its one frozen capacity prediction (w = −1) coincides with ΛCDM. |
| MOND scale, proton spin, baryon ratio (Part II) | Absent from the current README, docs and flagship paper; not re-checked. |
| OMEGA applications (Part VI) | Removed from the repository. |
| Corpus more careful than headlines (Part VII) | Stands in narrower form; see the lepton ratios below. |

### Two new headline numbers

**Charged-lepton mass ratios.** The README now highlights m_μ/m_e = 206.770 and m_τ/m_e = 3477.47, obtained with no measured mass as input. These are the Koide relation at its exact point, with amplitude ratio ρ = √2 and phase δ = 2/9, the parametrization examined in Part II. Recomputed independently:

| Ratio | Koide (√2, 2/9) | Measured | Difference |
|---|---|---|---|
| m_μ/m_e | 206.770316 | 206.7682827(46) | +9.83 ppm = **442σ** |
| m_τ/m_e | 3477.4728 | 3477.37 ± 0.18 | +0.61σ |

The τ ratio agrees only because the τ mass is known to about 50 ppm. The μ ratio is measured to 0.02 ppm and is missed by hundreds of standard deviations; matching it would need δ shifted by −1.75×10⁻⁷. In the new derivation, 2/9 is the probability of an exclusive-or of two events with probabilities 1/12 and 1/6, read as a phase in radians through a declared clock unit. The companion paper's abstract says the register is a declared construction and that no source-only mass prediction is claimed, and `docs/EMPIRICAL_STATUS.md` records four uncalibrated native candidates that failed first (ratios 1:3:12, 1:9:144, 1:30.8:452.6 and 1:382:5909). The README headline carries neither point. A Koide phase close to 2/9 has been noted in the literature since the mid-2000s, so this is a construction built to a known target, not a forecast.

**A fine-structure formula.** Upstream has adopted, with credit, a result from a separate preprint by A. D. Wissner-Gross (dated 2026-10-23, self-hosted): α = (79 + 48√2 + 42√3 + 3√6)/31104, so α⁻¹ = 137.035999189566. It is not derived from OPH, and upstream states that it does not solve OPH's own fixed-point maps. Recomputed independently:

| Reference | α⁻¹ | Pull of the formula |
|---|---|---|
| CODATA 2022 | 137.035999177(21) | +0.60σ |
| Electron g−2 (2023) | 137.035999166(15) | +1.6σ |
| Rubidium recoil (2020) | 137.035999206(11) | −1.5σ |
| Caesium recoil (2018) | 137.035999046(27) | +5.3σ |

The agreement is not explained by freedom in four small integers. The integers count 172 measurement records in four classes. Of the 877,975 ways to split 172 into four non-negative counts over the same denominator, this is the only one within 1,000σ of CODATA, and the local density of such formulas puts a chance hit within 1σ at roughly one in 5,000. What cannot be audited from outside is how many designs were considered: the preprint lists the definitional choices the number depends on and the alternatives it rules out, two of which give values within one percent. It constructs no momentum dependence, and its identification of the number with α at zero momentum transfer is stated as a conjecture. The formula stands or falls independently of OPH.

### Revised verdict

The formal core is sound and has been machine-checked upstream since July 2026, so the sharpest formal criticism in this report is withdrawn. The criticisms of the quantitative claims stand, and upstream has since adopted most of them: by its own registers OPH currently has no established physical result. The pattern of Part VII persists in narrower form, since the lepton-ratio headline drops a disclaimer that its own paper makes. The one new item worth watching is the Wissner-Gross formula, which is not an OPH result.

### Limits of the re-look

- The Lean library was scanned for admitted proofs, not built.
- Upstream's executable model and its verification suite were not run.
- The cosmological-constant, MOND, proton-spin and baryon numbers of Part II were not recomputed against the current corpus.
- The project's websites were not re-checked.
- The hypothesis notebook has not been updated; the ledger below is the July ledger with three rows annotated.

---

## Evidence ledger

Eighteen hypotheses (labbookql, domain `oph`), each with a concluded experiment and committed evidence. Confidence "mass" reflects the weight of evidence on 2026-07-13; annotations after a dash are from the November re-look.

| Mass | Hypothesis |
|---|---|
| 0.90 | α/EW chain uses no measured target **but is conditional on assumed MSSM/SUSY betas** |
| 0.90 | Prop 4.2 `sorry`-gap is fillable (concrete repair, gauge congruence proved) — upstream filled it on 2026-07-18 |
| 0.85 | Dynamical Prop 4.2 (iterated repair → consensus) machine-provable via Lyapunov descent |
| 0.80 | α⁻¹ ≈ 137 is a knife-edge selecting the MSSM integers |
| 0.80 | Multi-observer thesis machine-checkable, extending the single-carrier core |
| 0.70 | Spectral tilt n_s = 1 − P⋆/48 matches Planck (0.27σ) — but −2.4σ from ACT DR6 |
| 0.70 | Consensus/repair core is a consistent machine-checkable structure |
| 0.70 | Cosmological-constant magnitude (~10¹²²) is a genuine structural prediction |
| 0.65 | MOND scale a₀ matches empirical (within 15%) |
| 0.60 | Proton-spin fraction 4/13 matches (0.59σ) |
| 0.55 | Koide phase δ = 2/9 (real, but ppm precision is convention-dependent) |
| 0.45 | Baryon ratio (1/6)¹² (order-of-magnitude only, factor 1.33 low) |
| 0.40 | α⁻¹ is a **zero-input** prediction (genuine fixed point, but MSSM-conditional + hadron-incomplete) |
| 0.25 | Strict W/Z/H masses match **at measurement precision** (no — tens of σ) |
| 0.25 | Central consensus dynamics is machine-checked **in OPH's Lean** (no on 2026-07-13, when it was `sorry`) — yes since 2026-07-18 for gauge congruence, descent and termination |
| 0.25 | OPH predicts neutrino masses/mixing from source (no — rejected template) |
| 0.20 | OPH derives the sphaleron/baryogenesis value (no — disavowed in the corpus) |
| 0.20 | Bitcoin-in-ms compute claim is consistent with OPH's complexity limitation (no — contradiction) |

---

## Limitations of this study

- The dynamical convergence theorem is proved for an *abstract* potential and descent law; it does not construct a concrete non-trivial repair operator over general finite patch-nets with an *async schedule* and a derived potential. That fuller mechanization is not done here; upstream's Lean has had it since 2026-07-18 (Part V).
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
- **November re-look (Part IX):** upstream read at commit `6529d3ce7` with `git show upstream/main:<path>`; numbers from `verification/oph_relook_recheck.py` (needs `mpmath`, `numpy`); Lean scan from `verification/oph_lean_scan.py` run on `git archive upstream/main Lean`.

---

## Conclusion (July 2026)

*Part IX revises this verdict for November 2026.*

OPH deserves to be taken more seriously than a typical "theory of everything" and less literally than its marketing. Its consensus/repair core is a coherent, now fully machine-checked idea; its cosmological-constant result is genuinely impressive and survives provenance scrutiny; and its papers are honest about their many open gaps. But its flagship α claim is a supersymmetry-conditional knife-edge dressed as parameter-free, its electroweak "agreements" are many-sigma at real precision, and its applications layer overreaches to the point of self-contradiction.

The most durable output of this study is not the verdict but the **method and the extensions**: independent recomputation over trust, controlled single-variable experiments on the authors' own code, and an independent formalization of OPH's central thesis, written before its authors' own Lean proof landed — together with a concrete, testable falsifier they can adopt.
