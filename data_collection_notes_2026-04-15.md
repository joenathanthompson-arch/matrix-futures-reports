# Macro Data Collection Notes - 2026-04-15

## Source Log

1. **CME FedWatch**  
   URL: https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html  
   Observation: The page loaded successfully. The rendered page indicates the next FOMC meeting is in 14 days. A probability table is visible in the screenshot lower on the page, but the extracted markdown does not include the numeric probabilities, so additional extraction will be required.  
   Status: usable with further inspection.

2. **CNBC 10Y TIPS**  
   URL: https://www.cnbc.com/quotes/US10YTIP  
   Observation: Access was blocked by policy restrictions in the browsing environment.  
   Status: blocked in browser, fallback source required.

## Interim Assessment

- Fed policy data source is reachable but needs more detailed extraction.
- Real-yield primary fallback via CNBC is not accessible in the current browsing environment, so another allowed real-time source will be needed.
3. **Federal Reserve FOMC Calendar**  
   URL: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm  
   Observation: The page confirms the 2026 FOMC schedule. The next scheduled meeting is **April 28-29, 2026**. The page was last updated on **April 08, 2026**.  
   Status: current for catalyst timing.

4. **Atlanta Fed GDPNow**  
   URL: https://www.atlantafed.org/research-and-data/data/gdpnow  
   Observation: The latest GDPNow estimate for **2026:Q1 is 1.3%**, updated **April 09, 2026**, with the next update scheduled for **April 21, 2026**. This implies a relatively modest US growth backdrop rather than acceleration.  
   Status: usable for growth narrative.

## Updated Interim Assessment

- Next major Fed catalyst: April 28-29 FOMC.
- Current growth nowcast appears modest at 1.3%, which leans toward a stable-to-slowing interpretation rather than accelerating growth.
5. **CBOE VIX**  
   URL: https://www.cboe.com/tradable-products/vix/  
   Observation: The page reports **VIX spot at 18.19** as of **April 15, 2026**, with a **-0.93% (-0.17)** daily change and previous close of **18.36**. This places VIX in the **15-20 balanced range**, while the day-over-day direction is **falling**.  
   Status: current and usable.

6. **EIA Weekly Petroleum Status Report**  
   URL: https://www.eia.gov/petroleum/supply/weekly/  
   Observation: The latest visible release references **data for week ending April 3, 2026**, released **April 8, 2026**, with the next release due **April 15, 2026**. The page notes a crude oil production re-benchmarking adjustment lowering estimated production by **52,000 barrels per day**. The landing page itself does not provide the inventory headline figure, so a deeper extraction from the full report or data tables is still needed.  
   Status: partially usable; more detailed extraction required for inventories and supply interpretation.

## Updated Interim Assessment

- Risk mood currently screens as balanced based on VIX at 18.19.
- VIX direction is falling on the day, which is mildly supportive for equities and risk-sensitive FX.
- Oil market source is current enough to identify reporting cadence, but inventory and tighter/looser supply details still need confirmation from deeper data.
7. **World Gold Council Gold ETF Data**  
   URL: https://www.gold.org/goldhub/data/gold-etfs-holdings-and-flows  
   Observation: The page is current as of **13 April 2026** and references **ETF Flows: March 2026**. The public view confirms update cadence and timing, but the actual weekly or monthly flow values are hidden behind sign-in. This source is therefore useful for freshness confirmation but not sufficient by itself for the directional flow reading.  
   Status: partially usable; alternate reporting source may be needed for directional flow inference.

8. **ECB Press Releases / Publications by Date**  
   URL: https://www.ecb.europa.eu/press/pr/date/html/index.en.html  
   Observation: The landing page loaded, but cookie and rendering issues prevented extraction of the actual latest press-release list in markdown. The source is reachable but needs an alternate extraction path or a more specific ECB release page.  
   Status: reachable, not yet sufficient for stance classification.

## Updated Interim Assessment

- Gold ETF timing is recent, but the public page does not expose enough detail to classify flows without supporting evidence.
- ECB source accessibility is adequate, but the generic release index is not enough; a more specific monetary-policy decision page is preferable.
9. **Reserve Bank of Australia Monetary Policy**  
   URL: https://www.rba.gov.au/monetary-policy/  
   Observation: The site triggered a captcha in the browser environment, but the extracted markdown confirms the monetary-policy section is reachable as text. No current decision headline was captured from this landing page, so stance classification still requires a more specific release page or alternate extraction.  
   Status: partially reachable; detail insufficient.

