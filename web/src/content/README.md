# web/src/content

This directory is populated by the HCG (Headless Contract Gateway) builder:

```bash
python -m umcp.hcg.builder --all --output web/src/content
```

Each subdirectory becomes one autonomous domain site:

```
content/
├── index.md                    # Root network index
├── gcd/index.md               # Generative Collapse Dynamics
├── finance/index.md           # Finance
├── astronomy/index.md         # Astronomy
├── standard_model/index.md    # Standard Model
├── ...                        # 20 domains total
└── <domain>/_data/<domain>.json  # Client-side data
```

Do not edit these files manually — they are regenerated on every build.
The source of truth is the validation ledger + canon anchors + closures.
