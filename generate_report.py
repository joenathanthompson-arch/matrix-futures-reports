from __future__ import annotations

import json
from pathlib import Path
from statistics import mean

DATE = "2026-04-17"
GENERATED_AT = "2026-04-17T11:58:10Z"
STAMP = "2026-04-17_1158"
TIME_DISPLAY = "11:58 UTC"
METHODOLOGY_VERSION = "3.0_STRATEGY"

factor_states = {
    "fed_stance": {"label": "Neutral hold", "score": 0, "evidence": "FedWatch showed about 99.5% no change for the 30 Apr 2026 meeting."},
    "real_yields": {"label": "Flat", "score": 0, "evidence": "DFII10 rose only from 1.89 on 2026-04-14 to 1.90 on 2026-04-15, inside the ±5 bps flat band."},
    "usd": {"label": "Weak/Falling", "score": 1, "evidence": "TradingView showed DXY near 98.098, down about 0.08% on the day and 0.78% over five days."},
    "risk_mood": {"label": "Balanced", "score": 0, "evidence": "Cboe VIX was 17.86, which falls in the 15-20 balanced band."},
    "growth": {"label": "Slowing", "score": 1, "evidence": "Atlanta Fed GDPNow estimated Q1 2026 growth at 1.3% and described the trajectory as slowing."},
    "oil_supply": {"label": "Tightening/Disruption", "score": 1, "evidence": "Current oil reporting still describes a major supply shock and heavily disrupted Hormuz flows."},
    "gold_etf": {"label": "Outflows", "score": -1, "evidence": "World Gold Council said March 2026 saw record monthly outflows globally."},
    "credit": {"label": "Flat", "score": 0, "evidence": "HY OAS moved only from 2.84 on 2026-04-14 to 2.85 on 2026-04-15."},
    "vix_direction": {"label": "Falling", "score": 1, "evidence": "Cboe VIX was down 0.45% on the day."},
    "sox": {"label": "Rising", "score": 1, "evidence": "TradingView showed SOX up 0.97% on the day and 5.87% over five days."},
    "move": {"label": "Falling", "score": 1, "evidence": "TradingView showed MOVE down 3.01% on the day and 10.97% over five days."},
    "inventories": {"label": "Draw", "score": 1, "evidence": "EIA-reported crude inventories fell by 913,000 barrels in the week ended 2026-04-10."},
    "geopolitical": {"label": "Easing", "score": -1, "evidence": "Crude was falling on optimism around a U.S.-Iran ceasefire and possible Hormuz reopening."},
    "curve": {"label": "Steepening", "score": 1, "evidence": "2s10s rose from 0.53 on 2026-04-15 to 0.54 on 2026-04-16."},
    "copper": {"label": "Rising", "score": 1, "evidence": "Copper was on track for a fourth consecutive weekly advance above $6/lb."},
    "ecb": {"label": "Hawkish hold", "score": 1, "evidence": "ECB held rates but still highlighted upside inflation risks and raised inflation forecasts."},
    "eur_diff": {"label": "Widening vs USD", "score": 1, "evidence": "ECB remains firmer than a neutral Fed, modestly supporting the EUR rate differential at the margin."},
    "euro_growth": {"label": "Slowing", "score": -1, "evidence": "ECB staff projections cut 2026 euro-area growth to 0.9% and described a weaker short-term outlook."},
    "rba": {"label": "Hawkish/Tightening", "score": 1, "evidence": "RBA hiked to 4.1% in March after another hike in February and emphasized upside inflation risks."},
    "aud_diff": {"label": "Widening vs USD", "score": 1, "evidence": "Australia policy rate at 4.1% stands above the Fed's 3.5%-3.75% range."},
    "risk_sentiment": {"label": "Neutral", "score": 0, "evidence": "VIX in the balanced band implies neither risk-on nor risk-off for AUD."},
    "china_growth": {"label": "Accelerating", "score": 1, "evidence": "Official and private March PMIs were both above 50 at 50.4 and 50.8."},
    "boj": {"label": "Hawkish/Tightening", "score": 1, "evidence": "BoJ held at 0.75% but said it would continue raising rates if the outlook holds."},
    "jpy_diff": {"label": "Narrowing vs USD", "score": 1, "evidence": "BoJ normalization continues while the Fed remains on hold, gradually narrowing the policy divergence."},
}

