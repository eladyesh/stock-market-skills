# Sources and retrieval — news and sentiment

| Source | Public route | What it can establish |
| --- | --- | --- |
| Issuer IR / exchange announcements / [SEC EDGAR](https://www.sec.gov/edgar/search/) | Original releases and filings | Official company disclosures, not independent endorsement of every promotional claim |
| Official government, regulator and court sites | Statements, transcripts, awards and decisions | Exact public action/statement and date |
| [White House](https://www.whitehouse.gov/) and original verified speaker accounts | Accessible official transcripts/posts | Context for attributed political statements; verify the actual speaker/account |
| [Reuters](https://www.reuters.com/), [AP](https://apnews.com/), other reputable outlets | Freely readable reporting | Attributed event coverage; gated articles are not verified in full |
| [Google News](https://news.google.com/), [Yahoo Finance](https://finance.yahoo.com/), [Finviz](https://finviz.com/) | Discovery and linked stories | Headlines are leads; open original sources |
| [X](https://x.com/) / [Stocktwits](https://stocktwits.com/) / [Reddit](https://www.reddit.com/) | Accessible public posts/search | Observed discussion, not complete firehose or authenticated identity by appearance alone |
| [GDELT](https://www.gdeltproject.org/) | Public news datasets/tools | Corpus-defined coverage, duplicates, language and entity errors need review |
| Public bank/analyst notes and accessible summaries | Rating, estimate and target changes | Recommendation is not a purchase; verify new versus reiterated |
| User exports of news/social data | Dated corpus with provenance | Can support sample metrics after validation, not automatic population claims |

Queries: `"<company>" <date>`, `"$<ticker>"`, `"<issuer>" guidance cut OR raised`, `"<speaker>" "<company>" transcript`, `"<claim>" correction`, `site:sec.gov "<issuer>" 8-K`. Use original-language searches when important to the named region. Public search access does not imply direct authenticated access to a social platform.

Capture actual URLs and original timestamps; specify timezone before judging recency. When source access fails, use another accessible source and say which part remains unverified. No paid social API or sentiment vendor is required; without comparable corpus coverage, report qualitative observations rather than fabricated trending statistics.
