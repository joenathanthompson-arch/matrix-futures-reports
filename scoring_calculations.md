# Matrix Futures Bias Scoring Calculations
## Date: 2026-02-07

## Summary of Macro Factor Scores
- Fed Stance: +1 (Dovish hold)
- Real Yields: 0 (Flat)
- USD (DXY): +1 (Weak/Falling)
- Risk Mood (VIX): 0 (Balanced, VIX 15-20)
- VIX Direction: +1 (Falling)
- Growth (GDPNow): 0 (Stable)
- Credit Spreads (HY OAS): +1 (Narrowing)
- SOX: +1 (Rising)
- MOVE: 0 (Flat/Stable)
- 2s10s Curve: +1 (Steepening)
- Copper: +1 (Rising)
- Oil Supply: 0 (Neutral - assuming no major disruptions)
- Oil Inventories: +1 (Draw)
- Gold ETF Flows: +1 (Inflows)
- Geopolitical Risk: +1 (Rising)
- ECB Stance: 0 (Neutral)
- RBA Stance: 0 (Neutral)
- BoJ Stance: +1 (Hawkish)
- China Growth: 0 (Stable)

---

## GC (Gold) - Weight 2 on Real Yields
| Factor | Raw Score | Weight | Weighted Score |
|--------|-----------|--------|----------------|
| Fed stance | +1 | 1 | +1 |
| Real yields | 0 | 2 | 0 |
| USD (DXY) | +1 | 1 | +1 |
| Risk mood | 0 | 1 | 0 |
| Growth | 0 | 1 | 0 |
| Oil supply | 0 | 1 | 0 |
| Gold ETF flows | +1 | 1 | +1 |
| **TOTAL** | | | **+3** |

**Signal:** BULLISH (+3 to +4)
**Confidence:** 7/10 (good data quality, clear drivers)

---

## SI (Silver)
| Factor | Raw Score | Weight | Weighted Score |
|--------|-----------|--------|----------------|
| Fed stance | +1 | 1 | +1 |
| Real yields | 0 | 1 | 0 |
| USD (DXY) | +1 | 1 | +1 |
| Risk mood | 0 | 1 | 0 |
| Growth | 0 | 1 | 0 |
| Copper | +1 | 1 | +1 |
| Gold ETF flows | +1 | 1 | +1 |
| **TOTAL** | | | **+4** |

**Signal:** BULLISH (+3 to +4)
**Confidence:** 7/10 (industrial + precious hybrid showing strength)

---

## CL (WTI Crude) - Weight 2 on Oil Supply and Growth
| Factor | Raw Score | Weight | Weighted Score |
|--------|-----------|--------|----------------|
| Oil supply shock | 0 | 2 | 0 |
| Inventories | +1 | 1 | +1 |
| Growth | 0 | 2 | 0 |
| Geopolitical risk | +1 | 1 | +1 |
| USD (DXY) | +1 | 1 | +1 |
| **TOTAL** | | | **+3** |

**Signal:** BULLISH (+3 to +4)
**Confidence:** 6/10 (inventory draw supportive, but growth stable)

---

## ES (S&P 500) - Weight 2 on Real Yields
| Factor | Raw Score | Weight | Weighted Score |
|--------|-----------|--------|----------------|
| Fed stance | +1 | 1 | +1 |
| Real yields | 0 | 2 | 0 |
| USD (DXY) | +1 | 1 | +1 |
| Risk mood | 0 | 1 | 0 |
| Growth | 0 | 1 | 0 |
| Credit spreads | +1 | 1 | +1 |
| VIX direction | +1 | 1 | +1 |
| **TOTAL** | | | **+4** |

**Signal:** BULLISH (+3 to +4)
**Confidence:** 7/10 (dovish Fed, narrowing spreads, VIX falling)

---

## NQ (Nasdaq 100) - Weight 2 on Real Yields
| Factor | Raw Score | Weight | Weighted Score |
|--------|-----------|--------|----------------|
| Fed stance | +1 | 1 | +1 |
| Real yields | 0 | 2 | 0 |
| USD (DXY) | +1 | 1 | +1 |
| Risk mood | 0 | 1 | 0 |
| Growth | 0 | 1 | 0 |
| SOX | +1 | 1 | +1 |
| MOVE | 0 | 1 | 0 |
| **TOTAL** | | | **+3** |

**Signal:** BULLISH (+3 to +4)
**Confidence:** 7/10 (semis strong, Fed dovish)

---

## YM (Dow Jones) - Weight 2 on Growth
| Factor | Raw Score | Weight | Weighted Score |
|--------|-----------|--------|----------------|
| Fed stance | +1 | 1 | +1 |
| Real yields | 0 | 1 | 0 |
| USD (DXY) | +1 | 1 | +1 |
| Risk mood | 0 | 1 | 0 |
| Growth | 0 | 2 | 0 |
| Credit spreads | +1 | 1 | +1 |
| 2s10s curve | +1 | 1 | +1 |
| **TOTAL** | | | **+4** |

