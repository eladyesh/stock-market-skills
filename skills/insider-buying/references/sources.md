# Sources and retrieval — insider buying

Use original disclosures to qualify transactions; aggregators discover them. Recheck access and current reporting rules for each jurisdiction and run.

| Source | Free use | What it establishes / limits |
| --- | --- | --- |
| [SEC EDGAR search](https://www.sec.gov/edgar/search/) | Public filings | Form 4/4-A tables, acquisition codes and footnotes; Form 3 is initial ownership |
| [SEC insider bulletin](https://www.sec.gov/files/forms-3-4-5.pdf) | Public guide | Code meanings and basic reporting structure; verify newer rules when relevant |
| [SEC data APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) | Public, no API key | Filing discovery; retrieve ownership XML/HTML from the accession, not CompanyFacts for transactions |
| [OpenInsider](http://openinsider.com/) | Public screener pages where accessible | Purchase/cluster leads; verify original filings |
| [Finviz insider activity](https://finviz.com/insidertrading.ashx) | Public page, limited filters | Discovery, not complete or guaranteed live coverage |
| [Nasdaq](https://www.nasdaq.com/) and issuer IR | Public pages | Cross-check identity and company developments |
| [UK FCA NSM](https://www.fca.org.uk/markets/primary-markets/regulatory-disclosures/national-storage-mechanism) / issuer RNS | Public disclosures | PDMR/director transactions under local rules |
| [HKEXnews](https://www.hkexnews.hk/) | Public disclosure-of-interests and announcements | Hong Kong ownership and director disclosures |
| [MAYA](https://maya.tase.co.il/) / [MAGNA](https://www.magna.isa.gov.il/) | Public Israeli issuer reports | בעלי עניין, changes in holdings, placements; identify the actual transaction |

Search examples: `"<ticker>" "Form 4" purchase`, `"<issuer>" "director dealing"`, `"<issuer>" "10b5-1" purchase`, `"<issuer>" רכישת מניות בעל עניין`. Pair queries with the requested dates, then inspect both favorable and adverse results.

SEC submissions: `https://data.sec.gov/submissions/CIK##########.json`; use ten-digit CIKs. Follow the additional history files when the recent array is insufficient. Use an actual configured contact identity and the SEC's current fair-access limits for downloads, with caching and backoff. Do not invent an email. Browser/page retrieval and IR are valid alternatives when API access fails.

Common Form 4 timing is two business days, but report the actual filing date rather than assuming timely compliance. Foreign issuer coverage can differ. No filing found is not proof of no purchases. 13F is a portfolio-holdings report and is not a substitute for Form 4.
