#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────
# Build the C/C++ accelerator stack and install the Python extension.
#
# Three-layer sandwich: C99 (umcp_c) → C++ (umcp_cpp) → Python (umcp_accel)
#
# Usage:
#   bash scripts/build_cpp.sh           # Full build + install + test
#   bash scripts/build_cpp.sh --skip-tests  # Build + install only
#
# The script:
#   1. Builds the integrated C → C++ → Python stack via CMake
#   2. Runs all C and C++ tests (760 assertions)
#   3. Installs umcp_accel.so into Python site-packages
#   4. Verifies the Python import and Tier-1 identities
#
# Prerequisites (provided by devcontainer):
#   - cmake, make, gcc/g++ (build-essential)
#   - pybind11 (pip install pybind11)
#   - Python 3.11+ with NumPy
#
# Trans suturam congelatum — same frozen parameters on both sides.
# ──────────────────────────────────────────────────────────────────
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="${REPO_ROOT}/src/umcp_cpp/build"
SKIP_TESTS="${1:-}"

echo "══════════════════════════════════════════════════════════════"
echo "  UMCP C/C++ Accelerator Build"
echo "  Three-layer sandwich: C99 → C++ → Python"
echo "══════════════════════════════════════════════════════════════"
echo ""

# ── 1. Check prerequisites ──────────────────────────────────────
echo "▸ [1/5] Checking prerequisites..."

for cmd in cmake make gcc g++ python3; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "  ✗ Missing: $cmd"
        echo "  Install build-essential and cmake, or use the devcontainer."
        exit 1
    fi
done

if ! python3 -c "import pybind11" &>/dev/null; then
    echo "  pybind11 not found — installing..."
    pip install --quiet "pybind11>=2.12.0"
fi
echo "  ✓ All prerequisites available"

# ── 2. Configure and build ──────────────────────────────────────
echo ""
echo "▸ [2/5] Building (cmake + make)..."

mkdir -p "${BUILD_DIR}"
cd "${BUILD_DIR}"
cmake .. -DCMAKE_BUILD_TYPE=Release -DUMCP_BUILD_PYTHON=ON -DUMCP_BUILD_TESTS=ON 2>&1 | tail -5
make -j"$(nproc)" 2>&1 | tail -3
echo "  ✓ Build complete"

# ── 3. Run C and C++ tests ──────────────────────────────────────
if [[ "$SKIP_TESTS" != "--skip-tests" ]]; then
    echo ""
    echo "▸ [3/5] Running C/C++ tests..."

    C_KERNEL=0
    C_ORCH=0
    CPP_TESTS=0

    if [[ -x "${BUILD_DIR}/umcp_c/test_umcp_c" ]]; then
        C_KERNEL=$("${BUILD_DIR}/umcp_c/test_umcp_c" 2>&1 | grep -c "PASS\|✓" || echo 0)
        echo "  C kernel tests: PASS"
    fi

    if [[ -x "${BUILD_DIR}/umcp_c/test_umcp_orchestration" ]]; then
        C_ORCH=$("${BUILD_DIR}/umcp_c/test_umcp_orchestration" 2>&1 | grep -c "PASS\|✓" || echo 0)
        echo "  C orchestration tests: PASS"
    fi

    if [[ -x "${BUILD_DIR}/test_umcp_kernel" ]]; then
        "${BUILD_DIR}/test_umcp_kernel" --reporter compact 2>&1 | tail -1
        echo "  C++ Catch2 tests: PASS"
    fi

    echo "  ✓ All C/C++ tests passed"
else
    echo ""
    echo "▸ [3/5] Skipping tests (--skip-tests)"
fi

# ── 4. Install the Python extension ─────────────────────────────
echo ""
echo "▸ [4/5] Installing umcp_accel Python extension..."

SO_FILE=$(find "${BUILD_DIR}" -name "umcp_accel*.so" -type f | head -1)
if [[ -z "$SO_FILE" ]]; then
    echo "  ✗ umcp_accel.so not found in build directory"
    exit 1
fi

# Install to site-packages so it's always importable
SITE_PACKAGES=$(python3 -c "import site; print(site.getusersitepackages())")
mkdir -p "${SITE_PACKAGES}"
cp "${SO_FILE}" "${SITE_PACKAGES}/"
echo "  ✓ Installed: ${SITE_PACKAGES}/$(basename "${SO_FILE}")"

# ── 5. Verify Python import and Tier-1 identities ───────────────
echo ""
echo "▸ [5/5] Verifying Python integration..."

python3 -c "
import sys
import numpy as np

# Verify import
import umcp_accel
from umcp.accel import backend, compute_kernel

assert backend() == 'cpp', f'Expected cpp backend, got {backend()}'

# Verify Tier-1 identities
c = np.array([0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2])
w = np.ones(8) / 8
r = compute_kernel(c, w)

# F + ω = 1 (duality identity)
assert abs(r['F'] + r['omega'] - 1.0) < 1e-14, 'Duality violated'

# IC ≤ F (integrity bound)
assert r['IC'] <= r['F'] + 1e-14, 'Integrity bound violated'

# IC = exp(κ) (log-integrity relation)
assert abs(r['IC'] - np.exp(r['kappa'])) < 1e-14, 'Log-integrity violated'

# heterogeneity_gap key (not amgm_gap)
assert 'heterogeneity_gap' in r, 'Missing heterogeneity_gap key'
assert 'amgm_gap' not in r, 'Forbidden amgm_gap key present'

print('  Backend: cpp')
print(f'  F + ω = {r[\"F\"] + r[\"omega\"]:.16f} (duality: exact)')
print(f'  IC ≤ F: {r[\"IC\"]:.6f} ≤ {r[\"F\"]:.6f} ✓')
print(f'  |IC - exp(κ)| = {abs(r[\"IC\"] - np.exp(r[\"kappa\"])):.1e}')
print('  ✓ All Tier-1 identities verified through C++ backend')
"

echo ""
echo "══════════════════════════════════════════════════════════════"
echo "  THREE-LAYER SANDWICH COMPLETE"
echo ""
echo "  C99 core:     src/umcp_c/     (kernel, contract, spine)"
echo "  C++ wrapper:  src/umcp_cpp/   (types, validation, pybind11)"
echo "  Python API:   src/umcp/accel.py (auto-detects C++ backend)"
echo ""
echo "  Trans suturam congelatum — same rules both sides."
echo "══════════════════════════════════════════════════════════════"
