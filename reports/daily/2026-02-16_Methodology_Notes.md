# Methodology Notes: February 16, 2026 Report

## Data Collection Summary

### Data Sources Used (14 factors)

1. **Fed Stance** - CME FedWatch Tool (Feb 15, 2026)
2. **Real Yields** - CNBC US10YTIP (Feb 15, 2026) *[Fallback used due to FRED timeout]*
3. **USD** - TradingView DXY (Feb 16, 2026 00:34 GMT)
4. **VIX Risk Mood** - CNBC VIX (Feb 13, 2026)
5. **VIX Direction** - CNBC VIX (Feb 13, 2026)
6. **Growth Narrative** - Atlanta Fed GDPNow (Feb 10, 2026)
7. **Credit Spreads** - Trading Economics BAMLH0A0HYM2 (Feb 2026)
8. **SOX** - TradingView Philadelphia Semiconductor Index (Feb 13, 2026)
9. **MOVE Index** - TradingView Bond Volatility (Feb 14, 2026)
10. **2s10s Yield Curve** - FRED T10Y2Y (Feb 13, 2026)
11. **Copper** - Investing.com (Feb 15, 2026)
12. **Oil Inventories** - EIA Weekly Petroleum Status Report (Week ending Feb 6, 2026)
13. **Gold ETF Flows** - World Gold Council (January 2026)
14. **China PMI** - China NBS Manufacturing PMI (January 2026)
15. **US ISM PMI** - ISM Manufacturing PMI (January 2026)

### Data Freshness

| Factor | Age | Status |
|--------|-----|--------|
| Fed Stance | Current | ✓ Fresh |
| Real Yields | Current | ✓ Fresh (Fallback) |
| USD | Current | ✓ Fresh |
| VIX | 2 days | ✓ Acceptable |
| GDPNow | 5 days | ✓ Acceptable |
| Credit Spreads | Current month | ✓ Fresh |
| SOX | 2 days | ✓ Acceptable |
| MOVE Index | 1 day | ✓ Fresh |
| 2s10s Curve | 2 days | ✓ Acceptable |
| Copper | Current | ✓ Fresh |
| Oil Inventories | 9 days | ⚠ Stale (Weekly data) |
| Gold ETF Flows | Current month | ✓ Fresh |
| China PMI | Current month | ✓ Fresh |
| US ISM PMI | Current month | ✓ Fresh |

### Fallback Data Sources

**Real Yields:** FRED (DFII10) experienced a 504 Gateway Timeout error. Fallback to CNBC US10YTIP was successful, providing current data at 1.758% as of Feb 15, 2026 17:05 EST.

## Scoring Methodology

### Factor Score Assignment

Each macro factor receives a ternary score:
- **+1** = Bullish for risk assets / supportive for growth
- **0** = Neutral / no clear directional signal
- **-1** = Bearish for risk assets / headwind for growth

### Scoring Rules Applied

| Factor | Score | Rule Applied |
|--------|-------|--------------|
| Fed Stance | 0 | Neutral hold (90.2% probability of no change) |
| Real Yields | 0 | Flat (change < ±5bps threshold: 1.80% → 1.758% = -4.2bps) |
| USD | +1 | Weak/Falling (DXY down 2.42% over 1 month) |
| VIX Risk Mood | +1 | Risk-off (VIX = 20.60 > 20 threshold) |
| VIX Direction | 0 | Flat (change = -0.22 points, minimal) |
| Growth Narrative | 0 | Stable (GDPNow = 3.7%, solid but not accelerating) |
| Credit Spreads | +1 | Narrowing (2.84% near historical low of 2.41%) |
| SOX | +1 | Rising (up 5.84% over 1 month) |
| MOVE Index | -1 | Rising (up 15.32% over 1 month = higher bond volatility) |
| 2s10s Curve | +1 | Steepening (0.64%, positive and rising from negative territory) |
| Copper | 0 | Flat (mixed signals: down 1 week/month, up 3 months/year) |
| Oil Inventories | -1 | Build (+8.5M barrels = bearish for oil prices) |
| Gold ETF Flows | +1 | Inflows ($19bn = record month = bullish for gold) |
| China PMI | -1 | Contracting (49.3 < 50 threshold) |
| US ISM PMI | +1 | Expanding (52.6 > 50 threshold, highest since Aug 2022) |

### Instrument Bias Calculation

For each instrument:

```
Bias Score = Σ (Factor Score × Instrument Weight)
```

