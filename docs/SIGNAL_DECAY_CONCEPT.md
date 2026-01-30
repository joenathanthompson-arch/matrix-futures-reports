# Signal Decay Concept - Critical Addition to Scoring Methodology

**Date:** January 30, 2026 (2:43 AM EST)  
**Discovered During:** Three-way collaboration (User, Manus AI, Claude AI)  
**Impact:** Changes how scores reflect time horizon and catalyst proximity

---

## The Missing Piece: Temporal Information

### Problem Statement

Original scoring methodology focused on **strength of fundamental conditions** but didn't explicitly account for **when those conditions would matter**.

**Example:**
- BoJ hawkish stance (strong fundamental condition)
- But next meeting in **March** (2 months away)
- Should this get the same score as RBA hiking **Feb 3** (4 days away)?

**Answer:** No - **catalyst proximity matters** for short-term trading strategies.

---

## Signal Decay Defined

**Signal Decay** = The rate at which a fundamental condition loses relevance for near-term price action.

### Key Insight from User

> "Most of my strategies are trading shorter term... it helps to know that if the score is in the +8-+10 zone that the catalyst is likely going to occur within a few sessions and should be on my radar."

**Translation:** Scores should embed **temporal information** about when catalysts will materialize.

---

## Revised Score Thresholds with Time Horizon

| Score Range | Fundamental Strength | Catalyst Timing | Trading Implication |
|-------------|---------------------|-----------------|---------------------|
| **+8 to +10** | Exceptional conditions | **< 1 week** | Catalyst imminent - be ready NOW |
| **+6 to +7** | Strong conditions | **1-4 weeks** | Build position over time |
| **+4 to +5** | Good conditions | **No specific catalyst** | Trade when technicals align |
| **+2 to +3** | Slight edge | **Background support** | Small size, opportunistic |
| **+1** | Minimal edge | **Weak/distant** | Minimal exposure |
| **0** | No edge | **N/A** | Stand down |

### Mirror for Bearish Scores

Same logic applies to negative scores (-1 to -10).

---

## Examples from Current Market (Jan 30, 2026)

### Example 1: 6A (Australian Dollar)

**Fundamental Conditions:**
- RBA hawkish stance
- Copper at highs
- USD weak
- Rate differential widening

**Catalyst Timing:**
- **RBA decision: Feb 3, 2026** (4 days away)
- Expected to hike 25 bps

**Score Decision:**
- **Old thinking:** +6 or +7 (strong conditions)
- **New thinking:** **+8** (imminent catalyst + strong conditions)

**Why +8?**
- Catalyst is **within 1 week**
- All factors aligned
- Confidence 7/10
- **Trader should be on high alert for next few sessions**

### Example 2: 6J (Japanese Yen)

**Fundamental Conditions:**
- BoJ hawkish turn (historic shift)
- Rate differential narrowing
- USD weak
- All factors aligned

**Catalyst Timing:**
- **Next BoJ meeting: March 2026** (2 months away)
- No imminent catalyst

**Score Decision:**
- **Old thinking:** +8 (historic shift deserves max score)
- **New thinking:** **+7** (strong conditions but catalyst not imminent)

**Why +7 instead of +8?**
- Conditions are excellent BUT
- No catalyst within 1 week
- **Trader can build position over time, no urgency**

### Example 3: ES (S&P 500)

**Fundamental Conditions:**
- Credit spreads narrowing (supportive)
- USD weak (mild positive)
- Growth strong (mixed signal)

**Catalyst Timing:**
- **No specific catalyst**
- Background conditions

**Score Decision:**
- **Score: +2** (slight edge, no catalyst)
- **Trader should wait for technical setup, not urgent**

---

## Impact on Trading Decisions

### Without Signal Decay Awareness

```
6A: +7 (strong conditions)
6J: +8 (historic shift)

Trader treats 6J as higher priority than 6A
```

**Problem:** 6J catalyst is 2 months away, 6A catalyst is 4 days away.

### With Signal Decay Awareness

```
6A: +8 (imminent catalyst < 1 week)
6J: +7 (strong but catalyst distant)

Trader prioritizes 6A for next few sessions
```

**Benefit:** Capital allocated to where catalysts will materialize soonest.

---

## Implementation Rules

### Rule 1: Catalyst Proximity Determines Score Ceiling

```
If catalyst < 1 week:
  - Can reach +8 to +10 (if conditions strong)
  
If catalyst 1-4 weeks:
  - Max score +6 to +7 (even if conditions exceptional)
  
If no catalyst:
  - Max score +5 (background conditions only)
```

### Rule 2: Confidence Still Separate

**Important:** Signal decay affects **score**, not **confidence**.

```
6J: Score +7 (catalyst distant), Confidence 8 (very sure of assessment)
6A: Score +8 (catalyst imminent), Confidence 7 (pretty sure)
```

**PM then applies:**
- 6J: +7 → LONGS_ONLY (1.0x base) × conf 8 (1.25x) = 1.25x total
- 6A: +8 → MAX_LONG (1.5x base) × conf 7 (1.0x) = 1.5x total

**Result:** 6A gets more size due to imminent catalyst.

### Rule 3: Decay Rate Varies by Factor Type