**Signal:** BULLISH (+3 to +4)
**Confidence:** 7/10 (curve steepening, credit healthy)

---

## RTY (Russell 2000) - Weight 2 on Growth and Credit Spreads
| Factor | Raw Score | Weight | Weighted Score |
|--------|-----------|--------|----------------|
| Fed stance | +1 | 1 | +1 |
| Real yields | 0 | 1 | 0 |
| USD (DXY) | +1 | 1 | +1 |
| Risk mood | 0 | 1 | 0 |
| Growth | 0 | 2 | 0 |
| Credit spreads | +1 | 2 | +2 |
| 2s10s curve | +1 | 1 | +1 |
| **TOTAL** | | | **+5** |

**Signal:** STRONG_BULLISH (≥+5)
**Confidence:** 8/10 (credit spreads narrowing is key for small caps)

---

## M6E (Euro) - Weight 2 on Rate Differential
| Factor | Raw Score | Weight | Weighted Score |
|--------|-----------|--------|----------------|
| Fed stance | +1 | 1 | +1 |
| ECB stance | 0 | 1 | 0 |
| Rate differential (EUR-USD) | 0 | 2 | 0 |
| USD (DXY) | +1 | 1 | +1 |
| Risk mood | 0 | 1 | 0 |
| Eurozone growth | 0 | 1 | 0 |
| **TOTAL** | | | **+2** |

**Signal:** SLIGHT_BULLISH (+1 to +2)
**Confidence:** 6/10 (weak USD supportive, but rate differentials neutral)

---

## 6A (Australian Dollar) - Weight 2 on Risk Sentiment and China Growth
| Factor | Raw Score | Weight | Weighted Score |
|--------|-----------|--------|----------------|
| Fed stance | +1 | 1 | +1 |
| RBA stance | 0 | 1 | 0 |
| Rate differential (AUD-USD) | 0 | 1 | 0 |
| USD (DXY) | +1 | 1 | +1 |
| Risk sentiment | 0 | 2 | 0 |
| China growth | 0 | 2 | 0 |
| Copper | +1 | 1 | +1 |
| **TOTAL** | | | **+3** |

**Signal:** BULLISH (+3 to +4)
**Confidence:** 6/10 (copper supportive, but China growth neutral)

---

## 6J (Japanese Yen) - Weight 2 on BoJ Stance and Rate Differential
| Factor | Raw Score | Weight | Weighted Score |
|--------|-----------|--------|----------------|
| Fed stance | +1 | 1 | +1 |
| BoJ stance | +1 | 2 | +2 |
| Rate differential (JPY-USD) | +1 | 2 | +2 |
| USD (DXY) | +1 | 1 | +1 |
| Risk mood | 0 | 1 | 0 |
| **TOTAL** | | | **+6** |

**Signal:** STRONG_BEARISH (≤-6) 
**WAIT - ERROR IN INTERPRETATION!**

**CORRECTION:** For 6J, the scoring should reflect JPY strength = bullish 6J
- BoJ hawkish = JPY strength = bullish 6J = positive score
- But we need to check if rate differential widening (JPY-USD) means JPY getting stronger

Actually, reviewing methodology:
- Rate differential widening vs USD = positive for the foreign currency
- BoJ hawkish = JPY strength = positive for 6J
- Risk-off would be positive for JPY (safe haven)

Let me recalculate with correct interpretation:
- Fed dovish = negative for USD = positive for JPY = +1 for 6J
- BoJ hawkish = positive for JPY = +1 raw score × 2 weight = +2
- Rate differential: BoJ tightening while Fed dovish = differential widening in JPY favor = +1 × 2 = +2
- USD weak = positive for JPY = +1
- Risk mood balanced = 0

**TOTAL: +6**
**Signal:** STRONG_BULLISH (≥+5)
**Confidence:** 7/10 (BoJ divergence is clear driver)

---

## Asset Class Aggregation

### COMMODITIES (GC, SI, CL)
- GC: +3 (BULLISH)
- SI: +4 (BULLISH)
- CL: +3 (BULLISH)
- **Result:** 3/3 bullish → **BULLISH**

### INDICES (ES, NQ, YM, RTY)
- ES: +4 (BULLISH)
- NQ: +3 (BULLISH)
- YM: +4 (BULLISH)
- RTY: +5 (STRONG_BULLISH)
- **Result:** 4/4 bullish → **BULLISH**

### FX (M6E, 6A, 6J)
- M6E: +2 (SLIGHT_BULLISH)
- 6A: +3 (BULLISH)
- 6J: +6 (STRONG_BULLISH)
- **Result:** 3/3 bullish → **BULLISH**

---

## Key Drivers
1. Fed dovish hold with dissent for cuts supporting risk assets and weakening USD
2. Credit spreads narrowing and VIX falling signal improving risk appetite
3. Commodity strength across metals and energy with inventory draws and rising copper
4. BoJ policy divergence creating strong JPY bid
5. Curve steepening and stable growth supporting cyclical positioning
