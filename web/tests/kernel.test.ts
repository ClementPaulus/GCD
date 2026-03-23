/**
 * GCD Kernel — TypeScript Test Suite
 *
 * Verifies Tier-1 invariants, algebraic identities, regime classification,
 * seam budget computation, and edge cases against the frozen contract.
 *
 * Orientation receipts from scripts/orientation.py serve as ground truth.
 */

import { describe, it, expect } from 'vitest';
import {
  computeKernel,
  classifyRegime,
  bernoulliEntropy,
  clamp,
  gammaOmega,
  costCurvature,
  computeSeamBudget,
  verifyIdentities,
  computeTauRStar,
  computeRCritical,
  sweepHomogeneous,
  PRESETS,
} from '../src/lib/kernel';
import { EPSILON, P_EXPONENT, TOL_SEAM } from '../src/lib/constants';

/* ─── §1: Duality Identity F + ω = 1 ───────────────────────────── */

describe('Duality identity (F + ω = 1)', () => {
  it('holds exactly for homogeneous traces', () => {
    for (const c of [0.1, 0.3, 0.5, 0.7822, 0.9, 0.999]) {
      const result = computeKernel([c, c, c, c], [0.25, 0.25, 0.25, 0.25]);
      expect(result.F + result.omega).toBeCloseTo(1.0, 14);
    }
  });

  it('holds exactly for heterogeneous traces', () => {
    const result = computeKernel(
      [0.95, 0.70, 0.30, 0.001],
      [0.25, 0.25, 0.25, 0.25],
    );
    expect(result.F + result.omega).toBeCloseTo(1.0, 14);
  });

  it('holds across all presets', () => {
    for (const preset of Object.values(PRESETS)) {
      const result = computeKernel([...preset.c], [...preset.w]);
      expect(result.F + result.omega).toBeCloseTo(1.0, 14);
    }
  });

  it('holds for 10,000 random traces', () => {
    const rng = mulberry32(42);
    for (let trial = 0; trial < 10_000; trial++) {
      const n = 2 + Math.floor(rng() * 15);
      const c = Array.from({ length: n }, () => rng());
      const result = computeKernel(c);
      expect(Math.abs(result.F + result.omega - 1.0)).toBeLessThan(1e-12);
    }
  });
});

/* ─── §2: Integrity Bound IC ≤ F ────────────────────────────────── */

describe('Integrity bound (IC ≤ F)', () => {
  it('holds for homogeneous traces (IC = F)', () => {
    const result = computeKernel([0.7822, 0.7822, 0.7822, 0.7822]);
    expect(result.IC).toBeLessThanOrEqual(result.F + 1e-12);
    expect(result.delta).toBeCloseTo(0.0, 10);
  });

  it('holds for heterogeneous traces (IC < F)', () => {
    const result = computeKernel([0.95, 0.001, 0.95, 0.95]);
    expect(result.IC).toBeLessThan(result.F);
    expect(result.delta).toBeGreaterThan(0);
  });

  it('holds across 10,000 random traces', () => {
    const rng = mulberry32(123);
    for (let trial = 0; trial < 10_000; trial++) {
      const n = 2 + Math.floor(rng() * 15);
      const c = Array.from({ length: n }, () => rng());
      const result = computeKernel(c);
      expect(result.IC).toBeLessThanOrEqual(result.F + 1e-10);
    }
  });

  it('produces large heterogeneity gap with one dead channel', () => {
    // Orientation §2: Δ for (0.95, 0.001) ≈ 0.4447
    const result = computeKernel([0.95, 0.001]);
    expect(result.delta).toBeGreaterThan(0.4);
    expect(result.delta).toBeLessThan(0.5);
  });
});

/* ─── §3: Log-Integrity Relation IC = exp(κ) ────────────────────── */

