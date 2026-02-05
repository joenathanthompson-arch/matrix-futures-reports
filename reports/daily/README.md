# Matrix Futures Daily Bias Reports

This directory contains daily bias reports for 10 key futures instruments based on quantitative analysis of 14+ macroeconomic factors.

## Latest Report

**Date:** February 5, 2026  
**Files:**
- [Bias Summary (CSV)](./2026-02-05_bias_summary.csv)
- [Detailed Report (Markdown)](./2026-02-05_detailed_report.md)
- [Factor Contributions (JSON)](./2026-02-05_factor_contributions.json)

## Report Index

| Date | Bias Summary | Detailed Report | Factor Contributions |
|------|--------------|-----------------|---------------------|
| 2026-02-05 | [CSV](./2026-02-05_bias_summary.csv) | [MD](./2026-02-05_detailed_report.md) | [JSON](./2026-02-05_factor_contributions.json) |

## Instruments Covered

1. **ES** - E-mini S&P 500 (Equity Index)
2. **NQ** - E-mini Nasdaq-100 (Equity Index)
3. **RTY** - E-mini Russell 2000 (Equity Index)
4. **GC** - Gold (Precious Metal)
5. **SI** - Silver (Precious Metal)
6. **CL** - Crude Oil WTI (Energy)
7. **HG** - Copper (Industrial Metal)
8. **M6E** - Micro EUR/USD (FX)
9. **6A** - Australian Dollar (FX)
10. **6J** - Japanese Yen (FX)

## File Descriptions

### 1. Bias Summary (CSV)
Quick reference table with bias scores, labels, and conviction levels for all instruments. Ideal for programmatic consumption or spreadsheet analysis.

**Columns:**
- `Date`: Report date (YYYY-MM-DD)
- `Instrument`: Futures symbol
- `Name`: Full instrument name
- `Asset_Class`: Asset class category
- `Bias_Score`: Quantitative bias score (-10 to +10)
- `Bias_Label`: Qualitative bias label (Strong Bearish to Strong Bullish)
- `Conviction`: Conviction level (Very Low to Very High)

### 2. Detailed Report (Markdown)
Comprehensive analysis including:
- Executive summary with top opportunities
- Ranked bias scores table
- Macro environment snapshot
- Detailed instrument-by-instrument analysis
- Key drivers and rationale for each bias score
- Signal decay notes
- Methodology and risk disclaimer

### 3. Factor Contributions (JSON)
Machine-readable data structure containing:
- Macro environment snapshot with all factor values
- Per-instrument factor contributions
- Raw scores and bias score calculations
- Full transparency into the scoring methodology

## Methodology

Bias scores are calculated using a weighted multi-factor model:

1. **Data Collection:** 14+ macroeconomic factors collected from authoritative sources (Fed, FRED, EIA, central banks, etc.)
2. **Factor Scoring:** Each factor assigned a value of -1 (bearish), 0 (neutral), or +1 (bullish)
3. **Weighted Aggregation:** Factors weighted by relevance to each instrument (weights sum to 1.0)
4. **Bias Score:** Raw score scaled to -10 (Strong Bearish) to +10 (Strong Bullish)
5. **Conviction:** Absolute bias score determines conviction level

**Bias Score Scale:**
- **+7 to +10:** Strong Bullish
- **+4 to +6:** Bullish
- **+1 to +3:** Weak Bullish
- **-1 to +1:** Neutral
- **-1 to -3:** Weak Bearish
- **-4 to -6:** Bearish
- **-7 to -10:** Strong Bearish

**Conviction Levels:**
- **Very High:** |Bias Score| ≥ 8
- **High:** |Bias Score| ≥ 6
- **Moderate:** |Bias Score| ≥ 4
- **Low:** |Bias Score| ≥ 2
- **Very Low:** |Bias Score| < 2

## Signal Decay

Bias scores are time-sensitive. High-conviction signals (+8 to +10) typically reflect catalysts expected within 1 week. Lower-conviction signals may persist longer but are more susceptible to reversals. Users should reassess positions as new data emerges.

## Data Sources

- **CME FedWatch Tool:** Fed policy probabilities
- **FRED (St. Louis Fed):** Real yields, credit spreads, yield curve
- **TradingView:** DXY, SOX, MOVE Index
- **CNBC/Investing.com:** VIX, Copper
- **Atlanta Fed GDPNow:** Growth narrative
- **EIA:** Weekly petroleum inventories
- **World Gold Council:** Gold ETF flows
- **Central Banks:** ECB, RBA, BoJ policy statements
- **China NBS/Caixin:** Manufacturing PMI
- **News Sources:** Geopolitical risk assessment

## Usage

### For Traders
1. Review the **Bias Summary (CSV)** for quick bias scores
2. Read the **Detailed Report (MD)** for context and rationale
3. Focus on instruments with **Moderate to High conviction**
4. Monitor signal decay and reassess as new data emerges

### For Developers
1. Parse the **Factor Contributions (JSON)** for programmatic access
2. Build custom dashboards or alerts based on bias scores
3. Backtest strategies using historical bias scores
4. Integrate with trading systems or risk management tools

## Risk Disclaimer

These reports are for informational purposes only and do not constitute investment advice. Bias scores are based on quantitative analysis of macroeconomic factors and may not capture all market dynamics. Past performance does not guarantee future results. Users should conduct their own due diligence and consult with financial professionals before making trading decisions.

## Methodology Reference

For detailed methodology, see: [Macro_Bias_Scorer_Reference.md](../../docs/Macro_Bias_Scorer_Reference.md)

## Contact

**Repository:** https://github.com/joenathanthompson-arch/matrix-futures-reports  
**Issues:** https://github.com/joenathanthompson-arch/matrix-futures-reports/issues

---

**Last Updated:** 2026-02-05  
**Report Version:** 1.0
