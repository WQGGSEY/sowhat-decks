# Sources: 01 investor update

Illustrative example built from public filings. It is not produced by, affiliated with, or endorsed by Duolingo, Inc., and it is not investment advice.

Every number in `deck.pptx` comes from one of the three documents below, or is derived from them with the formula shown on the slide or in its speaker notes. All retrieved 2026-10-04.

| # | Document | Where | Used for |
|---|---|---|---|
| 1 | Duolingo, Inc., Form 10-K for fiscal year 2025 (filed 2026-02-27, accession 0001628280-26-012494) | https://www.sec.gov/Archives/edgar/data/1562088/000162828026012494/duol-20251231.htm, values read from the SEC XBRL company-facts API: https://data.sec.gov/api/xbrl/companyfacts/CIK0001562088.json | Revenue, gross profit, operating income, net income, operating cash flow, cash (FY2023-FY2025). Extract: `inputs/duolingo_10k_fy2025_xbrl.csv` |
| 2 | Q4 and FY2025 shareholder letter (exhibit to Form 8-K filed 2026-02-26, accession 0001628280-26-012246) | https://www.sec.gov/Archives/edgar/data/1562088/000162828026012246/q4fy25duolingo12-31x25shar.htm | Bookings, adjusted EBITDA and free cash flow (non-GAAP), DAUs, MAUs, paid subscribers (Q4 2025), the one-time tax benefit, 2026 guidance, the foregone-bookings estimate, the gross-margin outlook, the buyback authorization |
| 3 | Q4 and FY2024 shareholder letter (exhibit to Form 8-K, 2025, accession 0001562088-25-000039) | https://www.sec.gov/Archives/edgar/data/1562088/000156208825000039/q4fy24duolingo12-31x24shar.htm | Q4 2024 DAUs, MAUs and paid subscribers and their growth; FY2024 bookings growth |

## Derived figures

| Figure | Formula |
|---|---|
| Revenue growth 41% (FY2024), 39% (FY2025) | 748.0 / 531.1 - 1; 1,037.6 / 748.0 - 1 |
| Operating margin -2.5%, 8.4%, 13.1% | operating income / revenue |
| Gross margin 73.2%, 72.8%, 72.2% | gross profit / revenue |
| Net income without the one-time benefit, about $157M (62% from the benefit) | 414.1 - 256.7; 256.7 / 414.1. Not a company-reported figure |
| DAU/MAU 34.7%, 39.6% | 40.5 / 116.7; 52.7 / 133.1 |
| Paid share of MAUs 8.1%, 9.2% | 9.5 / 116.7; 12.2 / 133.1 |
| FY2026 bookings growth 11% | guidance midpoint (1,274 + 1,298) / 2 / 1,158.4 - 1 |

## How the figures were checked

- Source 1 values are machine-readable XBRL, exact to the dollar.
- Sources 2 and 3 were read from the SEC-hosted HTML when the storyline was written, and every figure the deck uses was read again from the same pages on 2026-10-04 before the deck was built. Revenue and net income also match source 1.
- Adjusted EBITDA and free cash flow are non-GAAP measures as defined by the company; the deck labels them. 2026 figures are company guidance, not results, and are labelled as such.
- Background notes from the storyline step: `inputs/source-notes.md`.
