# Contributing

Thank you for considering a contribution.

## Before opening an issue

- Search existing issues to avoid duplicates.
- Include the script name, Python version and operating system.
- Provide minimal reproducible steps and expected versus actual behaviour.
- Remove API keys, personal information and account identifiers from logs.

## Pull requests

1. Create a focused branch from `main`.
2. Keep changes small and explain the motivation.
3. Update documentation when behaviour or setup changes.
4. Add tests for new calculations and bug fixes.
5. Run the syntax check before submitting:

   ```bash
   python -m compileall -q .
   ```

6. Describe any external data sources, assumptions and limitations.

## Financial-data and strategy changes

- Do not describe a heuristic score as a probability of profit.
- Keep simulated and live data clearly distinguished.
- Include timestamps, units and source assumptions for market data.
- Never include credentials, broker tokens or private user data.
- Do not introduce live order execution without explicit risk controls, tests and documentation.

By submitting a contribution, you agree that it may be reviewed and discussed publicly in this repository.
