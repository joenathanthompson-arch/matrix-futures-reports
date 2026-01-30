# Manus Bias Scoring Comparison: Conservative vs. Recalibrated

**Date:** January 29, 2026  
**Purpose:** Compare current conservative scoring with proposed recalibrated scoring  
**Goal:** Show how using the full score range improves system differentiation

---

## Executive Summary

**Problem Identified:**
- Current scores cluster in +1 to +5 range (25% of available range)
- 9 out of 10 instruments map to the same environment code (12 - LONG_BIAS)
- System lacks differentiation between instruments

**Proposed Solution:**
- Recalibrate scoring to use full -8 to +8 range
- Apply confidence-based amplification
- More aggressive weighting for key factors
- Better differentiation → better trading decisions

---

## Scoring Philosophy Comparison

### Current Conservative Approach

| Score | Meaning | Frequency | Psychology |
|-------|---------|-----------|------------|
| +8 to +10 | "Perfect" setup | Almost never | Afraid to overstate |
| +6 to +7 | "Exceptional" setup | Rare | Reserved for unicorns |
| +4 to +5 | "Very good" setup | Occasional | This is my "A grade" |
| +2 to +3 | "Good" setup | Common | This is my "B grade" |
| +1 | "Slight edge" | Very common | This is my "C grade" |

**Result:** Grade inflation in reverse - treating scores like academic grades, not trading signals.

### Proposed Recalibrated Approach

| Score | Meaning | Frequency | Psychology |
|-------|---------|-----------|------------|
| +8 to +10 | Exceptional conviction, max size | Rare (1-2x/month) | All factors aligned + catalyst + high confidence |
| +6 to +7 | Strong conviction, larger size | Occasional (1-2x/week) | Most factors aligned + good confidence |
| +4 to +5 | Good conviction, normal size | Common (2-3x/week) | Clear edge, some mixed signals |
| +2 to +3 | Slight edge, reduced size | Common (daily) | Weak edge, multiple conflicts |
| +1 | Minimal edge, small size | Very common | One factor supporting |

**Result:** Scores reflect trading conviction, not academic perfection.

---

## Instrument-by-Instrument Comparison

### 1. GC (Gold)

#### Current Conservative Scoring

```
Factor                Weight   Raw   Weighted
Fed stance            1        0     0
Real yields           2        0     0
USD                   1        +1    +1
Risk mood             1        0     0
Growth                1        -1    -1
Oil supply            1        0     0
Gold ETFs             1        +1    +1
                              TOTAL: +1

Score: +1
Signal: SLIGHT_BULLISH
Confidence: 7/10
Env Code: 12 (LONG_BIAS)
```

**Rationale:** Mixed signals (USD weak but growth strong), no strong catalyst.

#### Recalibrated Scoring

```
Factor                Weight   Raw   Weighted   Notes
Fed stance            1        0     0          Neutral (no change)
Real yields           2        0     0          Flat (no change)
USD                   1        +1    +1         Weak USD (no change)
Risk mood             1        0     0          Neutral (no change)
Growth                1        -1    -1         Strong growth (no change)
Gold ETFs             2        +1    +2         ← INCREASED WEIGHT (was 1)
Geopolitical          1        +1    +1         ← ADDED FACTOR
                              TOTAL: +2

Score: +2
Signal: SLIGHT_BULLISH
Confidence: 7/10
Env Code: 12 (LONG_BIAS)
```

**Changes:**
- Increased ETF flows weight from 1 to 2 (strong inflows are key driver)
- Added geopolitical factor (+1 from Iran tensions)
- **Result:** +1 → +2 (still LONG_BIAS, but stronger)

**Verdict:** This one is probably correct as-is. Gold has mixed signals, so +2 is appropriate.

---

### 2. SI (Silver)

#### Current Conservative Scoring

```
TOTAL SI: +2
Score: +2
Signal: SLIGHT_BULLISH
Confidence: 6/10
Env Code: 12 (LONG_BIAS)
```

#### Recalibrated Scoring

```
Factor                Weight   Raw   Weighted   Notes
Fed stance            1        0     0          
Real yields           1        0     0          
USD                   1        +1    +1         
Risk mood             1        0     0          
Growth                1        -1    -1         
Copper                2        +1    +2         ← INCREASED WEIGHT (was 1)
Gold ETFs             1        +1    +1         
                              TOTAL: +3

Score: +3
Signal: BULLISH
Confidence: 6/10
Env Code: 12 (LONG_BIAS)
```

