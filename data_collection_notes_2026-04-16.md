# Macro Data Collection Notes - 2026-04-16 UTC

## Source Log

1. **CME FedWatch**  
   URL: https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html  
   Status: Accessed in browser. The page loaded, but the extracted text was sparse. Visible page content confirmed the FedWatch tool and displayed the next FOMC countdown. A probability table was visible in the screenshot lower on the page, indicating the current contract row had **0.0% ease, 99.0% no change, 1.0% hike** for the next meeting. Working classification: **Fed stance = Neutral hold / slightly hawkish hold**, pending cross-check from another accessible source.

2. **CNBC 10Y TIPS**  
   URL: https://www.cnbc.com/quotes/US10YTIP  
   Status: Blocked by policy restrictions in browser. Need alternative real-time source or fallback from repository tooling / another accessible site.

## Interim Interpretation

- Fed policy expectations remain overwhelmingly centered on **no change** at the next meeting.
- Real-yield classification still needs confirmation from an accessible fallback source.

3. **Atlanta Fed GDPNow**  
   URL: https://www.atlantafed.org/research-and-data/data/gdpnow  
   Status: Accessed in browser. The page showed **Latest GDPNow Estimate for 2026:Q1 = 1.3%**, updated **April 09, 2026**, with next update scheduled **April 21, 2026**. Working classification: **Growth narrative = Stable to mildly slowing** versus stronger earlier-cycle growth, but not recessionary.

4. **TradingView DXY**  
   URL: https://www.tradingview.com/symbols/TVC-DXY/  
   Status: Accessed in browser. Extracted values: **98.163**, **+0.12% on the day**, **-0.71% over 5 days**, **-1.70% over 1 month**. Working classification for macro bias model: **USD = Weak/Falling** on the relevant multi-day horizon despite a small positive daily move.

## Working Factor States After Four Sources

- **Fed stance:** Neutral hold
- **Growth narrative:** Stable / slightly slowing
- **USD (DXY):** Weak/Falling
- **Real yields:** Pending accessible fallback

5. **CBOE VIX**  
   URL: https://www.cboe.com/tradable-products/vix/  
   Status: Accessed in browser. Extracted values: **VIX spot 18.23**, **+0.33% (+0.06)**, previous close **18.17**, open **18.04**. Working classification: **Risk mood = Balanced** (15-20 zone), while **VIX direction = Rising** on the day.

6. **EIA Weekly Petroleum Status Report**  
   URL: https://www.eia.gov/petroleum/supply/weekly/  
   Status: Accessed in browser. The report page confirmed the latest weekly release schedule for **week ending Apr. 10, 2026**, released **Apr. 15, 2026**, with the detailed balance-sheet tables available. The landing page itself did not expose the inventory headline directly in extracted text, so the exact crude build/draw figure still needs follow-up from the full report/table. Working status: **current source confirmed; numeric inventory change pending extraction**.

## Updated Working Factor States

- **Fed stance:** Neutral hold
- **Growth narrative:** Stable / slightly slowing
- **USD (DXY):** Weak/Falling
- **Risk mood (VIX level):** Balanced
- **VIX direction:** Rising
- **Real yields:** Pending accessible fallback
- **Oil inventories / oil supply shock:** Current source confirmed, values pending follow-up

7. **World Gold Council ETF Flows**  
   URL: https://www.gold.org/goldhub/data/gold-etfs-holdings-and-flows  
   Status: Accessed in browser. The page confirmed **ETF Flows: March 2026** as the latest visible monthly file reference and showed an update date of **13 April 2026**, but the underlying flow chart is gated behind sign-in. Working classification: **gold ETF flows data source is current but direction is not directly visible on-page**, so this factor needs fallback handling or prior repository parsing.

8. **ECB Press Releases**  
   URL: https://www.ecb.europa.eu/press/pr/date/html/index.en.html  
   Status: Accessed in browser, but the publication list did not render in extracted text and the page required further interaction/cookie acceptance for deeper review. Working classification: **ECB source reachable but stance still pending direct extraction**.

## Current Data-Quality Notes

- Browser access succeeded for eight sources so far.
- Some sources expose the current page shell but not the needed numeric or directional value in extracted text.
- Current gaps requiring follow-up or fallback extraction: **real yields, inventories, gold ETF flow direction, ECB stance**.

9. **Federal Reserve FOMC Calendar**  
   URL: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm  
   Status: Accessed in browser. The page confirmed the 2026 FOMC calendar and stated the latest update was **April 08, 2026**. This supports the interpretation that the Fed remains in a normal scheduled-meeting **hold regime**, with the next meeting on **April 28-29, 2026**.

10. **RBA Monetary Policy**  
   URL: https://www.rba.gov.au/monetary-policy/  
   Status: Accessed in browser. The top-level page loaded successfully but mostly provided structural policy background rather than the most recent decision language. Working classification: **RBA source reachable; direct stance extraction still needs a more specific decision page or fallback**.

## Intermediate Interpretation

- Fed-related evidence from CME FedWatch plus the Fed calendar is consistent with a **neutral-hold** baseline.
- Australia-related central-bank evidence is not yet specific enough to call the RBA stance without follow-up to a decision page.

