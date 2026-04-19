from datetime import datetime, timezone
from pathlib import Path
import json

BASE = Path('/home/ubuntu/matrix-futures-reports')
BIAS_DIR = BASE / 'data' / 'bias_scores'
EXEC_DIR = BASE / 'data' / 'executive_summaries'
REPORTS_DIR = BASE / 'reports'
FACTORS_DIR = BASE / 'data' / 'factors'
for d in [BIAS_DIR, EXEC_DIR, REPORTS_DIR, FACTORS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

now = datetime.now(timezone.utc)
date_str = now.strftime('%Y-%m-%d')
time_hhmm = now.strftime('%H%M')
iso_str = now.strftime('%Y-%m-%dT%H:%M:%SZ')
human_date = now.strftime('%B %d, %Y')

scores = {
    'GC': {'score': 0, 'signal': 'NEUTRAL', 'confidence': 4, 'recommended_approach': 'RANGE_TRADE', 'recommended_mode': 'INTRADAY', 'hold_expectation': 'session'},
    'SI': {'score': 0, 'signal': 'NEUTRAL', 'confidence': 4, 'recommended_approach': 'RANGE_TRADE', 'recommended_mode': 'INTRADAY', 'hold_expectation': 'session'},
    'CL': {'score': 4, 'signal': 'BULLISH', 'confidence': 6, 'recommended_approach': 'TREND_FOLLOW', 'recommended_mode': 'SWING', 'hold_expectation': '1-2 days'},
    'ES': {'score': 0, 'signal': 'NEUTRAL', 'confidence': 4, 'recommended_approach': 'RANGE_TRADE', 'recommended_mode': 'INTRADAY', 'hold_expectation': 'session'},
    'NQ': {'score': 2, 'signal': 'SLIGHT_BULLISH', 'confidence': 6, 'recommended_approach': 'IB_BREAKOUT', 'recommended_mode': 'INTRADAY', 'hold_expectation': 'session'},
    'YM': {'score': 0, 'signal': 'NEUTRAL', 'confidence': 4, 'recommended_approach': 'RANGE_TRADE', 'recommended_mode': 'INTRADAY', 'hold_expectation': 'session'},
    'RTY': {'score': -1, 'signal': 'SLIGHT_BEARISH', 'confidence': 4, 'recommended_approach': 'FADE_RANGE', 'recommended_mode': 'INTRADAY', 'hold_expectation': 'session'},
    '6E': {'score': 1, 'signal': 'SLIGHT_BULLISH', 'confidence': 5, 'recommended_approach': 'RANGE_TRADE', 'recommended_mode': 'INTRADAY', 'hold_expectation': 'session'},
    '6A': {'score': 5, 'signal': 'STRONG_BULLISH', 'confidence': 6, 'recommended_approach': 'TREND_FOLLOW', 'recommended_mode': 'SWING', 'hold_expectation': '1-2 days'},
    '6J': {'score': 4, 'signal': 'BULLISH', 'confidence': 6, 'recommended_approach': 'TREND_FOLLOW', 'recommended_mode': 'SWING', 'hold_expectation': '1-2 days'},
}

asset_class_bias = {
    'COMMODITIES': 'MIXED',
    'INDICES': 'MIXED',
    'FX': 'BULLISH',
}

json_payload = {
    'date': date_str,
    'generated_at': iso_str,
    'methodology_version': '3.0_STRATEGY',
    'scores': scores,
    'asset_class_bias': asset_class_bias,
    'key_drivers': [
        'The dollar remains a broad cross-asset tailwind: TradingView showed DXY near 98.23, still down on both five-day and one-month horizons despite only a small daily bounce.',
        'Risk and duration conditions are constructive but not euphoric because VIX stayed balanced in the high teens while VIX direction fell, MOVE fell 11.24% over five days, and SOX surged 2.43% on the day and 8.44% over five days.',
        'Crude retains the firmest commodity setup because the latest official EIA week ended April 10 still points to a crude draw and a tightening supply backdrop.',
        'FX leadership is driven by policy divergence: the Fed is best treated as a hawkish hold, while the ECB remains firm, the RBA hiked to 4.10%, and the BoJ remains in a normalization regime.'
    ],
    'data_quality': {
        'stale_sources': [
            'Atlanta Fed GDPNow remains the April 9, 2026 official update at 1.3% for 2026:Q1.',
            'FRED DFII10 and BAMLH0A0HYM2 latest official observations lag the report timestamp by normal publication delay.',
            'World Gold Council ETF-flow evidence remains anchored to the March 2026 release.',
            'Detailed CME FedWatch probabilities were not fully machine-readable in-session, so Fed stance used readable same-week visibility plus conservative interpretation.'
        ],
        'fallbacks_used': [
            'TradingView was used for DXY, MOVE, SOX, and copper direction because some specified market pages were blocked or less accessible.',
            'Repository-verified same-week source snapshots were used to retain explicit copper, China-growth, and gold-ETF classifications where direct live extraction was incomplete.',
            'Direct official browser review confirmed the March 19 ECB hold, the March 17 RBA 25 bp hike to 4.10%, and the March 19 BoJ 0.75% hold.',
            'A readable same-session FedWatch view confirmed near-total pricing for no change at the next Fed meeting.'
        ],
        'overnight_changes': [
            'DXY remained broadly weak over both five-day and one-month horizons.',
            'VIX and MOVE both eased, improving the macro backdrop for duration-sensitive risk assets.',
            'SOX and copper both strengthened, reinforcing pro-cyclical and commodity-currency leadership.'
        ]
    },
    'catalyst_proximity': {
        'imminent': [
            'Atlanta Fed GDPNow update on April 21, 2026'
        ],
        'near_term': [
            'FOMC meeting on April 28-29, 2026',
            'BoJ normalization communication remains an active FX catalyst'
        ],
        'background': [
            'May RBA policy decision window',
            'Ongoing Gulf shipping and energy-supply headlines'
        ]
    }
}

md = f'''# Matrix Futures Daily Bias Report
**Date:** {human_date} | **Time:** {now.strftime("%H:%M")} UTC

---

## Overall Market Bias: MIXED

The cross-asset backdrop remains **constructive but uneven**. A broadly weaker U.S. dollar, falling rates volatility, and strong semiconductor leadership are supportive for pro-risk and FX trades, but that tailwind is offset by a still-restrictive Fed stance, only moderate growth momentum, and stale precious-metals flow inputs. The result is a **mixed** macro regime in which **FX carries the clearest directional edge**, crude retains a firm bullish setup, and U.S. equity index signals are selective rather than broad-based.

---

## Asset Class Summary

| Asset Class | Bias | Key Driver |
|-------------|------|------------|
| Commodities | MIXED | Crude inventory draw and supply tightness offset by negative March gold ETF flow evidence and flat real yields |
| Indices | MIXED | Falling VIX and MOVE support risk assets, but a hawkish Fed hold and only modest growth keep broad index conviction capped |
| Fx | BULLISH | Weak USD plus hawkish or normalizing non-U.S. central-bank regimes support 6A and 6J |

---

## Highest Conviction Signals

| Instrument | Score | Signal | Confidence |
|------------|-------|--------|------------|
| 6A | +5 | STRONG_BULLISH | 6/10 |
| CL | +4 | BULLISH | 6/10 |
| 6J | +4 | BULLISH | 6/10 |

---

## Full Instrument Breakdown

### GC (Gold): 0 NEUTRAL (4/10)
**Approach:** RANGE_TRADE | **Mode:** INTRADAY | **Hold:** session
Gold is caught between **supportive USD weakness and a firmer oil-inflation impulse** on one side and **flat real yields plus negative March ETF-flow evidence** on the other. The metal therefore lacks a clean trend catalyst despite the softer dollar backdrop. Recommended posture is **range trading** rather than trend chasing until yields or flows break more decisively.

### SI (Silver): 0 NEUTRAL (4/10)
**Approach:** RANGE_TRADE | **Mode:** INTRADAY | **Hold:** session
Silver benefits from the same **weak-dollar backdrop** as gold, and unlike gold it also receives help from **rising copper**, which points to healthier industrial demand conditions. However, the signal is held back by the **hawkish-hold Fed interpretation** and the same stale precious-metals flow evidence that weighs on gold. The setup is therefore neutral overall, with a tactical intraday bias only if metals break out on fresh macro news.

### CL (Crude Oil): +4 BULLISH (6/10)
**Approach:** TREND_FOLLOW | **Mode:** SWING | **Hold:** 1-2 days
Crude retains one of the cleaner bullish macro profiles because the latest official EIA week still shows a **commercial crude draw**, while the broader supply backdrop remains **tight rather than clearly easing**. A weaker dollar also adds support to the oil complex. The caveat is that geopolitical risk is elevated but not in fresh panic mode, so the preferred approach is **trend follow on strength**, not panic-premium chasing.

### ES (S&P 500): 0 NEUTRAL (4/10)
**Approach:** RANGE_TRADE | **Mode:** INTRADAY | **Hold:** session
The S&P 500 sees offsetting forces. On the positive side, **VIX direction is falling** and the **USD is softer**, but those gains are neutralized by a **hawkish Fed hold**, only **slowing GDPNow growth**, and the lack of a strong fresh real-yield tailwind. ES therefore looks more like a two-way intraday tape than a high-conviction macro trend.

### NQ (Nasdaq 100): +2 SLIGHT_BULLISH (6/10)
**Approach:** IB_BREAKOUT | **Mode:** INTRADAY | **Hold:** session
Nasdaq remains the strongest equity index from a macro perspective because it is helped by **falling MOVE**, **rising SOX**, and a **broadly weaker dollar**. Those positives more than offset the hawkish-hold Fed classification and the lack of a strongly falling real-yield impulse. The right expression is an **upside breakout bias**, but conviction is still moderate because the signal is more supportive than explosive.

### YM (Dow Jones): 0 NEUTRAL (4/10)
**Approach:** RANGE_TRADE | **Mode:** INTRADAY | **Hold:** session
The Dow gets some support from a **steepening yield curve** and weaker dollar, but that is offset by a **hawkish Fed hold** and slower U.S. growth. Because GDPNow is slowing rather than accelerating, the industrial and value-heavy Dow lacks a clear macro expansion impulse. YM is best treated as neutral and range-bound until growth or credit conditions move more decisively.

### RTY (Russell 2000): -1 SLIGHT_BEARISH (4/10)
**Approach:** FADE_RANGE | **Mode:** INTRADAY | **Hold:** session
Russell 2000 is the weakest equity index in the current set because its high sensitivity to **domestic growth** means the soft 1.3% GDPNow reading matters more here than elsewhere. The steepening curve and softer dollar help, but they are not enough to outweigh the combination of a **hawkish-hold Fed** and a soft growth backdrop. The bias is only slightly bearish, so the preferred tactic is to **fade upside extremes inside the range** rather than aggressively short trend lows.

### 6E (Euro): +1 SLIGHT_BULLISH (5/10)
**Approach:** RANGE_TRADE | **Mode:** INTRADAY | **Hold:** session
The euro keeps a mild bullish edge because the **ECB remains on a hawkish hold** and the **USD remains broadly weak**. However, the actual **rate-differential impulse is treated conservatively as stable**, not widening in the euro's favor, because the Fed is still restrictive and euro-area growth remains soft. That leaves 6E constructive but not strong enough for a high-conviction swing call.

### 6A (Australian Dollar): +5 STRONG_BULLISH (6/10)
**Approach:** TREND_FOLLOW | **Mode:** SWING | **Hold:** 1-2 days
AUD has the clearest upside case in today's report. The setup combines a **weak USD**, a still-**hawkish RBA** confirmed by the March 17 hike to 4.10%, a **supportive AUD-USD rate differential**, **rising copper**, and repository-verified **improvement in China manufacturing conditions**. Because VIX is only balanced rather than fully risk-on, this is not a runaway conviction score, but 6A still offers the cleanest bullish macro expression in the current slate.

### 6J (Japanese Yen): +4 BULLISH (6/10)
**Approach:** TREND_FOLLOW | **Mode:** SWING | **Hold:** 1-2 days
JPY remains supported by **BoJ normalization**, a **supportive policy-differential trend**, and the broader **weak-USD regime**. The fact that risk mood is merely balanced rather than clearly risk-off prevents an even stronger score, but the macro direction still favors yen strength on dips. This remains one of the better swing candidates among the major macro futures, with the usual reminder that **6J is inversely tied to USD/JPY**.

---

## Key Macro Themes

1. **Weak USD, selective risk support:** The dollar’s five-day and one-month declines continue to help commodities and FX, while falling VIX and MOVE support risk assets without pushing the market into a full risk-on regime.
2. **Policy divergence matters more than growth acceleration:** The Fed is still best viewed as a hawkish hold, but the ECB remains firm, the RBA stays hawkish, and the BoJ remains in normalization mode, making FX the cleanest expression of current macro asymmetry.
3. **Crude is firmer than broad commodities:** Oil keeps support from tight supply and a fresh crude draw, while precious metals are held back by flat real yields and stale but still negative ETF-flow evidence.

---

## Upcoming Catalysts

### Imminent (< 1 Week)
- Atlanta Fed GDPNow update on April 21, 2026

### Near-Term (1-4 Weeks)
- FOMC meeting on April 28-29, 2026
- BoJ normalization communication remains an active FX catalyst
- Early-May RBA decision window

---

## Data Quality
- FRED real-yield and HY-spread observations remain subject to normal publication lag.
- GDPNow is still the April 9 official update, so the growth input is stable but stale.
- World Gold Council flow evidence is still anchored to the March 2026 release.
- CME FedWatch probabilities were only partially readable during this run, so the Fed stance used direct visible probabilities plus conservative interpretation.
- Average confidence across the 10 instruments is **4.9/10**.

---
**End of Report**
'''

timestamped_json = BIAS_DIR / f'{date_str}_{time_hhmm}.json'
latest_json = BIAS_DIR / 'latest.json'
timestamped_md = EXEC_DIR / f'{date_str}_{time_hhmm}.md'
latest_md = EXEC_DIR / 'latest.md'
report_csv = REPORTS_DIR / 'latest.csv'
factor_detail = FACTORS_DIR / f'{date_str}_{time_hhmm}_summary.json'

for path, payload in [(timestamped_json, json_payload), (latest_json, json_payload)]:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)
        f.write('\n')

