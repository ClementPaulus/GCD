"""
UMCP Authentication & Role-Based Access Control

Two roles govern the API:
  - **public**: Read all data, compute kernels, run closures, translate via
    Rosetta — everything that does NOT mutate server-side state.  No API key
    required.
  - **admin**: All public access PLUS state-mutating operations (seam reset,
    integrity updates, future write endpoints).  Requires the admin key set
    via UMCP_ADMIN_KEY (env) or the legacy UMCP_API_KEY.

Design:
  Public endpoints call ``require_public`` (no-op — always succeeds).
  Admin endpoints call ``require_admin`` (checks the X-API-Key header).
  Dev mode (UMCP_DEV_MODE=1) promotes every caller to admin.

The module is the single source of truth imported by both api_umcp.py and
api_routes_v2.py, eliminating the previous auth duplication.
"""

from __future__ import annotations

import hmac
import os

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

# ── Configuration (read once at import time) ──
ADMIN_KEY: str = os.environ.get(
    "UMCP_ADMIN_KEY",
    os.environ.get("UMCP_API_KEY", "umcp-dev-key"),
)
DEV_MODE: bool = os.environ.get("UMCP_DEV_MODE", "0").lower() in (
    "1",
    "true",
    "yes",
)

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


# ── Dependency functions (used as FastAPI Security dependencies) ──


def require_public(
    api_key: str | None = Security(_api_key_header),
) -> str:
    """Allow any caller — no credentials needed.

    Returns the provided key (or "public") for logging purposes.
    """
    return api_key or "public"


def require_admin(
    api_key: str | None = Security(_api_key_header),
) -> str:
    """Require a valid admin key.

    In dev mode every caller is promoted to admin.
    Uses constant-time comparison to prevent timing attacks.
    """
    if DEV_MODE:
        return "dev-mode-admin"
    if not api_key or not hmac.compare_digest(api_key, ADMIN_KEY):
        raise HTTPException(
            status_code=401,
            detail="Admin API key required for this operation",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return api_key
