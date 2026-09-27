# UMCP Kernel Specification

**Specification ID:** `UMCP-KERNEL-SPEC.v2.4.0-rc3`  
**Status:** Freeze-controlled repair candidate; not a Tier-1 freeze  
**Prepared:** 2026-09-27, America/Chicago  
**Supersedes for review:** `UMCP-KERNEL-SPEC.v2.4.0-rc2`  
**Implementation baseline:** GCD / UMCP repository v2.3.3  
**Burden:** Specify the fixed kernel, typed-return interface, seam-accounting interface, validators, run record, and implementation boundaries  
**Corpus role:** Local technical witness under *Summa Reditus*, Architecture Freeze v1.0  
**Repair class:** Boundary/readback repair; no Tier-1 formula, exact identity, reserved namespace, typed-return rule, seam profile, validator gate, or run-record field is changed

## 0. Receipt

### 0.1 Placement

- **Reditus:** object - admissible return through collapse under declared conditions.
- **Structura Reditus:** field.
- **GCD:** foundational theory.
- **UMCP:** functional system for measurement and evaluation.
- **RCFT:** exploration before freeze.
- **ULRC:** preservation of meaning, translation, contact, critique, refusal, pedagogy, and repair.
- **Tier-1 / Tier-0 / Tier-2:** authority axis, not functional systems.
- ***Summa Reditus*:** completed canon-facing treatise and whole-work return of the corpus.

This specification is not the corpus, does not replace *Summa Reditus*, and does not absorb RCFT or ULRC.

### 0.2 Axiom and order

> Collapse is generative; only what returns through collapse is real.

```latex
\textit{Collapsus generativus est; solum quod per collapsum redit, reale est.}
```

Operationally: collapse generates; return admits; integrity reconciles; stance derives.

Every stance-bearing run follows:

```text
Object / Contract -> Canon -> Closures -> Integrity Ledger -> Stance
```

The kernel computes admitted structure. It does not independently authorize final stance.

### 0.3 Normative labels

| Label | Authority |
| --- | --- |
| `[T1]` | Reserved kernel meaning, exact identity, primitive distinction, or immutable namespace boundary. |
| `[T0]` | Contract, adapter, validator, closure, return, seam, ledger, run, audit, or stance rule. |
| `[T2]` | Domain translation, diagnostic, overlay, or candidate extension. |
| `[LEGACY]` | Historical or implementation-compatible form retained for reproduction, not promoted by retention. |

### 0.4 Open seams

This candidate preserves rather than resolves three active seams:

1. **Roughness:** repository v2.3.3 computes unweighted population dispersion; the active UMCP operating witness specifies weighted dispersion. The executable baseline and repair target are not identical for nonuniform weights.
2. **Return credit:** inherited Tier-0 lineage uses `R * tau_R`; later language witnesses separate independently defined return credit `Q_R`. Neither form is universal, and they may not be mixed within one run.
3. **Criticality:** repository v2.3.3 may emit `CRITICAL` as a primary regime; the mature grammar treats `IC < 0.30` as an overlay on Stable / Watch / Collapse.

No historical run is rewritten by this candidate.

---

# I. Object, Contract, and Trace

## 1. Evaluated object `[T0]`

An evaluated object is the declared entity, process, state, artifact, trace source, or comparison being tested. Its declaration records, as applicable:

- identity, version, scope, and exclusions;
- source and evidence boundaries;
- adapter, channel semantics, and time base;
- missingness policy;
- return domain and closure registry;
- authority boundary;
- output burden.

Changing object identity creates a new object state. If continuity is claimed, declare a seam.

## 2. Frozen contract `[T0]`

A frozen contract is the rule-set governing one run:

```text
Phi = (
  object,
  adapter,
  channel_map,
  weights,
  normalization,
  face_policy,
  epsilon,
  missingness_policy,
  metric,
  return_tolerance,
  return_domain,
  horizon,
  closure_registry,
  regime_rules,
  seam_tolerance,
  authority_record,
  numerical_precision
)
```

Frozen means unchanged across the identity or continuity comparison. Future contracts may change only as declared new contract states or across explicit seams.

**No retroactive tuning.** Do not alter a threshold, adapter, weight, normalization, missingness rule, return domain, closure, or authority status after seeing the outcome and represent it as part of the original run.

