# 2026-04-14 Macro Data Collection Notes

## Fed policy
- **Source:** https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html
- **Observed on page:** Next FOMC meeting shown as **30 Apr 2026** with probabilities approximately **0.0% ease / 99.5% no change / 0.5% hike**.
- **Scoring implication:** **Fed stance = Neutral hold (0)** because the market overwhelmingly prices no change at the next meeting.

## USD and volatility backdrop
- **Source:** https://www.tradingview.com/symbols/TVC-DXY/
- **Observed on page:** DXY at **98.079**, down **0.30%** on the day and down **0.99%** over 5 days.
- **Scoring implication:** **USD (DXY) = Weak/Falling (+1)**.

- **Source:** https://www.cboe.com/tradable-products/vix/
- **Observed on page:** VIX spot at **18.31**, down **4.24% (-0.81)** from a prior close of **19.12**.
- **Scoring implication:** **Risk mood = Balanced (0)** because VIX is in the 15-20 range, and **VIX direction = Falling (+1)**.

## Growth and real yields
- **Source:** https://www.atlantafed.org/research-and-data/data/gdpnow
- **Observed on page:** **GDPNow 2026:Q1 estimate = 1.3%**, updated **2026-04-09**, with the next update scheduled for **2026-04-21**.
- **Scoring implication:** **Growth narrative = Stable (0)** for now, pending comparison to prior update if needed.

- **Primary source attempt:** https://www.cnbc.com/quotes/US10YTIP
- **Status:** Access was blocked in-browser by policy restrictions.
- **Action:** A fallback browser source is required for the real-yield factor, and confidence should be reduced if no clean live fallback can be verified.

## Fallback rates and credit observations
- **Source:** https://fred.stlouisfed.org/series/DFII10
- **Observed on page:** Latest available **DFII10 = 1.95** for **2026-04-10**, updated **2026-04-13**.
- **Scoring implication:** The latest official observation is recent but not intraday; relative to the prior verified repository run, real yields appear **flat** rather than clearly rising or falling, so provisional score is **0** unless a cleaner live fallback is found.

- **Source:** https://fred.stlouisfed.org/series/BAMLH0A0HYM2
- **Observed on page:** Latest available **HY OAS = 2.94** for **2026-04-10**.
- **Scoring implication:** Credit spreads remain **tight to modestly improving**, supporting a **Narrowing (+1)** classification on a provisional basis.

## Curve and semiconductor observations
- **Source:** https://fred.stlouisfed.org/series/T10Y2Y
- **Observed on page:** Latest available **2s10s spread = 0.52** for **2026-04-13**.
- **Scoring implication:** The curve remains positively sloped and broadly **steepening/healthy (+1)** versus the deeply inverted regime that prevailed in prior years.

- **Source:** https://www.tradingview.com/symbols/NASDAQ-SOX/
- **Observed on page:** **SOX = 9,039.52**, up **1.68%** on the day and **6.37%** over 5 days.
- **Scoring implication:** **SOX = Rising (+1)**.

## Rates volatility and crude backdrop
- **Source:** https://www.tradingview.com/symbols/TVC-MOVE/
- **Observed on page:** **MOVE = 74.4185**, up **3.14%** on the day, though still down **10.50%** over 5 days.
- **Scoring implication:** For the day’s read, **MOVE = Rising (-1)** because rates volatility increased versus the prior close.

- **Source:** https://www.eia.gov/petroleum/supply/weekly/
- **Observed on page:** Latest weekly report covers the **week ending 2026-04-03**, released **2026-04-08**, with the next release due **2026-04-15**.
- **Scoring implication:** The landing page confirms the current report window, but the inventory build/draw and supply-tightening call still require the report highlights or summary PDF for precise classification.

## Precious metals and ECB follow-up
- **Source:** https://www.gold.org/goldhub/research/gold-etfs-holdings-and-flows/2026/04
- **Observed on page:** World Gold Council reports **record March outflows of US$12bn**, the largest monthly outflow on record, even though Q1 remained net positive.
- **Scoring implication:** **Gold ETF flows = Outflows (-1)**.

- **Source attempted:** https://www.ecb.europa.eu/press/pr/date/html/index.en.html
- **Status:** The initial page load was obscured by the ECB cookie layer and did not yet expose the latest policy release in the extracted text.
- **Action:** A follow-up browser interaction is required to accept cookies and inspect the latest ECB policy communication.

## ECB browser follow-up
- **Action taken:** Accepted the cookie prompt and reloaded the ECB press-release index.
- **Result:** The page remained stuck on a loading state in-browser, so the latest ECB monetary-policy release was not reliably extractable from the rendered page.
- **Implication:** ECB stance remains a documented verification gap and may need a different official ECB page or another browser-accessible ECB publication.

## RBA follow-up
- **Source:** https://www.rba.gov.au/monetary-policy/
- **Observed on page:** The RBA monetary-policy section loaded successfully, and the latest decision archive for **2021–2026** was exposed, but the specific latest decision text was not yet opened.
- **Implication:** The source is reachable and suitable for extracting the current RBA stance in the next step.

## RBA archive status
- **Action taken:** Expanded the RBA monetary-policy decision archives.
- **Result:** The **2026** decision links are now exposed in the page navigation, confirming that the current RBA decision set is directly reachable from the official site.
- **Next step:** Open the **2026** entry and extract the latest policy decision wording to classify the RBA stance.

## RBA policy stance
- **Source:** https://www.rba.gov.au/media-releases/2026/mr-26-08.html
- **Observed on page:** On **17 March 2026**, the RBA **increased the cash rate target by 25 bps to 4.10%** and emphasized upside inflation risks.
- **Scoring implication:** **RBA stance = Hawkish (+1)**.

## BOJ policy source
- **Source:** https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2026/index.htm
- **Observed on page:** The BOJ 2026 monetary-policy releases list shows official statements on **19 March 2026** and **23 January 2026**, confirming the current decision trail is directly accessible from the Bank of Japan.
- **Implication:** The next step is to open the latest **Statement on Monetary Policy** to classify the BOJ stance for JPY scoring.

## BOJ policy stance
- **Source:** https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2026/k260319a.pdf
- **Observed in PDF viewer:** On **19 March 2026**, the BOJ stated that it would keep the uncollateralized overnight call rate at around **0.75%**. The statement described financial conditions as **accommodative** while noting inflation expectations had risen moderately.
- **Scoring implication:** The BOJ appears **neutral to mildly hawkish**, but for the bias model the safer provisional classification is **Neutral (0)** unless a stronger tightening signal is confirmed.

## China manufacturing PMI
- **Source attempted:** https://www.stats.gov.cn/english/PressRelease/202604/t20260401_1959379.html
- **Result:** The direct official release URL returned **404**, so it was not usable in-browser.
- **Fallback source:** https://tradingeconomics.com/china/manufacturing-pmi
- **Observed on page:** China manufacturing PMI was **50.8 in March 2026**, down from **52.1 in February**, still above 50 but showing slower expansion.
- **Scoring implication:** **China growth impulse = Improving but slowing / Neutral-to-positive**. For the model, a conservative provisional classification is **Positive (+1)** because PMI remains in expansion territory, though with reduced momentum.

