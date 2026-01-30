# Manus AI Bias Report Format Specification

**Last Updated:** January 30, 2026
**Version:** 2.0

## Problem
Manus is producing reports in the wrong format. PM cannot read them.

## Required File Structure

```
matrix-futures-reports/
├── data/
│   ├── bias_scores/
│   │   ├── 2026-01-30_0730.json    ← Timestamped copy
│   │   └── latest.json              ← PM READS THIS (CRITICAL!)
│   ├── executive_summaries/
│   │   ├── 2026-01-30_0730.md      ← Timestamped copy
│   │   └── latest.md               ← PM's /summary reads this
│   └── factors/
│       └── 2026-01-30_0730.csv     ← Macro factor breakdown (optional)
└── reports/
    └── 2026-01-30_Bias-Scores.csv  ← Human-readable summary
```

---

## 1. CRITICAL: `latest.json` Format

**Path:** `data/bias_scores/latest.json`

```json
{
  "date": "2026-01-30",
  "generated_at": "2026-01-30T07:30:00Z",
  "methodology_version": "2.0_RECALIBRATED",
  "scores": {
    "GC": {"score": 5, "signal": "STRONG_BULLISH", "confidence": 7},
    "SI": {"score": 5, "signal": "STRONG_BULLISH", "confidence": 7},
    "CL": {"score": 7, "signal": "STRONG_BULLISH", "confidence": 7},
    "ES": {"score": 1, "signal": "SLIGHT_BULLISH", "confidence": 6},
    "NQ": {"score": 1, "signal": "SLIGHT_BULLISH", "confidence": 6},
    "YM": {"score": 2, "signal": "SLIGHT_BULLISH", "confidence": 6},
    "RTY": {"score": 3, "signal": "BULLISH", "confidence": 7},
    "M6E": {"score": 2, "signal": "SLIGHT_BULLISH", "confidence": 5},
    "6A": {"score": 3, "signal": "BULLISH", "confidence": 7},
    "6J": {"score": 6, "signal": "STRONG_BULLISH", "confidence": 7}
  },
  "asset_class_bias": {
    "COMMODITIES": "STRONG_BULLISH",
    "INDICES": "SLIGHT_BULLISH",
    "FX": "BULLISH"
  },
  "key_drivers": [
    "Weak US Dollar (DXY down 1.93% week)",
    "Dovish Fed Stance (15.3% probability of March cut)",
    "Rising Geopolitical Risk (US-Iran tensions)"
  ],
  "data_quality": {
    "stale_sources": [],
    "fallbacks_used": [],
    "overnight_changes": []
  },
  "catalyst_proximity": {
    "imminent": [],
    "near_term": ["RBA Decision Feb 3"],
    "background": ["BoJ hawkish stance continues"]
  }
}
```

### Field Requirements:

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `date` | string | YES | YYYY-MM-DD |
| `generated_at` | string | YES | ISO 8601 UTC (ends with Z) |
| `scores` | object | YES | All 10 symbols required |
| `scores.[SYM].score` | integer | YES | -10 to +10 (INTEGER, no decimals) |
| `scores.[SYM].signal` | string | YES | See signal mapping below |
| `scores.[SYM].confidence` | integer | YES | 1-10 (separate from score!) |
| `asset_class_bias` | object | YES | COMMODITIES, INDICES, FX |
| `key_drivers` | array | YES | 3-5 string items |
| `data_quality` | object | NO | Optional tracking |
| `catalyst_proximity` | object | NO | Optional event timing |

### Signal Mapping (MUST USE EXACTLY):

| Score Range | Signal String |
|-------------|---------------|
| +7 to +10 | `STRONG_BULLISH` |
| +5 to +6 | `STRONG_BULLISH` |
| +3 to +4 | `BULLISH` |
| +1 to +2 | `SLIGHT_BULLISH` |
| 0 | `NEUTRAL` |
| -1 to -2 | `SLIGHT_BEARISH` |
| -3 to -4 | `BEARISH` |
| -5 to -10 | `STRONG_BEARISH` |

### 10 Required Symbols:
`GC`, `SI`, `CL`, `ES`, `NQ`, `YM`, `RTY`, `M6E`, `6A`, `6J`

---

## 2. Executive Summary Format

**Path:** `data/executive_summaries/latest.md`