## 3. Admitted bounded trace `[T0 -> T1]`

```latex
\Psi(t)=\bigl(c_1(t),\ldots,c_n(t)\bigr)\in[0,1]^n.
```

`Psi(t)` is the domain object after admission through the frozen adapter and normalization rule.

Weights are contract fields:

```latex
w_i\ge 0,
\qquad
\sum_{i=1}^n w_i=1.
```

For fixed guard band:

```latex
0<\varepsilon<\frac12,
```

define:

```latex
c_{i,\varepsilon}(t)
=
\min\!\left\{1-\varepsilon,\max\!\left\{\varepsilon,c_i(t)\right\}\right\},
```

```latex
\Psi_\varepsilon(t)
=
\bigl(c_{1,\varepsilon}(t),\ldots,c_{n,\varepsilon}(t)\bigr)
\in[\varepsilon,1-\varepsilon]^n.
```

All logarithmic kernel quantities use `Psi_epsilon`. Record every clipping event under the active face/OOR policy; clipping must not conceal a malformed adapter or invalid input.

---

# II. Fixed Kernel

## 4. Kernel map and namespace `[T1]`

```latex
K:[\varepsilon,1-\varepsilon]^n\times\Delta^n
\longrightarrow
(F,\omega,S,C,\kappa,IC).
```

Reserved namespace:

```text
{omega, F, S, C, tau_R, kappa, IC}
```

Closures and diagnostics may use these quantities; they may not redefine them.

## 5. Kernel definitions `[T1]`

### 5.1 Fidelity and drift

```latex
F(t)=\sum_{i=1}^{n}w_i c_{i,\varepsilon}(t),
\qquad
\omega(t)=1-F(t).
```

`F` is weighted arithmetic retention. `omega` is its complement, not an independent degree of freedom.

### 5.2 Bernoulli field entropy

For `c in (0,1)`:

```latex
h(c)=-c\ln c-(1-c)\ln(1-c).
```

```latex
S(t)=\sum_{i=1}^{n}w_i h\!\left(c_{i,\varepsilon}(t)\right).
```

`S` is the weighted mean of per-channel binary-form uncertainty, not the entropy of the arithmetic mean. Read it probabilistically only when the contract authorizes the coordinates as Bernoulli probabilities.

### 5.3 Roughness

`C` means normalized inter-channel roughness or dispersion, not geometric curvature.

Executable v2.3.3 compatibility form:

```latex
C_{\mathrm{pop}}(t)
=
\frac{\operatorname{StdDev}_{\mathrm{pop}}
\left(c_{1,\varepsilon}(t),\ldots,c_{n,\varepsilon}(t)\right)}{0.5}.
```

Weighted repair target in the active UMCP operating witness:

```latex
C_w(t)
=
\frac{\operatorname{StdDev}_{w}
\left(c_{1,\varepsilon}(t),\ldots,c_{n,\varepsilon}(t)\right)}{0.5}.
```

The forms coincide for uniform weights and generally diverge otherwise. Every run must name its convention. `C_pop` remains the historical executable baseline; adopting `C_w` as the definitive Tier-1 form requires an authority decision, implementation change, validator/test migration, numerical crosswalk, and seam record.

Geometric, Fisher-Rao, graph, or manifold curvature may exist only under a distinct symbol and declared Tier-2 role.

### 5.4 Log-integrity and integrity composite

```latex
\kappa(t)=\sum_{i=1}^{n}w_i\ln c_{i,\varepsilon}(t),
```

```latex
IC(t)=e^{\kappa(t)}=\prod_{i=1}^{n}c_{i,\varepsilon}(t)^{w_i}.
```

`kappa` is additive log-integrity. `IC` is weighted geometric coherence.

## 6. Exact identities, bounds, and dimension `[T1]`

```latex
F+\omega=1,
\qquad
IC=e^{\kappa},
\qquad
IC\le F.
```

Equality in `IC <= F` holds exactly when all positive-weight channels are equal.

Only the first two relations are exact output equalities. Therefore the six reported outputs have at most four exact algebraically independent coordinates, for example:

```text
(F, kappa, S, C)
```

No Tier-1 identity in this candidate makes `S` an exact function of `(F,C)` for arbitrary traces. Any lower statistical rank requires a declared ensemble, approximation, or analysis rule.

