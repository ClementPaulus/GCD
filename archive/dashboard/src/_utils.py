"""
Shared utilities, constants, and data loaders for UMCP Dashboard.

Contains:
  - Constants: REGIME_COLORS, KERNEL_SYMBOLS, STATUS_COLORS, THEMES
  - Data loaders: load_ledger, load_casepacks, load_contracts, load_closures
  - Helpers: classify_regime, get_regime_color, format_bytes, etc.
  - Path setup: _setup_closures_path, _ensure_closures_path, get_repo_root
"""
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportMissingTypeStubs=false

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from umcp.dashboard._deps import _cache_data, np, pd, st

# Import UMCP core modules
try:
    from umcp import __version__
except ImportError:
    __version__ = "2.0.0"


def _setup_closures_path() -> None:
    """Add repo root to sys.path so closures package is importable.

    Works across editable installs, Docker, and Streamlit subprocess contexts.
    """
    import importlib
    from pathlib import Path

    # Check if closures is already importable via editable install
    spec = importlib.util.find_spec("closures")
    if spec is not None and spec.origin is not None:
        return  # Already resolvable — nothing to do

    # Find repo root (contains pyproject.toml)
    current = Path(__file__).parent.resolve()
    while current != current.parent:
        if (current / "pyproject.toml").exists():
            repo_root = str(current)
            if repo_root not in sys.path:
                sys.path.insert(0, repo_root)
            return
        current = current.parent

    # Fallback: check common Docker paths
    for path in ["/app", "/workspaces/UMCP-Metadata-Runnable-Code"]:
        if Path(path).exists() and path not in sys.path:
            sys.path.insert(0, path)


_setup_closures_path()


def _ensure_closures_path() -> None:
    """Ensure closures/ package is importable (idempotent, safe to call multiple times).

    This is a safety net for Streamlit subprocesses where _setup_closures_path()
    may not have resolved the repo root correctly. Uses get_repo_root() which
    interrogates ``pyproject.toml`` location at runtime.
    """

    repo_root = get_repo_root()
    repo_str = str(repo_root)
    if repo_str not in sys.path:
        sys.path.insert(0, repo_str)


# ============================================================================
# Constants and Configuration
# ============================================================================

REGIME_COLORS = {
    "STABLE": "#28a745",  # Green
    "WATCH": "#ffc107",  # Yellow/Amber
    "COLLAPSE": "#dc3545",  # Red
    "CRITICAL": "#6f42c1",  # Purple
}

# Kernel invariants from KERNEL_SPECIFICATION.md
# Tier-1 outputs: F, ω, S, C, κ, IC computed from frozen trace Ψ(t)
KERNEL_SYMBOLS = {
    # Core Tier-1 Invariants
    "omega": "ω (Drift = 1-F)",
    "F": "F (Fidelity)",
    "S": "S (Bernoulli Field Entropy)",
    "C": "C (Curvature Proxy)",
    "tau_R": "τ_R (Return Time)",
    "IC": "IC (Integrity Composite = exp(κ))",
    "kappa": "κ (Log-Integrity = Σwᵢ ln cᵢ)",
    # Derived/Seam Values
    "stiffness": "Stiffness",
    "delta_kappa": "Δκ (Seam Curvature Change)",
    "curvature": "C (Curvature = std/0.5)",
    "freshness": "Freshness (1-ω)",
    "seam_residual": "s (Seam Residual)",
    # Meta
    "timestamp": "Timestamp",
    "run_status": "Status",
    "Phi_gen": "Φ_gen (Generative Flux)",
}

STATUS_COLORS = {
    "CONFORMANT": "#28a745",
    "NONCONFORMANT": "#dc3545",
    "NON_EVALUABLE": "#6c757d",
}

