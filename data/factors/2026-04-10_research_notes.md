# 2026-04-10 Research Notes

## Methodology
- Read the complete methodology document from the repository raw URL before any other work.
- Confirmed required instruments, factor weights, integer-only scoring, required four-file output workflow, and mandatory post-push verification of `latest.json` and `latest.md`.
- Confirmed signal thresholds: >= +5 STRONG_BULLISH; +3 to +4 BULLISH; +1 to +2 SLIGHT_BULLISH; -1 to +1 NEUTRAL; -2 to -3 SLIGHT_BEARISH; -4 to -5 BEARISH; <= -6 STRONG_BEARISH.

## DXY
- Source: https://www.tradingview.com/symbols/TVC-DXY/
- TradingView showed DXY at 98.697 USD, down 0.098 points (-0.10%) versus previous close 98.795 USD.
- Classification for methodology: USD weak/falling = +1 for USD-sensitive long-risk and commodity/FX factors.

## VIX
Cboe's VIX product page showed a VIX spot price of **19.23** as of April 10, 2026, with a daily change of **-1.33% (-0.26)** and a previous close of **19.49**. Under the methodology, a VIX level between 15 and 20 maps to a neutral/balanced **risk_mood = 0**, while the negative daily change maps to **vix_direction = +1** because volatility is falling.

## DFII10
The FRED DFII10 series page listed the latest available observation as **1.96** on **2026-04-08**, updated April 9, 2026. Relative to the recent repository baseline, the latest official real-yield reading remains unchanged, so the methodology maps this to **real_yields = 0** (flat on latest official print).

## Credit Spreads
The FRED BAMLH0A0HYM2 page showed the latest available **ICE BofA US High Yield Index Option-Adjusted Spread** at **2.90** on **2026-04-09**. That is tighter than the prior repository baseline of 2.94 on 2026-04-08, so the methodology maps this to **credit_spreads = +1** (tightening spreads).

## Yield Curve
The FRED T10Y2Y page showed the latest available 10Y-2Y Treasury spread at **0.51** on **2026-04-09**. A positive reading means the curve remains positively sloped/normalized, so the methodology maps this to **yield_curve_2s10s = +1**.

## SOX
TradingView showed the **Philadelphia Semiconductor Index (SOX)** at **8,889.83**, up **200.30 points (+2.31%)** from a previous close of **8,689.53**. That clearly maps to **sox = +1** under the methodology because semiconductor leadership is positive.

## MOVE
TradingView showed the **MOVE Index** at **72.1541**, down **1.8588 points (-2.51%)** from a previous close of **74.0129**. That maps to **move_index = +1** because Treasury volatility is falling, which is supportive for growth/risk assets.

## GDPNow
The Atlanta Fed GDPNow landing page did not surface the live figure in static extraction, so a same-day TradingView/Mace News relay of the Atlanta Fed update was used as a fallback. It reported on **2026-04-09** that the **Atlanta Fed GDPNow model estimated Q1 2026 real GDP growth at 1.3%**, **unchanged from the April 7 estimate**. Relative to the latest repository baseline, this supports a **growth_narrative = 0** assessment (no new improvement on the latest update).