instrument_configs = {
    "GC": [("fed_stance", 1), ("real_yields", 2), ("usd", 1), ("risk_mood", 1), ("growth", 1), ("oil_supply", 1), ("gold_etf", 1)],
    "SI": [("fed_stance", 1), ("real_yields", 1), ("usd", 1), ("risk_mood", 1), ("growth", 1), ("copper", 1), ("gold_etf", 1)],
    "CL": [("oil_supply", 2), ("inventories", 1), ("growth", 2), ("geopolitical", 1), ("usd", 1)],
    "ES": [("fed_stance", 1), ("real_yields", 2), ("usd", 1), ("risk_mood", 1), ("growth", 1), ("credit", 1), ("vix_direction", 1)],
    "NQ": [("fed_stance", 1), ("real_yields", 2), ("usd", 1), ("risk_mood", 1), ("growth", 1), ("sox", 1), ("move", 1)],
    "YM": [("fed_stance", 1), ("real_yields", 1), ("usd", 1), ("risk_mood", 1), ("growth", 2), ("credit", 1), ("curve", 1)],
    "RTY": [("fed_stance", 1), ("real_yields", 1), ("usd", 1), ("risk_mood", 1), ("growth", 2), ("credit", 2), ("curve", 1)],
    "6E": [("fed_stance", 1), ("ecb", 1), ("eur_diff", 2), ("usd", 1), ("risk_mood", 1), ("euro_growth", 1)],
    "6A": [("fed_stance", 1), ("rba", 1), ("aud_diff", 1), ("usd", 1), ("risk_sentiment", 2), ("china_growth", 2), ("copper", 1)],
    "6J": [("fed_stance", 1), ("boj", 2), ("jpy_diff", 2), ("usd", 1), ("risk_mood", 1)],
}

confidence_map = {
    "GC": 5,
    "SI": 6,
    "CL": 7,
    "ES": 6,
    "NQ": 7,
    "YM": 6,
    "RTY": 6,
    "6E": 6,
    "6A": 8,
    "6J": 7,
}

strategy_map = {
    "GC": ("IB_BREAKOUT", "INTRADAY", "session"),
    "SI": ("IB_BREAKOUT", "INTRADAY", "session"),
    "CL": ("TREND_FOLLOW", "SWING", "2-5 days"),
    "ES": ("IB_BREAKOUT", "INTRADAY", "session"),
    "NQ": ("TREND_FOLLOW", "SWING", "1-2 days"),
    "YM": ("IB_BREAKOUT", "INTRADAY", "session"),
    "RTY": ("IB_BREAKOUT", "INTRADAY", "session"),
    "6E": ("IB_BREAKOUT", "INTRADAY", "session"),
    "6A": ("TREND_FOLLOW", "SWING", "2-5 days"),
    "6J": ("TREND_FOLLOW", "SWING", "2-5 days"),
}

name_map = {
    "GC": "Gold",
    "SI": "Silver",
    "CL": "Crude Oil",
    "ES": "S&P 500",
    "NQ": "Nasdaq 100",
    "YM": "Dow Jones",
    "RTY": "Russell 2000",
    "6E": "Euro",
    "6A": "Australian Dollar",
    "6J": "Japanese Yen",
}


def get_signal(score: int) -> str:
    if score >= 5:
        return "STRONG_BULLISH"
    if score >= 3:
        return "BULLISH"
    if score >= 1:
        return "SLIGHT_BULLISH"
    if score == 0:
        return "NEUTRAL"
    if score >= -2:
        return "SLIGHT_BEARISH"
    if score >= -4:
        return "BEARISH"
    return "STRONG_BEARISH"


def class_bias(scores: list[int]) -> str:
    avg = round(mean(scores))
    return get_signal(avg)


results = {}
for symbol, config in instrument_configs.items():
    score = sum(factor_states[f]["score"] * w for f, w in config)
    signal = get_signal(score)
    approach, mode, hold = strategy_map[symbol]
    results[symbol] = {
        "score": score,
        "signal": signal,
        "confidence": confidence_map[symbol],
        "recommended_approach": approach,
        "recommended_mode": mode,
        "hold_expectation": hold,
    }

asset_class_bias = {
    "COMMODITIES": class_bias([results[s]["score"] for s in ["GC", "SI", "CL"]]),
    "INDICES": class_bias([results[s]["score"] for s in ["ES", "NQ", "YM", "RTY"]]),
    "FX": class_bias([results[s]["score"] for s in ["6E", "6A", "6J"]]),
}