# Theme configurations
THEMES = {
    "Default": {
        "primary": "#007bff",
        "secondary": "#6c757d",
        "success": "#28a745",
        "danger": "#dc3545",
        "warning": "#ffc107",
        "info": "#17a2b8",
        "bg_primary": "#ffffff",
        "bg_secondary": "#f8f9fa",
    },
    "Dark": {
        "primary": "#0d6efd",
        "secondary": "#adb5bd",
        "success": "#198754",
        "danger": "#dc3545",
        "warning": "#ffc107",
        "info": "#0dcaf0",
        "bg_primary": "#212529",
        "bg_secondary": "#343a40",
    },
    "Ocean": {
        "primary": "#0077b6",
        "secondary": "#90e0ef",
        "success": "#2a9d8f",
        "danger": "#e63946",
        "warning": "#f4a261",
        "info": "#48cae4",
        "bg_primary": "#caf0f8",
        "bg_secondary": "#ade8f4",
    },
}


# ============================================================================
# Utility Functions
# ============================================================================


def get_repo_root() -> Path:
    """Find the repository root (contains pyproject.toml)."""
    current = Path(__file__).parent.resolve()
    while current != current.parent:
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent
    return Path.cwd()


@_cache_data(ttl=60)
def load_ledger() -> Any:
    """Load the return log ledger as a DataFrame."""
    if pd is None:
        raise ImportError("pandas not installed. Run: pip install umcp[viz]")

    repo_root = get_repo_root()
    ledger_path = repo_root / "ledger" / "return_log.csv"

    if not ledger_path.exists():
        return pd.DataFrame()

    df = pd.read_csv(ledger_path)

    # Ensure tau_R stays as string column — INF_REC is a typed sentinel
    # that cannot be coerced to int64 by PyArrow serialization.
    # Uses canonical tau_R_display for consistent formatting.
    if "tau_R" in df.columns:
        try:
            from .measurement_engine import tau_R_display
        except ImportError:
            from umcp.measurement_engine import tau_R_display  # type: ignore[no-redef]

        df["tau_R"] = df["tau_R"].apply(tau_R_display)

    # Parse timestamp
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"])

    return df


@_cache_data(ttl=60)
def load_casepacks() -> list[dict[str, Any]]:
    """Load casepack information with extended metadata."""
    repo_root = get_repo_root()
    casepacks_dir = repo_root / "casepacks"

    if not casepacks_dir.exists():
        return []

    casepacks: list[dict[str, Any]] = []
    for casepack_dir in sorted(casepacks_dir.iterdir()):
        if not casepack_dir.is_dir():
            continue

        manifest_path = casepack_dir / "manifest.json"
        if not manifest_path.exists():
            manifest_path = casepack_dir / "manifest.yaml"

        casepack_info: dict[str, Any] = {
            "id": casepack_dir.name,
            "path": str(casepack_dir),
            "version": "unknown",
            "description": None,
            "contract": None,
            "closures_count": 0,
            "test_vectors": 0,
            "files_count": 0,
        }

        # Count files
        casepack_info["files_count"] = len(list(casepack_dir.rglob("*")))

        # Count closures
        closures_dir = casepack_dir / "closures"
        if closures_dir.exists():
            casepack_info["closures_count"] = len(list(closures_dir.glob("*.py")))

        # Count test vectors
        test_file = casepack_dir / "test_vectors.csv"
        if not test_file.exists():
            test_file = casepack_dir / "raw_measurements.csv"
        if test_file.exists():
            with open(test_file) as f:
                casepack_info["test_vectors"] = max(0, sum(1 for _ in f) - 1)

        # Load manifest
        if manifest_path.exists():
            try:
                if manifest_path.suffix == ".json":
                    with open(manifest_path) as f:
                        manifest = json.load(f)
                else:
                    import yaml

                    with open(manifest_path) as f:
                        manifest = yaml.safe_load(f)

                if manifest and "casepack" in manifest:
                    cp = manifest["casepack"]
                    casepack_info["id"] = cp.get("id", casepack_dir.name)
                    casepack_info["version"] = cp.get("version", "unknown")
                    casepack_info["description"] = cp.get("description")
                    casepack_info["title"] = cp.get("title")
                if manifest and "refs" in manifest:
                    refs = manifest["refs"]
                    if "contract" in refs:
                        casepack_info["contract"] = refs["contract"].get("id")
            except Exception:
                pass

        casepacks.append(casepack_info)

    return casepacks


