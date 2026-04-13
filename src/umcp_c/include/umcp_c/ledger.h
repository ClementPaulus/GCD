/**
 * @file ledger.h
 * @brief Integrity Ledger — C formalization (Tier-0 Protocol)
 *
 * The Integrity Ledger is the fourth stop in the spine:
 *   Contract → Canon → Closures → INTEGRITY LEDGER → Stance
 *
 * It debits Drift + Roughness, credits Return, and reconciles.
 * The ledger is append-only — history is never rewritten, only welded.
 *
 * Historia numquam rescribitur; sutura tantum additur.
 *
 * Collapsus generativus est; solum quod redit, reale est.
 */

#ifndef UMCP_C_LEDGER_H
#define UMCP_C_LEDGER_H

#include "types.h"
#include "kernel.h"
#include "contract.h"

#ifdef __cplusplus
extern "C" {
#endif

/* ─── Ledger Entry ──────────────────────────────────────────────── */

/**
 * A single ledger row — one observation in the return log.
 *
 * Debit: D_ω (drift cost) + D_C (roughness cost)
 * Credit: R · τ_R (return credit × return time)
 * Residual: Δκ_budget − Δκ_ledger
 */
typedef struct {
    uint64_t             timestamp;   /**< Monotonic row ID           */
    umcp_kernel_result_t kernel;      /**< Full kernel output         */
    umcp_regime_with_overlay_t regime;/**< Derived regime + overlay   */
    double               D_omega;     /**< Drift cost Γ(ω)           */
    double               D_C;         /**< Roughness cost α·C        */
    double               R;           /**< Return credit              */
    double               tau_R;       /**< Return time                */
    double               delta_kappa; /**< Observed Δκ = κ(t) - κ(t-1) */
    double               budget;      /**< R·τ_R − (D_ω + D_C)       */
    double               residual;    /**< budget − delta_kappa       */
    umcp_seam_status_t   seam;        /**< PASS / FAIL / PENDING      */
    umcp_verdict_t       verdict;     /**< Identity check result      */
} umcp_ledger_entry_t;

/* ─── Ledger (Append-Only) ──────────────────────────────────────── */

/**
 * The integrity ledger — an append-only sequence of observations.
 *
 * The ledger provides O(1) running statistics:
 *   - Cumulative residual (for return dynamics check)
 *   - Maximum residual (for worst-case analysis)
 *   - Total entries and regime counts
 */
typedef struct {
    umcp_ledger_entry_t *entries;     /**< Caller-allocated buffer    */
    size_t               capacity;    /**< Max entries                */
    size_t               count;       /**< Current entry count        */

    /* O(1) running statistics */
    double               cum_residual;   /**< Σ|residual|            */
    double               max_residual;   /**< max(|residual|)        */
    double               cum_delta_kappa;/**< Σ Δκ                   */
    uint32_t             stable_count;    /**< STABLE regime count    */
    uint32_t             watch_count;     /**< WATCH regime count     */
    uint32_t             collapse_count;  /**< COLLAPSE regime count  */
    uint32_t             critical_count;  /**< CRITICAL overlay count */
    uint32_t             pass_count;      /**< Number of PASS seams   */
    uint32_t             fail_count;      /**< Number of FAIL seams   */
} umcp_ledger_t;

/* ─── Ledger Operations ─────────────────────────────────────────── */

/**
 * Initialize a ledger with caller-provided storage.
 *
 * @param ledger   Output ledger
 * @param buffer   Caller-allocated entry buffer
 * @param capacity Size of the buffer (max entries)
 * @return UMCP_OK on success
 */
int umcp_ledger_init(umcp_ledger_t *ledger,
                      umcp_ledger_entry_t *buffer, size_t capacity);

/**
 * Append a fully-populated entry to the ledger.
 * Updates running statistics in O(1).
 *
 * @param ledger Ledger to append to
 * @param entry  Entry to append (copied into buffer)
 * @return UMCP_OK on success, UMCP_ERR_RANGE if ledger is full
 */
int umcp_ledger_append(umcp_ledger_t *ledger,
                        const umcp_ledger_entry_t *entry);

/**
 * Build a ledger entry from a kernel result and contract.
 *
 * Computes:
 *   - Regime classification
 *   - Cost closures (D_ω, D_C)
 *   - Budget and residual (if prior κ is available)
 *   - Seam PASS/FAIL check
 *   - Tier-1 identity validation
 *
 * @param entry     Output entry
 * @param result    Kernel computation output
 * @param contract  Frozen contract parameters
 * @param prior_kappa Previous κ value (NAN if no prior)
 * @param R         Return credit
 * @param tau_R     Return time (UMCP_TAU_R_INF_REC for no return)
 * @return UMCP_OK on success
 */
int umcp_ledger_build_entry(
    umcp_ledger_entry_t *entry,
    const umcp_kernel_result_t *result,
    const umcp_contract_t *contract,
    double prior_kappa,
    double R, double tau_R);

/* ─── Ledger Queries ────────────────────────────────────────────── */

/**
 * Get the mean absolute residual across all entries.
 * Used for return dynamics diagnostic (Lemma 27).
 */
double umcp_ledger_mean_residual(const umcp_ledger_t *ledger);

/**
 * Get the most recent entry (or NULL if empty).
 */
const umcp_ledger_entry_t *umcp_ledger_latest(const umcp_ledger_t *ledger);

/**
 * Get the regime distribution as fractions.
 */
void umcp_ledger_regime_fractions(const umcp_ledger_t *ledger,
                                   double *stable, double *watch,
                                   double *collapse, double *critical);

/**
 * Determine the overall verdict for the ledger.
 *
 * CONFORMANT:     All identity checks passed, no FAIL seams
 * NONCONFORMANT:  At least one identity violation or FAIL seam
 * NON_EVALUABLE:  Ledger is empty or all seams are PENDING
 */
umcp_verdict_t umcp_ledger_verdict(const umcp_ledger_t *ledger);

#ifdef __cplusplus
}
#endif

#endif /* UMCP_C_LEDGER_H */