10. **Bank of Japan Monetary Policy**  
   URL: https://www.boj.or.jp/en/mopo/index.htm  
   Observation: The BoJ monetary-policy landing page loaded successfully and confirms access to current policy materials, but the extracted markdown from the landing page does not itself state the latest decision. A more specific release or summary page is required for stance classification.  
   Status: reachable, but more specific source still needed.

## Updated Interim Assessment

- RBA and BoJ official sites are reachable enough to use, but landing pages are not sufficient for classifying current stance without deeper policy pages.
- Additional source-specific extraction remains necessary for FX central-bank scoring.
11. **TradingView DXY**  
   URL: https://www.tradingview.com/symbols/TVC-DXY/  
   Observation: DXY is **98.257**, up **0.15%** on the day as of **11:38 GMT**. However, the same page shows **5-day performance of -0.62%** and **1-month performance of -2.16%**, which indicates the broader dollar trend remains weaker even though the intraday move is mildly positive.  
   Status: current and highly usable.

12. **FRED HY OAS**  
   URL: https://fred.stlouisfed.org/series/BAMLH0A0HYM2  
   Observation: The latest high-yield option-adjusted spread is **2.95** on **2026-04-13**, updated **Apr 14, 2026 9:21 AM CDT**. The chart suggests spreads remain relatively contained rather than stress-level wide, supportive of a stable-to-narrow credit interpretation.  
   Status: usable, though not intraday.

## Updated Interim Assessment

- The US dollar is stronger intraday but weaker over the recent weekly and monthly windows, so the scoring choice will need a clearly defined time horizon.
- Credit conditions remain relatively benign based on HY OAS at 2.95, which is generally supportive for equities, especially small caps.
13. **FRED 2s10s Yield Curve**  
   URL: https://fred.stlouisfed.org/series/T10Y2Y  
   Observation: The latest 10y-2y Treasury spread is **0.50** on **2026-04-14**, updated **Apr 14, 2026 4:02 PM CDT**. The chart indicates the curve remains positively sloped relative to the prior inversion regime, which supports a steepening/benign-growth interpretation rather than flattening stress.  
   Status: usable.

14. **TradingView MOVE Index**  
   URL: https://www.tradingview.com/symbols/TVC-MOVE/  
   Observation: The MOVE index is **74.3509**, down **0.09%** on the day and **5.57%** over five days, with a **1-month change of -21.98%**. This clearly supports a **falling** rates-volatility classification.  
   Status: current and usable.

## Updated Interim Assessment

- The yield curve remains positively sloped, which is mildly supportive for cyclicals and domestic growth-sensitive assets.
- Rates volatility is falling materially, which is supportive for duration-sensitive equity exposures such as NQ.
15. **Investing.com Copper**  
   URL: https://www.investing.com/commodities/copper  
   Observation: Access to the page was blocked by policy restrictions in the browser environment.  
   Status: blocked in browser; alternate source required for copper direction.

16. **TradingView SOX**  
   URL: https://www.tradingview.com/symbols/NASDAQ-SOX/  
   Observation: The Philadelphia Semiconductor Index is **9,224.12**, up **2.04%** on the day, **7.74%** over five days, and **19.11%** over one month as of the Apr 14 close. This clearly supports a **rising** SOX classification.  
   Status: current and usable.

## Updated Interim Assessment

- The research set now includes more than 15 source visits via browser navigation.
- Semiconductor leadership is strong, which is supportive for NQ.
- Copper still needs an alternate source because the originally referenced page was blocked.
17. **Forex Factory Calendar**  
   URL: https://www.forexfactory.com/calendar  
   Observation: Access was blocked by policy restrictions in the browser environment.  
   Status: blocked; substitute source required.

18. **Yahoo Finance Economic Calendar**  
   URL: https://finance.yahoo.com/calendar/economic?day=2026-04-15  
   Observation: The page loaded successfully and lists **92 economic events** for **Wednesday, April 15, 2026**. Visible items include euro-area industrial production at **09:00 UTC**, U.S. mortgage market index data at **11:00 UTC**, and several European CPI updates earlier in the session. This provides a usable substitute calendar source for the daily report.  
   Status: usable substitute for calendar coverage.

## Updated Interim Assessment

- Forex Factory remains inaccessible in this environment, but Yahoo Finance provides an accessible substitute for the same-day economic calendar.
- The report can still include a daily calendar section while noting the blocked primary source.
