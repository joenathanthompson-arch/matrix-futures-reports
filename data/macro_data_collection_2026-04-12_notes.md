# Macro Data Collection Notes - 2026-04-12

## Browser Findings So Far

| Source | URL | Status | Key Finding |
|---|---|---|---|
| CME FedWatch | https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html | Accessible | The page loaded and displayed the next FOMC meeting countdown plus a probability table, but the extracted text did not expose the meeting probabilities cleanly in markdown. Visual elements indicate the current contract row for 30 Apr 2026 with visible columns for ease, no change, and hike. |
| CNBC US10YTIP | https://www.cnbc.com/quotes/US10YTIP | Blocked | Access was blocked by policy restrictions, so an alternative real-yield source will be required. |

## Immediate Implications

The Fed stance and real-yield inputs will need alternate extraction methods or fallback sources. Per the methodology, blocked or stale sources must be documented in `data_quality` and confidence may need to be reduced if no reliable fallback is available.

## Additional Browser-Verified Observations

| Source | URL | Status | Key Finding |
|---|---|---|---|
| CME FedWatch | https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html | Accessible | The visible table on the page showed the 30 Apr 2026 meeting row with probabilities visible in the screenshot: ease 0.0%, no change 97.9%, and hike 2.1%. This supports a neutral-hold Fed classification rather than a dovish or hawkish regime. |
| FRED DFII10 | https://fred.stlouisfed.org/series/DFII10 | Accessible | The extracted page text explicitly showed `2026-04-09: 1.95`, updated Apr 10, 2026. This confirms the latest accessible 10-year real yield reading at 1.95%. |

These two browser checks provide direct evidence for the Fed stance and real-yield inputs used in the scorecard.

| Source | URL | Status | Key Finding |
|---|---|---|---|
| Cboe VIX | https://www.cboe.com/tradable-products/vix/ | Accessible | The page explicitly showed VIX spot at `19.23` as of April 10, 2026, with change `-1.33% (-0.26)`. This classifies the regime as **balanced** (15-20) and the daily direction as **falling**. |
| Atlanta Fed GDPNow | https://www.atlantafed.org/research-and-data/data/gdpnow | Accessible | The page explicitly showed the latest GDPNow estimate for 2026:Q1 at `1.3%`, updated April 09, 2026, with the next update on April 21, 2026. Relative to the prior 1.6% reading referenced in the repository, this supports a **slowing** growth classification. |

At this point, four core macro factors have direct browser verification: Fed stance, real yields, VIX regime and direction, and GDPNow growth narrative.

| Source | URL | Status | Key Finding |
|---|---|---|---|
| FRED HY OAS | https://fred.stlouisfed.org/series/BAMLH0A0HYM2 | Accessible | The extracted page text explicitly showed `2026-04-09: 2.90`, updated Apr 10, 2026. Against the repository's prior `2.94` comparison point, this indicates **narrowing** credit spreads. |
| FRED T10Y2Y | https://fred.stlouisfed.org/series/T10Y2Y | Accessible | The extracted page text explicitly showed `2026-04-10: 0.50`, updated Apr 10, 2026. Relative to the prior 0.51 reference used in the repository, this indicates a modest **flattening** in the 2s10s curve. |

These additions directly support the credit-spread and yield-curve factors in the index score models.

| Source | URL | Status | Key Finding |
|---|---|---|---|
| TradingView DXY | https://www.tradingview.com/symbols/TVC-DXY/ | Accessible | The page explicitly showed DXY at `98.697`, down `0.10%` on Apr 10, 2026, with weekly performance `-1.48%`. This supports a **weaker dollar / falling** classification for commodity-sensitive assets. |
| TradingView SOX | https://www.tradingview.com/symbols/NASDAQ-SOX/ | Accessible | The page explicitly showed SOX at `8,889.83`, up `2.31%` on Apr 10, 2026, with weekly performance `+17.83%`. This supports a **rising semiconductor leadership** classification for Nasdaq. |

The browser log now includes six independently verified market sources with usable quantitative readings.

