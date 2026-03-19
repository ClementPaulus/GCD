# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 2.2.x   | :white_check_mark: |
| 2.1.x   | :white_check_mark: |
| < 2.1   | :x:                |

## Reporting a Vulnerability

**Please do not open a public issue for security vulnerabilities.**

Use GitHub's private vulnerability reporting:

1. Go to the repository [Security Advisories](https://github.com/calebpruett927/GENERATIVE-COLLAPSE-DYNAMICS/security/advisories)
2. Click **Report a vulnerability**
3. Provide:
   - Description of the vulnerability
   - Steps to reproduce
   - Affected UMCP version(s)
   - Potential impact assessment

### Response Timeline

| Stage          | Target       |
|----------------|--------------|
| Acknowledgment | 48 hours     |
| Assessment     | 1 week       |
| Fix & release  | 2 weeks      |

Severity determines actual response time. Critical issues (e.g., arbitrary code
execution through contract injection) are treated as emergencies.

## Security Model

UMCP processes user-supplied contracts, closures, and casepacks. The security
boundary is:

- **Trusted**: The kernel (`src/umcp/kernel_optimized.py`), frozen contract
  constants (`src/umcp/frozen_contract.py`), and validation engine.
- **Untrusted**: User-provided YAML contracts, JSON manifests, closure data,
  and any external input to the CLI or API.

### Design Principles

1. **No `eval()` or `exec()`** — User input is never executed as code.
2. **Schema validation first** — All YAML/JSON input is validated against
   JSON Schema Draft 2020-12 before processing.
3. **SHA-256 integrity** — All tracked files are checksummed; tampering is
   detected by `umcp integrity`.
4. **Frozen parameters** — Kernel constants are immutable within a run;
   they cannot be overridden by user input.
5. **Three-valued verdicts** — Ambiguous states produce `NON_EVALUABLE`,
   never silent acceptance.

### Known Attack Surface

| Vector                    | Mitigation                                       |
|---------------------------|--------------------------------------------------|
| Malformed YAML/JSON       | jsonschema validation before any processing      |
| Path traversal in casepacks | Paths resolved relative to casepack root only  |
| Denial of service (large input) | Configurable limits on trace vector size    |
| Dependency vulnerabilities | Dependabot monitors all ecosystems weekly        |
| API injection (FastAPI)   | Pydantic model validation on all endpoints       |

### For Contributors

Before submitting code:

- [ ] No hardcoded secrets or credentials
- [ ] No `eval()`, `exec()`, `__import__()` on user input
- [ ] All file paths validated and sandboxed
- [ ] New dependencies reviewed for known vulnerabilities
- [ ] SHA-256 integrity updated (`python scripts/update_integrity.py`)
