/**
 * @file pipeline.h
 * @brief Validation Pipeline — The Spine in C (Tier-0 Protocol)
 *
 * The spine is the fixed five-stop discourse structure:
 *   Contract → Canon → Closures → Integrity Ledger → Stance
 *
 * This module orchestrates the full validation pipeline in C:
 *   1. Accept a frozen contract
 *   2. Accept trace vectors (channel data from Tier-2 closures)
 *   3. Compute kernel invariants
 *   4. Classify regime
 *   5. Validate Tier-1 identities
 *   6. Compute cost closures and seam budget
 *   7. Append to ledger
 *   8. Derive stance (verdict)
 *
 * The pipeline is the orchestration layer that decides when
 * computation happens and in what order — formalizing the
 * protocol in C for maximum portability and embeddability.
 *
 * Spina non negotiabilis est. — The spine is non-negotiable.
 *
 * Collapsus generativus est; solum quod redit, reale est.
 */

#ifndef UMCP_C_PIPELINE_H
#define UMCP_C_PIPELINE_H

#include "types.h"
#include "contract.h"
#include "kernel.h"
#include "regime.h"
#include "trace.h"
#include "ledger.h"

#ifdef __cplusplus
extern "C" {
#endif

/* ─── Pipeline Configuration ────────────────────────────────────── */

/**
 * Pipeline state — manages the full validation flow.
 *
 * The pipeline holds a frozen contract and an integrity ledger.
 * Each call to umcp_pipeline_step() processes one trace and
 * appends the result to the ledger.
 */
typedef struct {
    umcp_contract_t     contract;     /**< Frozen contract (immutable per run) */
    umcp_ledger_t       ledger;       /**< Append-only integrity ledger        */
    double              prior_kappa;  /**< κ from previous step (NAN initially)*/
    int                 initialized;  /**< 1 after umcp_pipeline_init()        */
} umcp_pipeline_t;

/**
 * The result of one pipeline step.
 * Contains all computed values for inspection/logging.
 */
typedef struct {
    umcp_kernel_result_t kernel;      /**< Full kernel output        */
    umcp_regime_with_overlay_t regime;/**< Classified regime + overlay */
    umcp_verdict_t       identity_check; /**< Tier-1 identity result */
    umcp_seam_status_t   seam;        /**< Seam PASS/FAIL            */
    umcp_stance_t        stance;      /**< Combined stance           */
    double               D_omega;     /**< Drift cost                */
    double               D_C;         /**< Curvature cost            */
    double               budget;      /**< Budget Δκ                 */
    double               residual;    /**< Seam residual             */
} umcp_pipeline_result_t;

/* ─── Pipeline Lifecycle ────────────────────────────────────────── */

/**
 * Initialize a pipeline with a frozen contract and ledger storage.
 *
 * @param pipeline       Output pipeline
 * @param contract       Frozen contract (copied into pipeline)
 * @param ledger_buffer  Caller-allocated ledger entry buffer
 * @param ledger_capacity Max ledger entries
 * @return UMCP_OK on success
 */
int umcp_pipeline_init(umcp_pipeline_t *pipeline,
                        const umcp_contract_t *contract,
                        umcp_ledger_entry_t *ledger_buffer,
                        size_t ledger_capacity);

/**
 * Process one trace through the full spine.
 *
 * This is the core orchestration function. It executes all five stops:
 *   1. Contract (already frozen in pipeline)
 *   2. Canon (kernel computation)
 *   3. Closures (cost computation + regime gates)
 *   4. Integrity Ledger (append + reconcile)
 *   5. Stance (derive verdict)
 *
 * @param pipeline Pipeline state
 * @param trace    Input trace vector (c, w, n)
 * @param R        Return credit for this step
 * @param tau_R    Return time for this step
 * @param out      Output result (all computed values)
 * @return UMCP_OK on success
 */
int umcp_pipeline_step(umcp_pipeline_t *pipeline,
                        const umcp_trace_t *trace,
                        double R, double tau_R,
                        umcp_pipeline_result_t *out);

/**
 * Get the current stance (latest verdict from the ledger).
 */
umcp_stance_t umcp_pipeline_stance(const umcp_pipeline_t *pipeline);

/**
 * Get the overall verdict across all ledger entries.
 */
umcp_verdict_t umcp_pipeline_verdict(const umcp_pipeline_t *pipeline);

/**
 * Get the number of steps processed.
 */
size_t umcp_pipeline_step_count(const umcp_pipeline_t *pipeline);

#ifdef __cplusplus
}
#endif

#endif /* UMCP_C_PIPELINE_H */