```markdown
# Matrix Futures Daily Bias Report
**Date:** January 30, 2026 | **Time:** 07:30 EST

---

## Overall Market Bias: [BULLISH/BEARISH/MIXED]

[2-3 sentence summary of overall market conditions]

---

## Asset Class Summary

| Asset Class | Bias | Key Driver |
|-------------|------|------------|
| Commodities | STRONG_BULLISH | Weak USD, Geopolitical Risk |
| Indices | SLIGHT_BULLISH | Dovish Fed, Rising VIX concern |
| FX | BULLISH | Weak USD, BoJ Tightening |

---

## Highest Conviction Signals

| Instrument | Score | Signal | Confidence |
|------------|-------|--------|------------|
| CL | +7 | STRONG_BULLISH | 7/10 |
| 6J | +6 | STRONG_BULLISH | 7/10 |
| GC | +5 | STRONG_BULLISH | 7/10 |

---

## Full Instrument Breakdown

### GC (Gold): +5 STRONG_BULLISH (7/10)
[2-3 sentence analysis with key drivers]

### SI (Silver): +5 STRONG_BULLISH (7/10)
[Analysis]

### CL (Crude Oil): +7 STRONG_BULLISH (7/10)
[Analysis]

### ES (S&P 500): +1 SLIGHT_BULLISH (6/10)
[Analysis]

### NQ (Nasdaq 100): +1 SLIGHT_BULLISH (6/10)
[Analysis]

### YM (Dow Jones): +2 SLIGHT_BULLISH (6/10)
[Analysis]

### RTY (Russell 2000): +3 BULLISH (7/10)
[Analysis]

### M6E (Euro): +2 SLIGHT_BULLISH (5/10)
[Analysis]

### 6A (Australian Dollar): +3 BULLISH (7/10)
[Analysis]

### 6J (Japanese Yen): +6 STRONG_BULLISH (7/10)
[Analysis]

---

## Key Macro Themes

1. **[Theme 1]**: [Explanation]
2. **[Theme 2]**: [Explanation]
3. **[Theme 3]**: [Explanation]

---

## Upcoming Catalysts

### Imminent (< 1 Week)
- [Event] (Date)

### Near-Term (1-4 Weeks)
- [Event] (Date)

---

## Data Quality
- All data sources current as of [Date]
- No stale data used
- Average confidence: X.X/10

---
**End of Report**
```

---

## 3. CSV Format (Optional but Useful)

**Path:** `reports/2026-01-30_Bias-Scores.csv`

```csv
Ticker,Instrument,Numeric Bias,Signal,Confidence
GC,Gold,+5,STRONG_BULLISH,7
SI,Silver,+5,STRONG_BULLISH,7
CL,Crude Oil,+7,STRONG_BULLISH,7
ES,S&P 500,+1,SLIGHT_BULLISH,6
NQ,Nasdaq 100,+1,SLIGHT_BULLISH,6
YM,Dow Jones,+2,SLIGHT_BULLISH,6
RTY,Russell 2000,+3,BULLISH,7
M6E,Euro,+2,SLIGHT_BULLISH,5
6A,Australian Dollar,+3,BULLISH,7
6J,Japanese Yen,+6,STRONG_BULLISH,7
```

---

## 4. Asset Class Bias (Include in JSON)

Manus correctly computed asset class biases. Include them in `latest.json` under `asset_class_bias`:

```json
"asset_class_bias": {
  "COMMODITIES": "STRONG_BULLISH",
  "INDICES": "SLIGHT_BULLISH",
  "FX": "BULLISH"
}
```

**Asset Class Grouping:**
- **COMMODITIES:** GC, SI, CL (average their signals)
- **INDICES:** ES, NQ, YM, RTY (average their signals)
- **FX:** M6E, 6A, 6J (average their signals)

---

## 5. CRITICAL Rules for Manus

1. **ALWAYS create both:**
   - `data/bias_scores/latest.json` ← PM reads this!
   - `data/executive_summaries/latest.md` ← `/pm summary` reads this!

2. **Also create timestamped copies:**
   - `data/bias_scores/2026-01-30_0730.json`
   - `data/executive_summaries/2026-01-30_0730.md`

3. **Integer scores only** - No decimals (use +5 not +5.0)

4. **Score ≠ Confidence:**
   - Score = direction/magnitude (-10 to +10)
   - Confidence = certainty of assessment (1-10)

5. **All 10 symbols required** - Never skip any

6. **Signal strings must match exactly** - PM parses these

---

## 6. Common Mistakes to Avoid

