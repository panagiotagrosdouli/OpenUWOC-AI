# Engineering Report

## Objective

The engineering objective is to make OpenUWOC-AI reproducible, testable, and maintainable as open-source research software. The project should support deterministic simulation, clear configuration, automated checks, and honest reporting of limitations.

## Implemented Engineering Practices

- Python packaging through `pyproject.toml`.
- Optional development dependencies for formatting, linting, typing, and testing.
- Configuration-driven experiment execution.
- Deterministic seeds for synthetic simulations.
- CI workflow for linting, formatting, typing, and tests.
- Dockerfile for repeatable execution in a controlled environment.

## Expected Engineering Impact

These practices reduce environment drift, make results easier to reproduce, and make future algorithmic changes safer. The Docker and CI additions support external review and enable contributors to validate changes without relying on the original development machine.

## Remaining Risks

- Optional AI dependencies can increase CI runtime and should remain separate from core tests unless GPU/CPU budgets are explicitly defined.
- Generated assets can become large; long videos and datasets should use releases, artifacts, or external data storage rather than bloating Git history.
- Simulation presets should be versioned whenever physical assumptions change.

## Recommended Next Steps

1. Add a small smoke-test experiment that runs under one minute in CI.
2. Add schema validation for experiment YAML files.
3. Add benchmark manifests that explicitly mark missing baselines as `Pending`.
4. Store generated reports under timestamped `results/experiments/<run_id>/` directories.
5. Add pre-commit hooks mirroring the CI checks.