json_payload = {
    "date": DATE,
    "generated_at": GENERATED_AT,
    "methodology_version": METHODOLOGY_VERSION,
    "scores": results,
    "asset_class_bias": asset_class_bias,
    "key_drivers": [
        "Broad USD weakness is still supporting commodities and non-USD FX despite a neutral Fed-hold setup.",
        "Energy markets remain supply-tight, but ceasefire optimism has started to compress the geopolitical premium at the margin.",
        "SOX strength and a sharply lower MOVE index are giving growth-sensitive risk assets a cleaner tailwind than broad volatility alone suggests.",
        "Australia and Japan retain the strongest non-U.S. central-bank support, while eurozone growth remains a limiting factor for the euro.",
    ],
    "data_quality": {
        "stale_sources": [
            "Atlanta Fed GDPNow was last updated on 2026-04-09 and remains the latest official estimate.",
            "FRED DFII10 and BAMLH0A0HYM2 latest observations are from 2026-04-15, so those series carry normal reporting lag.",
        ],
        "fallbacks_used": [
            "Used direct CME FedWatch page inspection for hold probabilities.",
            "Used TradingEconomics central-bank and market pages for ECB, RBA, BoJ, Fed, and copper context where direct primary pages were less accessible in-session.",
            "Used BOE Report's readable Reuters pickup to confirm the latest EIA crude inventory draw.",
            "Used World Gold Council April 2026 ETF-flows research to confirm March gold outflows.",
        ],
        "overnight_changes": [
            "DXY remained weak at roughly 98.10 and was down about 0.78% over five days.",
            "VIX sat at 17.86 and fell 0.45% on the day, keeping the regime balanced rather than risk-off.",
            "MOVE fell 3.01% on the day while SOX rose 0.97%, reinforcing a selective pro-growth risk backdrop.",
            "WTI slipped toward $91 on Iran-deal optimism even though physical Gulf disruptions still underpin supply tightness.",
        ],
    },
    "catalyst_proximity": {
        "imminent": [
            "Middle East ceasefire and U.S.-Iran negotiation headlines remain an active day-to-day oil catalyst."
        ],
        "near_term": [
            "Federal Reserve meeting on 2026-04-28 to 2026-04-29"
        ],
        "background": [
            "BoJ normalization and RBA inflation vigilance continue to support JPY and AUD relative to USD."
        ],
    },
}

summary_lines = [
    "# Matrix Futures Daily Bias Report",
    f"**Date:** {DATE} | **Time:** {TIME_DISPLAY}",
    "",
    "---",
    "",
    "## Overall Market Bias: BULLISH",
    "",
    "The macro map remains constructive, with the dollar still soft, crude supply conditions still tight, and non-U.S. central-bank support strongest in Australia and Japan. The main offset is that volatility is only balanced rather than overtly risk-on, while growth data remain mixed and somewhat stale in a few U.S. macro series.",
    "",
    "U.S. equities lean bullish rather than explosive, because semiconductors and lower rates volatility are supportive but the Fed signal itself is neutral. Commodities are positive, with crude clearly stronger than the precious-metals complex, and FX remains the most favorable asset class overall.",
    "",
    "---",
    "",
    "## Asset Class Summary",
    "",
    "| Asset Class | Bias | Key Driver |",
    "|-------------|------|------------|",
    f"| Commodities | {asset_class_bias['COMMODITIES']} | Weak USD and a still-tight oil backdrop outweigh ETF-flow drag in metals |",
    f"| Indices | {asset_class_bias['INDICES']} | Falling MOVE and strong SOX leadership support risk assets despite only balanced VIX conditions |",
    f"| FX | {asset_class_bias['FX']} | AUD and JPY retain the strongest central-bank support against a softer USD |",
    "",
    "---",
    "",
    "## Highest Conviction Signals",
    "",
    "| Instrument | Score | Signal | Confidence |",
    "|------------|-------|--------|------------|",
    f"| 6A | +{results['6A']['score']} | {results['6A']['signal']} | {results['6A']['confidence']}/10 |",
    f"| CL | +{results['CL']['score']} | {results['CL']['signal']} | {results['CL']['confidence']}/10 |",
    f"| 6J | +{results['6J']['score']} | {results['6J']['signal']} | {results['6J']['confidence']}/10 |",
    "",
    "---",
    "",
    "## Full Instrument Breakdown",
    "",
]