@_cache_data(ttl=60)
def load_contracts() -> list[dict[str, Any]]:
    """Load contract information with extended metadata."""
    repo_root = get_repo_root()
    contracts_dir = repo_root / "contracts"

    if not contracts_dir.exists():
        return []

    contracts: list[dict[str, Any]] = []
    for contract_path in sorted(contracts_dir.glob("*.yaml")):
        filename = contract_path.stem
        parts = filename.split(".")
        domain = parts[0] if parts else "unknown"
        version = parts[-1] if len(parts) > 1 and parts[-1].startswith("v") else "v1"

        # Get file size
        size_bytes = contract_path.stat().st_size

        contracts.append(
            {
                "id": filename,
                "domain": domain,
                "version": version,
                "path": str(contract_path),
                "size_bytes": size_bytes,
            }
        )

    return contracts


@_cache_data(ttl=60)
def load_closures() -> list[dict[str, Any]]:
    """Load closure information."""
    repo_root = get_repo_root()
    closures_dir = repo_root / "closures"

    if not closures_dir.exists():
        return []

    closures: list[dict[str, Any]] = []

    def _infer_domain(path: Path) -> str:
        """Infer domain from file name or parent directory name."""
        # Check parent directory name first (e.g., closures/gcd/, closures/rcft/)
        rel = path.relative_to(closures_dir)
        parts_lower = [p.lower() for p in rel.parts]
        combined = " ".join(parts_lower)
        if "gcd" in combined or "curvature" in combined or "gamma" in combined:
            return "GCD"
        if "kin" in combined:
            return "KIN"
        if "rcft" in combined:
            return "RCFT"
        if "weyl" in combined:
            return "WEYL"
        if "security" in combined:
            return "SECURITY"
        if "astro" in combined:
            return "ASTRO"
        if "nuclear" in combined or "nuc" in combined:
            return "NUC"
        if "quantum" in combined or "qm" in combined:
            return "QM"
        if "finance" in combined or "fin" in combined:
            return "FIN"
        if "evolution" in combined or "brain" in combined or "evo" in combined:
            return "EVO"
        if "everyday" in combined:
            return "EVERYDAY"
        if "material" in combined:
            return "MAT"
        if "standard_model" in combined or "sm" in combined:
            return "SM"
        if "atomic" in combined:
            return "ATOM"
        return "unknown"

    # Python closures (recursive)
    for closure_path in sorted(closures_dir.rglob("*.py")):
        if closure_path.name.startswith("_"):
            continue

        name = closure_path.stem
        size_bytes = closure_path.stat().st_size
        domain = _infer_domain(closure_path)

        # Count lines
        with open(closure_path) as f:
            lines = len(f.readlines())

        closures.append(
            {
                "name": name,
                "domain": domain,
                "path": str(closure_path),
                "type": "python",
                "size_bytes": size_bytes,
                "lines": lines,
            }
        )

    # YAML closures (recursive)
    for closure_path in sorted(closures_dir.rglob("*.yaml")):
        if closure_path.name == "registry.yaml":
            continue

        name = closure_path.stem
        size_bytes = closure_path.stat().st_size
        domain = _infer_domain(closure_path)

        closures.append(
            {
                "name": name,
                "domain": domain,
                "path": str(closure_path),
                "type": "yaml",
                "size_bytes": size_bytes,
                "lines": 0,
            }
        )

    return closures


def classify_regime(omega: float, seam_residual: float = 0.0) -> str:
    """
    Classify the computational regime based on kernel invariants.

    Regimes (from KERNEL_SPECIFICATION.md):
      - STABLE: ω ∈ [0.3, 0.7], |s| ≤ 0.005
      - WATCH: ω ∈ [0.1, 0.3) ∪ (0.7, 0.9], |s| ≤ 0.01
      - COLLAPSE: ω < 0.1 or ω > 0.9
      - CRITICAL: |s| > 0.01
    """
    if abs(seam_residual) > 0.01:
        return "CRITICAL"
    if omega < 0.1 or omega > 0.9:
        return "COLLAPSE"
    if 0.3 <= omega <= 0.7:
        return "STABLE"
    return "WATCH"


def get_regime_color(regime: str) -> str:
    """Get color for regime visualization."""
    return REGIME_COLORS.get(regime, "#6c757d")