---

# III. Typed Return

## 7. Return-state and eligible-anchor domains `[T0]`

The contract first declares an admissible return-state domain:

```latex
\mathcal D_\Phi(t)\subseteq[\varepsilon,1-\varepsilon]^n.
```

This state domain answers whether the candidate state is admissible at return time.

A deterministic generator forms eligible anchors:

```latex
D_\theta(t)\subseteq\{0,1,\ldots,t-1\}.
```

It may encode horizon, forbidden intervals, provenance, missingness, or other declared eligibility conditions.

`mathcal D_Phi(t)` and `D_theta(t)` are distinct: the first contains admissible states; the second contains eligible historical indices. A contract must declare both when both burdens are active.

For contract metric `d` and tolerance `eta_R`:

```latex
U_\theta(t)
=
\left\{
u\in D_\theta(t):
d\!\left(\Psi_\varepsilon(t),\Psi_\varepsilon(u)\right)\le\eta_R
\right\}.
```

The metric and tolerance define nearness; `D_theta` defines admissibility. Nearness without admissibility is not Reditus.

## 8. Return delay and types `[T1/T0]`

If `D_theta(t)` is evaluable and `U_theta(t)` is nonempty:

```latex
\tau_R(t)=\min\{t-u:u\in U_\theta(t)\}.
```

| Result | Meaning |
| --- | --- |
| finite `tau_R` | Admissible re-entry was found under the frozen contract. |
| `INF_REC` | The eligible domain was evaluable, but no admissible re-entry occurred within it. |
| `UNIDENTIFIABLE` | The eligible domain or comparison cannot be validly formed under the active sampling, provenance, missingness, or contract conditions. |
| `OOR` / `bottom_oor` | A declared domain or typing boundary failed before valid return evaluation. |

Never replace `INF_REC` or `UNIDENTIFIABLE` with an arbitrary large finite number. `INF_REC` earns no finite return credit. `UNIDENTIFIABLE` earns no inferred positive credit and normally blocks stance when return is stance-authorizing.

## 9. Reditus condition `[T0]`

For a declared collapse or perturbation:

```latex
\Psi(t_0)\to\Psi(t_1)\to\Psi(t_R),
\qquad t_R>t_1,
```

Reditus is admitted only when:

1. the same frozen contract governs the comparison, or a declared seam reconciles contract change;
2. the candidate state satisfies:

```latex
\Psi_\varepsilon(t_R)\in\mathcal D_\Phi(t_R);
```

3. return is finite and typed as demonstrated;
4. no blocking missingness or authority defect invalidates the claim.

Repetition, resemblance, persistence, repair, restoration, recovery, resilience, or narrative continuity alone do not satisfy Reditus.

---

# IV. Seam Accounting and Welds

## 10. Observed change `[T0]`

For seam endpoints `t_0` and `t_1`:

```latex
\Delta\kappa_{\mathrm{ledger}}
=
\kappa(t_1)-\kappa(t_0)
=
\ln\!\left(\frac{IC(t_1)}{IC(t_0)}\right),
```

```latex
i_r
=
\frac{IC(t_1)}{IC(t_0)}
=
e^{\Delta\kappa_{\mathrm{ledger}}}.
```

The identity must hold to declared numerical precision.

## 11. Accounting profiles `[T0]`

There is no universal seam-budget equation. A run must freeze exactly one adopted accounting profile.

### 11.1 Inherited `R * tau_R` profile

Current implementation lineage declares:

```latex
D_\omega
=
\Gamma(\omega;p,\varepsilon),
\qquad
\Gamma(\omega;p,\varepsilon)
=
\frac{\omega^p}{1-\omega+\varepsilon},
```

```latex
D_C=\alpha C,
```

```latex
\Delta\kappa_{\mathrm{budget}}
=
R\tau_R-(D_\omega+D_C),
```

```latex
s
=
\Delta\kappa_{\mathrm{budget}}-\Delta\kappa_{\mathrm{ledger}}
=
R\tau_R-
\left(\Delta\kappa_{\mathrm{ledger}}+D_\omega+D_C\right).
```

If `tau_R = INF_REC`, typed censoring sets the return-credit term to zero:

```latex
R\tau_R:=0.
```