**Changes:**
- Increased copper weight from 1 to 2 (industrial demand key for silver)
- **Result:** +2 → +3 (still LONG_BIAS but stronger conviction)

**Verdict:** Minor improvement, still appropriate range.

---

### 3. CL (WTI Crude)

#### Current Conservative Scoring

```
TOTAL CL: +1
Score: +1
Signal: SLIGHT_BULLISH
Confidence: 6/10
Env Code: 12 (LONG_BIAS)
```

#### Recalibrated Scoring

```
Factor                Weight   Raw   Weighted   Notes
Oil supply shock      2        +1    +2         Geopolitical risk
Inventories           1        -1    -1         Bearish
Growth narrative      2        -1    -2         Strong growth = less urgency
Geopolitical risk     1        +1    +1         Iran tensions
USD                   1        +1    +1         
                              TOTAL: +1

Score: +1
Signal: SLIGHT_BULLISH
Confidence: 6/10
Env Code: 12 (LONG_BIAS)
```

**Changes:**
- No changes needed - genuinely mixed signals
- **Result:** +1 (appropriate)

**Verdict:** Correct as-is.

---

### 4. ES (S&P 500)

#### Current Conservative Scoring

```
TOTAL ES: +1
Score: +1
Signal: SLIGHT_BULLISH
Confidence: 6/10
Env Code: 12 (LONG_BIAS)
```

#### Recalibrated Scoring

```
Factor                Weight   Raw   Weighted   Notes
Fed stance            1        0     0          
Real yields           2        0     0          
USD                   1        +1    +1         
Risk mood             1        0     0          
Growth narrative      1        -1    -1         
Credit spreads        2        +1    +2         ← INCREASED WEIGHT (was 1)
VIX direction         1        0     0          
                              TOTAL: +2

Score: +2
Signal: SLIGHT_BULLISH
Confidence: 6/10
Env Code: 12 (LONG_BIAS)
```

**Changes:**
- Increased credit spreads weight from 1 to 2 (HY spreads at 2.71% = very supportive)
- **Result:** +1 → +2 (still LONG_BIAS, slightly stronger)

**Verdict:** Minor improvement.

---

### 5. NQ (Nasdaq 100)

#### Current Conservative Scoring

```
TOTAL NQ: +2
Score: +2
Signal: SLIGHT_BULLISH
Confidence: 7/10
Env Code: 12 (LONG_BIAS)
```

#### Recalibrated Scoring

```
Factor                Weight   Raw   Weighted   Notes
Fed stance            1        0     0          
Real yields           2        0     0          
USD                   1        +1    +1         
Risk mood             1        0     0          
Growth narrative      1        -1    -1         
SOX                   2        +1    +2         ← INCREASED WEIGHT (was 1)
MOVE                  1        +1    +1         
                              TOTAL: +3

PLUS Confidence Boost:
- Confidence 7/10 (good)
- SOX very strong (key driver)
- Multiply by 1.2: +3 × 1.2 = +3.6 → round to +4

Score: +4
Signal: BULLISH
Confidence: 7/10
Env Code: 12 (LONG_BIAS)
```

**Changes:**
- Increased SOX weight from 1 to 2 (semiconductors are THE key driver for NQ)
- Applied confidence boost (7/10 = good conviction)
- **Result:** +2 → +4 (still LONG_BIAS but much stronger)

**Verdict:** Better reflects tech sector strength.

---

### 6. YM (Dow Jones)

#### Current Conservative Scoring

```
TOTAL YM: +1
Score: +1
Signal: SLIGHT_BULLISH
Confidence: 6/10
Env Code: 12 (LONG_BIAS)
```

#### Recalibrated Scoring

```
Factor                Weight   Raw   Weighted   Notes
Fed stance            1        0     0          
Real yields           1        0     0          
USD                   1        +1    +1         
Risk mood             1        0     0          
Growth narrative      2        -1    -2         
Credit spreads        1        +1    +1         
2s10s curve           2        +1    +2         ← INCREASED WEIGHT (was 1)
                              TOTAL: +2

Score: +2
Signal: SLIGHT_BULLISH
Confidence: 6/10
Env Code: 12 (LONG_BIAS)
```

