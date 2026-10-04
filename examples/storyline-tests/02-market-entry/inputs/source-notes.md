# Source notes (retrieved 2026-10-04)

World Bank, World Development Indicators, via the public API (no key). WDI "last updated" for all series: 2026-07-13.
One request per indicator, countries IDN;VNM;PHL;THA, years 2015-2025:

| Indicator | Code | API URL |
|---|---|---|
| Population, total | SP.POP.TOTL | https://api.worldbank.org/v2/country/VNM;IDN;PHL;THA/indicator/SP.POP.TOTL?format=json&date=2015:2025&per_page=200 |
| Individuals using the Internet (% of population) | IT.NET.USER.ZS | https://api.worldbank.org/v2/country/VNM;IDN;PHL;THA/indicator/IT.NET.USER.ZS?format=json&date=2015:2025&per_page=200 |
| GDP per capita, PPP (current international $) | NY.GDP.PCAP.PP.CD | https://api.worldbank.org/v2/country/VNM;IDN;PHL;THA/indicator/NY.GDP.PCAP.PP.CD?format=json&date=2015:2025&per_page=200 |
| GDP per capita (current US$) | NY.GDP.PCAP.CD | https://api.worldbank.org/v2/country/VNM;IDN;PHL;THA/indicator/NY.GDP.PCAP.CD?format=json&date=2015:2025&per_page=200 |
| GDP growth (annual %) | NY.GDP.MKTP.KD.ZG | https://api.worldbank.org/v2/country/VNM;IDN;PHL;THA/indicator/NY.GDP.MKTP.KD.ZG?format=json&date=2015:2025&per_page=200 |
| Population ages 15-64 (% of total) | SP.POP.1564.TO.ZS | https://api.worldbank.org/v2/country/VNM;IDN;PHL;THA/indicator/SP.POP.1564.TO.ZS?format=json&date=2015:2025&per_page=200 |
| Mobile cellular subscriptions (per 100 people) | IT.CEL.SETS.P2 | https://api.worldbank.org/v2/country/VNM;IDN;PHL;THA/indicator/IT.CEL.SETS.P2?format=json&date=2015:2025&per_page=200 |

All raw values are in worldbank_wdi.csv. Internet-use data are latest for 2024; GDP and population run to 2025.
Human-readable series pages: https://data.worldbank.org/indicator/<code>