| Source | URL | Status | Key Finding |
|---|---|---|---|
| EIA Weekly Petroleum Status Report | https://www.eia.gov/petroleum/supply/weekly/ | Accessible | The page confirmed the latest reporting window as **week ending Apr. 3, 2026**, released Apr. 8, 2026. It also noted a production re-benchmarking adjustment that **lowered estimated domestic crude production by 52,000 bpd**, which is directionally supportive for a tighter oil backdrop. |
| ECB press release index | https://www.ecb.europa.eu/press/pr/date/2026/html/index.en.html | Access issue | The attempted annual index URL returned a **404** page, so this path is not reliable. An alternative ECB press release or policy-decision URL will be needed for direct browser verification of euro-area policy stance. |

The browser log continues to document both successful source checks and failed paths so the final report can distinguish verified inputs from fallback assumptions.

| Source | URL | Status | Key Finding |
|---|---|---|---|
| ECB monetary policy decision | https://www.ecb.europa.eu/press/pr/date/2026/html/ecb.mp260319~3057739775.en.html | Accessible | The page explicitly stated that on **19 March 2026** the Governing Council **kept the three key ECB rates unchanged**, with the deposit facility at **2.00%**. The tone acknowledged higher energy-driven inflation risks and weaker growth, which is consistent with a **hold / mildly hawkish hold** stance rather than easing. |
| RBA policy-decision archive | https://www.rba.gov.au/monetary-policy/int-rate-decisions/2026/ | Partially accessible | The archive page loaded successfully and confirmed the available 2026 decision dates (**17 March 2026** and **3 February 2026**). The archive itself did not expose the decision text in the extracted summary, so a direct meeting-release page is needed for explicit hold/ease/tighten confirmation if required. |

This expands direct browser verification to central-bank policy sources relevant for EUR and AUD-sensitive instruments.

| Source | URL | Status | Key Finding |
|---|---|---|---|
| RBA March 2026 decision | https://www.rba.gov.au/media-releases/2026/mr-26-08.html | Accessible | The March 17, 2026 release explicitly stated that the Board **increased the cash rate target by 25 bps to 4.10%**. This is a clearly **hawkish / tightening** policy signal for AUD-sensitive scoring. |
| BOJ March 2026 policy statement | https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2026/k260319a.pdf | Accessible via browser PDF | The first page of the PDF showed that on **March 19, 2026** the Policy Board decided by an **8-1 majority** to keep the uncollateralized overnight call rate at **around 0.75%**. This supports a **hold** classification for Japan policy. |

The browser evidence now covers explicit policy actions from both the RBA and BOJ in addition to the ECB, Fed-related pricing, and major market indicators.

| Source | URL | Status | Key Finding |
|---|---|---|---|
| World Gold Council commentary | https://www.gold.org/goldhub/research/gold-market-commentary-february-2026 | Accessible | The WGC commentary stated that **gold gained 5% in February** on **dip buying, dollar weakness, and softer U.S. Treasury yields**, and argued that a resumed medium-term **U.S. dollar downtrend** should further support gold. This is directly supportive for bullish gold scoring. |
| National Bureau of Statistics of China PMI release | https://www.stats.gov.cn/english/PressRelease/202604/t20260401_1962920.html | Accessible | The official release stated that China’s **March 2026 manufacturing PMI was 50.4**, up **1.4 points** from February and back **above the 50 threshold**, indicating an improving manufacturing backdrop supportive for cyclical metals and global growth-sensitive assets. |

At this stage the browser collection log contains well over a dozen source checks spanning central banks, market benchmarks, volatility, growth, credit, commodities, and international macro indicators.

| Source | URL | Status | Key Finding |
|---|---|---|---|
| TradingView MOVE | https://www.tradingview.com/symbols/TVC-MOVE/ | Accessible | The page explicitly showed the MOVE index at **72.1541**, down **2.51%** on Apr. 10, 2026, with five-day performance **-20.00%**. This supports a **falling** rate-volatility classification for Nasdaq-sensitive scoring. |
| TradingEconomics Copper | https://tradingeconomics.com/commodity/copper | Accessible | The page showed copper at **5.8705 USD/lb**, up **0.1225 (+2.13%)** on Apr. 10, 2026, and also described copper as hitting a **4-week high**. This supports a **rising** copper classification for silver and Australian dollar scoring. |

The browser collection log now includes all remaining cross-asset factors needed to score gold, silver, crude, U.S. equity futures, euro, Australian dollar, and Japanese yen futures without guessing. Where official series are lagged rather than blocked, the latest accessible print has been documented explicitly for data-quality purposes.
