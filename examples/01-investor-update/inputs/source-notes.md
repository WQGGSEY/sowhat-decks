# Source notes (all retrieved 2026-10-04)

## SRC 1 - Form 10-K, fiscal year 2025 (filed 2026-02-27, accession 0001628280-26-012494)

- Filing: https://www.sec.gov/Archives/edgar/data/1562088/000162828026012494/duol-20251231.htm
- Figures read from the SEC XBRL "company facts" API for CIK 0001562088, filtered to this accession:
  https://data.sec.gov/api/xbrl/companyfacts/CIK0001562088.json
- Extract saved as `duolingo_10k_fy2025_xbrl.csv` (USD, full fiscal years 2023-2025; balance-sheet items at year end).

## SRC 2 - Q4 and FY2025 shareholder letter (exhibit to Form 8-K filed 2026-02-26, accession 0001628280-26-012246)

- https://www.sec.gov/Archives/edgar/data/1562088/000162828026012246/q4fy25duolingo12-31x25shar.htm
- Figures used (as printed in the letter):
  - FY2025 revenue $1,037.6M vs $748.0M in FY2024, +39% YoY
  - FY2025 total bookings $1,158.4M vs $870.6M, +33% YoY; subscription bookings $996.3M vs $730.7M, +36%
  - FY2025 net income $414.1M vs $88.6M
  - One-time income-tax benefit of $256.7M from releasing the valuation allowance on federal and state deferred tax assets (2025)
  - Adjusted EBITDA $305.9M, 29.5% margin (FY2025) vs $191.9M, 25.7% (FY2024) - non-GAAP
  - Free cash flow $360.4M (FY2025) vs $264.4M (FY2024), +36% - non-GAAP
  - Q4 2025 DAUs 52.7M (+30% YoY); MAUs 133.1M (+14%); paid subscribers 12.2M (+28%)
  - Q4 2024 DAUs 40.5M; MAUs 116.7M; paid subscribers 9.5M
  - 2026 guidance: bookings $1,274-1,298M (+10% to +12%); revenue $1,197-1,221M (+15% to +18%); adjusted EBITDA margin 25.0%
  - Strategy: 2026 strategy to grow users more rapidly, which will lower financial results in the short term; management estimates more than $50M of foregone bookings (about 5 points of year-over-year bookings growth) invested into the free user experience
  - Gross margin: FY2025 72.2% vs 72.8% in FY2024; expected about 71% in Q1 2026 and roughly 69% for the rest of 2026, driven mainly by expanding AI-powered features to all users
  - Share repurchase: $400 million authorization approved by the Board; timing at the company's discretion

## SRC 3 - Q4 and FY2024 shareholder letter (exhibit to Form 8-K, 2025, accession 0001562088-25-000039)

- https://www.sec.gov/Archives/edgar/data/1562088/000156208825000039/q4fy24duolingo12-31x24shar.htm
- Figures used: Q4 2024 DAUs 40.5M (+51% YoY); MAUs 116.7M (+32%); paid subscribers 9.5M (+43%); FY2024 revenue $748.0M (+41%); FY2024 total bookings $870.6M (+40%); adjusted EBITDA margin 25.7%.

## How the figures were read

- SRC 1: machine-readable XBRL values, exact to the dollar.
- SRC 2 and SRC 3: read from the SEC-hosted HTML letters with a page-reading tool. Every figure that also appears in SRC 1 (revenue FY2024/FY2025, net income) matched. The user metrics were consistent across two separate reads. Spot-check against the letter before publishing.