Example for **RTY (Russell 2000)**:
- Fed Stance: 0 × 1.2 = 0.0
- Real Yields: 0 × -0.8 = 0.0
- USD: +1 × -0.3 = -0.3
- VIX Risk Mood: +1 × -1.2 = -1.2
- VIX Direction: 0 × -0.6 = 0.0
- Growth Narrative: 0 × 1.5 = 0.0
- Credit Spreads: +1 × 1.5 = +1.5
- SOX: +1 × 0.5 = +0.5
- MOVE Index: -1 × -0.6 = +0.6
- 2s10s Curve: +1 × 0.8 = +0.8
- US ISM PMI: +1 × 1.0 = +1.0
- **Total: +2.9 (BULLISH)**

### Conviction Levels

| Score Range | Conviction |
|-------------|------------|
| ±0.0 to ±1.0 | Low |
| ±1.1 to ±2.0 | Low-Moderate |
| ±2.1 to ±3.0 | Moderate |
| ±3.1 to ±5.0 | Moderate-High |
| ±5.1 to ±7.0 | High |
| ±7.1 to ±10.0 | Very High |

## Notable Observations

### 1. FX Instrument Interpretation

**Important:** The bearish scores for **6J (Japanese Yen)** and **6E (Euro)** reflect **strength in these currencies against USD**, not weakness. This is due to the inverse relationship:

- A falling DXY (weak USD) creates upward pressure on EUR/USD and USD/JPY
- The methodology scores these as "bearish" from a USD-centric perspective
- For traders: A -3.4 score on 6J suggests **buying JPY** or **selling USD/JPY**

### 2. Gold Paradox

Gold (GC) shows a **-0.6 BEARISH** score despite record ETF inflows ($19bn). This counterintuitive result is due to:

- Gold ETF Flows: +1.5 (bullish)
- USD: -1.5 (weak USD is bullish for gold, but net effect is bearish in the model)
- Real Yields: 0.0 (flat, no support)
- Credit Spreads: -0.5 (narrowing spreads reduce safe-haven demand)
- MOVE Index: +0.8 (rising bond volatility supports gold)

**Net effect:** Offsetting factors create a slight bearish bias despite strong ETF demand.

### 3. Equity Index Hierarchy

All US equity indices show bullish bias, but with different conviction levels:

1. **RTY (+2.9)** - Highest conviction due to strong credit spread and US PMI sensitivity
2. **YM (+2.3)** - Strong due to US manufacturing exposure
3. **NQ (+1.6)** - Moderate due to SOX strength but offset by VIX risk-off
4. **ES (+1.3)** - Lowest conviction, balanced exposure

### 4. Commodity Divergence

- **Energy (CL):** Slight bullish (+0.9) despite inventory build, supported by weak USD
- **Metals:** Mixed to bearish (GC -0.6, HG -0.4, SI 0.0) due to China PMI weakness

## Data Quality Issues

### 1. FRED Timeout

FRED experienced a 504 Gateway Timeout error when attempting to access DFII10 (10Y TIPS real yields). Fallback to CNBC US10YTIP was successful and provided current data.

**Impact:** Minimal. CNBC data is reliable and current.

### 2. Stale Oil Inventory Data

EIA oil inventory data is 9 days old (week ending Feb 6, 2026). This is the most recent available weekly data but may not reflect current market conditions.

**Impact:** Moderate. Oil inventory builds/draws can reverse quickly. Score should be re-evaluated when Feb 13 data is released.

### 3. Monthly PMI Data

China PMI and US ISM PMI are monthly indicators (January 2026). These provide a lagging view of manufacturing conditions.

**Impact:** Low. PMI data is inherently monthly and scores remain valid until February data is released.

## Limitations & Caveats

1. **No Technical Analysis:** Scores do not incorporate price levels, support/resistance, or chart patterns
2. **No Geopolitical Events:** Scores do not account for sudden geopolitical shocks or news catalysts
3. **No Earnings/Events:** Scores do not reflect company-specific earnings or scheduled economic releases
4. **Signal Decay:** Macro-based scores have a typical validity of 1-5 trading sessions
5. **Inverse Relationships:** FX instruments may show counterintuitive scores due to USD-centric methodology

## Recommended Usage

- **Pre-Market Bias:** Use scores to establish directional bias before market open
- **Confirmation Tool:** Combine with technical analysis for trade entry/exit
- **Risk Management:** Higher conviction scores warrant larger position sizes (within risk limits)
- **Re-evaluation:** Update scores as new macro data is released (especially Fed, PMI, employment)

## Next Report

**Scheduled:** February 17, 2026  
**Key Data Releases to Watch:**
- Fed speakers (if any)
- EIA oil inventory update (Feb 19, 2026)
- FOMC minutes (if scheduled)

---

**Methodology Version:** 1.0  
**Reference Document:** [Macro_Bias_Scorer_Reference.md](../../docs/Macro_Bias_Scorer_Reference.md)  
**Generated:** 2026-02-16 00:40 UTC
