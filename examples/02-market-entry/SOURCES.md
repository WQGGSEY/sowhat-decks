# Sources: 02 market entry

The company in this example is hypothetical: its product, budget, team and plans are invented. Every market statistic is real public data from the World Bank, cited on each slide.

Source: World Bank, World Development Indicators (WDI), via the public API (no key needed). WDI last updated 2026-07-13; retrieved 2026-10-04. Raw values for 2015-2025: `inputs/worldbank_wdi.csv`.

| Indicator | Code | API request (Indonesia, Vietnam, Philippines, Thailand, 2015-2025) |
|---|---|---|
| Population, total | SP.POP.TOTL | https://api.worldbank.org/v2/country/VNM;IDN;PHL;THA/indicator/SP.POP.TOTL?format=json&date=2015:2025&per_page=200 |
| Individuals using the Internet (% of population) | IT.NET.USER.ZS | https://api.worldbank.org/v2/country/VNM;IDN;PHL;THA/indicator/IT.NET.USER.ZS?format=json&date=2015:2025&per_page=200 |
| GDP per capita, PPP (current international $) | NY.GDP.PCAP.PP.CD | https://api.worldbank.org/v2/country/VNM;IDN;PHL;THA/indicator/NY.GDP.PCAP.PP.CD?format=json&date=2015:2025&per_page=200 |
| GDP growth (annual %) | NY.GDP.MKTP.KD.ZG | https://api.worldbank.org/v2/country/VNM;IDN;PHL;THA/indicator/NY.GDP.MKTP.KD.ZG?format=json&date=2015:2025&per_page=200 |
| Population ages 15-64 (% of total) | SP.POP.1564.TO.ZS | https://api.worldbank.org/v2/country/VNM;IDN;PHL;THA/indicator/SP.POP.1564.TO.ZS?format=json&date=2015:2025&per_page=200 |
| Mobile cellular subscriptions (per 100 people) | IT.CEL.SETS.P2 | https://api.worldbank.org/v2/country/VNM;IDN;PHL;THA/indicator/IT.CEL.SETS.P2?format=json&date=2015:2025&per_page=200 |

Human-readable pages: `https://data.worldbank.org/indicator/<code>`. Also listed in `inputs/source-notes.md`.

## Derived figures

| Figure | Formula |
|---|---|
| Internet users (e.g. Indonesia 206.3M in 2024) | population x internet use % |
| Users added 2019-2024, offline population 2024 | users 2024 - users 2019; population 2024 - users 2024 |
| Income-adjusted market (e.g. Indonesia $3.40T) | internet users x GDP per capita PPP, 2024. A ranking proxy that assumes users' ability to pay tracks national income per person; not a revenue estimate |
| Average GDP growth 2021-2025 | mean of the five annual values |
| Income growth 2019-2025 | GDP per capita PPP 2025 / 2019 - 1 |

All derived values were recomputed from `inputs/worldbank_wdi.csv` on 2026-10-04, and one series (internet use, Indonesia and the Philippines, 2023-2024) was re-fetched from the API and matched.

## Not in public data

Willingness to pay, competitors and their prices, payment methods, acquisition cost and local rules are not in WDI. The deck says so (slide 9) and proposes how to find out; it does not estimate them.