def format_bytes(size: int) -> str:
    """Format bytes to human readable string."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size //= 1024
    return f"{size:.1f} TB"


def get_trend_indicator(current: float, previous: float, invert: bool = False) -> str:
    """Get trend arrow indicator."""
    threshold = 1.01
    if current > previous * threshold:
        return "📉" if invert else "📈"
    elif current < previous / threshold:
        return "📈" if invert else "📉"
    return "➡️"


def detect_anomalies(series: Any, threshold: float = 2.5) -> Any:
    """Detect anomalies using z-score method."""
    if pd is None or np is None:
        return []
    mean = series.mean()
    std = series.std()
    if std == 0:
        return pd.Series([False] * len(series), index=series.index)
    z_scores = (series - mean) / std
    return abs(z_scores) > threshold


# ============================================================================
# Shared UI Helpers — Professional Polish
# ============================================================================

# Custom CSS injected once via inject_custom_css()
_CUSTOM_CSS = """
<style>
/* ══════════════════════════════════════════════════════════════════
   UMCP Dashboard — Professional Theme
   Generative Collapse Dynamics · 45 pages · 15 domains
   ══════════════════════════════════════════════════════════════════ */

/* ── Global typography and spacing ────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

section[data-testid="stSidebar"] > div:first-child {
    padding-top: 0.5rem;
}

/* Main content area */
.main .block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

.stMetric label {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #6b7280 !important;
}
.stMetric [data-testid="stMetricValue"] {
    font-size: 1.4rem !important;
    font-weight: 700 !important;
}

