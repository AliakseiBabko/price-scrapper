# Annual Average Exchange Rates Reference

This reference records annual average exchange rate benchmarks used across the renovation vault to normalize historical or secondary reference price estimates.

> [!IMPORTANT]
> **Source-Year Conversion Policy**
> Historical prices from video sources are converted using the average exchange rate of the **source year** (or explicitly stated video year), never the current spot rate. Unverified rates are marked `TODO / needs source`. Projections (e.g. 2026) must not be used for historical price normalization.

## Annual Average Benchmark Table

| year | currency_pair | average_rate | retrieval_date | source_url | confidence | notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **2017** | USD/RUB | 58.3 RUB per USD | 2026-08-20 | https://www.cbr.ru/content/document/file/165597/on_eng_2025%282026-2027%29.pdf | confirmed | Bank of Russia, Table 3, nominal exchange rate RUB/USD, yearly average |
| **2018** | USD/RUB | 62.5 RUB per USD | 2026-08-20 | https://www.cbr.ru/content/document/file/165597/on_eng_2025%282026-2027%29.pdf | confirmed | Bank of Russia, Table 3, nominal exchange rate RUB/USD, yearly average |
| **2019** | USD/RUB | 64.7 RUB per USD | 2026-08-20 | https://www.cbr.ru/content/document/file/165597/on_eng_2025%282026-2027%29.pdf | confirmed | Bank of Russia, Table 3, nominal exchange rate RUB/USD, yearly average |
| **2020** | USD/RUB | 71.9 RUB per USD | 2026-08-20 | https://www.cbr.ru/content/document/file/165597/on_eng_2025%282026-2027%29.pdf | confirmed | Bank of Russia, Table 3, nominal exchange rate RUB/USD, yearly average |
| **2021** | USD/RUB | 73.6 RUB per USD | 2026-08-20 | https://www.cbr.ru/content/document/file/165597/on_eng_2025%282026-2027%29.pdf | confirmed | Bank of Russia, Table 3, nominal exchange rate RUB/USD, yearly average |
| **2022** | USD/RUB | 67.5 RUB per USD | 2026-08-20 | https://www.cbr.ru/content/document/file/165597/on_eng_2025%282026-2027%29.pdf | confirmed | Bank of Russia, Table 3, nominal exchange rate RUB/USD, yearly average |
| **2023** | USD/RUB | 84.7 RUB per USD | 2026-08-20 | https://www.cbr.ru/content/document/file/165597/on_eng_2025%282026-2027%29.pdf | confirmed | Bank of Russia, Table 3, nominal exchange rate RUB/USD, yearly average |
| **2024** | USD/RUB | 92.66 RUB per USD | 2026-08-21 | https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=01/01/2024&date_req2=31/12/2024&VAL_NM_RQ=R01235 | confirmed | Bank of Russia official daily-rate archive, full calendar year, mean of 248 published daily rates (business days only, as CBR publishes) |
| **2025** | USD/RUB | 83.21 RUB per USD | 2026-08-21 | https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=01/01/2025&date_req2=31/12/2025&VAL_NM_RQ=R01235 | confirmed | Bank of Russia official daily-rate archive, full calendar year, mean of 247 published daily rates |
| **2017** | USD/BYN | unverified / needs source | 2026-08-20 | https://www.nb-rb.by/engl/statistics/rates/avgrate.htm | unverified / needs source | NBRB annual-average page located; a direct daily-archive pull for this year was attempted 2026-08-21 and returned an incomplete series (176 of ~365 days) - not used, per the no-partial-year-average rule |
| **2018** | USD/BYN | unverified / needs source | 2026-08-20 | https://www.nb-rb.by/engl/statistics/rates/avgrate.htm | unverified / needs source | NBRB annual-average page located; specific annual figure not confirmed in this lookup |
| **2019** | USD/BYN | unverified / needs source | 2026-08-20 | https://www.nb-rb.by/engl/statistics/rates/avgrate.htm | unverified / needs source | NBRB annual-average page located; specific annual figure not confirmed in this lookup |
| **2020** | USD/BYN | unverified / needs source | 2026-08-20 | https://www.nb-rb.by/engl/statistics/rates/avgrate.htm | unverified / needs source | NBRB annual-average page located; a direct daily-archive pull for this year was attempted 2026-08-21 and returned no data (empty result) - not used |
| **2021** | USD/BYN | unverified / needs source | 2026-08-20 | https://www.nb-rb.by/engl/statistics/rates/avgrate.htm | unverified / needs source | NBRB annual-average page located; a direct daily-archive pull for this year was attempted 2026-08-21 and returned an incomplete series (176 of ~365 days, appears to be roughly Jan-Jun only) - not used, per the no-partial-year-average rule |
| **2022** | USD/BYN | 2.6290 BYN per USD | 2026-08-21 | https://www.nbrb.by/api/exrates/rates/dynamics/431?startDate=2022-01-01&endDate=2022-12-31 | confirmed | National Bank of the Republic of Belarus official daily-rate archive, full calendar year, mean of 365 published daily rates |
| **2023** | USD/BYN | 3.0091 BYN per USD | 2026-08-21 | https://www.nbrb.by/api/exrates/rates/dynamics/431?startDate=2023-01-01&endDate=2023-12-31 | confirmed | National Bank of the Republic of Belarus official daily-rate archive, full calendar year, mean of 365 published daily rates |
| **2024** | USD/BYN | 3.2458 BYN per USD | 2026-08-21 | https://www.nbrb.by/api/exrates/rates/dynamics/431?startDate=2024-01-01&endDate=2024-12-31 | confirmed | National Bank of the Republic of Belarus official daily-rate archive, full calendar year, mean of 365 published daily rates |
| **2025** | USD/BYN | 3.0694 BYN per USD | 2026-08-21 | https://www.nbrb.by/api/exrates/rates/dynamics/431?startDate=2025-01-01&endDate=2025-12-31 | confirmed | National Bank of the Republic of Belarus official daily-rate archive, full calendar year, mean of 365 published daily rates |
| **2026** | USD/BYN | unverified / partial-year; do not use for historical normalization | 2026-08-20 | https://www.nb-rb.by/engl/statistics/rates/avgrate.htm | projection (do not use for historical normalization) | No complete annual average exists yet |
| **2026** | USD/RUB | unverified / partial-year; do not use for historical normalization | 2026-08-20 | https://www.cbr.ru/eng/currency_base/dynamics/ | projection (do not use for historical normalization) | No complete annual average exists yet |
| **unknown** | USD/BYN | unverified / needs source | 2026-08-20 | https://www.nb-rb.by/engl/statistics/rates/avgrate.htm | unaligned | Mark source_year as unknown; do not present converted values as directly comparable |
| **unknown** | USD/RUB | unverified / needs source | 2026-08-20 | https://www.cbr.ru/eng/currency_base/dynamics/ | unaligned | Mark source_year as unknown; do not present converted values as directly comparable |
