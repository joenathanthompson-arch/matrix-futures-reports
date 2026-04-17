from __future__ import annotations

import json
from pathlib import Path
from statistics import mean

DATE = "2026-04-17"
GENERATED_AT = "2026-04-17T06:46:04Z"
NY_TIME = "02:46 EDT"
STAMP = "2026-04-17_0246"
METHODOLOGY_VERSION = "3.0_STRATEGY"

ROOT = Path("/home/ubuntu/matrix-futures-reports")
BIAS_DIR = ROOT / "data" / "bias_scores"
EXEC_DIR = ROOT / "data" / "executive_summaries"

for directory in [BIAS_DIR, EXEC_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

macro = {
    "fed_stance": {"classification": "NEUTRAL_HOLD", "score": 0, "note": "FedWatch direct access returned 403 in-session, but the latest repository-verified April 16 read remained overwhelmingly centered on no change for the April 28-29 FOMC meeting."},
    "real_yields": {"classification": "FLAT", "score": 0, "note": "FRED DFII10 rose only 1 bp to 1.90 on April 15, which remains inside the methodology's flat band."},
    "dxy": {"classification": "WEAK_ON_5D", "score": 1, "note": "DXY was 98.280, up 0.10% on the day but down 0.60% over five days and 1.28% over one month."},
    "risk_mood": {"classification": "BALANCED", "score": 0, "note": "VIX spot at 17.94 remains in the balanced 15-20 band."},
    "vix_direction": {"classification": "FLAT", "score": 0, "note": "Cboe showed 0.00% day-over-day change for VIX."},
    "growth": {"classification": "STABLE", "score": 0, "note": "Atlanta Fed GDPNow held at 1.3% for 2026:Q1, implying a soft but not decisively deteriorating growth backdrop."},
    "credit_spreads": {"classification": "WIDENING", "score": -1, "note": "HY OAS widened marginally to 2.85 from 2.84."},
    "curve": {"classification": "STEEPENING", "score": 1, "note": "The 2s10s curve rose to 0.54 from 0.53, indicating mild steepening."},
    "move": {"classification": "FALLING", "score": 1, "note": "MOVE fell 3.01% on the day and 10.97% over five days."},
    "sox": {"classification": "RISING", "score": 1, "note": "SOX rose 0.97% on the day and 5.87% over five days."},
    "oil_supply": {"classification": "TIGHTENING", "score": 1, "note": "Markets still face an effectively closed Strait of Hormuz and active supply-disruption risk despite diplomacy."},
    "inventories": {"classification": "DRAW", "score": 1, "note": "EIA weekly summary reported a 0.9 million barrel crude draw."},
    "geopolitical": {"classification": "STABLE", "score": 0, "note": "Ceasefire-extension optimism is offset by blockade and shipping-risk language, so the conflict premium is mixed rather than clearly rising or easing."},
    "gold_etf_flows": {"classification": "OUTFLOWS", "score": -1, "note": "World Gold Council reported record March outflows of US$12bn, the largest monthly outflow on record."},
    "ecb_stance": {"classification": "HAWKISH_HOLD", "score": 1, "note": "The ECB left rates unchanged in March but maintained an upside-inflation-risk tone."},
    "eurozone_growth": {"classification": "STABLE", "score": 0, "note": "Eurozone growth remains subdued rather than decisively reaccelerating."},
    "rba_stance": {"classification": "HAWKISH", "score": 1, "note": "The RBA raised the cash rate by 25 bps to 4.10% in March and stressed upside inflation risks."},
    "aud_rate_diff": {"classification": "SUPPORTIVE", "score": 1, "note": "RBA hawkishness versus a neutral Fed keeps the AUD-USD rate backdrop supportive."},
    "china_growth": {"classification": "ACCELERATING", "score": 1, "note": "The accessible China PMI page showed official NBS manufacturing PMI at 50.4 in March versus 49.0 prior, returning to expansion."},
    "copper": {"classification": "RISING", "score": 1, "note": "Copper held above $6/lb and was on track for a fourth consecutive weekly advance."},
    "boj_stance": {"classification": "HAWKISH", "score": 1, "note": "The March 19 BoJ statement said the Bank would continue to raise the policy rate if the outlook is realized."},
    "jpy_rate_diff": {"classification": "NARROWING_SUPPORTIVE", "score": 1, "note": "BoJ normalization still narrows the historic policy gap versus the Fed."},
    "eur_rate_diff": {"classification": "SUPPORTIVE", "score": 1, "note": "ECB firmness versus a neutral Fed leaves the EUR-USD rate differential supportive."},
}

signals = [
    (7, "STRONG_BULLISH"),
    (5, "STRONG_BULLISH"),
    (3, "BULLISH"),
    (1, "SLIGHT_BULLISH"),
    (0, "NEUTRAL"),
    (-1, "SLIGHT_BEARISH"),
    (-3, "BEARISH"),
    (-5, "STRONG_BEARISH"),
]


def score_to_signal(score: int) -> str:
    if score >= 5:
        return "STRONG_BULLISH"
    if score >= 3:
        return "BULLISH"
    if score >= 1:
        return "SLIGHT_BULLISH"
    if score == 0:
        return "NEUTRAL"
    if score <= -5:
        return "STRONG_BEARISH"
    if score <= -3:
        return "BEARISH"
    return "SLIGHT_BEARISH"


def strategy(score: int, symbol: str) -> tuple[str, str, str]:
    if score == 0:
        return ("RANGE_TRADE", "INTRADAY", "session")
    if abs(score) >= 5:
        return ("TREND_FOLLOW", "SWING", "2-5 days")
    if abs(score) >= 3:
        if symbol in {"NQ", "CL", "6E"}:
            return ("TREND_FOLLOW", "SWING", "1-2 days")
        return ("TREND_FOLLOW", "SWING", "1-2 days")
    if symbol in {"ES", "NQ", "YM", "RTY"}:
        return ("IB_BREAKOUT", "INTRADAY", "session")
    return ("IB_BREAKOUT", "INTRADAY", "session")


def confidence(score: int, symbol: str) -> int:
    base = {
        0: 5,
        1: 6,
        2: 6,
        3: 7,
        4: 7,
        5: 7,
        6: 8,
        7: 8,
        8: 8,
        9: 8,
        10: 9,
    }[abs(score)]
    if symbol == "GC":
        base -= 1
    if symbol in {"6E", "6J"}:
        base += 0
    return max(1, min(10, base))


scores = {
    "GC": {
        "instrument": "Gold",
        "score": macro["fed_stance"]["score"] + macro["real_yields"]["score"] * 2 + macro["dxy"]["score"] + macro["risk_mood"]["score"] + macro["growth"]["score"] + macro["oil_supply"]["score"] + macro["gold_etf_flows"]["score"],
        "analysis": "Gold retains a mild bullish bias because the broader dollar trend remains weak and oil-related inflation risk has not fully disappeared. Flat real yields and record March ETF outflows keep conviction modest rather than high, so the metal is treated as a directional but lower-energy upside setup.",
    },
    "SI": {
        "instrument": "Silver",
        "score": macro["fed_stance"]["score"] + macro["real_yields"]["score"] + macro["dxy"]["score"] + macro["risk_mood"]["score"] + macro["growth"]["score"] + macro["copper"]["score"] + macro["gold_etf_flows"]["score"],
        "analysis": "Silver inherits support from the softer multi-session dollar backdrop and a clearly rising copper market. ETF-flow headwinds and a balanced risk backdrop prevent a stronger score, but the industrial-metals tone keeps bias modestly constructive.",
    },
    "CL": {
        "instrument": "Crude Oil",
        "score": macro["oil_supply"]["score"] * 2 + macro["inventories"]["score"] * 2 + macro["growth"]["score"] * 2 + macro["geopolitical"]["score"] * 2 + macro["dxy"]["score"],
        "analysis": "Crude oil is the highest-conviction commodity long in this run. The EIA crude draw, still-disrupted Hormuz backdrop, and weaker dollar all support higher prices even though diplomacy has prevented a full re-acceleration in the conflict premium.",
    },
    "ES": {
        "instrument": "S&P 500",
        "score": macro["fed_stance"]["score"] + macro["real_yields"]["score"] * 2 + macro["dxy"]["score"] + macro["risk_mood"]["score"] + macro["growth"]["score"] + macro["credit_spreads"]["score"] + macro["vix_direction"]["score"],
        "analysis": "The broad equity benchmark is neutral because supportive dollar conditions are offset by slightly wider credit spreads and only a balanced volatility regime. Without falling real yields or a stronger growth impulse, ES lacks enough macro fuel for a higher-conviction directional call.",
    },
    "NQ": {
        "instrument": "Nasdaq 100",
        "score": macro["fed_stance"]["score"] + macro["real_yields"]["score"] * 2 + macro["dxy"]["score"] + macro["risk_mood"]["score"] + macro["growth"]["score"] + macro["sox"]["score"] * 2 + macro["move"]["score"],
        "analysis": "Nasdaq keeps a bullish bias because semiconductors remain firmly bid and rates volatility is falling sharply. A softer dollar also helps growth assets, leaving NQ with one of the cleaner pro-risk setups among the index complex.",
    },
    "YM": {
        "instrument": "Dow Jones",
        "score": macro["fed_stance"]["score"] + macro["real_yields"]["score"] + macro["dxy"]["score"] + macro["risk_mood"]["score"] + macro["growth"]["score"] * 2 + macro["credit_spreads"]["score"] + macro["curve"]["score"],
        "analysis": "Dow bias is only slightly bullish. The softer dollar and a mild steepening in the curve help cyclicals, but wider credit spreads and only stable growth keep the signal in the lower-conviction bucket.",
    },
    "RTY": {
        "instrument": "Russell 2000",
        "score": macro["fed_stance"]["score"] + macro["real_yields"]["score"] + macro["dxy"]["score"] + macro["risk_mood"]["score"] + macro["growth"]["score"] * 2 + macro["credit_spreads"]["score"] * 2 + macro["curve"]["score"],
        "analysis": "Russell 2000 remains neutral because the small-cap complex benefits from a weaker dollar and slightly steeper curve, but it is more sensitive to the modest widening in high-yield spreads than the large-cap benchmarks. That leaves RTY without a clean macro edge at the moment.",
    },
    "6E": {
        "instrument": "Euro",
        "score": macro["ecb_stance"]["score"] * 2 + macro["eurozone_growth"]["score"] + macro["eur_rate_diff"]["score"] * 2 + macro["dxy"]["score"] + macro["risk_mood"]["score"],
        "analysis": "The euro posts a strong bullish bias because the ECB's still-firm inflation posture combines with a supportive rate differential and a weaker multi-session dollar trend. Eurozone growth is not a fresh upside catalyst, but it is stable enough not to dilute the policy-driven FX tailwind.",
    },
    "6A": {
        "instrument": "Australian Dollar",
        "score": macro["rba_stance"]["score"] * 2 + macro["china_growth"]["score"] * 2 + macro["copper"]["score"] + macro["dxy"]["score"] + macro["risk_mood"]["score"] + macro["aud_rate_diff"]["score"] * 2,
        "analysis": "The Australian dollar is the strongest FX expression in the report. A hawkish RBA, improving China manufacturing momentum, rising copper, and a weaker dollar all point in the same direction, creating a durable macro tailwind for AUD futures.",
    },
    "6J": {
        "instrument": "Japanese Yen",
        "score": macro["boj_stance"]["score"] * 2 + macro["jpy_rate_diff"]["score"] * 2 + macro["dxy"]["score"] + macro["risk_mood"]["score"],
        "analysis": "The yen remains strongly supported by the combination of ongoing BoJ normalization and a narrower U.S.-Japan rate gap than in prior years. The weak multi-session dollar trend adds to that support even though risk mood itself is not overtly defensive.",
    },
}

for symbol, data in scores.items():
    s = data["score"]
    signal = score_to_signal(s)
    approach, mode, hold = strategy(s, symbol)
    data["signal"] = signal
    data["confidence"] = confidence(s, symbol)
    data["recommended_approach"] = approach
    data["recommended_mode"] = mode
    data["hold_expectation"] = hold

asset_groups = {
    "COMMODITIES": [scores[s]["score"] for s in ["GC", "SI", "CL"]],
    "INDICES": [scores[s]["score"] for s in ["ES", "NQ", "YM", "RTY"]],
    "FX": [scores[s]["score"] for s in ["6E", "6A", "6J"]],
}
asset_class_bias = {k: score_to_signal(round(mean(v))) for k, v in asset_groups.items()}

payload = {
    "date": DATE,
    "generated_at": GENERATED_AT,
    "methodology_version": METHODOLOGY_VERSION,
    "scores": {
        symbol: {
            "score": data["score"],
            "signal": data["signal"],
            "confidence": data["confidence"],
            "recommended_approach": data["recommended_approach"],
            "recommended_mode": data["recommended_mode"],
            "hold_expectation": data["hold_expectation"],
        }
        for symbol, data in scores.items()
    },
    "asset_class_bias": asset_class_bias,
    "key_drivers": [
        "Weak multi-session U.S. dollar trend despite a small daily DXY uptick",
        "Non-U.S. central-bank support remains stronger than the Fed backdrop for EUR, AUD, and JPY",
        "SOX strength and a sharply lower MOVE index are supporting tech and broader risk appetite",
        "WTI remains supported by a crude draw and persistent Middle East supply-disruption risk",
    ],
    "data_quality": {
        "stale_sources": [
            "CME FedWatch probabilities were not directly accessible in-session because the page returned HTTP 403.",
            "GDPNow was last updated on 2026-04-09 and remains the latest official Atlanta Fed estimate.",
        ],
        "fallbacks_used": [
            "Used the repository's April 16 FedWatch note plus the official Fed calendar after direct CME access failed.",
            "Used TradingEconomics copper and crude market pages where Reuters or Investing.com access was restricted.",
            "Used the World Gold Council April ETF-flows research page to confirm March outflows.",
            "Used the locally extracted BoJ March 19 PDF and EIA weekly petroleum PDF summary.",
        ],
        "overnight_changes": [
            "DXY remained weak on the 5-day and 1-month horizon even as it rose 0.10% intraday.",
            "VIX sat at 17.94 with a flat daily change, keeping risk mood balanced.",
            "SOX extended its advance while MOVE fell another 3.01%, reinforcing the tech-risk backdrop.",
        ],
    },
    "catalyst_proximity": {
        "imminent": ["Bank of Japan policy normalization remains a live FX catalyst"],
        "near_term": ["Federal Reserve meeting on 2026-04-28 to 2026-04-29"],
        "background": ["Middle East supply-risk negotiations continue to influence oil and inflation expectations"],
    },
}

json_text = json.dumps(payload, indent=2)
(BIAS_DIR / f"{STAMP}.json").write_text(json_text + "\n", encoding="utf-8")
(BIAS_DIR / "latest.json").write_text(json_text + "\n", encoding="utf-8")

highest = sorted(scores.items(), key=lambda item: abs(item[1]["score"]), reverse=True)[:3]
overall = "MIXED"
if len({v for v in asset_class_bias.values()}) == 1:
    overall = next(iter(asset_class_bias.values()))
elif any(v.startswith("STRONG") for v in asset_class_bias.values()):
    overall = "BULLISH"
else:
    overall = "MIXED_TO_BULLISH"

lines = []
lines.append("# Matrix Futures Daily Bias Report")
lines.append(f"**Date:** {DATE} | **Time:** {NY_TIME}")
lines.append("")
lines.append("---")
lines.append("")
lines.append(f"## Overall Market Bias: {overall}")
lines.append("")
lines.append("The current macro map leans constructive rather than uniformly aggressive. A weaker multi-session dollar, strong non-U.S. rate-differential support, firm semiconductor leadership, and lower rates volatility are offset only partially by slightly wider credit spreads and a still-balanced volatility regime.")
lines.append("")
lines.append("Crude oil and the FX complex carry the clearest directional macro alignment, while U.S. equity indices are more selective, with Nasdaq stronger than the broader benchmark set. Commodities outside crude remain positive but lower-conviction because ETF-flow and real-yield signals are not fully aligned.")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## Asset Class Summary")
lines.append("")
lines.append("| Asset Class | Bias | Key Driver |")
lines.append("|-------------|------|------------|")
lines.append(f"| Commodities | {asset_class_bias['COMMODITIES']} | Weak USD and resilient oil-inflation impulse offset gold-flow headwinds |")
lines.append(f"| Indices | {asset_class_bias['INDICES']} | SOX leadership and falling MOVE support risk assets, but credit spreads temper breadth |")
lines.append(f"| FX | {asset_class_bias['FX']} | ECB, RBA, and BoJ policy support combines with a weaker USD backdrop |")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## Highest Conviction Signals")
lines.append("")
lines.append("| Instrument | Score | Signal | Confidence |")
lines.append("|------------|-------|--------|------------|")
for symbol, data in highest:
    lines.append(f"| {symbol} | {data['score']:+d} | {data['signal']} | {data['confidence']}/10 |")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## Full Instrument Breakdown")
lines.append("")
order = ["GC", "SI", "CL", "ES", "NQ", "YM", "RTY", "6E", "6A", "6J"]
for symbol in order:
    data = scores[symbol]
    lines.append(f"### {symbol} ({data['instrument']}): {data['score']:+d} {data['signal']} ({data['confidence']}/10)")
    lines.append(f"**Approach:** {data['recommended_approach']} | **Mode:** {data['recommended_mode']} | **Hold:** {data['hold_expectation']}")
    lines.append(data['analysis'])
    lines.append("")
lines.append("---")
lines.append("")
lines.append("## Key Macro Themes")
lines.append("")
lines.append("1. **Dollar softness still matters**: DXY has only a mild daily bounce, but the five-day and one-month trend remains negative, keeping a broad tailwind under non-USD assets.")
lines.append("2. **Leadership is selective, not universal**: SOX and MOVE clearly support Nasdaq-style risk, while wider credit spreads keep broad beta and small caps from matching that strength.")
lines.append("3. **Energy risk premium has compressed only partially**: diplomacy has limited the geopolitical escalation score, but physical supply risk in the Gulf still supports WTI.")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## Upcoming Catalysts")
lines.append("")
lines.append("### Imminent (< 1 Week)")
lines.append("- Ongoing Middle East negotiations affecting oil supply expectations")
lines.append("")
lines.append("### Near-Term (1-4 Weeks)")
lines.append("- Federal Reserve meeting (2026-04-28 to 2026-04-29)")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## Data Quality")
lines.append("")
lines.append("- Most pricing and central-bank inputs were refreshed in-session from official or accessible market pages on 2026-04-17.")
lines.append("- FedWatch required a documented fallback because direct CME access returned HTTP 403; conviction was kept moderate where that mattered.")
lines.append(f"- Average confidence: {mean([scores[s]['confidence'] for s in order]):.1f}/10")
lines.append("")
lines.append("---")
lines.append("**End of Report**")

md_text = "\n".join(lines) + "\n"
(EXEC_DIR / f"{STAMP}.md").write_text(md_text, encoding="utf-8")
(EXEC_DIR / "latest.md").write_text(md_text, encoding="utf-8")

print(f"Wrote {BIAS_DIR / f'{STAMP}.json'}")
print(f"Wrote {BIAS_DIR / 'latest.json'}")
print(f"Wrote {EXEC_DIR / f'{STAMP}.md'}")
print(f"Wrote {EXEC_DIR / 'latest.md'}")