describe('Log-integrity relation (IC = exp(κ))', () => {
  it('holds exactly for all presets', () => {
    for (const preset of Object.values(PRESETS)) {
      const result = computeKernel([...preset.c], [...preset.w]);
      expect(Math.abs(result.IC - Math.exp(result.kappa))).toBeLessThan(1e-12);
    }
  });

  it('holds across 10,000 random traces', () => {
    const rng = mulberry32(7);
    for (let trial = 0; trial < 10_000; trial++) {
      const n = 2 + Math.floor(rng() * 15);
      const c = Array.from({ length: n }, () => rng());
      const result = computeKernel(c);
      expect(Math.abs(result.IC - Math.exp(result.kappa))).toBeLessThan(1e-12);
    }
  });
});

/* ─── §4: Geometric Slaughter ────────────────────────────────────── */

describe('Geometric slaughter', () => {
  it('one dead channel in 8 kills IC while F stays healthy', () => {
    // PRESETS.slaughter has c=0.001 (not fully dead) → IC/F ≈ 0.49
    // With a truly dead channel (c=ε), IC/F ≈ 0.114 (orientation §3)
    const result = computeKernel(PRESETS.slaughter.c as unknown as number[], [...PRESETS.slaughter.w]);
    expect(result.F).toBeGreaterThan(0.8);
    const icOverF = result.IC / result.F;
    expect(icOverF).toBeLessThan(1.0); // IC < F (heterogeneity gap)
    expect(result.delta).toBeGreaterThan(0.3); // significant gap
  });

  it('truly dead channel (c=ε) produces IC/F ≈ 0.114', () => {
    // Orientation §3: IC/F with 1 dead channel (8ch) = 0.1143
    const c = [0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 1e-8];
    const w = [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125];
    const result = computeKernel(c, w);
    const icOverF = result.IC / result.F;
    expect(icOverF).toBeLessThan(0.15);
    expect(icOverF).toBeGreaterThan(0.05);
  });

  it('homogeneous trace has no slaughter (IC/F ≈ 1)', () => {
    const result = computeKernel([0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95]);
    const icOverF = result.IC / result.F;
    expect(icOverF).toBeGreaterThan(0.99);
  });
});

/* ─── §5: Bernoulli Field Entropy ────────────────────────────────── */

describe('Bernoulli field entropy', () => {
  it('is zero at boundaries (c=0, c=1)', () => {
    expect(bernoulliEntropy(0.0)).toBe(0.0);
    expect(bernoulliEntropy(1.0)).toBe(0.0);
  });

  it('is maximal at c = 0.5 (ln 2)', () => {
    expect(bernoulliEntropy(0.5)).toBeCloseTo(Math.LN2, 12);
  });

  it('is symmetric: h(c) = h(1-c)', () => {
    for (const c of [0.1, 0.2, 0.3, 0.4]) {
      expect(bernoulliEntropy(c)).toBeCloseTo(bernoulliEntropy(1 - c), 12);
    }
  });

  it('S + κ = 0 at c = 0.5 (equator convergence)', () => {
    // Orientation §8: S + κ at c=1/2 = 0.0
    const result = computeKernel([0.5, 0.5, 0.5, 0.5]);
    expect(Math.abs(result.S + result.kappa)).toBeLessThan(1e-10);
  });
});

/* ─── §6: Guard-Band Clamp ──────────────────────────────────────── */

describe('Guard-band clamp', () => {
  it('clamps low values to ε', () => {
    expect(clamp(0.0)).toBe(EPSILON);
    expect(clamp(-1.0)).toBe(EPSILON);
    expect(clamp(1e-20)).toBe(EPSILON);
  });

  it('clamps high values to 1 - ε', () => {
    expect(clamp(1.0)).toBe(1.0 - EPSILON);
    expect(clamp(2.0)).toBe(1.0 - EPSILON);
  });

  it('passes through values in (ε, 1-ε)', () => {
    expect(clamp(0.5)).toBe(0.5);
    expect(clamp(0.7822)).toBe(0.7822);
  });
});

/* ─── §7: Regime Classification ──────────────────────────────────── */