| Wrong | Correct |
|-------|---------|
| `matrix.csv` | `data/bias_scores/latest.json` |
| `public_report.md` | `data/executive_summaries/latest.md` |
| `asset_class_bias.csv` | Include in `latest.json` |
| Score as float (5.0) | Score as integer (5) |
| Missing symbols | All 10 required |

---

## 7. Verification Checklist

Before committing, verify:

- [ ] `data/bias_scores/latest.json` exists and is valid JSON
- [ ] JSON has all 10 symbols with score, signal, confidence
- [ ] All scores are integers (-10 to +10)
- [ ] Signal strings match exactly (STRONG_BULLISH, BULLISH, etc.)
- [ ] `data/executive_summaries/latest.md` exists
- [ ] Timestamped copies created for both files
- [ ] `asset_class_bias` included in JSON

---

## 8. PM Reading Code Reference

PM parses `latest.json` in `ParseBiasScores()` around line 1800 of PortfolioManager.mq5:

```cpp
// Expected JSON structure:
// scores.GC.score = integer
// scores.GC.signal = string
// scores.GC.confidence = integer
```

If format is wrong, PM silently fails to update bias data.

---

## 9. POST-COMMIT VERIFICATION (REQUIRED)

**After EVERY report generation, Manus MUST verify the committed files are correct:**

### Verification Steps:

1. **Fetch and validate `latest.json`:**
   ```
   curl -s https://raw.githubusercontent.com/joenathanthompson-arch/matrix-futures-reports/main/data/bias_scores/latest.json | jq .
   ```

   Verify:
   - [ ] Valid JSON (no parse errors)
   - [ ] Contains `scores` object with all 10 symbols
   - [ ] Each symbol has `score` (integer), `signal` (string), `confidence` (integer)
   - [ ] `asset_class_bias` object exists with COMMODITIES, INDICES, FX
   - [ ] `date` matches today's date

2. **Fetch and validate `latest.md`:**
   ```
   curl -s https://raw.githubusercontent.com/joenathanthompson-arch/matrix-futures-reports/main/data/executive_summaries/latest.md | head -20
   ```

   Verify:
   - [ ] File exists and is not empty
   - [ ] Contains proper markdown formatting
   - [ ] Has all 10 instrument sections
   - [ ] Date in header matches today

3. **Verify directory structure:**
   ```
   Check GitHub repo shows:
   - data/bias_scores/latest.json
   - data/bias_scores/YYYY-MM-DD_HHMM.json (timestamped copy)
   - data/executive_summaries/latest.md
   - data/executive_summaries/YYYY-MM-DD_HHMM.md (timestamped copy)
   ```

### Sample Validation Command:
```bash
# Quick JSON validation
curl -s https://raw.githubusercontent.com/joenathanthompson-arch/matrix-futures-reports/main/data/bias_scores/latest.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
required_symbols = ['GC', 'SI', 'CL', 'ES', 'NQ', 'YM', 'RTY', 'M6E', '6A', '6J']
scores = data.get('scores', {})
missing = [s for s in required_symbols if s not in scores]
if missing:
    print(f'ERROR: Missing symbols: {missing}')
    sys.exit(1)
for sym in required_symbols:
    s = scores[sym]
    if not all(k in s for k in ['score', 'signal', 'confidence']):
        print(f'ERROR: {sym} missing required fields')
        sys.exit(1)
    if not isinstance(s['score'], int):
        print(f'ERROR: {sym} score must be integer, got {type(s[\"score\"])}')
        sys.exit(1)
print('✅ Validation PASSED')
"
```

### If Verification Fails:
1. **DO NOT** report success to user
2. Fix the format issues immediately
3. Commit corrected files
4. Re-run verification
5. Only report success after verification passes

---

## 10. Error Recovery

If PM reports it cannot read bias data:

1. Check `latest.json` exists at correct path
2. Validate JSON syntax
3. Verify all 10 symbols present
4. Check signal strings match exactly (case-sensitive)
5. Ensure scores are integers, not floats

---

## 11. URLs Reference

| Purpose | URL |
|---------|-----|
| Bias JSON (PM reads) | `https://raw.githubusercontent.com/joenathanthompson-arch/matrix-futures-reports/main/data/bias_scores/latest.json` |
| Executive Summary | `https://raw.githubusercontent.com/joenathanthompson-arch/matrix-futures-reports/main/data/executive_summaries/latest.md` |
| Repository | `https://github.com/joenathanthompson-arch/matrix-futures-reports` |