Parameters `p`, `epsilon`, `alpha`, the estimator/meaning of `R`, and the timing/aggregation rules are contract-frozen.

### 11.2 Independent `Q_R` profile

Later witnesses propose:

```latex
\Delta\kappa_{\mathrm{expected}}
=
Q_R-(D_\omega+D_C).
```

This profile is not adopted by this candidate. Adoption requires an independent estimator, provenance and anti-circularity rules, units and sign convention, timing, `INF_REC` and `UNIDENTIFIABLE` behavior, validators, migration rules, and a versioned seam.

The profiles must never be mixed or declared identical inside one run.

## 12. Seam and weld `[T0]`

- A **seam** is a declared continuity-bearing boundary between object, contract, version, policy, or run states.
- A **weld** is an accepted seam whose active return, identity, residual, contract, and missingness gates close.

For the inherited profile, a minimum weld requires:

```latex
\tau_R<\infty_{\mathrm{rec}},
\qquad
|s|\le\mathrm{tol},
```

plus every other declared gate.

| Seam result | Meaning |
| --- | --- |
| `PASS` / `WELDED` | Every declared weld condition closes. |
| `FAIL` | An evaluable weld condition fails. |
| `NOT_WELDABLE` | The comparison is outside the declared interface or structurally ineligible. |
| `NON_EVALUABLE` | Required contract, return, evidence, missingness, or authority structure is insufficient. |

A failed seam denies earned continuity under this burden; it does not automatically prove the object false.

## 13. Minimum weld-closure record `[T0]`

Freeze at least:

1. object and pre/post anchors;
2. adapter and channel semantics;
3. weights and roughness convention;
4. `epsilon` and face policy;
5. return metric, tolerance, eligible domain, and horizon;
6. debit definitions and parameters;
7. the single active return-credit profile and its estimator;
8. timing and aggregation rules;
9. seam tolerance and numerical precision;
10. identity checks;
11. missingness policy;
12. authority record;
13. stance-authorizing conditions.

A missing stance-essential field makes the weld claim `NON_EVALUABLE`.

---

# V. Diagnostics, Missingness, and Stance

## 14. Default diagnostic regime `[T0]`

These are v2.3.3 contract defaults, not natural constants:

```text
COLLAPSE:
    omega >= 0.30

STABLE:
    omega < 0.038
    S < 0.15
    C < 0.14

WATCH:
    omega < 0.30
    and not all STABLE conditions hold
```

Because `F = 1 - omega`, `omega < 0.038` implies `F > 0.962`; the historical `F > 0.90` stable check is redundant under this gate.

Criticality is an overlay:

```text
critical = (IC < 0.30)
```

Regime reads trace condition; it does not decide stance.

## 15. Missingness `[T0]`

Type missingness before interpreting it:

- non-blocking;
- evaluability-blocking;
- contract-violating;
- authority-boundary;
- source-boundary;
- publication-boundary;
- repairable;
- unresolved seam.

Do not invent absent structure or collapse missingness into failure.

## 16. Stance `[T0]`

```text
Stance in {CONFORMANT, NONCONFORMANT, NON_EVALUABLE}
```

- **CONFORMANT:** the object satisfies every active stance-authorizing contract, closure, return, ledger, missingness, and authority condition.
- **NONCONFORMANT:** an evaluable, declared stance-authorizing condition is violated.
- **NON_EVALUABLE:** available structure cannot authorize either verdict.

Stance derives last. No regime, diagnostic, candidate theorem, source citation, public status, fluent explanation, or apparent coherence may substitute for it.

---

# VI. Exact Results and Qualified Diagnostics

## 17. Exact kernel results `[T1]`

All results assume positive normalized weights and clipped coordinates unless stated otherwise.

### 17.1 Bounds and invariance

```latex
\varepsilon\le F,\omega,IC\le1-\varepsilon,
```

```latex
\ln\varepsilon\le\kappa\le\ln(1-\varepsilon),
```

```latex
0\le S\le\ln2,
```

with clipped-domain entropy minimum `h(epsilon)` when all positive-weight channels lie on a clipped face.

For either valid normalized roughness convention:

```latex
0\le C\le1-2\varepsilon<1.
```

Permuting channel values and their corresponding weights together preserves all kernel outputs.

### 17.2 Stability and monotonicity

For traces `c` and `c_tilde` under the same weights:

