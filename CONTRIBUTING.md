# Contributing

Contribute a focused, independently usable workflow for stock discovery or company research. Keep the distinction between facts, assumptions, calculations and judgment clear.

## Add or change a skill

1. Create `skills/<lowercase-hyphenated-name>/SKILL.md` with YAML `name` and a concise, discriminating `description`. Match the directory name. Avoid triggering on unrelated financial tasks.
2. Write an actionable workflow with sensible, disclosed defaults and precise evidence requirements. Keep the entry point concise and put conditional detail in local `references/` files.
3. Add a detailed `README.md` explaining inputs, outputs, free-source routes, limitations, standalone usage and realistic prompts. Include a clearly labeled worked or synthetic example. English instructions with multilingual prompt examples are welcome; research outputs should follow the user's language.
4. Add `agents/openai.yaml` with quoted display name, 25–64-character short description and a default prompt mentioning `$<skill-name>`. Keep normal implicit discovery enabled unless explicitly intended otherwise.
5. Give source URLs and retrieval strategies, explain delays/access limits, and distinguish discovery aggregators from original documents. Do not claim to have checked a source you could not read.
6. Keep every required file inside the skill folder. Other skills may provide optional support, but document a standalone fallback; do not hardcode a user's installed plugin paths.
7. Add deterministic scripts only for calculations/data handling that benefit from reuse. Keep calculators offline and standard-library-only unless a documented need justifies a dependency. No API keys, personal data, broker exports or credentials in examples.
8. Add the skill to the main catalog and update any affected migration/source documentation. Preserve original provenance and existing user changes.

## Research quality

Follow [RESEARCH_STANDARD.md](docs/RESEARCH_STANDARD.md). In particular:

- Compare like fiscal periods, accounting bases, currencies, share classes and observation windows.
- Carry publication/filing dates and observation dates separately.
- Label unavailable data unknown; return a smaller verified set instead of inventing a match.
- Use declared universe coverage, not an unexplained sample presented as a market-wide scan.
- Justify valuation multiples and report dilution-aware returns. Do not replace missing consensus with unlabeled extrapolation.
- Interpret 13F, Form 4, option volume/OI, fund flows and short interest according to their actual definitions.
- Attribute allegations, public-official disclosures and social claims accurately; seek primary support and counterevidence.
- The workflows are research-only. A skill does not confer authority to trade, buy data, send messages or schedule monitoring.

## Validation

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests -v
```

The format check validates YAML/name/metadata, local links and isolation of required SKILL references. It does not prove research quality. For meaningful code changes, test observable financial invariants, missing inputs and invalid data; do not merely assert that a heading or phrase exists.

For complex workflow changes, try realistic tasks with raw evidence and examine whether the skill reaches appropriately qualified conclusions. Keep synthetic data visibly synthetic and offline. Do not give an evaluator the intended answer as part of the input.

When submitting a change, describe the research problem, resulting behavior, source assumptions and validation. Do not claim that structure checks or synthetic tests establish live-data coverage or profitable returns.
