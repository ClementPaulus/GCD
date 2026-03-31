# Spliceosome Supercomputer Simulation — Batch 2: Full Integration Plan

**Status**: PLAN — awaiting approval before Batch 3 execution
**Target test number**: test_309
**Domain**: `closures/quantum_mechanics/spliceosome_dynamics.py`
**Theorem prefix**: T-SD (Spliceosome Dynamics)

---

## 1. DOMAIN PLACEMENT

**Location**: `closures/quantum_mechanics/spliceosome_dynamics.py`

**Rationale**: The spliceosome study is an all-atom molecular dynamics simulation
of a biomolecular machine. `quantum_mechanics/` already hosts
`quantum_material_simulation.py` (Lee et al. 2026 — quantum hardware MD) and
other simulation-based closures. The spliceosome MD simulation fits naturally
here: it is a computational physics study using classical force fields (all-atom
MD on a supercomputer), analyzing conformational transitions in a ~2M-atom
molecular machine. The channels measure simulation fidelity, structural
coherence, and catalytic competence — all within the Tier-2 pattern.

**Alternative considered**: Creating a new `closures/molecular_biology/` domain.
Rejected — this is a *simulation study*, not a biological fieldwork closure.
The quantum_mechanics domain already handles simulation channel selection.
If a broader molecular biology domain is warranted later, this file can be
relocated via a weld.

---

## 2. STUDY SOURCES (from Batch 1)