**Changes:**
- Increased curve weight from 1 to 2 (steepening curve is key for value stocks)
- **Result:** +1 → +2 (still LONG_BIAS, slightly stronger)

**Verdict:** Minor improvement.

---

### 7. RTY (Russell 2000)

#### Current Conservative Scoring

```
TOTAL RTY: +2
Score: +2
Signal: SLIGHT_BULLISH
Confidence: 6/10
Env Code: 12 (LONG_BIAS)
```

#### Recalibrated Scoring

```
Factor                Weight   Raw   Weighted   Notes
Fed stance            1        0     0          
Real yields           1        0     0          
USD                   1        +1    +1         
Risk mood             1        0     0          
Growth narrative      2        -1    -2         
Credit spreads        3        +1    +3         ← INCREASED WEIGHT (was 2)
2s10s curve           1        +1    +1         
                              TOTAL: +3

Score: +3
Signal: BULLISH
Confidence: 6/10
Env Code: 12 (LONG_BIAS)
```

**Changes:**
- Increased credit spreads weight from 2 to 3 (HY spreads are THE key driver for small caps)
- **Result:** +2 → +3 (still LONG_BIAS but stronger)

**Verdict:** Better reflects credit-driven small cap rally.

---

### 8. M6E (Micro Euro FX)

#### Current Conservative Scoring

```
TOTAL M6E: +1
Score: +1
Signal: SLIGHT_BULLISH
Confidence: 5/10
Env Code: 12 (LONG_BIAS)
```

#### Recalibrated Scoring

```
Factor                Weight   Raw   Weighted   Notes
Fed stance            1        0     0          
ECB stance            1        -1    -1         ← CHANGED (ECB concerned about strong EUR)
Rate differential     2        0     0          
USD                   1        +1    +1         
Risk mood             1        0     0          
Eurozone growth       1        0     0          
                              TOTAL: 0

Score: 0
Signal: NEUTRAL
Confidence: 5/10
Env Code: 30 (NEUTRAL)
```

**Changes:**
- Changed ECB stance from 0 to -1 (ECB verbally concerned about strong EUR)
- **Result:** +1 → 0 (NEUTRAL instead of LONG_BIAS)

**Verdict:** More accurate - EUR is purely USD-driven with ECB pushback.

---

### 9. 6A (Australian Dollar) ⭐ MAJOR CHANGE

#### Current Conservative Scoring

```
TOTAL 6A: +4
Score: +4
Signal: BULLISH
Confidence: 7/10
Env Code: 12 (LONG_BIAS)
```

**Issue:** This should be LONGS_ONLY (code 10), not LONG_BIAS (code 12).

#### Recalibrated Scoring

```
Factor                Weight   Raw   Weighted   Notes
Fed stance            1        0     0          
RBA stance            2        +1    +2         ← INCREASED WEIGHT (was 1)
Rate differential     2        +1    +2         ← INCREASED WEIGHT (was 1)
USD                   1        +1    +1         
Risk sentiment        2        0     0          
China growth          2        0     0          
Copper                2        +1    +2         ← INCREASED WEIGHT (was 1)
                              TOTAL: +7

PLUS Confidence Boost:
- Confidence 7/10 (good)
- RBA hiking Feb 3 (imminent catalyst)
- Multiply by 1.1: +7 × 1.1 = +7.7 → round to +8

Score: +8
Signal: STRONG_BULLISH
Confidence: 7/10
Env Code: 14 (MAX_LONG)
```

**Changes:**
- Increased RBA stance weight from 1 to 2 (RBA is THE key driver)
- Increased rate differential weight from 1 to 2 (divergence is key)
- Increased copper weight from 1 to 2 (AUD is commodity currency)
- Applied confidence boost (7/10 + imminent catalyst)
- **Result:** +4 → +8 (MAX_LONG instead of LONG_BIAS)

**Verdict:** THIS IS THE BIG ONE. RBA hiking Feb 3 with copper strong and USD weak is a MAX_LONG setup.

---

### 10. 6J (Japanese Yen) ⭐ MAJOR CHANGE

#### Current Conservative Scoring

```
TOTAL 6J: +5
Score: +5
Signal: STRONG_BULLISH
Confidence: 8/10
Env Code: 10 (LONGS_ONLY)
```

**Issue:** This should be higher given the conviction.

#### Recalibrated Scoring