11. **Bank of Japan Monetary Policy**  
   URL: https://www.boj.or.jp/en/mopo/index.htm  
   Status: Accessed in browser. The page structure loaded and exposed links to monetary policy releases, outlook, minutes, and summary of opinions, but the top-level extracted text did not include the latest stance headline. Working classification: **BoJ source reachable; stance still pending direct release-page extraction or repository fallback**.

12. **TradingView MOVE Index**  
   URL: https://www.tradingview.com/symbols/TVC-MOVE/  
   Status: Accessed in browser. Extracted values: **67.9410**, **-8.62% on the day**, **-8.20% over 5 days**, **-25.48% over 1 month**. Working classification: **MOVE / rate volatility = Falling**, clearly supportive for duration-sensitive risk assets such as NQ.

## Updated Working Factor States

- **Fed stance:** Neutral hold
- **Growth narrative:** Stable / slightly slowing
- **USD (DXY):** Weak/Falling
- **Risk mood (VIX level):** Balanced
- **VIX direction:** Rising
- **MOVE:** Falling
- **Oil inventories / oil supply shock:** Pending detailed extraction
- **Gold ETF flows:** Current source but direction not directly visible
- **ECB / RBA / BoJ stances:** Need specific policy-release follow-up or fallback handling

13. **TradingView SOX**  
   URL: https://www.tradingview.com/symbols/NASDAQ-SOX/  
   Status: Accessed in browser. Extracted values: **9,239.29**, **+0.16% on the day**, **+4.85% over 5 days**, **+17.75% over 1 month**. Working classification: **SOX = Rising**, supportive for NQ relative strength.

14. **Investing.com Copper**  
   URL: https://www.investing.com/commodities/copper  
   Status: Browser access blocked by policy restrictions. Need an alternative copper source or repository fallback for same-session classification.

## Source Count

A total of **14 browser source attempts** have now been made, including successfully accessed market, central-bank, and macro pages plus blocked pages documented for fallback handling.

15. **FRED 2s10s Yield Curve (T10Y2Y)**  
   URL: https://fred.stlouisfed.org/series/T10Y2Y  
   Status: Accessed in browser. Extracted latest observation: **0.53** on **2026-04-15**, updated **Apr. 15, 2026 4:09 PM CDT**. The level remains positively sloped; follow-up comparison is needed to decide whether the curve is currently **steepening or flattening** versus recent sessions.

16. **FRED High Yield OAS (BAMLH0A0HYM2)**  
   URL: https://fred.stlouisfed.org/series/BAMLH0A0HYM2  
   Status: Accessed in browser. Extracted latest observation: **2.84** on **2026-04-14**, updated **Apr. 15, 2026 9:00 AM CDT**. The source is current enough for a preliminary credit-spread read, though a recent comparison point is still needed to classify the move as widening, flat, or narrowing.

## Browser Collection Status

A total of **16 browser source attempts** have now been logged, comfortably above the requested 15+ sources. The remaining task is to normalize these source readings, fill the few blocked/gated gaps with documented fallbacks, and run the weighted scoring model.

17. **ECB Monetary Policy Decision (19 March 2026)**  
   URL: https://www.ecb.europa.eu/press/pr/date/2026/html/ecb.mp260319~3057739775.en.html  
   Status: Accessed in browser. The Governing Council **kept the three key ECB interest rates unchanged**, but emphasized upside inflation risks from higher energy prices and explicitly stated that it stands ready to adjust instruments as needed. Working classification: **ECB stance = Neutral to mildly hawkish hold**.

18. **RBA Monetary Policy Decision (17 March 2026)**  
   URL: https://www.rba.gov.au/media-releases/2026/mr-26-08.html  
   Status: Accessed in browser. The Board **raised the cash rate target by 25 bps to 4.10%** and stated that inflation risks had tilted further to the upside. Working classification: **RBA stance = Hawkish**.

## Central-Bank Classification Update

The evidence base now supports explicit central-bank tags for the FX models: the **Fed remains neutral-hold**, the **ECB is neutral/slightly hawkish**, and the **RBA is hawkish**. The remaining major central-bank gap is the **BoJ stance**, which still needs a direct release-page classification or a documented fallback from the available BoJ release artifact.

19. **BoJ Statements on Monetary Policy 2026 index**  
   URL: https://www.boj.or.jp/en/mopo/mpmdeci/state_2026/index.htm  
   Status: Accessed in browser. The annual statements page confirmed a March 19, 2026 statement link was available for the latest policy decision.

20. **BoJ Statement on Monetary Policy (19 March 2026 PDF)**  
   URL: https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2026/k260319a.pdf  
   Status: Opened in browser PDF viewer. The visible first-page text confirms that the Policy Board, by an **8-1 majority**, decided to keep the uncollateralized overnight call rate at **around 0.75%**. The statement also described financial conditions as accommodative and noted inflation expectations had risen moderately. Working classification: **BoJ stance = Neutral hold with tightening bias / mildly hawkish hold**.

## Central-Bank Coverage Complete

With the Fed, ECB, RBA, and BoJ now all classified from current source material or direct release pages, the central-bank input set required for the FX and rates models is operationally complete.