narratives = {
    "GC": "Gold is mildly constructive at +2 because a weaker dollar and slower U.S. growth continue to offer macro support. Flat real yields and heavy March ETF outflows keep conviction restrained, so this is better treated as a tactical upside bias than a high-energy trend signal.",
    "SI": "Silver also carries a slight bullish bias at +2. The weaker dollar and a clearly rising copper market help the industrial side of the metal, but gold-flow outflows and only balanced risk conditions stop the score from pushing higher.",
    "CL": "Crude oil remains a strong bullish macro expression at +5. The latest EIA draw and still-disrupted Gulf supply backdrop dominate, although ceasefire optimism has started to cap the geopolitical premium and explains why the score is strong rather than extreme.",
    "ES": "The S&P 500 shifts into a bullish rather than neutral stance at +3. A softer dollar, slower-growth Fed backdrop, and falling VIX direction help, but the absence of falling real yields and only flat credit spreads argue for a breakout-style setup instead of a deep-conviction swing call.",
    "NQ": "Nasdaq holds one of the cleaner pro-risk signals at +4. Strong semiconductor leadership and a sharply lower MOVE index reinforce the softer-dollar backdrop, so technology remains better supported than the broader index complex.",
    "YM": "Dow futures also score +4, reflecting slower-growth support, a softer dollar, and a slightly steeper curve. Even so, the lack of real-yield relief and only flat credit spreads suggest a directional bias with moderate rather than maximum follow-through expectations.",
    "RTY": "Russell 2000 improves to +4 because slower-growth Fed logic, a weaker dollar, and a slightly steeper curve all help domestic cyclicals. However, small caps would look stronger if high-yield spreads were clearly narrowing, so conviction remains only moderate.",
    "6E": "The euro posts a bullish +3 score as the ECB's firmer inflation posture and a softer dollar outweigh the drag from slowing euro-area growth. That mix supports an upside bias, but the growth downgrade argues for a shorter-horizon execution style rather than full trend-chasing.",
    "6A": "The Australian dollar is the strongest signal in the book at +6. A hawkish RBA, a positive Australia-U.S. rate differential, improving China PMI readings, and rising copper all align with the weaker-USD backdrop to create a durable bullish setup.",
    "6J": "The yen remains strongly bullish at +5 because BoJ normalization is still intact and the U.S.-Japan policy gap is gradually narrowing. Dollar softness adds another tailwind, even though the VIX regime itself is balanced rather than overtly defensive.",
}

for symbol in ["GC", "SI", "CL", "ES", "NQ", "YM", "RTY", "6E", "6A", "6J"]:
    info = results[symbol]
    score_text = f"+{info['score']}" if info['score'] > 0 else str(info['score'])
    summary_lines.extend([
        f"### {symbol} ({name_map[symbol]}): {score_text} {info['signal']} ({info['confidence']}/10)",
        f"**Approach:** {info['recommended_approach']} | **Mode:** {info['recommended_mode']} | **Hold:** {info['hold_expectation']}",
        narratives[symbol],
        "",
    ])

avg_conf = round(mean(v["confidence"] for v in results.values()), 1)
summary_lines.extend([
    "---",
    "",
    "## Key Macro Themes",
    "",
    "1. **Dollar weakness still matters**: DXY remains soft enough to support both commodities and non-USD FX even without a dovish-cut Fed impulse.",
    "2. **Energy is tight but less panicked**: physical supply disruption still matters for oil, yet ceasefire optimism has started to reduce the marginal geopolitical premium.",
    "3. **Risk leadership is selective**: semiconductors and lower rate volatility favor NQ-style risk more clearly than a broad, euphoric index breakout regime.",
    "",
    "---",
    "",
    "## Upcoming Catalysts",
    "",
    "### Imminent (< 1 Week)",
    "- U.S.-Iran and broader Middle East ceasefire negotiations affecting oil and inflation expectations",
    "",
    "### Near-Term (1-4 Weeks)",
    "- Federal Reserve meeting (2026-04-28 to 2026-04-29)",
    "",
    "---",
    "",
    "## Data Quality",
    "",
    "- GDPNow is not fully fresh and several FRED series reflect normal one- to two-day reporting lag, so conviction was capped in rate-sensitive instruments.",
    "- Central-bank stance and inventory inputs were refreshed from accessible live pages and readable secondary pickups tied to official releases.",
    f"- Average confidence: {avg_conf}/10",
    "",
    "---",
    "**End of Report**",
])

summary_text = "\n".join(summary_lines) + "\n"

repo = Path("/home/ubuntu/matrix-futures-reports")
json_ts = repo / "data" / "bias_scores" / f"{STAMP}.json"
json_latest = repo / "data" / "bias_scores" / "latest.json"
md_ts = repo / "data" / "executive_summaries" / f"{STAMP}.md"
md_latest = repo / "data" / "executive_summaries" / "latest.md"

json_text = json.dumps(json_payload, indent=2) + "\n"
for path, content in [
    (json_ts, json_text),
    (json_latest, json_text),
    (md_ts, summary_text),
    (md_latest, summary_text),
]:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

print(json.dumps({
    "json_timestamped": str(json_ts),
    "json_latest": str(json_latest),
    "md_timestamped": str(md_ts),
    "md_latest": str(md_latest),
}, indent=2))
