# Manus AI Bias Scoring Methodology - Clarifications & Updates

**Date:** January 29, 2026  
**Purpose:** Document clarifications from 3-way collaboration (User, Manus AI, Claude AI)  
**Context:** Matrix Futures System Review

---

## Table of Contents

1. [Overview: How Manus Scores Flow Through the System](#overview)
2. [Score vs. Signal vs. Confidence - Definitions](#definitions)
3. [Confidence Scoring Methodology](#confidence-methodology)
4. [Current Score Distribution Issue](#score-distribution-issue)
5. [Confidence → Position Sizing Recommendation](#confidence-sizing)
6. [Questions for Further Discussion](#questions)

---

## Overview: How Manus Scores Flow Through the System {#overview}

```
Manus AI (Fundamental Analysis)
    ↓
GitHub: latest.json
    {
      "scores": {
        "GC": {"score": 1, "signal": "SLIGHT_BULLISH", "confidence": 7}
      }
    }
    ↓
PM: ParseBiasScores() extracts:
    - biasScore (integer: -10 to +10)
    - biasSignal (string: "BULLISH", "BEARISH", "NEUTRAL")
    - confidence (integer: 1-10)
    ↓
PM: DetermineStrategy() maps:
    - score → envCode (0-99 from CSV)
    - signal → biasTrend ("long", "short", "neutral")
    ↓
PM: PublishStrategyToGlobals()
    - PM_[SYM]_ENV_CODE
    - PM_[SYM]_TREND
    - PM_[SYM]_CONVICTION (raw score)
    ↓
Traders: Read PM globals and execute
```

---

## Score vs. Signal vs. Confidence - Definitions {#definitions}

### **Score** (Integer: -10 to +10)

**What it is:** Numeric magnitude of directional bias

**How it's calculated:**
- Sum of weighted factor scores
- Example: GC (Gold) = Fed(+1) + RealYields(0×2) + USD(+1) + Risk(0) + Growth(-1) + Oil(0) + ETFs(+1) = **+1**

**What it determines:**
- Environment code (via CSV mapping)
- Strength of conviction

**Range in practice:**
- Theoretical: -10 to +10
- Actual (today): -3 to +6
- **Issue:** Not using full range → all instruments map to similar codes

### **Signal** (String: "BULLISH", "BEARISH", "NEUTRAL")

**What it is:** Qualitative directional label

**How it's determined:**
- Mapped from score using thresholds:
  - ≥ +5: STRONG_BULLISH
  - +3 to +4: BULLISH
  - +1 to +2: SLIGHT_BULLISH
  - -1 to +1: NEUTRAL
  - -2 to -3: SLIGHT_BEARISH
  - -4 to -5: BEARISH
  - ≤ -6: STRONG_BEARISH

**What it determines:**
- Trend direction in PM: "long", "short", "neutral"
- Human-readable label for Telegram messages

### **Confidence** (Integer: 1-10)

**What it is:** Manus's conviction in the score based on data quality and signal clarity

**What it determines:**
- **Currently:** Stored but NOT used in trading decisions
- **Should determine:** Position sizing (see section below)

**Common misconception:** "Confidence = how many sources validate the data"
- **Reality:** It's about data freshness, signal alignment, and event risk (see next section)

---

## Confidence Scoring Methodology {#confidence-methodology}

### Three Factors That Determine Confidence

#### 1. **Data Freshness** (Most Important)

| Data Age | Confidence Impact | Example |
|----------|-------------------|---------|
| < 24 hours | No penalty | Real-time VIX, DXY |
| 1-2 days old | -1 to -2 points | FRED data (common) |
| > 2 days old | -2 to -3 points | Stale economic data |

**Why it matters:** Stale data means my score might be based on outdated conditions.

#### 2. **Signal Clarity** (Factor Alignment)

| Condition | Confidence Range | Example |
|-----------|------------------|---------|
| All factors aligned | 8-10 | 6J today: All bullish |
| Some conflicting | 6-7 | GC today: Mixed signals |
| Many conflicting | 4-5 | M6E today: USD weak but ECB concerned |
| Extreme conflict | 1-3 | Don't trade |

**Why it matters:** Conflicting signals mean the macro picture is unclear.

#### 3. **Catalyst Proximity** (Event Risk)

| Situation | Confidence Impact | Example |
|-----------|-------------------|---------|
| Far from events | No penalty | Normal trading days |
| Pre-FOMC/CPI/NFP | -1 to -2 points | Week before major data |
| Immediate post-event | -1 to -2 points | Day after surprise move |

**Why it matters:** Major events can invalidate my analysis instantly.

### Confidence Scoring Examples from Today's Report (Jan 29, 2026)

#### **High Confidence: 6J (Japanese Yen) = 8/10**

```
Score: +5 (STRONG_BULLISH)
Confidence: 8/10

Why 8/10?
✓ Data freshness: All current (BoJ meeting Jan 22-23)
✓ Signal clarity: ALL factors aligned bullish
  - Fed dovish: +1
  - BoJ hawkish: +1 (weighted 2x = +2)
  - Rate differential: +1 (weighted 2x = +2)
  - USD weak: +1
  - Risk mood: 0
  - Total: +6 (strong conviction)
✓ No major events imminent
✗ Minor deduction: Next BoJ meeting in March could shift

Result: High conviction trade
```

#### **Moderate Confidence: GC (Gold) = 7/10**

```
Score: +1 (SLIGHT_BULLISH)
Confidence: 7/10

Why 7/10?
✓ Data freshness: Good (ETF flows current, USD current)
✓ Most factors current
✗ Mixed signals:
  - USD weak (bullish) ✓
  - ETF inflows (bullish) ✓
  - Real yields flat (neutral) ○
  - Growth accelerating (bearish) ✗
✗ Geopolitical premium uncertain

Result: Good setup but not slam dunk
```

#### **Low Confidence: M6E (Euro) = 5/10**

```
Score: +1 (SLIGHT_BULLISH)
Confidence: 5/10

Why only 5/10?
✓ Data current
✗ Conflicting signals:
  - USD weak (bullish for EUR) BUT
  - ECB concerned about strong EUR (bearish)
  - Rate differentials neutral (no edge)
✗ Score driven by ONLY ONE factor (USD weakness)
✗ ECB meeting Feb 5 approaching (event risk)

Result: Edge exists but very uncertain
```

### When Confidence Drops to 1-3 (Don't Trade Territory)

Confidence 1-3 means one or more of:
- **Stale data:** Couldn't verify key sources
- **Pre-major event:** FOMC/CPI/NFP within 24-48 hours
- **Extreme conflict:** Factors pointing in opposite directions with equal weight
- **Data quality issues:** Multiple fallback sources used, still uncertain

**Example scenario (hypothetical):**
```
Pre-FOMC (day before decision):
- Score: +3 (bullish based on current data)
- Confidence: 3/10 (FOMC could reverse everything)
- Recommendation: Don't trade OR minimal size (0.25x)
```

---

## Current Score Distribution Issue {#score-distribution-issue}

### Problem: Narrow Score Range

**Today's scores (Jan 29, 2026):**
- GC: +1, SI: +2, CL: +1, ES: +1, NQ: +2, YM: +1, RTY: +2, M6E: +1, 6A: +4, 6J: +5

**Score distribution:**
- Range: +1 to +5 (only 5 points used)
- Theoretical range: -10 to +10 (20 points available)
- **Utilization: 25%**

### Impact on Environment Code Mapping

**CSV mapping (from PM_ENVIRONMENT_CODES.csv):**
```
Score +5 to +6  → Code 10 (LONGS_ONLY)
Score +3 to +4  → Code 12 (LONG_BIAS)
Score +1 to +2  → Code 12 (LONG_BIAS)
Score -1 to +1  → Code 30 (NEUTRAL)
```

**Result:**
- 9 out of 10 instruments → Code 12 (LONG_BIAS)
- 1 out of 10 instruments → Code 10 (LONGS_ONLY)
- **No differentiation between instruments**

### Why This Happens

**Manus scoring methodology uses conservative weights:**
- Most factors weighted 1x
- Only key factors weighted 2x (e.g., real yields for gold)
- Maximum possible score per instrument: typically +8 to +12
- Actual scores: much lower due to mixed signals

**Example: GC (Gold) today**
```
Factor                Weight   Raw   Weighted
Fed stance            1        +1    +1
Real yields           2         0     0
USD                   1        +1    +1
Risk mood             1         0     0
Growth                1        -1    -1
Oil supply            1         0     0
Gold ETFs             1        +1    +1
                              TOTAL: +2

But signal mapping: +2 → SLIGHT_BULLISH (not BULLISH)
```

### Potential Solutions

**Option A: Increase factor weights**
- Make more factors 2x or 3x weighted
- Risk: Over-sensitivity to single factors

**Option B: Adjust signal thresholds**
- Change mapping: +1 to +2 → Code 30 (NEUTRAL) instead of Code 12
- Forces higher scores to trigger directional bias
- Risk: Miss subtle edges

**Option C: Use confidence to amplify scores**
- High confidence → multiply score by 1.2-1.5x
- Low confidence → multiply score by 0.5-0.8x
- Example: 6J score +5 × confidence 0.8 (8/10) = +4 effective
- Risk: Complexity

**Option D: Expand score range artificially**
- Multiply all scores by 1.5x or 2x
- +2 becomes +3 or +4
- Risk: Loses granularity

**Recommendation:** Discuss with user which approach aligns with trading philosophy.

---

## Confidence → Position Sizing Recommendation {#confidence-sizing}

### Current State

**Confidence is calculated but NOT used in trading decisions.**

From PM code (line 1753):
```cpp
int confidence = ExtractJsonInt(symbolBlock, "confidence");
g_symbols[i].drivers = "Confidence: " + IntegerToString(confidence) + "/10";
```

It's stored as a string in `drivers` but not used for sizing or trade decisions.

### Proposed Implementation: Hybrid Approach

**Confidence should affect BOTH trade threshold AND position sizing.**

#### Tier 1: High Confidence (8-10)
```
Meaning: Fresh data, aligned signals, no event risk
Action: Trade with INCREASED size
Size modifier: 1.0x to 1.25x
Example: 6J today (conf 8, score +5)
  → LONGS_ONLY (code 10) + 1.25x size
  → Aggressive long position
```

#### Tier 2: Moderate Confidence (6-7)
```
Meaning: Good setup, minor uncertainty
Action: Trade with NORMAL size
Size modifier: 0.75x to 1.0x
Example: GC today (conf 7, score +1)
  → LONG_BIAS (code 12) + 1.0x size
  → Normal long bias
```

#### Tier 3: Low Confidence (4-5)
```
Meaning: Edge exists but uncertain
Action: Trade with REDUCED size
Size modifier: 0.5x (half size)
Example: M6E today (conf 5, score +1)
  → LONG_BIAS (code 12) + 0.5x size
  → Small long bias (test position)
```

#### Tier 4: Very Low Confidence (1-3)
```
Meaning: Data stale, extreme conflict, or pre-major event
Action: DON'T TRADE or minimal size
Size modifier: 0.25x OR shouldTrade = false
Example: Hypothetical pre-FOMC (conf 3, score +3)
  → NO TRADE or 0.25x size
  → Too risky to commit capital
```

### Why This Makes Sense

**From Manus's perspective:**

When I assign confidence 8-10, I'm saying:
- "I've verified all my data sources"
- "All factors point the same direction"
- "No major events could invalidate this"
- **→ You should trade this with conviction**

When I assign confidence 4-5, I'm saying:
- "There's an edge here, but I'm not sure"
- "Some factors conflict"
- "Or data is slightly stale"
- **→ Trade small to test the thesis**

When I assign confidence 1-3, I'm saying:
- "Something is wrong with my data"
- "Or we're about to have a major event"
- "Or signals are completely mixed"
- **→ Don't trade this, it's too uncertain**

### Implementation in PM

**Suggested code addition in `DetermineStrategy()` or `PublishStrategyToGlobals()`:**

```cpp
// After determining envCode from score
int confidence = g_symbols[idx].confidence;  // Need to store this first
double sizeModifier = 1.0;

if(confidence >= 8)
{
   sizeModifier = 1.25;  // High conviction
}
else if(confidence >= 6)
{
   sizeModifier = 1.0;   // Normal
}
else if(confidence >= 4)
{
   sizeModifier = 0.5;   // Half size
}
else // confidence 1-3
{
   g_symbols[idx].shouldTrade = false;  // Don't trade
   // OR sizeModifier = 0.25;  // Minimal exposure
}

// Publish to global variable
GlobalVariableSet("PM_" + symbol + "_SIZE_MOD", sizeModifier);
```

### Real-World Example from Today

**Without confidence sizing (current):**
```
M6E: Score +1, Confidence 5
  → LONG_BIAS (code 12)
  → Full size long bias
  → Risk: Trading with full size despite uncertainty
```

**With confidence sizing (proposed):**
```
M6E: Score +1, Confidence 5
  → LONG_BIAS (code 12) + 0.5x size modifier
  → Half size long bias
  → Better: Testing the thesis with reduced risk
```

**Comparison:**
```
6J: Score +5, Confidence 8
  → LONGS_ONLY (code 10) + 1.25x size
  → High conviction = larger position

M6E: Score +1, Confidence 5
  → LONG_BIAS (code 12) + 0.5x size
  → Low conviction = smaller position

Result: Position sizing now reflects conviction level
```

---

## Questions for Further Discussion {#questions}

### 1. Score Range Utilization

**Current:** Using +1 to +5 (25% of available range)  
**Issue:** All instruments map to similar environment codes  

**Questions:**
- Should Manus use more aggressive weights to spread scores?
- Should CSV mapping thresholds be adjusted?
- Should confidence amplify/dampen scores?

### 2. Confidence Implementation

**Current:** Confidence calculated but not used  
**Proposed:** Hybrid approach (threshold + sizing)  

**Questions:**
- Should confidence < 4 prevent trading entirely?
- Or should it just reduce size to 0.25x?
- Should high confidence (8-10) increase size to 1.5x or 2x?

### 3. Signal vs. Score Redundancy

**Current:** Both signal and score convey direction  
**Observation:** Signal is derived from score  

**Questions:**
- Is signal still needed if score exists?
- Or is signal useful for human readability?
- Could signal be more nuanced (e.g., "CAUTIOUS_BULLISH")?

### 4. Asset Class Aggregation

**Current:** PM extracts "COMMODITIES", "INDICES", "FX" bias from JSON  
**Usage:** Displayed in Telegram but not used in trading logic  

**Questions:**
- Should asset class bias affect individual symbol decisions?
- Example: If "INDICES: BEARISH" but ES score is +2, should ES still trade long?
- Or should asset class bias override individual scores?

### 5. Data Quality Reporting

**Current:** Manus reports `stale_sources` and `fallbacks_used` in JSON  
**Usage:** Not consumed by PM  

**Questions:**
- Should PM read data quality and adjust confidence?
- Should stale data trigger alerts?
- Should fallback usage reduce position sizing?

---

## Next Steps

1. **User Decision:** Which score distribution solution to implement (A/B/C/D)?
2. **Claude Implementation:** Add confidence-based sizing to PM
3. **Manus Adjustment:** Potentially adjust scoring weights based on user feedback
4. **Testing:** Run system with new logic and compare results
5. **Documentation:** Update SYSTEM_WORKFLOW.md with confidence sizing logic

---

## Appendix: Today's Full Scoring Breakdown (Jan 29, 2026)

### GC (Gold): Score +1, Confidence 7

```
Factor              Weight  Raw   Weighted
Fed stance          1       0     0
Real yields         2       0     0
USD                 1       +1    +1
Risk mood           1       0     0
Growth              1       -1    -1
Oil supply          1       0     0
Gold ETFs           1       +1    +1
                          TOTAL:  +1

Signal: SLIGHT_BULLISH
Confidence: 7/10 (good data, mixed signals)
```

### 6J (Japanese Yen): Score +5, Confidence 8

```
Factor              Weight  Raw   Weighted
Fed stance          1       0     0
BoJ stance          2       +1    +2
Rate differential   2       +1    +2
USD                 1       +1    +1
Risk mood           1       0     0
                          TOTAL:  +5

Signal: STRONG_BULLISH
Confidence: 8/10 (all aligned, fresh data)
```

### M6E (Euro): Score +1, Confidence 5

```
Factor              Weight  Raw   Weighted
Fed stance          1       0     0
ECB stance          1       0     0
Rate differential   2       0     0
USD                 1       +1    +1
Risk mood           1       0     0
Eurozone growth     1       0     0
                          TOTAL:  +1

Signal: SLIGHT_BULLISH
Confidence: 5/10 (conflicting signals, ECB concerns)
```

---

**End of Document**