/* ── Section cards with glass-morphism ────────────────────────── */
div[data-testid="stExpander"] {
    border: 1px solid rgba(128, 128, 128, 0.12);
    border-radius: 10px;
    backdrop-filter: blur(10px);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
div[data-testid="stExpander"]:hover {
    border-color: rgba(99, 102, 241, 0.25);
    box-shadow: 0 2px 12px rgba(99, 102, 241, 0.06);
}

/* ── Tab styling ──────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    border-bottom: 2px solid rgba(128, 128, 128, 0.1);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px 6px 0 0;
    padding: 8px 16px;
    font-weight: 500;
    font-size: 0.88rem;
}
.stTabs [aria-selected="true"] {
    border-bottom: 2px solid #6366f1 !important;
}

/* ── Compact mode adjustments ─────────────────────────────────── */
.compact .stMarkdown p { margin-bottom: 0.3rem; }
.compact .stMetric { padding: 0.3rem 0; }

/* ── Regime badge pills ───────────────────────────────────────── */
.regime-badge {
    display: inline-block;
    padding: 3px 14px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    color: white;
    letter-spacing: 0.03em;
    text-shadow: 0 1px 2px rgba(0,0,0,0.15);
}
.regime-stable  { background: linear-gradient(135deg, #22c55e, #16a34a); }
.regime-watch   { background: linear-gradient(135deg, #f59e0b, #d97706); color: #1a1a2e; text-shadow: none; }
.regime-collapse { background: linear-gradient(135deg, #ef4444, #dc2626); }
.regime-critical { background: linear-gradient(135deg, #8b5cf6, #7c3aed); }

/* ── Status badges ────────────────────────────────────────────── */
.status-conformant    { color: #16a34a; font-weight: 600; }
.status-nonconformant { color: #dc2626; font-weight: 600; }
.status-non-evaluable { color: #6b7280; font-weight: 600; }

/* ── Metric highlight cards ───────────────────────────────────── */
.metric-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.06) 0%, rgba(99,102,241,0.02) 100%);
    border: 1px solid rgba(99,102,241,0.12);
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.metric-card:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(99,102,241,0.1);
}
.metric-card h4 {
    margin: 0 0 4px 0;
    font-size: 0.82rem;
    color: #6b7280;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}
.metric-card .value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #1e1b4b;
}

/* ── Kernel metric cards row ──────────────────────────────────── */
.kernel-metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 10px;
    margin: 12px 0;
}
.kernel-metric {
    background: linear-gradient(135deg, rgba(15,23,42,0.04) 0%, rgba(15,23,42,0.01) 100%);
    border: 1px solid rgba(15,23,42,0.08);
    border-radius: 10px;
    padding: 12px 14px;
    text-align: center;
}
.kernel-metric .symbol {
    font-size: 1.1rem;
    font-weight: 700;
    color: #6366f1;
    font-family: 'JetBrains Mono', monospace;
}
.kernel-metric .val {
    font-size: 1.3rem;
    font-weight: 700;
    color: #1e1b4b;
    margin: 4px 0 2px 0;
}
.kernel-metric .label {
    font-size: 0.72rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Info panels ──────────────────────────────────────────────── */
.info-panel {
    background: linear-gradient(135deg, rgba(6,182,212,0.06) 0%, rgba(6,182,212,0.02) 100%);
    border-left: 3px solid #06b6d4;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin: 10px 0;
    font-size: 0.9rem;
    line-height: 1.5;
}

/* ── Domain page headers ──────────────────────────────────────── */
.domain-header {
    background: linear-gradient(135deg, rgba(99,102,241,0.08) 0%, rgba(168,85,247,0.04) 100%);
    border: 1px solid rgba(99,102,241,0.12);
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 20px;
}
.domain-header h2 {
    margin: 0 0 4px 0;
    font-weight: 700;
}
.domain-header .subtitle {
    color: #6b7280;
    font-size: 0.9rem;
}

/* ── Navigation category headers ──────────────────────────────── */
.nav-category {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #9ca3af;
    margin: 14px 0 6px 0;
    padding: 0;
}

/* ── Sidebar branding ─────────────────────────────────────────── */
.sidebar-brand {
    text-align: center;
    padding: 8px 0 12px 0;
    border-bottom: 1px solid rgba(128,128,128,0.1);
    margin-bottom: 8px;
}
.sidebar-brand .title {
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.sidebar-brand .version {
    font-size: 0.72rem;
    color: #9ca3af;
    margin-top: 2px;
    letter-spacing: 0.02em;
}

/* ── Theorem proof badges ─────────────────────────────────────── */
.proof-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 2px 10px;
    border-radius: 16px;
    font-size: 0.75rem;
    font-weight: 600;
}
.proof-proven {
    background: rgba(34,197,94,0.12);
    color: #16a34a;
    border: 1px solid rgba(34,197,94,0.2);
}
.proof-failed {
    background: rgba(239,68,68,0.12);
    color: #dc2626;
    border: 1px solid rgba(239,68,68,0.2);
}

/* ── Data tables ──────────────────────────────────────────────── */
.stDataFrame {
    border-radius: 8px;
    overflow: hidden;
}

/* ── Code blocks ──────────────────────────────────────────────── */
.stCodeBlock {
    border-radius: 8px;
}

/* ── Button improvements ──────────────────────────────────────── */
.stButton > button {
    border-radius: 8px;
    font-weight: 500;
    transition: all 0.15s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* ── Scrollbar styling ────────────────────────────────────────── */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: rgba(128,128,128,0.2);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(128,128,128,0.35);
}
</style>
"""

_CSS_INJECTED = False


def inject_custom_css() -> None:
    """Inject shared CSS styles once per Streamlit session.

    Call this at the top of ``main()`` after ``st.set_page_config()``.
    Idempotent — safe to call from any page.
    """
    global _CSS_INJECTED
    if _CSS_INJECTED or st is None:
        return
    st.markdown(_CUSTOM_CSS, unsafe_allow_html=True)
    _CSS_INJECTED = True


def page_header(
    title: str,
    icon: str,
    subtitle: str,
    *,
    contract: str | None = None,
    tier: str = "Tier-2",
) -> None:
    """Render a consistent page header with icon, subtitle, and tier badge.

    Parameters
    ----------
    title : str
        Page title (no emoji prefix — ``icon`` supplies it).
    icon : str
        Single emoji for the page.
    subtitle : str
        One-line description shown as caption below the title.
    contract : str, optional
        Contract reference (e.g. ``"EVO.INTSTACK.v1"``).
    tier : str
        Tier label, default ``"Tier-2"``.
    """
    if st is None:
        return
    st.title(f"{icon} {title}")
    parts = [subtitle]
    if contract:
        parts.append(f"Contract: {contract}")
    parts.append(tier)
    st.caption(" | ".join(parts))


def section_divider(label: str | None = None) -> None:
    """Render a labeled section divider."""
    if st is None:
        return
    if label:
        st.markdown(
            f'<p class="nav-category">{label}</p>',
            unsafe_allow_html=True,
        )
    st.divider()


def regime_badge(regime: str) -> str:
    """Return HTML for an inline regime badge pill.

    Usage::

        st.markdown(regime_badge("Stable"), unsafe_allow_html=True)
    """
    cls = f"regime-{regime.lower()}"
    return f'<span class="regime-badge {cls}">{regime}</span>'


def metric_row(metrics: list[tuple[str, str | float, str | None]]) -> None:
    """Render a row of metrics in equal columns.

    Parameters
    ----------
    metrics : list of (label, value, delta_or_none) tuples
    """
    if st is None:
        return
    cols = st.columns(len(metrics))
    for col, (label, value, delta) in zip(cols, metrics, strict=False):
        with col:
            st.metric(label, value, delta=delta)


# ── Shared chart layout defaults ─────────────────────────────────────────────

CHART_MARGINS_COMPACT: dict[str, int] = {"t": 10, "b": 30, "l": 40, "r": 10}
CHART_MARGINS_NORMAL: dict[str, int] = {"t": 30, "b": 40, "l": 50, "r": 20}
CHART_HEIGHT_SM = 280
CHART_HEIGHT_MD = 380
CHART_HEIGHT_LG = 500


def apply_chart_style(fig: Any, *, height: int = CHART_HEIGHT_MD, compact: bool = False) -> Any:
    """Apply consistent layout defaults to a Plotly figure.

    Parameters
    ----------
    fig : plotly Figure
        The figure to style.
    height : int
        Chart height in pixels (default: 380).
    compact : bool
        If True, use tighter margins.

    Returns
    -------
    The figure (for chaining).
    """
    margins = CHART_MARGINS_COMPACT if compact else CHART_MARGINS_NORMAL
    fig.update_layout(
        height=height,
        margin=margins,
        font={"family": "Inter, system-ui, sans-serif", "size": 12},
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        hoverlabel={"font_size": 12},
    )
    return fig


# Navigation category definitions for grouped sidebar
NAV_CATEGORIES: dict[str, list[str]] = {
    "Core": [
        "Overview",
        "Domain Overview",
        "Health",
        "Ledger",
        "Metrics",
    ],
    "Science Domains": [
        "Cosmology",
        "Astronomy",
        "Nuclear",
        "Quantum",
        "Atomic Physics",
        "Standard Model",
        "Materials Science",
        "Finance",
        "RCFT",
        "Security",
        "Everyday Physics",
    ],
    "Evolution & Cognition": [
        "Evolution Kernel",
        "Brain Kernel",
        "Awareness Manifold",
        "Cognitive Traversal",
    ],
    "Analysis": [
        "Regime",
        "Time Series",
        "Comparison",
        "Formula Builder",
        "Precision",
    ],
    "Exploration": [
        "Canon Explorer",
        "Geometry",
        "Rosetta Translation",
        "Orientation Protocol",
        "Physics",
        "Kinematics",
    ],
    "Tools": [
        "Casepacks",
        "Contracts",
        "Closures",
        "Closure Explorer",
        "Live Runner",
        "Batch Validation",
        "Test Templates",
        "Work Templates",
    ],
    "Diagnostics": [
        "τ_R* Diagnostic",
        "Epistemic",
        "Insights",
    ],
    "Manage": [
        "Exports",
        "Bookmarks",
        "Notifications",
        "API Integration",
    ],
}

# Category icons for sidebar
NAV_CATEGORY_ICONS: dict[str, str] = {
    "Core": "🏠",
    "Science Domains": "🔬",
    "Evolution & Cognition": "🧬",
    "Analysis": "📊",
    "Exploration": "🧭",
    "Tools": "🛠️",
    "Diagnostics": "🩺",
    "Manage": "⚙️",
}


# ============================================================================
# Dashboard Pages
# ============================================================================