```latex
|F-\widetilde F|
\le
\sum_i w_i|c_i-\widetilde c_i|,
\qquad
|\omega-\widetilde\omega|=|F-\widetilde F|.
```

```latex
\frac{\partial\kappa}{\partial c_i}=\frac{w_i}{c_i},
\qquad
\left|\frac{\partial\kappa}{\partial c_i}\right|\le\frac{w_i}{\varepsilon}.
```

```latex
|\kappa-\widetilde\kappa|
\le
\frac1\varepsilon\sum_iw_i|c_i-\widetilde c_i|.
```

```latex
|S-\widetilde S|
\le
\ln\!\left(\frac{1-\varepsilon}{\varepsilon}\right)
\sum_iw_i|c_i-\widetilde c_i|.
```

Componentwise `c_i <= c_tilde_i` implies:

```latex
F\le\widetilde F,
\quad
\omega\ge\widetilde\omega,
\quad
\kappa\le\widetilde\kappa,
\quad
IC\le\widetilde{IC}.
```

No global componentwise monotonicity is claimed for `S` or `C`.

### 17.3 Entropy and heterogeneity

By concavity:

```latex
S\le h(F)=h(1-\omega).
```

Equality holds for positive-weight homogeneity.

Define the AM-GM gap:

```latex
J_{\mathrm{AMGM}}=F-IC\ge0.
```

It is a derived diagnostic, not a replacement for `C` or a stance gate unless Tier-0 explicitly adopts it.

## 18. Return and ledger results `[T0]`

1. A finite evaluable `D_theta(t)` and nonempty `U_theta(t)` guarantee a finite minimum `tau_R`; an empty evaluable candidate set yields `INF_REC`; an invalid domain yields `UNIDENTIFIABLE`.
2. Relaxing tolerance or enlarging the eligible domain cannot increase the minimum return delay, but this is a cross-contract fact and does not authorize direct stance comparison.
3. A return anchor with margin `2 delta` remains admissible when the metric is 1-Lipschitz in each endpoint and both endpoints move by at most `delta`; a shorter return may appear.
4. Under a full-window policy, `INF_REC` means no eligible near anchor exists in the horizon. It is not automatic collapse, failure, or ontological nonexistence.

For contract-equivalent seam endpoints:

```latex
|\Delta\kappa_{\mathrm{ledger}}-
\Delta\widetilde\kappa_{\mathrm{ledger}}|
\le
\frac1\varepsilon
\sum_{t\in\{t_0,t_1\}}
\sum_iw_i|c_i(t)-\widetilde c_i(t)|.
```

Ledger change telescopes:

```latex
\Delta\kappa_{0\to2}
=
\Delta\kappa_{0\to1}+\Delta\kappa_{1\to2}.
```

Seam residuals do not automatically compose because anchors, horizons, closure inputs, and return delays may reset. A chain weld requires its own composition contract.

For the inherited finite-return profile:

```latex
|s-\widetilde s|
\le
|\tau_R|\,|R-\widetilde R|
+
|\widetilde R|\,|\tau_R-\widetilde\tau_R|
+
|D_\omega-\widetilde D_\omega|
+
|D_C-\widetilde D_C|
+
|\Delta\kappa_{\mathrm{ledger}}-
\Delta\widetilde\kappa_{\mathrm{ledger}}|.
```

Return-boundary changes can therefore make residuals discontinuous.

## 19. Corrected supporting results

### 19.1 Weight perturbation

For normalized weights `w` and `w_tilde`, let:

```latex
\delta_w=\|w-\widetilde w\|_1.
```

For a fixed clipped trace:

```latex
|F-\widetilde F|\le(1-\varepsilon)\delta_w,
```

```latex
|\kappa-\widetilde\kappa|
\le
\max\{|\ln\varepsilon|,|\ln(1-\varepsilon)|\}\delta_w,
```

```latex
|S-\widetilde S|\le(\ln2)\delta_w.
```

### 19.2 Temporal coarse-graining

For block average:

```latex
\overline\Psi(t')
=
\frac1M\sum_{k=0}^{M-1}\Psi(Mt'+k),
```

with fixed weights and no nonlinear post-averaging adapter:

```latex
F(\overline\Psi(t'))
=
\frac1M\sum_{k=0}^{M-1}F(\Psi(Mt'+k)).
```