```
Factor                Weight   Raw   Weighted   Notes
Fed stance            1        0     0          
BoJ stance            3        +1    +3         ← INCREASED WEIGHT (was 2)
Rate differential     3        +1    +3         ← INCREASED WEIGHT (was 2)
USD                   1        +1    +1         
Risk mood             1        0     0          
                              TOTAL: +7

PLUS Confidence Boost:
- Confidence 8/10 (high)
- All factors aligned
- Fresh data (BoJ meeting Jan 22-23)
- Multiply by 1.2: +7 × 1.2 = +8.4 → round to +8

Score: +8
Signal: STRONG_BULLISH
Confidence: 8/10
Env Code: 14 (MAX_LONG)
```

**Changes:**
- Increased BoJ stance weight from 2 to 3 (BoJ is THE key driver)
- Increased rate differential weight from 2 to 3 (historic shift)
- Applied confidence boost (8/10 = high conviction)
- **Result:** +5 → +8 (MAX_LONG instead of LONGS_ONLY)

**Verdict:** THIS IS THE OTHER BIG ONE. BoJ hawkish turn is historic - deserves max conviction.

---

## Summary Comparison Table

| Symbol | Old Score | Old Code | Old Signal | New Score | New Code | New Signal | Change |
|--------|-----------|----------|------------|-----------|----------|------------|--------|
| **GC** | +1 | 12 | SLIGHT_BULLISH | +2 | 12 | SLIGHT_BULLISH | Minor ↑ |
| **SI** | +2 | 12 | SLIGHT_BULLISH | +3 | 12 | BULLISH | Minor ↑ |
| **CL** | +1 | 12 | SLIGHT_BULLISH | +1 | 12 | SLIGHT_BULLISH | No change |
| **ES** | +1 | 12 | SLIGHT_BULLISH | +2 | 12 | SLIGHT_BULLISH | Minor ↑ |
| **NQ** | +2 | 12 | SLIGHT_BULLISH | +4 | 12 | BULLISH | Moderate ↑ |
| **YM** | +1 | 12 | SLIGHT_BULLISH | +2 | 12 | SLIGHT_BULLISH | Minor ↑ |
| **RTY** | +2 | 12 | SLIGHT_BULLISH | +3 | 12 | BULLISH | Minor ↑ |
| **M6E** | +1 | 12 | SLIGHT_BULLISH | 0 | 30 | NEUTRAL | ↓ to neutral |
| **6A** | +4 | 12 | BULLISH | **+8** | **14** | **STRONG_BULLISH** | **MAJOR ↑** |
| **6J** | +5 | 10 | STRONG_BULLISH | **+8** | **14** | **STRONG_BULLISH** | **MAJOR ↑** |

---

## Environment Code Distribution

### Current Conservative (Old)

| Env Code | Name | Count | Symbols |
|----------|------|-------|---------|
| 12 | LONG_BIAS | **9** | GC, SI, CL, ES, NQ, YM, RTY, M6E, 6A |
| 10 | LONGS_ONLY | 1 | 6J |

**Problem:** 90% of instruments get identical treatment.

### Recalibrated (New)

| Env Code | Name | Count | Symbols |
|----------|------|-------|---------|
| 30 | NEUTRAL | 1 | M6E |
| 12 | LONG_BIAS | 6 | GC, SI, CL, ES, YM, NQ, RTY |
| 14 | MAX_LONG | 2 | **6A, 6J** |

**Improvement:** Better differentiation with 3 distinct environment codes.

---

## Impact on Trading Decisions

### Without Recalibration (Current)

```
All 9 instruments → LONG_BIAS (code 12)
- Same position sizing
- Same risk allocation
- No differentiation between GC (+1, conf 7) and 6A (+4, conf 7)
```

### With Recalibration (Proposed)

```
M6E → NEUTRAL (code 30)
  - Trade based on technicals only
  - No macro edge

GC, SI, CL, ES, YM, NQ, RTY → LONG_BIAS (code 12)
  - Normal long bias
  - With confidence-based sizing:
    * GC (+2, conf 7): 1.0x size
    * NQ (+4, conf 7): 1.0x size

6A, 6J → MAX_LONG (code 14)
  - Aggressive long positioning
  - 1.5x size modifier from CSV
  - Plus confidence boost:
    * 6A (+8, conf 7): 1.5x × 1.0 = 1.5x total
    * 6J (+8, conf 8): 1.5x × 1.25 = 1.875x total
```

**Result:** Capital allocated more efficiently to highest conviction trades.