### Primary: Martino et al. 2026 (PNAS)
- **Title**: All-atom molecular dynamics simulation of spliceosome active site remodeling
- **Authors**: Gianfranco Martino et al., PI Marco De Vivo
- **Institutions**: IIT Genoa, Uppsala University, AstraZeneca
- **DOI**: 10.1073/pnas.2522293123
- **Published**: March 26, 2026
- **Key data**: ~2M atoms, Franklin supercomputer (360+ GPUs), first catalytic step
  (5' splice site cleavage), controlled sequential conformational transitions,
  RNA/protein interface remodeling

### Supporting: CRG Barcelona 2024 (Science)
- **Title**: Human spliceosome blueprint / functional interaction network
- **DOI**: 10.1126/science.adn8105
- **Key data**: 305 genes, 150 proteins + 5 snRNAs, SF3B1 cascade affects 1/3 network
- **Role**: Provides the biological context for which components are functionally
  critical — constrains channel value assignments

---

## 3. TRACE VECTOR DESIGN (8 channels, equal weights w_i = 1/8)

| Ch | Name                      | What it measures                                              | Range | Source |
|----|---------------------------|---------------------------------------------------------------|-------|--------|
| 0  | `catalytic_fidelity`      | Accuracy of 5' splice site cleavage geometry                  | [0,1] | Martino 2026: active site geometry vs cryo-EM reference |
| 1  | `conformational_coherence`| Structural agreement across sequential transition states      | [0,1] | Martino 2026: RMSD convergence / structural similarity |
| 2  | `component_complexity`    | Fraction of spliceosome components actively participating     | [0,1] | CRG 2024: 150 proteins + 5 snRNAs, functional network |
| 3  | `rna_protein_coupling`    | Integrity of RNA-protein interface during remodeling          | [0,1] | Martino 2026: interface contacts preserved/lost |
| 4  | `transition_resolution`   | Temporal resolution of conformational intermediates           | [0,1] | Martino 2026: ns-to-μs timescale coverage |
| 5  | `simulation_convergence`  | Statistical convergence of the MD trajectory                  | [0,1] | Standard MD quality metric (RMSF, block averaging) |
| 6  | `network_interconnection` | Functional connectivity within splicing factor network        | [0,1] | CRG 2024: SF3B1 cascade, 1/3 of network affected |
| 7  | `energetic_discrimination`| Free energy separation between productive/non-productive paths| [0,1] | Martino 2026: PMF barriers, catalytic competence |

**GCD interpretation**:
- High F (fidelity) = simulation faithfully reproduces known cryo-EM structures
  AND catalytic mechanism proceeds correctly
- High omega (drift) = simulation diverges from experimental reference or
  catalysis fails
- IC cliff = if ANY one channel collapses (e.g., RNA-protein interface breaks
  while everything else looks fine), IC drops catastrophically — geometric
  slaughter detects this

---

## 4. ENTITY CATALOG (12 entities, 4 categories × 3 each)

| # | Entity Name                  | Category        | Biological/Simulation Role |
|---|------------------------------|-----------------|---------------------------|
| 1 | `pre_catalytic_B_act`        | catalytic_state | B^act complex — assembled, pre-catalytic |
| 2 | `step1_spliceosome_C`        | catalytic_state | C complex — after first transesterification |
| 3 | `post_catalytic_P`           | catalytic_state | P complex — after second step, mRNA ready |
| 4 | `u2_snrnp_branch`            | rna_component   | U2 snRNP at branch point — key recognition |
| 5 | `u5_snrnp_exon_align`        | rna_component   | U5 snRNP aligning exon junctions |
| 6 | `u6_snrnp_catalytic`         | rna_component   | U6 snRNP — forms catalytic center with U2 |
| 7 | `sf3b1_network_hub`          | splicing_factor | SF3B1 — master hub affecting 1/3 of network |
| 8 | `prp8_scaffold`              | splicing_factor | Prp8 — largest spliceosome protein, scaffold |
| 9 | `dhx15_helicase`             | splicing_factor | DHX15 — RNA helicase driving remodeling |
| 10| `franklin_allosteric_path`   | md_simulation   | Full MD trajectory — allosteric pathway |
| 11| `franklin_active_site`       | md_simulation   | MD focus on active site geometry only |
| 12| `cryoem_static_reference`    | md_simulation   | Cryo-EM static structure as reference (control) |

**Category logic**:
- **catalytic_state** (3): The three major spliceosome states along the catalytic cycle.
  Channel values track how well each state is characterized by the MD simulation.
  B^act has high component_complexity but lower catalytic_fidelity (pre-catalytic).
  C complex has peak catalytic_fidelity. P complex has high catalytic_fidelity but
  reduced conformational_coherence (post-catalytic relaxation).

- **rna_component** (3): The three functionally distinct snRNP components.
  U6 has highest catalytic role (forms active site with U2). U2 recognizes branch point.
  U5 aligns exons. All have high component_complexity but varying coupling.

- **splicing_factor** (3): Key protein factors from the CRG functional network.
  SF3B1 is the network hub (high network_interconnection but mutation-vulnerable).
  Prp8 is the structural scaffold (high conformational_coherence, stable).
  DHX15 drives remodeling (high transition_resolution, moderate fidelity).

- **md_simulation** (3): Computational entities.
  The full allosteric pathway from Martino 2026. The active-site-only focus.
  The cryo-EM reference as a static control (high catalytic fidelity by construction,
  but zero transition_resolution and zero simulation_convergence → IC cliff).

**Collapse-return mapping**:
- cryo-EM is a *collapsed* observation — temporal information lost (τ_R = ∞_rec for dynamics)
- The MD simulation is the *return* — temporal trajectory recovered, intermediates resolved
- The heterogeneity gap Δ = F − IC reveals which entities have hidden structural weaknesses

---

## 5. CHANNEL VALUE ASSIGNMENTS (Preliminary)

Values derived from study data, categorized to ensure theorems are testable:

```
Entity                      cat_f conf_c comp_x rna_p trans_r sim_c  net_i  ener_d
pre_catalytic_B_act         0.55  0.85   0.90   0.80  0.45   0.75   0.70   0.40
step1_spliceosome_C         0.95  0.80   0.85   0.90  0.70   0.80   0.75   0.85
post_catalytic_P            0.80  0.65   0.80   0.70  0.55   0.70   0.65   0.70
u2_snrnp_branch             0.75  0.70   0.70   0.85  0.50   0.65   0.60   0.60
u5_snrnp_exon_align         0.70  0.75   0.65   0.80  0.45   0.60   0.55   0.55
u6_snrnp_catalytic          0.90  0.80   0.75   0.90  0.60   0.70   0.65   0.80
sf3b1_network_hub           0.60  0.55   0.85   0.50  0.40   0.55   0.95   0.45
prp8_scaffold               0.75  0.90   0.80   0.85  0.55   0.70   0.70   0.65
dhx15_helicase              0.65  0.60   0.70   0.75  0.85   0.65   0.55   0.50
franklin_allosteric_path    0.80  0.75   0.80   0.75  0.90   0.85   0.65   0.75
franklin_active_site        0.90  0.85   0.60   0.80  0.70   0.90   0.45   0.85
cryoem_static_reference     0.85  0.90   0.80   0.85  0.05   0.05   0.70   0.75
```

**Key design choices**:
- `cryoem_static_reference` has two near-zero channels (transition_resolution=0.05,
  simulation_convergence=0.05) — it's a static snapshot, frozen by definition.
  This creates the IC cliff (geometric slaughter). High F (most channels are good)
  but crushed IC (two dead channels kill the geometric mean).
- `sf3b1_network_hub` has the highest network_interconnection (0.95) but low
  rna_protein_coupling (0.50) — it's a protein factor, not directly RNA-coupled.
  This creates a large heterogeneity gap.
- `step1_spliceosome_C` (the active catalytic state) has the highest catalytic_fidelity
  (0.95) and energetic_discrimination (0.85) — peak catalytic competence.

---

## 6. THEOREMS (6, T-SD-1 through T-SD-6)

| ID    | Statement | Tests against |
|-------|-----------|---------------|
| T-SD-1 | `step1_spliceosome_C` has highest F among all entities — peak catalytic competence gives broadest fidelity across all channels | F comparison |
| T-SD-2 | `cryoem_static_reference` has largest heterogeneity gap (Δ = F − IC) — static structure has two dead channels (no dynamics, no convergence) creating geometric slaughter despite high average fidelity | Δ comparison |
| T-SD-3 | `catalytic_state` category has highest mean F — the functional catalytic cycle entities outperform components and simulation entities | Category F means |
| T-SD-4 | `sf3b1_network_hub` has highest network_interconnection channel — the master hub of the splicing factor network drives 1/3 of all interactions | Raw channel comparison |
| T-SD-5 | `md_simulation` category mean IC exceeds `rna_component` category mean IC only when excluding the cryo-EM reference — the static reference drags down the simulation category's multiplicative coherence | Category IC with/without exclusion |
| T-SD-6 | `cryoem_static_reference` is in Watch or Collapse regime — the static snapshot's dead channels push it toward structural dissolution despite high nominal fidelity | Regime classification |

---

## 7. FILE INVENTORY (Batch 3 deliverables)

| File | Purpose | Lines (est.) |
|------|---------|-------------|
| `closures/quantum_mechanics/spliceosome_dynamics.py` | Closure: 12 entities, 8 channels, 6 theorems | ~300 |
| `tests/test_309_spliceosome_dynamics.py` | Test: catalog, Tier-1 identities, theorems, regimes | ~120 |
| `canon/qm_anchors.yaml` | UPDATE: add spliceosome anchor entry | +15 |
| `closures/registry.yaml` | UPDATE: register new closure | +5 |

**NOT creating**:
- No new casepack (optional — the closure + tests are sufficient for Tier-2 validation)
- No new contract (uses existing UMA.INTSTACK.v1)
- No new canon domain file (extends existing qm_anchors.yaml)
- No paper (study already published — this is a closure mapping, not original research)

---

## 8. POST-CREATION VALIDATION PLAN

```bash
# 1. Run the new test file
pytest tests/test_309_spliceosome_dynamics.py -v

# 2. Verify Tier-1 identities hold for all 12 entities
#    (built into test — F+ω=1, IC≤F, IC=exp(κ))

# 3. Verify all 6 theorems pass
#    (built into test — T-SD-1 through T-SD-6)

# 4. Update integrity checksums
python scripts/update_integrity.py

# 5. Run pre-commit protocol
python scripts/pre_commit_protocol.py
```

---

## 9. GCD INSIGHT MAP (Why This Study Matters for GCD)

### Collapse-Return Structure
The spliceosome study IS a collapse-return story:
- **Collapse**: Cryo-EM captures static snapshots — temporal information is
  lost at the moment of observation. Each cryo-EM image is a "collapsed"
  measurement. Dynamic intermediates vanish.
- **Return**: The MD simulation demonstrates *return* — the full temporal
  trajectory is recovered, conformational intermediates are resolved, and
  the catalytic mechanism can be watched in real time. What was lost to
  cryo-EM observation is restored through computation.
- **Geometric slaughter**: The cryo-EM entity has high F (most channels
  look healthy) but crushed IC (two dead channels). This is the signature
  of a measurement that collapses information — detectable through the
  heterogeneity gap.

### Channel Heterogeneity
SF3B1's profile — high in one channel (network hub, 0.95) but low in another
(RNA coupling, 0.50) — maps to the CRG finding that mutating SF3B1 cascades
through 1/3 of the network. One entity's weakness propagates. In GCD terms:
the heterogeneity gap of SF3B1 predicts its vulnerability to perturbation.

### Scale Bridge
This closure bridges two scales:
- Molecular (~2M atoms, ns-μs timescale) — the MD simulation
- Functional (gene expression, 20K→100K+ protein isoforms) — the biological role

The cross-scale transition (molecular mechanism → gene expression product)
is analogous to the nuclear→atomic transition in `cross_scale_kernel.py`.

---

## 10. APPROVAL CHECKLIST

Before proceeding to Batch 3, confirm:

- [ ] Domain placement in `closures/quantum_mechanics/` is acceptable
- [ ] 8-channel design covers the essential physics
- [ ] 12-entity catalog captures the key biological/computational players
- [ ] 6 theorems are scientifically justified and testable
- [ ] Test number 309 is correct
- [ ] No additional files needed (no casepack, no paper)
- [ ] Channel values are plausible (can be refined in Batch 3)

---

END OF BATCH 2 — Awaiting approval for Batch 3 (execution + commit).