`F` and `omega` coarse-grain exactly; `kappa`, `IC`, `S`, and `C` generally do not. Cross-scale comparison of the nonlinear quantities requires a declared closure or seam.

### 19.3 Dead-channel sensitivity

If positive-weight channel `k` falls to `epsilon`:

```latex
IC_{\mathrm{new}}
=
\varepsilon^{w_k}\prod_{i\ne k}c_i^{w_i},
```

```latex
F_{\mathrm{new}}
=
F_{\mathrm{old}}-w_k(c_k-\varepsilon).
```

A weak channel can therefore cause a far larger proportional loss in `IC` than in `F`. "Geometric slaughter" may name this diagnostic phenomenon but is not a new invariant.

## 20. Degeneracy and effective rank

For a homogeneous positive-weight trace `c_i = c_0`:

```latex
F=IC=c_0,
\quad
\kappa=\ln c_0,
\quad
C=0,
\quad
S=h(c_0),
\quad
\omega=1-c_0.
```

For exactly two equal-weight positive channels:

```latex
F=\frac{c_1+c_2}{2},
\qquad
IC=\sqrt{c_1c_2},
```

```latex
|c_1-c_2|=2\sqrt{F^2-IC^2},
\qquad
C_{\mathrm{pop}}=2\sqrt{F^2-IC^2}.
```

These are exact lower-dimensional classes, not a reconstruction theorem for arbitrary `n >= 3`.

Under a declared small-dispersion regime and matching variance convention:

```latex
S
\approx
h(F)-\frac{C^2}{8F(1-F)}.
```

This is a Tier-2 approximation, not an exact constraint. Any PCA or effective-rank claim must record the trace distribution, channel and weight distributions, roughness convention, sample size, preprocessing, centering/scaling, variance threshold, and reproducibility state.

---

# VII. Contract Equivalence and Change Control

## 21. Contract equivalence `[T0]`

Two records are contract-equivalent only when every stance-relevant semantic field is preserved, including:

- object identity or a declared equivalence rule;
- adapter, channels, normalization, face policy, and `epsilon`;
- weights and roughness convention;
- missingness and time-base rules;
- return metric, tolerance, domain, and horizon;
- closures and parameters;
- authority record;
- numerical precision where it can change a gate.

Numerical resemblance is not contract equivalence.

## 21A. Kernel identity, realization, preservation, and translation readback `[T0/T2]`

This section adds a bounded readback layer for comparing kernel realizations. It does not redefine the Tier-1 kernel.

### Canonical kernel identity

Kernel identity means the already-authorized Tier-1 object: reserved meanings, exact identities, primitive distinctions, and canon-fixed boundaries.

Kernel identity is not implementation identity.

### Analytical burden signature

For representation analysis only, let

```latex
F_K:X\to Z_K
```

denote a signature of the active canonical kernel burden. `F_K` is local analytical notation, not a new Tier-1 function or replacement for the canonical kernel map `K`.

### Kernel realization

A representation or implementation

```latex
E:X\to Y
```

realizes the active kernel burden when there exists

```latex
q:\operatorname{Im}(E)\to Z_K
```

such that

```latex
F_K=q\circ E.
```

Equivalently,

```latex
\ker E\subseteq\ker F_K.
```

Here `ker E` means equality fibers of `E`, not the UMCP kernel. A realization may carry surplus information.

### Kernel preservation

Let

```latex
C_E=\{(x,x')\in X^2:x\ne x',\ E(x)=E(x')\},
```

and

```latex
D_K=\{(x,x')\in X^2:F_K(x)\ne F_K(x')\}.
```

Exact kernel preservation requires

```latex
C_E\cap D_K=\varnothing.
```

This does not establish implementation identity, provenance, historical continuity, or Reditus.

### Kernel concordance

Two realizations are kernel-concordant when

```latex
F_K=q_1\circ E_1=q_2\circ E_2.
```

Concordance does not require equal realization fibers.

### Fiber equivalence

```latex
\ker E_1=\ker E_2
```

means the realizations distinguish exactly the same admitted alternatives. It is not canonical semantic identity.

### Exact translation

Exact deterministic translation `E_1\to E_2` on realized images exists iff

```latex
\ker E_1\subseteq\ker E_2.
```