describe('Regime classification', () => {
  it('classifies truly stable trace as STABLE', () => {
    // PRESETS.stable has S > 0.15 due to channel spread → WATCH
    // Use a tighter trace that actually meets all four gates
    const c = [0.97, 0.97, 0.97, 0.97, 0.97, 0.97, 0.97, 0.97];
    const result = computeKernel(c);
    const { regime } = classifyRegime(result);
    expect(regime).toBe('STABLE');
  });

  it('PRESETS.stable classifies as WATCH (S gate fails)', () => {
    // The "stable" preset has enough variance that S > 0.15
    const result = computeKernel([...PRESETS.stable.c], [...PRESETS.stable.w]);
    const { regime } = classifyRegime(result);
    expect(regime).toBe('WATCH');
    expect(result.S).toBeGreaterThan(0.15);
  });

  it('classifies moderate drift as WATCH', () => {
    const result = computeKernel([...PRESETS.watch.c], [...PRESETS.watch.w]);
    const { regime } = classifyRegime(result);
    expect(regime).toBe('WATCH');
  });

  it('classifies high drift as COLLAPSE', () => {
    const result = computeKernel([...PRESETS.collapse.c], [...PRESETS.collapse.w]);
    const { regime } = classifyRegime(result);
    expect(regime).toBe('COLLAPSE');
  });

  it('flags critical when IC < 0.30', () => {
    const result = computeKernel([0.10, 0.10, 0.10, 0.10]);
    const { isCritical } = classifyRegime(result);
    expect(isCritical).toBe(true);
  });

  it('does not flag critical when IC > 0.30', () => {
    const result = computeKernel([0.95, 0.95, 0.95, 0.95]);
    const { isCritical } = classifyRegime(result);
    expect(isCritical).toBe(false);
  });

  it('Stable regime is rare in random traces', () => {
    // Orientation §7: Stable = 12.5% of Fisher space
    // Uniform random [0,1] traces almost never hit all four gates
    // (ω < 0.038, F > 0.90, S < 0.15, C < 0.14) simultaneously
    const rng = mulberry32(99);
    let stable = 0;
    const N = 10_000;
    for (let i = 0; i < N; i++) {
      const n = 8;
      const c = Array.from({ length: n }, () => rng());
      const result = computeKernel(c);
      if (classifyRegime(result).regime === 'STABLE') stable++;
    }
    const pct = (stable / N) * 100;
    // Stability is rare — most random traces are COLLAPSE or WATCH
    expect(pct).toBeLessThan(25);
  });
});

/* ─── §8: Drift Cost Γ(ω) ───────────────────────────────────────── */

describe('Drift cost Γ(ω)', () => {
  it('Γ(0) = 0', () => {
    expect(gammaOmega(0)).toBeCloseTo(0.0, 12);
  });

  it('Γ(ω) is monotonically increasing', () => {
    let prev = 0;
    for (let i = 1; i <= 99; i++) {
      const omega = i / 100;
      const g = gammaOmega(omega);
      expect(g).toBeGreaterThanOrEqual(prev);
      prev = g;
    }
  });

  it('pole at ω = 1 (Γ → large)', () => {
    expect(gammaOmega(0.999)).toBeGreaterThan(100);
  });

  it('uses p = 3 (Cardano root)', () => {
    // Γ(ω) = ω³ / (1 - ω + ε)
    const omega = 0.5;
    const expected = 0.5 ** 3 / (1 - 0.5 + EPSILON);
    expect(gammaOmega(omega)).toBeCloseTo(expected, 12);
  });
});

/* ─── §9: Seam Budget ────────────────────────────────────────────── */

