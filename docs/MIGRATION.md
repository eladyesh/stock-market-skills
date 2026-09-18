# Migration from stock-opportunity-scanner

The all-in-one skill has been replaced in the active `skills/` catalog by nine independent skills. The old tree and documentation remain in Git history; no archived SKILL.md is left to be accidentally discovered as a tenth active skill.

| Former mode/capability | Current owner |
| --- | --- |
| insider-buying | insider-buying |
| fund-accumulation | institutional-ownership |
| growth-value / forward valuation | fundamental-valuation |
| earnings-gap | news-sentiment establishes event/reaction; fundamental-valuation checks guidance, cash economics and price |
| moat-bottleneck | emerging-companies and fundamental-valuation; sector-flows maps relevant exposures |
| ipo-emerging | emerging-companies |
| post-dilution | emerging-companies, with valuation follow-through |
| Private startup watchlist | emerging-companies, kept separate from listed securities |
| Supplied-universe and free-source research contract | Embedded in every skill |
| Insider transaction arithmetic | insider-buying/scripts/insiders.py |
| Split-adjusted disclosed-holdings comparison | institutional-ownership/scripts/holdings.py |
| Plain completed common-offering dilution | emerging-companies/scripts/dilution.py |
| General screen/forecast calculator | Replaced by fundamental-valuation/scripts/valuation.py for explicit three-year annual tests and supplied terminal cases; richer financial models remain a documented research task |
| Technical signals | New independent skill and signals.py |
| Options, sector flows, short research, news sentiment | New independent skills |

The three migrated calculators keep their command names (`insiders`, `holdings`, `dilution`) but have new script/example paths. New valuation input is intentionally explicit about per-metric forecast provenance and does not accept the old scenario-growth-array schema. Its scope is P/E arithmetic, not a complete three-statement or book-equity model; the valuation reference explains the additional research/modeling requirements.

No installed personal skill, account configuration or scheduler is changed by this repository migration. To use a new skill in a host, import/copy its full folder through that host's supported workflow.
