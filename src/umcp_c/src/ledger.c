/**
 * @file ledger.c
 * @brief Integrity Ledger implementation
 *
 * The ledger is the fourth stop in the spine.
 * It debits Drift + Roughness, credits Return, and reconciles.
 * Append-only — history is never rewritten; only a weld is added.
 *
 * Historia numquam rescribitur; sutura tantum additur.
 */

#include "umcp_c/ledger.h"
#include "umcp_c/regime.h"
#include "umcp_c/trace.h"
#include <math.h>
#include <string.h>

/* ─── Ledger Initialization ─────────────────────────────────────── */

int umcp_ledger_init(umcp_ledger_t *ledger,
                      umcp_ledger_entry_t *buffer, size_t capacity)
{
    if (!ledger || !buffer || capacity == 0) return UMCP_ERR_NULL_PTR;

    memset(ledger, 0, sizeof(*ledger));
    ledger->entries  = buffer;
    ledger->capacity = capacity;
    ledger->count    = 0;

    ledger->cum_residual    = 0.0;
    ledger->max_residual    = 0.0;
    ledger->cum_delta_kappa = 0.0;
    ledger->pass_count      = 0;
    ledger->fail_count      = 0;

    ledger->stable_count = 0;
    ledger->watch_count = 0;
    ledger->collapse_count = 0;
    ledger->critical_count = 0;

    return UMCP_OK;
}

/* ─── Append Entry ──────────────────────────────────────────────── */

int umcp_ledger_append(umcp_ledger_t *ledger,
                        const umcp_ledger_entry_t *entry)
{
    if (!ledger || !entry) return UMCP_ERR_NULL_PTR;
    if (ledger->count >= ledger->capacity) return UMCP_ERR_RANGE;

    /* Copy entry into buffer */
    ledger->entries[ledger->count] = *entry;
    ledger->count++;

    /* O(1) running statistics */
    double abs_res = fabs(entry->residual);
    ledger->cum_residual += abs_res;
    if (abs_res > ledger->max_residual) {
        ledger->max_residual = abs_res;
    }
    ledger->cum_delta_kappa += entry->delta_kappa;

    /* Regime distribution (overlay-aware) */
    switch (entry->regime.base_regime) {
        case UMCP_REGIME_STABLE:   ledger->stable_count++; break;
        case UMCP_REGIME_WATCH:    ledger->watch_count++; break;
        case UMCP_REGIME_COLLAPSE: ledger->collapse_count++; break;
        default: break;
    }
    if (entry->regime.is_critical) {
        ledger->critical_count++;
    }

    /* Seam counts */
    if (entry->seam == UMCP_SEAM_PASS) ledger->pass_count++;
    else if (entry->seam == UMCP_SEAM_FAIL) ledger->fail_count++;

    return UMCP_OK;
}

/* ─── Build Entry From Kernel Result ────────────────────────────── */

int umcp_ledger_build_entry(
    umcp_ledger_entry_t *entry,
    const umcp_kernel_result_t *result,
    const umcp_contract_t *contract,
    double prior_kappa,
    double R, double tau_R)
{
    if (!entry || !result || !contract) return UMCP_ERR_NULL_PTR;

    memset(entry, 0, sizeof(*entry));

    /* Copy kernel output */
    entry->kernel = *result;

    /* Classify regime (overlay-aware) */
    entry->regime = umcp_classify_regime_with_overlay(result, &contract->thresholds);

    /* Compute cost closures */
    entry->D_omega = umcp_gamma_omega(result->omega,
                                       contract->p_exponent,
                                       contract->epsilon);
    entry->D_C = umcp_cost_curvature(result->C, contract->alpha);

    /* Return parameters */
    entry->R     = R;
    entry->tau_R = tau_R;

    /* Observed Δκ (requires prior) */
    if (isnan(prior_kappa)) {
        entry->delta_kappa = 0.0;
        entry->budget      = 0.0;
        entry->residual    = 0.0;
        entry->seam        = UMCP_SEAM_PENDING;
    } else {
        entry->delta_kappa = result->kappa - prior_kappa;
        entry->budget = umcp_budget_delta_kappa(R, tau_R,
                                                 entry->D_omega,
                                                 entry->D_C);
        entry->residual = umcp_seam_residual(entry->budget,
                                              entry->delta_kappa);

        /* Seam PASS check */
        double I_ratio = (prior_kappa != 0.0)
            ? result->IC / exp(prior_kappa)
            : 1.0;

        entry->seam = umcp_check_seam_pass(
            entry->residual, tau_R, I_ratio,
            entry->delta_kappa, contract->tol_seam, 1e-6,
            NULL, 0);
    }

    /* Validate Tier-1 identities */
    entry->verdict = umcp_validate_identities(result, 1e-9);

    return UMCP_OK;
}

/* ─── Queries ───────────────────────────────────────────────────── */

double umcp_ledger_mean_residual(const umcp_ledger_t *ledger)
{
    if (!ledger || ledger->count == 0) return 0.0;
    return ledger->cum_residual / (double)ledger->count;
}

const umcp_ledger_entry_t *umcp_ledger_latest(const umcp_ledger_t *ledger)
{
    if (!ledger || ledger->count == 0) return NULL;
    return &ledger->entries[ledger->count - 1];
}

void umcp_ledger_regime_fractions(const umcp_ledger_t *ledger,
                                   double *stable, double *watch,
                                   double *collapse, double *critical)
{
    if (!ledger || ledger->count == 0) {
        if (stable)   *stable   = 0.0;
        if (watch)    *watch    = 0.0;
        if (collapse) *collapse = 0.0;
        if (critical) *critical = 0.0;
        return;
    }

    double total = (double)ledger->count;
    if (stable)   *stable   = (double)ledger->stable_count   / total;
    if (watch)    *watch    = (double)ledger->watch_count    / total;
    if (collapse) *collapse = (double)ledger->collapse_count / total;
    if (critical) *critical = (double)ledger->critical_count / total;
}

umcp_verdict_t umcp_ledger_verdict(const umcp_ledger_t *ledger)
{
    if (!ledger || ledger->count == 0) return UMCP_NON_EVALUABLE;

    /* Check for any FAIL seams */
    if (ledger->fail_count > 0) return UMCP_NONCONFORMANT;

    /* Check all entries have valid verdicts */
    int has_conformant = 0;
    int all_pending    = 1;

    for (size_t i = 0; i < ledger->count; ++i) {
        const umcp_ledger_entry_t *e = &ledger->entries[i];

        if (e->verdict == UMCP_NONCONFORMANT) return UMCP_NONCONFORMANT;
        if (e->verdict == UMCP_CONFORMANT) has_conformant = 1;
        if (e->seam != UMCP_SEAM_PENDING) all_pending = 0;
    }

    /* If all seams are pending, we haven't evaluated yet */
    if (all_pending && !has_conformant) return UMCP_NON_EVALUABLE;

    return UMCP_CONFORMANT;
}