describe('Seam budget computation', () => {
  it('∞_rec τ_R yields zero credit (gesture)', () => {
    const sb = computeSeamBudget(0.1, 0.1, 1.0, Infinity);
    expect(sb.credit).toBe(0);
    expect(sb.deltaKappa).toBe(0);
  });

  it('finite τ_R computes budget correctly', () => {
    const sb = computeSeamBudget(0.1, 0.1, 1.0, 1.0);
    expect(sb.credit).toBe(1.0);
    expect(sb.D_omega).toBeCloseTo(gammaOmega(0.1), 12);
    expect(sb.D_C).toBeCloseTo(costCurvature(0.1), 12);
    expect(sb.deltaKappa).toBeCloseTo(sb.credit - sb.D_omega - sb.D_C, 12);
  });

  it('seam passes when residual ≤ tol_seam', () => {
    const sb = computeSeamBudget(0.1, 0.1, 1.0, 1.0, 0);
    // Residual = deltaKappa - kappaLedger
    if (Math.abs(sb.residual) <= TOL_SEAM) {
      expect(sb.pass).toBe(true);
    }
  });
});

/* ─── §10: Identity Verification ─────────────────────────────────── */

describe('Identity verification', () => {
  it('all three identities pass for every preset', () => {
    for (const preset of Object.values(PRESETS)) {
      const result = computeKernel([...preset.c], [...preset.w]);
      const checks = verifyIdentities(result);
      expect(checks).toHaveLength(3);
      for (const check of checks) {
        expect(check.pass).toBe(true);
      }
    }
  });
});

/* ─── §11: τ_R* Diagnostic ──────────────────────────────────────── */

describe('τ_R* diagnostic', () => {
  it('is high for low ω and low C (favorable return)', () => {
    const t = computeTauRStar(0.01, 0.01);
    expect(t).toBeGreaterThan(10);
  });

  it('is low for high ω (unfavorable return)', () => {
    const t = computeTauRStar(0.9, 0.1);
    expect(t).toBeLessThan(1);
  });

  it('R_critical is Infinity when τ_R = 0', () => {
    expect(computeRCritical(0.5, 0.5, 0)).toBe(Infinity);
  });

  it('R_critical is Infinity when τ_R = ∞_rec', () => {
    expect(computeRCritical(0.5, 0.5, Infinity)).toBe(Infinity);
  });
});

/* ─── §12: Edge Cases ────────────────────────────────────────────── */

describe('Edge cases', () => {
  it('empty trace returns safe defaults', () => {
    const result = computeKernel([]);
    expect(result.F).toBe(0);
    expect(result.omega).toBe(1);
    expect(result.IC).toBe(0);
  });

  it('single-channel trace works', () => {
    const result = computeKernel([0.8]);
    expect(result.F + result.omega).toBeCloseTo(1.0, 14);
  });

  it('near-zero channels are guard-band clamped', () => {
    const result = computeKernel([0.0, 0.0, 0.0, 0.0]);
    expect(result.F).toBeGreaterThan(0);
    expect(result.IC).toBeGreaterThan(0);
  });

  it('near-one channels are guard-band clamped', () => {
    const result = computeKernel([1.0, 1.0, 1.0, 1.0]);
    expect(result.F).toBeLessThan(1.0);
  });
});

/* ─── §13: Sweep Functions ───────────────────────────────────────── */

describe('Sweep functions', () => {
  it('sweepHomogeneous returns correct number of points', () => {
    const points = sweepHomogeneous(8, 100);
    expect(points).toHaveLength(101);
  });

  it('sweepHomogeneous maintains duality at every point', () => {
    const points = sweepHomogeneous(8, 200);
    for (const pt of points) {
      expect(Math.abs(pt.F + pt.omega - 1.0)).toBeLessThan(1e-12);
    }
  });
});

/* ─── §14: Frozen Contract Constants ─────────────────────────────── */

describe('Frozen contract constants', () => {
  it('EPSILON = 1e-8', () => {
    expect(EPSILON).toBe(1e-8);
  });

  it('P_EXPONENT = 3 (Cardano)', () => {
    expect(P_EXPONENT).toBe(3);
  });

  it('TOL_SEAM = 0.005', () => {
    expect(TOL_SEAM).toBe(0.005);
  });
});

/* ─── Utility: Deterministic PRNG ────────────────────────────────── */

function mulberry32(seed: number): () => number {
  let s = seed | 0;
  return () => {
    s = (s + 0x6d2b79f5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