---

## Recalibration Rules Applied

### Rule 1: Increase Key Factor Weights

**Old approach:** Most factors 1x, some 2x  
**New approach:** Key drivers 2x to 3x

**Examples:**
- BoJ stance for JPY: 2x → 3x
- RBA stance for AUD: 1x → 2x
- Credit spreads for RTY: 2x → 3x
- SOX for NQ: 1x → 2x

### Rule 2: Apply Confidence-Based Amplification

**Formula:**
```
If confidence >= 8: multiply score by 1.2
If confidence >= 7: multiply score by 1.1
If confidence >= 6: no change
If confidence <= 5: multiply score by 0.9
```

**Applied to:**
- 6J: +7 × 1.2 = +8.4 → +8
- 6A: +7 × 1.1 = +7.7 → +8
- NQ: +3 × 1.2 = +3.6 → +4

### Rule 3: Reduce Conservative Bias

**Old mindset:** "Is this really a +7? Better make it +5 to be safe."  
**New mindset:** "All factors aligned + high confidence = +7 or +8."

**Applied to:**
- 6J: Was +5, now +8 (stopped being conservative)
- 6A: Was +4, now +8 (stopped being conservative)

### Rule 4: Account for Negative Factors

**Old approach:** Ignored some negative factors  
**New approach:** Include ECB concerns, conflicting signals

**Applied to:**
- M6E: Added ECB concern (-1), dropped from +1 to 0

---

## Expected Score Distribution (After Recalibration)

### Over 1-2 Weeks

| Score Range | Frequency | Environment Code | Example Setups |
|-------------|-----------|------------------|----------------|
| **+8 to +10** | 1-2x per week | 14 (MAX_LONG) | All aligned + catalyst + conf 8+ |
| **+6 to +7** | 2-3x per week | 14 (MAX_LONG) or 10 (LONGS_ONLY) | Most aligned + conf 7+ |
| **+4 to +5** | Daily | 10 (LONGS_ONLY) or 12 (LONG_BIAS) | Clear edge + conf 6+ |
| **+2 to +3** | Daily | 12 (LONG_BIAS) | Weak edge + mixed signals |
| **+1** | Daily | 12 (LONG_BIAS) | Minimal edge |
| **0** | Occasional | 30 (NEUTRAL) | No macro edge |
| **-1 to -8** | Mirror of above | Bearish codes | |

**Goal:** Use full range, not just +1 to +5.

---

## Risk Considerations

### Potential Concerns