Mutual exact translation requires equal fibers. Kernel concordance is weaker than exact translation.

### Validation and open-seam boundary

A finite validator establishes only its declared tested surface unless the admitted domain is finite and exhausted or a proof supplies universal coverage.

Kernel-sameness readbacks must name any seam-bearing convention that can affect the comparison, including the active nonuniform-weight roughness convention, seam-credit profile, and criticality representation where material.

No sameness or concordance claim may silently resolve an open authority seam.

---

## 22. Change-control matrix

| Change | Same contract? | Seam if continuity is claimed? |
| --- | ---: | ---: |
| Reorder channels and weights together | Yes | No |
| Add a zero-weight channel | Depends on active `C`; `C_pop` may change | Yes if any reported quantity changes |
| Change positive weights, adapter, channel meaning, normalization, `epsilon`, or missingness policy | No | Yes |
| Change return metric, tolerance, domain, or horizon | No | Yes |
| Change roughness convention | No | Yes |
| Change seam debit/credit profile or closure | No | Yes |
| Change regime thresholds | No at protocol level | Yes for stance continuity |
| Add an explicitly non-authorizing diagnostic | Potentially yes | No unless later promoted |
| Promote a diagnostic to a gate | No | Yes |

---

# VIII. Implementation Baseline v2.3.3

## 23. Defaults

| Field | Default | Role |
| --- | ---: | --- |
| `epsilon` | `1e-8` | Log-domain guard band |
| `p` | `3` | `Gamma(omega)` exponent |
| `alpha` | `1.0` | `D_C = alpha * C` coefficient |
| `lambda` | `0.2` | EMA support where declared |
| `tol_seam` | `0.005` | Default residual gate |
| `omega_stable_max` | `0.038` | Diagnostic regime default |
| `F_stable_min` | `0.90` | Redundant compatibility check |
| `S_stable_max` | `0.15` | Diagnostic regime default |
| `C_stable_max` | `0.14` | Diagnostic regime default |
| `omega_collapse_min` | `0.30` | Diagnostic regime default |
| `IC_critical_max` | `0.30` | Critical overlay default |

Defaults are contract choices, not exact identities or natural constants.

## 24. Implementation conformance

| Surface | v2.4.0-rc2 target | v2.3.3 state | Readback |
| --- | --- | --- | --- |
| `F`, `omega`, `S`, `kappa`, `IC` | Definitions above | Conforms | `CONFORMANT` |
| `C` name | Roughness / normalized dispersion | Comments may say curvature proxy | Repairable semantic drift |
| `C` weighting | Active convention must be explicit | Unweighted population std | Open source/implementation seam |
| Return typing | finite / `INF_REC` / `UNIDENTIFIABLE` / OOR | Typed machinery distributed across modules | Module-level audit required |
| Seam accounting | One declared profile per run | Inherited `R * tau_R` profile | Conforms to that lineage only |
| Criticality | Overlay on three regimes | May be primary enum | `NONCONFORMANT` to mature grammar |
| Stable `F > 0.90` | Redundant under `omega < 0.038` | Still checked | Compatible, removable |
| Final stance | Three-valued and last | Typed validator surfaces exist | Run-dependent audit required |

This is a specification-level crosswalk, not an exhaustive repository validation.

## 25. Trap-point diagnostic

For the v2.3.3 closure:

```latex
\frac{\omega^3}{1-\omega+\varepsilon}=\alpha.
```

At `alpha = 1` and small `epsilon`:

```latex
\omega_{\mathrm{trap}}\approx0.6823.
```

This is closure-derived, not a Tier-1 invariant. The same rule applies to Lambert-W fixed points, reciprocal-gate normal forms, and any constant dependent on a specific analytic closure.

---

# IX. Validators and Run Record

## 26. Minimum validators `[T0]`

Check at least:

1. finite, nonnegative, normalized weights;
2. admitted coordinates and face policy;
3. clipped inputs for logarithms;
4. `F + omega = 1` within tolerance;
5. `IC = exp(kappa)` within tolerance;
6. `IC <= F` within tolerance;
7. valid `S` and convention-specific `C` ranges;
8. finite reserved outputs where required;
9. recorded clipping/OOR events;
10. named roughness convention;
11. typed return result;
12. zero return credit for `INF_REC` under the active profile;
13. single, declared seam-accounting profile;
14. closure and missingness reconciliation before stance.