for path, text in [(timestamped_md, md), (latest_md, md)]:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

with open(report_csv, 'w', encoding='utf-8') as f:
    f.write('symbol,instrument,bias_score,signal,confidence,recommended_approach,recommended_mode,hold_expectation\n')
    names = {
        'GC':'Gold','SI':'Silver','CL':'WTI Crude Oil','ES':'S&P 500 E-mini','NQ':'Nasdaq 100 E-mini','YM':'Dow Jones E-mini','RTY':'Russell 2000 E-mini','6E':'Euro FX','6A':'Australian Dollar','6J':'Japanese Yen'
    }
    for sym in ['GC','SI','CL','ES','NQ','YM','RTY','6E','6A','6J']:
        d = scores[sym]
        f.write(f"{sym},{names[sym]},{d['score']:+d},{d['signal']},{d['confidence']},{d['recommended_approach']},{d['recommended_mode']},{d['hold_expectation']}\n")

with open(factor_detail, 'w', encoding='utf-8') as f:
    json.dump({
        'date': date_str,
        'generated_at': iso_str,
        'source_basis': '2026-04-19 live-source verification plus repository-verified same-week fallbacks',
        'scoring_reference': str(BASE / 'scoring_calculations_2026-04-19.md')
    }, f, indent=2)
    f.write('\n')

print(timestamped_json)
print(latest_json)
print(timestamped_md)
print(latest_md)
print(report_csv)
print(factor_detail)