**Fast decay (matters for short-term):**
- Central bank meetings (RBA, BoJ, Fed)
- Economic data releases (CPI, NFP, GDP)
- Geopolitical events (elections, conflicts)

**Slow decay (matters for medium-term):**
- Credit spreads
- Yield curve shape
- Growth narrative

**No decay (structural):**
- Long-term trends (demographics, policy shifts)

---

## Scoring Checklist (New Process)

### Step 1: Calculate Raw Score (Factor Alignment)

```
Sum of weighted factors:
- Fed stance × weight
- Real yields × weight
- USD × weight
- etc.

Result: Raw score (e.g., +7)
```

### Step 2: Check Catalyst Proximity

```
Is there a catalyst < 1 week?
  YES → Can use full raw score (+7 or higher)
  NO → Cap at +7 or reduce by 1 point
```

### Step 3: Assign Confidence (Separate)

```
Based on:
- Data freshness
- Signal clarity
- Event risk

Result: Confidence 1-10
```

### Step 4: Output to PM

```
JSON:
{
  "score": 7,
  "signal": "STRONG_BULLISH",
  "confidence": 8
}
```

**PM then handles sizing based on both score and confidence.**

---

## Expected Score Distribution (With Signal Decay)

### Per Report (2-4x Daily)

| Score Range | Frequency | Reason |
|-------------|-----------|--------|
| **+8 to +10** | 0-2 per report | Rare - requires imminent catalyst + alignment |
| **+6 to +7** | 1-3 per report | Strong conditions, catalyst 1-4 weeks out |
| **+4 to +5** | 2-4 per report | Good conditions, no specific catalyst |
| **+2 to +3** | 3-5 per report | Slight edge, background support |
| **+1** | 1-3 per report | Minimal edge |
| **0** | 0-2 per report | No fundamental edge |

**Key point:** +8 to +10 should be **rare** because imminent catalysts are rare.

---

## Report Frequency Considerations

### User's Question: "Is 4x daily overkill?"

**Answer depends on signal decay:**

**Fast-decaying signals (central bank meetings, data releases):**
- Need frequent updates (4x daily makes sense)
- Catalyst timing matters intraday

**Slow-decaying signals (credit spreads, yield curves):**
- 2x daily sufficient
- Conditions don't change intraday

### Recommended Schedule

**2x Daily (Baseline):**
- **5:30 PM EST** - Before Asia open
- **7:30 AM EST** - Before US open

**4x Daily (When Needed):**
- Add **2:30 AM EST** - Mid-Asia (if BoJ/RBA/ECB event)
- Add **2:30 PM EST** - Mid-US (if FOMC/CPI/NFP day)

**Benefit:** Catch catalyst timing without noise.

---

## Examples of Catalyst-Driven Scoring

### High-Frequency Catalysts (Score +8 to +10)

| Catalyst | Timing | Score Impact |
|----------|--------|--------------|
| RBA decision | Feb 3, 9:30 PM EST | 6A → +8 (4 days out) |
| FOMC decision | Feb 1, 2:00 PM EST | ES/NQ → +8 or -8 (if clear direction) |
| NFP release | Feb 7, 8:30 AM EST | USD pairs → +8 or -8 (if clear setup) |
| BoJ meeting | Mar 18-19 | 6J → +7 (too far out for +8) |

### Medium-Frequency Catalysts (Score +6 to +7)

| Catalyst | Timing | Score Impact |
|----------|--------|--------------|
| ECB meeting | Feb 5 | M6E → +6 (if clear direction) |
| Fed speaker | Next week | USD → +6 (if hawkish/dovish) |
| CPI release | Feb 13 | Broad impact → +6 to +7 |

### Background Conditions (Score +4 to +5)

| Condition | Timing | Score Impact |
|-----------|--------|--------------|
| Credit spreads narrowing | Ongoing | ES/RTY → +4 |
| SOX strength | Ongoing | NQ → +4 |
| Copper rally | Ongoing | 6A → +5 (if no RBA meeting) |

---

## Key Takeaways

1. **Scores now embed time horizon** - not just strength of conditions
2. **+8 to +10 = catalyst imminent** (< 1 week) - be on high alert
3. **+6 to +7 = strong setup** but catalyst 1-4 weeks out - build position
4. **+4 to +5 = good conditions** but no specific catalyst - opportunistic
5. **Signal decay varies by factor** - central banks decay fast, credit spreads decay slow
6. **Confidence remains separate** - PM applies sizing based on both score and confidence

---

## Integration with Existing Methodology

This concept **enhances** the existing methodology, doesn't replace it:

**Existing:**
- Factor weighting (1x, 2x, 3x)
- Confidence scoring (1-10)
- Score → environment code mapping

**New Addition:**
- Catalyst proximity check
- Score ceiling based on timing
- Temporal awareness in scoring

**Result:** More actionable scores for short-term trading strategies.

---

## Next Steps

1. ✅ Document signal decay concept (this file)
2. ✅ Update scoring methodology to include catalyst proximity check
3. ✅ Generate next report (Jan 30, 2:43 AM EST) with new methodology
4. Monitor for 1 week to ensure score distribution is appropriate
5. Adjust catalyst timing thresholds if needed

---

**End of Signal Decay Concept Documentation**
