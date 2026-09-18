# Contributing

Keep skills useful as standalone research workflows and maintain clear boundaries between sourced facts, calculations, and judgment.

## Add a skill

1. Create a folder under `skills/` using a short lowercase, hyphenated name.
2. Add `SKILL.md` with YAML `name` and `description` fields, followed by focused instructions.
3. Put conditional research detail in `references/` and deterministic reusable code in `scripts/`.
4. Add optional `agents/openai.yaml` metadata appropriate to the supported host.
5. Add clearly labeled synthetic examples and meaningful checks for executable calculations.
6. Update the main README's catalog and usage instructions.

Keep the repository, skill instructions, UI metadata, and examples in English. A skill may follow an explicit request to produce research in another language.

## Research standards

- Preserve primary-source links, accounting basis, fiscal periods, units, and publication dates.
- Label original analysis and modeled forecasts separately from actual results, guidance, and consensus.
- Report the universe actually reviewed and any access failures or missing data.
- Keep free public-source access as the scanner's default. Document optional dependencies and their limitations.
- Respect source access rules; do not add paywall bypasses or repeated blocked requests.
- Do not include personal watchlists, broker exports, authentication tokens, or private research in example files.
- Avoid universal valuation filters across unrelated sectors.
- Treat corporate actions, amendments, dilution, and per-share denominators explicitly.

## Code and validation

The existing helper uses the Python standard library. Preserve its ability to run without installing packages unless a change has a clear justification and updated setup instructions.

Run:

```bash
python3 -m unittest discover -s tests -v
```

For meaningful changes, include a realistic input that exercises the financial behavior. Test invariants and failure cases rather than duplicating the implementation line by line. Do not add live web calls or paid data dependencies to the offline test suite.

When publishing changes, explain the problem, the resulting behavior, and how it was validated. Avoid claiming that arithmetic tests establish an investment edge.