Validators confirm declared conformance. Passing one does not create Tier-1 meaning.

## 27. Minimum run record `[T0]`

```text
run_id
object_id
object_version
contract_id
contract_hash
adapter_id
channel_map
weights
normalization
face_policy
epsilon
missingness_policy
roughness_convention
metric
return_tolerance
return_domain
horizon
closure_registry
seam_accounting_profile
regime_rules
seam_tolerance
numerical_precision
authority_record
source_manifest
kernel_outputs
return_result
seam_result
ledger_record
stance
residual_blockers
repair_note
```

Add domain fields as needed. Do not omit any field required to reproduce a stance-bearing result.

---

# X. Open Burdens Before Freeze

## 28. Required resolutions

### 28.1 Roughness

Choose one nonuniform-weight Tier-1 definition or split the namespace. Supply proof of bounds, authority record, implementation and validator updates, test migration, casepack impact, numerical crosswalk, and historical seam declaration.

### 28.2 Critical overlay

Implement:

```text
primary_regime in {STABLE, WATCH, COLLAPSE}
critical_overlay in {true, false}
```

### 28.3 Return-credit profile

Either retain the inherited profile explicitly or adopt a fully specified `Q_R` profile. Adoption by wording alone is prohibited.

### 28.4 Rank claim

Prove an exact universal Rank-3 theorem without counting statistical approximation as algebraic identity, or retain rank three as an ensemble-specific diagnostic.

### 28.5 Legacy empirical claims

Keep legacy items 35-47 in a Tier-2 candidate register unless separately proved or validated under their own domain contracts. Their lineage and repaired typing are preserved in the companion repair audit.

---

# XI. Sources, Symbols, and Readback

## 29. Source roles

| Source | Admitted burden |
| --- | --- |
| *Summa Reditus*, Architecture Freeze v1.0 | Whole-corpus placement and completed-treatise status |
| *The Threefold Authority Order* | Authority-axis meanings and promotion limits |
| *UMCP Operating System* | Active functional definition, contract-first grammar, weighted roughness target, return/seam/ledger/stance discipline |
| *Structura Collapsus* | Technical lineage and earlier `C_pop` implementation-facing form |
| *Liber Collapsus* v2.0 | Active language witness, typed return, roughness language, and later accounting pressure |
| `UMCP-KERNEL-SPEC.v2.4.0-rc1` | Immediate repair-candidate source |
| GCD / UMCP repository v2.3.3 | Executable baseline |

Source roles are not equal. Disagreement remains a seam rather than being averaged away.

## 30. Symbol index

| Symbol | Meaning | Authority |
| --- | --- | --- |
| `Phi` | Frozen contract | Tier-0 |
| `Psi(t)` | Admitted trace | T0 -> T1 interface |
| `c_i`, `w_i` | Channel and contract weight | Interface |
| `epsilon` | Guard band | Tier-0 parameter |
| `F`, `omega`, `S`, `C`, `kappa`, `IC` | Fixed-kernel outputs | Tier-1 |
| `tau_R` | Typed return delay | T1/T0 boundary |
| `D_theta`, `U_theta` | Eligible domain and candidate set | Tier-0 |
| `D_omega`, `D_C` | Declared seam debits | Tier-0 |
| `R * tau_R` or `Q_R` | Profile-specific return credit | Tier-0; mutually exclusive per run |
| `Delta kappa_ledger` | Observed log-integrity change | Tier-0 |
| `Delta kappa_budget` | Profile-specific modeled change | Tier-0 |
| `s`, `tol` | Seam residual and tolerance | Tier-0 |
| `Stance` | Derived final state | Tier-0 |

## 31. Final readback

The kernel measures an admitted trace under one frozen contract. Its exact identities are:

```latex
F+\omega=1,
\qquad
IC=e^\kappa,
\qquad
IC\le F.
```

`C` remains a declared convention seam for nonuniform weights. Return is typed admissible re-entry, not resemblance. Seam accounting is profile-bound, not universal. Finite return does not prove a weld. Regime is diagnostic. Missingness remains visible. Stance derives last.

> The kernel measures. The contract fixes meaning. Return must be demonstrated. Continuity must reconcile. No source seam is closed by prose alone.

---