**1. Over-trading high conviction setups**
- **Mitigation:** Confidence threshold (< 4 = don't trade)
- **Mitigation:** Size limits in PM (max 1.5x from CSV)

**2. Missing subtle edges**
- **Mitigation:** Still score +1 and +2 for weak edges
- **Mitigation:** Confidence-based sizing allows small positions

**3. Whipsaw on recalibrated scores**
- **Mitigation:** Monitor for 1-2 weeks before finalizing
- **Mitigation:** Can revert if distribution is wrong

### Benefits Outweigh Risks

**Benefits:**
- Better capital allocation (more to 6A/6J, less to M6E)
- System differentiation (3 codes instead of 1)
- Aligned with trading conviction (not academic grading)

**Risks:**
- Temporary adjustment period
- Need to monitor score distribution

---

## Implementation Plan

### Phase 1: Test Recalibration (1 Week)

1. Generate reports with both old and new scores
2. Compare environment code distribution
3. Monitor if scores are too aggressive or still too conservative
4. Adjust weights if needed

### Phase 2: Implement Confidence Sizing (Parallel)

1. Claude implements confidence → size modifier in PM
2. Test with recalibrated scores
3. Verify position sizing makes sense

### Phase 3: Go Live (After 1 Week)

1. Switch to recalibrated scoring permanently
2. Monitor score distribution over 2-4 weeks
3. Fine-tune weights based on real-world results

---

## Questions for Discussion

### 1. Are the recalibrated scores too aggressive?

**Specifically:**
- Is 6A at +8 (MAX_LONG) appropriate for RBA hiking Feb 3?
- Is 6J at +8 (MAX_LONG) appropriate for BoJ hawkish turn?
- Or should they be +6 or +7 instead?

### 2. Should confidence amplification be applied?

**Current proposal:**
- Confidence 8+ → multiply score by 1.2
- Confidence 7 → multiply score by 1.1
- Confidence 6 → no change

**Alternative:**
- Skip amplification, just use increased weights

### 3. How often should we expect +7 or +8 scores?

**Proposed:** 1-2x per week  
**Too frequent?** Should it be 1-2x per month?

### 4. Should M6E really be 0 (NEUTRAL)?

**Current:** +1 (LONG_BIAS)  
**Proposed:** 0 (NEUTRAL) due to ECB concerns

**Question:** Is this too harsh? Should it stay at +1?

---

## Next Steps

1. **User + Claude review this comparison**
2. **Decide on:**
   - Are recalibrated scores appropriate?
   - Should confidence amplification be used?
   - Any adjustments needed?
3. **Manus implements changes** for tomorrow's report (Jan 30)
4. **Monitor for 1 week** and adjust if needed

---

## Appendix: Full Recalibrated Scoring Breakdown

### GC (Gold): +2

```
Factor                Weight   Raw   Weighted
Fed stance            1        0     0
Real yields           2        0     0
USD                   1        +1    +1
Risk mood             1        0     0
Growth                1        -1    -1
Gold ETFs             2        +1    +2
Geopolitical          1        +1    +1
                              TOTAL: +2
```

### SI (Silver): +3

```
Factor                Weight   Raw   Weighted
Fed stance            1        0     0
Real yields           1        0     0
USD                   1        +1    +1
Risk mood             1        0     0
Growth                1        -1    -1
Copper                2        +1    +2
Gold ETFs             1        +1    +1
                              TOTAL: +3
```

### CL (WTI Crude): +1

```
Factor                Weight   Raw   Weighted
Oil supply shock      2        +1    +2
Inventories           1        -1    -1
Growth narrative      2        -1    -2
Geopolitical risk     1        +1    +1
USD                   1        +1    +1
                              TOTAL: +1
```

### ES (S&P 500): +2

```
Factor                Weight   Raw   Weighted
Fed stance            1        0     0
Real yields           2        0     0
USD                   1        +1    +1
Risk mood             1        0     0
Growth narrative      1        -1    -1
Credit spreads        2        +1    +2
VIX direction         1        0     0
                              TOTAL: +2
```

### NQ (Nasdaq 100): +4

```
Factor                Weight   Raw   Weighted
Fed stance            1        0     0
Real yields           2        0     0
USD                   1        +1    +1
Risk mood             1        0     0
Growth narrative      1        -1    -1
SOX                   2        +1    +2
MOVE                  1        +1    +1
                              TOTAL: +3

Confidence boost: +3 × 1.2 = +3.6 → +4
```

### YM (Dow Jones): +2

```
Factor                Weight   Raw   Weighted
Fed stance            1        0     0
Real yields           1        0     0
USD                   1        +1    +1
Risk mood             1        0     0
Growth narrative      2        -1    -2
Credit spreads        1        +1    +1
2s10s curve           2        +1    +2
                              TOTAL: +2
```

### RTY (Russell 2000): +3

```
Factor                Weight   Raw   Weighted
Fed stance            1        0     0
Real yields           1        0     0
USD                   1        +1    +1
Risk mood             1        0     0
Growth narrative      2        -1    -2
Credit spreads        3        +1    +3
2s10s curve           1        +1    +1
                              TOTAL: +3
```

### M6E (Micro Euro FX): 0

```
Factor                Weight   Raw   Weighted
Fed stance            1        0     0
ECB stance            1        -1    -1
Rate differential     2        0     0
USD                   1        +1    +1
Risk mood             1        0     0
Eurozone growth       1        0     0
                              TOTAL: 0
```

### 6A (Australian Dollar): +8

```
Factor                Weight   Raw   Weighted
Fed stance            1        0     0
RBA stance            2        +1    +2
Rate differential     2        +1    +2
USD                   1        +1    +1
Risk sentiment        2        0     0
China growth          2        0     0
Copper                2        +1    +2
                              TOTAL: +7

Confidence boost: +7 × 1.1 = +7.7 → +8
```

### 6J (Japanese Yen): +8

```
Factor                Weight   Raw   Weighted
Fed stance            1        0     0
BoJ stance            3        +1    +3
Rate differential     3        +1    +3
USD                   1        +1    +1
Risk mood             1        0     0
                              TOTAL: +7

Confidence boost: +7 × 1.2 = +8.4 → +8
```

---

**End of Comparison Document**
