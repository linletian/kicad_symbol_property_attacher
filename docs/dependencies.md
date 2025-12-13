# Dependencies

Primary runtime:
- `click==8.1.*` — CLI framework
- `sexpdata==0.0.3` — S-expression parsing

Dev tooling:
- `pytest==8.*`, `pytest-cov==5.*` — testing
- `ruff==0.6.*`, `black==24.*` — lint/format
- `mypy==1.11.*` — typing checks

Policy:
- Prefer LTS/stable versions; pin ranges as specified
- Monitor advisories; patch vulnerable dependencies promptly
- Use lock/pinning strategy (pip, uv, pip-tools) for reproducibility
