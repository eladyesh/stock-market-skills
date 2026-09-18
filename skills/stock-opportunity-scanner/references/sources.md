# Free public sources

Use these starting points, checked in September 2026; confirm live access and dates per run. Capture value, units/currency, period/as-of, accounting basis, source URL and publication/filing date. Computed metrics must retain links to their inputs. Never cite an unread search snippet as a read document.

Prioritize original filings, issuer IR/prospectuses, exchange announcements and official fund reports. Use identifiable public prices with exchange/currency/timestamp. Secondary screeners and articles are discovery aids; verify material claims at the source.

## SEC fundamentals

- API documentation: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- Search: https://www.sec.gov/edgar/search/
- History: `https://data.sec.gov/submissions/CIK##########.json`
- Facts: `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json`
- Bulk facts: `https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip`
- Bulk histories: `https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip`
- Fair access: https://www.sec.gov/about/developer-resources

Official SEC APIs require no API key or subscription; commercial services with SEC in their name are separate. For large universes use cached bulk snapshots and incremental updates, current access limits and a real configured contact identity. Do not invent an email to enable downloads.

CompanyFacts is not a ready-clean dataset with prices, consensus, all custom KPIs or all segment data. Align duration/instant contexts, units, calendars, restatements, forms and accession numbers. Historical tests must use only facts available as of the test date; latest-restated data introduces look-ahead risk.

Find the needed actual documents: 10-K/10-Q/20-F/6-K, 8-K exhibits, S-1/F-1, 424B4/424B5, DEF 14A, 13F-HR/amendments, SC 13D/G and Form 4/4-A. Filing metadata alone does not verify contents.

## Optional tooling

- EdgarTools library: https://github.com/dgunning/edgartools
- Documentation: https://edgartools.readthedocs.io/
- yfinance documentation: https://ranaroussi.github.io/yfinance/

Use existing EdgarTools if available and inspect current APIs before coding. The free self-run library and hosted service are separate. Its MCP/Claude skills are not automatically installed in ChatGPT by this skill.

yfinance is unofficial and subject to Yahoo terms and availability. It is optional. Record split/total-return adjustment for history; use the actual quote and matched share/ADR basis for current valuation. Without historical prices do not claim a verified event return.

## Ownership

- 13F FAQ: https://www.sec.gov/rules-regulations/staff-guidance/division-investment-management-frequently-asked-questions/frequently-asked-questions-about-form-13f
- Insider bulletin: https://www.sec.gov/files/forms-3-4-5.pdf

Determine value units from filing/schema/date: modern 13F dollar values differ from older thousands-of-dollars formatting. Never multiply all filings by 1,000. Reconcile amendments and manager relationships. Use the original dated manager letter if citing one.

## International

- UK FCA National Storage Mechanism: https://www.fca.org.uk/markets/primary-markets/regulatory-disclosures/national-storage-mechanism
- HKEX announcements: https://www1.hkexnews.hk/search/titlesearch.xhtml?lang=en
- Israel: discover current official MAGNA/MAYA filings and issuer IR for the named security.
- Elsewhere: find the official local issuer/director/substantial-holder disclosure system and check the applicable coverage.

13F can cover a foreign manager's reportable securities, not its complete global book. Local substantial-holder reports are not a uniform global quarterly portfolio feed. State the named managers/markets covered and missing portions; never promise exhaustive worldwide purchases.

## Web-only fallback

Build a bounded lead list by mode and date; open original filings/results and extract a small normalized table for finalists. Run the math helper on those sourced values. This is a focused research scan, not an exhaustive numeric screen of thousands of issuers. Do not require signups/packages/API keys, bypass paywalls, or substitute old/unrelated data for missing fields. Ask for a source only when indispensable to the requested comparison.
