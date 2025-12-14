# Contributing Guide

Thanks for your interest in contributing! This project welcomes issues and pull requests.

## Workflow
- Fork the repo and create a feature branch (e.g., `feat/xyz` or `fix/abc`).
- Run checks locally: ruff, black, mypy, pytest.
- Write tests for changes; keep PRs focused and well-described.
- Open a PR; link to related issues; follow the template.

## Code Style & Quality
- Python: target `py311`; line length 120.
- Lint/format: `ruff`, `black`.
- Typing: `mypy` with strict-ish defaults.
- Tests: `pytest` + `pytest-cov`; include unit/integration where applicable.

## Commit & PR
- Conventional messages preferred (e.g., `feat:`, `fix:`, `docs:`).
- Include CHANGELOG updates when user-facing.
- Keep PRs small; explain rationale in the description.

## Running Locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev] --no-build-isolation
pytest -q
```

## License and DCO
- By contributing, you agree your contributions are licensed under the project license (GPL-3.0).
- Optionally include a Developer Certificate of Origin (DCO) sign-off: `Signed-off-by: Your Name <email>`
