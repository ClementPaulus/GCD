/**
 * @file pipeline.c
 * @brief Validation Pipeline — The Spine in C
 *
 * Orchestrates the full five-stop validation spine:
 *   Contract → Canon → Closures → Integrity Ledger → Stance
 *
 * This is the C-level orchestration layer. It decides what
 * computation happens, in what order, and using which modules.
 *
 * Spina non negotiabilis est. — The spine is non-negotiable.
 */

#include "umcp_c/pipeline.h"
#include <math.h>
#include <string.h>

/* ─── Pipeline Lifecycle ────────────────────────────────────────── */

int umcp_pipeline_init(umcp_pipeline_t *pipeline,
                        const umcp_contract_t *contract,
                        umcp_ledger_entry_t *ledger_buffer,
                        size_t ledger_capacity)
{
    if (!pipeline || !contract || !ledger_buffer) return UMCP_ERR_NULL_PTR;
    if (ledger_capacity == 0) return UMCP_ERR_ZERO_DIM;

    /* Validate the contract before accepting it */
    int rc = umcp_contract_validate(contract);
    if (rc != UMCP_OK) return rc;

    /* Freeze the contract into the pipeline */
    pipeline->contract = *contract;

    /* Initialize the ledger */
    rc = umcp_ledger_init(&pipeline->ledger, ledger_buffer, ledger_capacity);
    if (rc != UMCP_OK) return rc;

    /* No prior κ on first step */
    pipeline->prior_kappa = NAN;
    pipeline->initialized = 1;

    return UMCP_OK;
}

/* ─── Pipeline Step (One Full Spine Pass) ───────────────────────── */

int umcp_pipeline_step(umcp_pipeline_t *pipeline,
                        const umcp_trace_t *trace,
                        double R, double tau_R,
                        umcp_pipeline_result_t *out)
{
    if (!pipeline || !trace || !out) return UMCP_ERR_NULL_PTR;
    if (!pipeline->initialized) return UMCP_ERR_RANGE;

    memset(out, 0, sizeof(*out));

    /* ── Stop 1: Contract (already frozen in pipeline) ────────── */
    const umcp_contract_t *ct = &pipeline->contract;

    /* ── Stop 2: Canon (kernel computation) ───────────────────── */
    int rc = umcp_kernel_compute(
        trace->c, trace->w, trace->n,
        ct->epsilon, &out->kernel);
    if (rc != UMCP_OK) return rc;

    /* ── Stop 3: Closures (gates + cost computation) ──────────── */

    /* Regime classification (overlay-aware) */
    out->regime = umcp_classify_regime_with_overlay(&out->kernel, &ct->thresholds);

    /* Identity validation */
    out->identity_check = umcp_validate_identities(&out->kernel, 1e-9);

    /* Cost closures */
    out->D_omega = umcp_gamma_omega(out->kernel.omega,
                                     ct->p_exponent, ct->epsilon);
    out->D_C = umcp_cost_curvature(out->kernel.C, ct->alpha);

    /* Budget and residual */
    if (!isnan(pipeline->prior_kappa)) {
        double delta_kappa = out->kernel.kappa - pipeline->prior_kappa;
        out->budget = umcp_budget_delta_kappa(R, tau_R,
                                               out->D_omega, out->D_C);
        out->residual = umcp_seam_residual(out->budget, delta_kappa);

        /* Seam PASS check */
        double I_ratio = (pipeline->prior_kappa != 0.0)
            ? out->kernel.IC / exp(pipeline->prior_kappa)
            : 1.0;
        out->seam = umcp_check_seam_pass(
            out->residual, tau_R, I_ratio,
            delta_kappa, ct->tol_seam, 1e-6,
            NULL, 0);
    } else {
        out->budget   = 0.0;
        out->residual = 0.0;
        out->seam     = UMCP_SEAM_PENDING;
    }

    /* ── Stop 4: Integrity Ledger (append + reconcile) ────────── */
    umcp_ledger_entry_t entry;
    rc = umcp_ledger_build_entry(&entry, &out->kernel, ct,
                                  pipeline->prior_kappa, R, tau_R);
    if (rc != UMCP_OK) return rc;

    entry.timestamp = (uint64_t)pipeline->ledger.count;

    rc = umcp_ledger_append(&pipeline->ledger, &entry);
    if (rc != UMCP_OK) return rc;

    /* ── Stop 5: Stance (derive verdict) ──────────────────────── */
    out->stance.regime     = out->regime;
    out->stance.seam       = out->seam;
    out->stance.confidence = fabs(out->residual);

    /* Verdict: combine identity check + seam status */
    if (out->identity_check == UMCP_NONCONFORMANT) {
        out->stance.verdict = UMCP_NONCONFORMANT;
    } else if (out->seam == UMCP_SEAM_FAIL) {
        out->stance.verdict = UMCP_NONCONFORMANT;
    } else if (out->seam == UMCP_SEAM_PENDING) {
        out->stance.verdict = (out->identity_check == UMCP_CONFORMANT)
            ? UMCP_CONFORMANT : UMCP_NON_EVALUABLE;
    } else {
        out->stance.verdict = UMCP_CONFORMANT;
    }

    /* Update prior κ for next step */
    pipeline->prior_kappa = out->kernel.kappa;

    return UMCP_OK;
}

/* ─── Pipeline Queries ──────────────────────────────────────────── */

umcp_stance_t umcp_pipeline_stance(const umcp_pipeline_t *pipeline)
{
    umcp_stance_t empty = {
        .regime = {UMCP_REGIME_WATCH, 0},
        .seam = UMCP_SEAM_PENDING,
        .verdict = UMCP_NON_EVALUABLE,
        .confidence = 0.0
    };
    if (!pipeline || pipeline->ledger.count == 0) return empty;

    const umcp_ledger_entry_t *latest = umcp_ledger_latest(&pipeline->ledger);
    if (!latest) return empty;

    umcp_stance_t stance;
    stance.regime     = latest->regime;
    stance.seam       = latest->seam;
    stance.verdict    = umcp_ledger_verdict(&pipeline->ledger);
    stance.confidence = fabs(latest->residual);
    return stance;
}

umcp_verdict_t umcp_pipeline_verdict(const umcp_pipeline_t *pipeline)
{
    if (!pipeline) return UMCP_NON_EVALUABLE;
    return umcp_ledger_verdict(&pipeline->ledger);
}

size_t umcp_pipeline_step_count(const umcp_pipeline_t *pipeline)
{
    if (!pipeline) return 0;
    return pipeline->ledger.count;
}
