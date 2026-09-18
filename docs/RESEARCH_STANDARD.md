# Research standard

These are maintainer conventions, not an extra file required to install any one skill. Each skill carries its essential contract and domain source map locally.

## Coverage and search depth

Respect the user's market, universe and time window. Default to a declared US-listed common-stock/ADR universe only when none is supplied. ETFs can be data vehicles in sector work; do not accidentally count them as operating-stock candidates. Separate preferreds, warrants, SPAC shells and private companies.

Use the relevant available official data, company documents, free screeners, accessible forecast sites, news and social channels. Broaden searches by issuer/legal name, identifiers, event terminology, local language and source family. Search counterarguments. Discovery from one convenient screener is not an exhaustive universe review. For a large universe, process available datasets in batches and maintain discovered/reviewed/verified/rejected/unreviewed counts. A bounded web scan is acceptable when described as such.

Stop when the requested scope has adequate evidence, or when additional available source families no longer resolve material gaps. Report gaps and the routes attempted. Do not declare that all websites were searched. Never confuse blocked access with zero matches. Do not bypass access restrictions, invent credentials, subscribe to paid services or make a free trial mandatory.

## Evidence ledger

For every material number or claim retain issuer/identifier, source URL, original publisher, publication or filing time, underlying event/observation date, retrieval time, fiscal period, units/currency and accounting or data basis. Record the access posture: original read, accessible secondary report, user-supplied extract, or unverified lead. A search snippet is not a read filing.

Classify evidence as reported actual, disclosed transaction/holding, company guidance, dated consensus, individual analyst estimate, attributed third-party claim, derived estimate or model scenario. A computed number retains the provenance of its inputs; it is not an independent source. Multiple sites redistributing one vendor or wire do not provide independent confirmation.

## Normalize before inferring

Reconcile filings/amendments, restatements, fiscal calendars, units, share classes, ADRs, corporate actions and adjusted versus reported metrics. Match observation windows. Avoid historical look-ahead by using information available at the test date. Distinguish EPS weighted-average shares from current/future valuation shares and enterprise value from common equity.

Keep stale observations dated. A late holding disclosure is not a current trade; an old social story reposted today is not a new corporate event. Never infer precise transaction values from reported ranges or fill absent data with zero.

## Output and decisions

Start with the answer supported by evidence and describe what was actually reviewed. Use compact source-linked tables and short finalist notes. Report confidence based on evidence quality and explain the strongest alternative explanation. Separate research candidates, incomplete watchlist entries and rejected false positives. No match is a valid outcome.

Financial arithmetic, hypothetical upside and qualitative confidence are not promises of returns. Justify assumptions and show adverse scenarios when valuation matters. If execution details are requested, distinguish a research case from current broker-dependent feasibility.

## Data routes and maintenance

SEC public API documentation is at https://www.sec.gov/search-filings/edgar-application-programming-interfaces . Public data endpoints do not require a paid SEC-branded vendor. Use actual configured contact identity and current fair-access rules for programmatic access, with caching/backoff and bulk files where useful. Use ordinary accessible page retrieval/issuer IR when downloads are blocked. A source map is a maintained set of starting points, not a claim that every page is live or fully free.

Source links were selected during the September 2026 repository restructuring. Primary methodology references and the DSA design were read; many discovery-site entries are prospective routes whose live coverage must be checked at execution time. The checked-in examples are not live investment research.
