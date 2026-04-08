from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
BIAS_DIR = BASE_DIR / "data" / "bias_scores"
EXEC_DIR = BASE_DIR / "data" / "executive_summaries"
FACTOR_DIR = BASE_DIR / "data" / "factors"

for path in (BIAS_DIR, EXEC_DIR, FACTOR_DIR):
    path.mkdir(parents=True, exist_ok=True)

# Refreshed April 8, 2026 inputs collected or confirmed during this session.
# Where live sources were inaccessible, previously verified same-day repository notes were retained.
macro_data = {
    "fed_stance": 0,
    "real_yields": 0,
    "usd_dxy": 1,
    "risk_mood": 1,
    "vix_direction": 1,
    "growth_narrative": 0,
    "credit_spreads": 0,
    "sox": 1,
    "move_index": 1,
    "yield_curve_2s10s": 1,
    "copper": 1,
    "oil_inventories": -1,
    "oil_supply_shock": 1,
    "geopolitical_risk": 1,
    "gold_etf_flows": 1,
    "ecb_stance": -1,
    "rba_stance": 1,
    "boj_stance": 1,
    "china_growth": 1,
    "eurozone_growth": -1,
    "rate_diff_eur_usd": -1,
    "rate_diff_aud_usd": 1,
    "rate_diff_jpy_usd": 1,
    "risk_sentiment_aud": -1,
}

instrument_configs = {
    "GC": {
        "name": "Gold Futures",
        "factors": {
            "fed_stance": 1,
            "real_yields": 2,
            "usd_dxy": 1,
            "risk_mood": 1,
            "growth_narrative": 1,
            "oil_supply_shock": 1,
            "gold_etf_flows": 1,
        },
    },
    "SI": {
        "name": "Silver Futures",
        "factors": {
            "fed_stance": 1,
            "real_yields": 1,
            "usd_dxy": 1,
            "risk_mood": 1,
            "growth_narrative": 1,
            "copper": 1,
            "gold_etf_flows": 1,
        },
    },
    "CL": {
        "name": "WTI Crude Oil",
        "factors": {
            "oil_supply_shock": 2,
            "oil_inventories": 1,
            "growth_narrative": 2,
            "geopolitical_risk": 1,
            "usd_dxy": 1,
        },
    },
    "ES": {
        "name": "S&P 500 E-mini",
        "factors": {
            "fed_stance": 1,
            "real_yields": 2,
            "usd_dxy": 1,
            "risk_mood": 1,
            "growth_narrative": 1,
            "credit_spreads": 1,
            "vix_direction": 1,
        },
    },
    "NQ": {
        "name": "Nasdaq 100 E-mini",
        "factors": {
            "fed_stance": 1,
            "real_yields": 2,
            "usd_dxy": 1,
            "risk_mood": 1,
            "growth_narrative": 1,
            "sox": 1,
            "move_index": 1,
        },
    },
    "YM": {
        "name": "Dow Jones E-mini",
        "factors": {
            "fed_stance": 1,
            "real_yields": 1,
            "usd_dxy": 1,
            "risk_mood": 1,
            "growth_narrative": 2,
            "credit_spreads": 1,
            "yield_curve_2s10s": 1,
        },
    },
    "RTY": {
        "name": "Russell 2000 E-mini",
        "factors": {
            "fed_stance": 1,
            "real_yields": 1,
            "usd_dxy": 1,
            "risk_mood": 1,
            "growth_narrative": 2,
            "credit_spreads": 2,
            "yield_curve_2s10s": 1,
        },
    },
    "6E": {
        "name": "Euro FX",
        "factors": {
            "fed_stance": 1,
            "ecb_stance": 1,
            "rate_diff_eur_usd": 2,
            "usd_dxy": 1,
            "risk_mood": 1,
            "eurozone_growth": 1,
        },
    },
    "6A": {
        "name": "Australian Dollar",
        "factors": {
            "fed_stance": 1,
            "rba_stance": 1,
            "rate_diff_aud_usd": 1,
            "usd_dxy": 1,
            "risk_sentiment_aud": 2,
            "china_growth": 2,
            "copper": 1,
        },
    },
    "6J": {
        "name": "Japanese Yen",
        "factors": {
            "fed_stance": 1,
            "boj_stance": 2,
            "rate_diff_jpy_usd": 2,
            "usd_dxy": 1,
            "risk_mood": 1,
        },
    },
}

factor_notes = {
    "fed_stance": "Repository-local CME FedWatch note dated April 8, 2026 showed 99.5% probability of no change for the April 30 FOMC meeting, supporting a neutral-hold classification.",
    "real_yields": "FRED DFII10 page showed the latest official observation at 1.96% on 2026-04-07; because a machine-readable prior-close comparison could not be fully verified during this session, the factor was scored FLAT conservatively.",
    "usd_dxy": "TradingView DXY page showed 99.024 on 2026-04-08, down 0.492 points (-0.49%) from a prior close of 99.516.",
    "risk_mood": "Cboe VIX page showed a spot price of 21.04 on 2026-04-08, which remains above the 20 threshold and therefore keeps the regime risk-off.",
    "vix_direction": "Cboe VIX page showed a daily change of -18.39% (-4.74) on 2026-04-08, so the directional VIX signal is falling.",
    "growth_narrative": "Atlanta Fed GDPNow was 1.3% for 2026:Q1 on 2026-04-07, unchanged versus the repository's earlier same-day reference point, so the growth signal was classified as stable rather than slowing further.",
    "credit_spreads": "FRED HY OAS remained available only with a lagged official print from 2026-04-06; absent a clearly verified directional change, the factor was kept FLAT.",
    "sox": "Previously verified same-day repository factor set recorded SOX at 8,003.87, up 1.11% on the day and 6.08% over five days.",
    "move_index": "Previously verified same-day repository factor set recorded MOVE at 83.1452, down 3.24% over 24 hours and down 27.04% over the past week.",
    "yield_curve_2s10s": "Previously verified same-day repository factor set recorded FRED T10Y2Y at 0.52% on 2026-04-07, leaving the curve positively sloped and normalized from inversion.",
    "copper": "Previously verified same-day repository factor set recorded HG1! at 5.7490 USD/lb, up 3.34% on the day and 2.20% over five days.",
    "oil_inventories": "Previously verified same-day repository factor set used the EIA Weekly Petroleum Status Report showing commercial crude inventories rose by 5.5 million barrels to 461.6 million.",
    "oil_supply_shock": "Previously verified same-day repository factor set retained Reuters-syndicated and EIA-linked reporting that Strait of Hormuz disruption continued to tighten effective global oil supply.",
    "geopolitical_risk": "Middle East conflict and tanker-flow uncertainty continue to keep energy-market geopolitical risk elevated.",
    "gold_etf_flows": "Previously verified same-day repository factor set used a World Gold Council weekly monitor reference showing global gold ETFs recorded a 21-tonne inflow at the start of April.",
    "ecb_stance": "ECB key policy rates remain at 2.00% deposit, 2.15% MRO, and 2.40% marginal lending after a sequence of cuts, preserving an easing bias.",
    "rba_stance": "RBA cash rate target remains 4.10% following the March 18, 2026 increase.",
    "boj_stance": "BoJ policy remains around 0.75% with normalization still the dominant direction of travel, supporting a hawkish relative stance.",
    "china_growth": "Previously verified same-day repository factor set retained the official China NBS manufacturing PMI rebound to 50.4 in March from 49.0 in February.",
    "eurozone_growth": "Previously verified same-day repository factor set retained euro area composite PMI at 50.7 in March, down from 51.9 in February.",
    "rate_diff_eur_usd": "A neutral Fed against an easing-biased ECB keeps the policy differential moving against EUR.",
    "rate_diff_aud_usd": "RBA policy at 4.10% versus Fed 3.50%-3.75% keeps the AUD rate differential supportive.",
    "rate_diff_jpy_usd": "BoJ normalization keeps improving the JPY side of the rate-differential narrative versus a neutral Fed.",
    "risk_sentiment_aud": "AUD remains a pro-cyclical currency, and VIX above 20 keeps the risk-sentiment input mildly adverse.",
}

instrument_display = {
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

analysis_paragraphs = {
    "GC": "Gold holds a constructive bias because the dollar weakened and the volatility regime remains defensive with VIX still above 20. Conviction is moderated by flat rather than falling real yields and by the fact that the growth signal stabilized rather than deteriorated further, which keeps the setup positive without turning into a full high-conviction breakout call.",
    "SI": "Silver also leans higher because a softer dollar and a previously verified rising copper tape continue to support the metal's industrial and precious-metal channels simultaneously. The signal is stronger than a marginal upside lean but still not an outright strong-trend regime because real yields were conservatively held flat and the macro growth signal is no longer worsening intraday.",
    "CL": "WTI crude retains a bullish bias because supply-disruption and geopolitical-risk factors remain supportive while a weaker dollar helps the commodity complex at the margin. The score is held below the strongest tier because the latest verified U.S. inventory signal was still a bearish build and GDPNow was stable rather than accelerating.",
    "ES": "The S&P 500 improves into a bullish but still moderate configuration because the VIX direction turned sharply supportive, the dollar softened, and real yields were not confirmed higher. Even so, the regime is not clean risk-on because the VIX level itself remains above 20 and high-yield spreads were only conservatively treated as flat.",
    "NQ": "Nasdaq gains support from the weaker dollar, a sharply falling VIX direction, and previously verified strength in semiconductors and rates-volatility conditions. Because real yields were not confirmed lower and the VIX level remains elevated, the setup favors bullish participation but not an aggressive extended-duration trend call.",
    "YM": "The Dow carries a bullish bias as the weaker dollar, still-positive curve shape, and stable growth backdrop leave the more cyclical large-cap complex in a better balance than earlier in the session. The signal remains moderate because neither credit spreads nor real yields delivered a freshly verified tailwind beyond flat.",
    "RTY": "Russell 2000 also improves to bullish territory because small caps benefit from a weaker dollar, a normalized curve, and the absence of an additional GDPNow downgrade. Confidence remains only moderate because VIX is still above 20 and the credit-spread input was kept flat rather than positively re-rated.",
    "6E": "The euro remains the main laggard in the basket because the softer dollar is outweighed by an ECB easing bias, a policy differential that still works against EUR, and weak euro-area growth data. That combination leaves the contract mildly bearish rather than neutral even though broad USD conditions were less hostile during the session.",
    "6A": "The Australian dollar stays one of the clearer constructive setups because RBA policy remains supportive, China growth improved in the latest official PMI release, and copper direction remained firm in the previously verified same-day factor set. Risk sentiment is not fully clean with VIX still above 20, but the policy and commodity mix continues to favor AUD strength.",
    "6J": "The Japanese yen remains the highest-conviction signal because the contract benefits simultaneously from dollar weakness, a still-defensive volatility regime, and the ongoing Bank of Japan normalization story. Since 6J rises when the yen strengthens, that combination continues to justify a strong bullish classification even though the Fed itself is only neutral.",
}


def calculate_score(config: dict) -> tuple[int, dict]:
    total = 0
    detail = {}
    for factor, weight in config["factors"].items():
        raw = macro_data[factor]
        weighted = raw * weight
        total += weighted
        detail[factor] = {
            "raw": raw,
            "weight": weight,
            "weighted": weighted,
            "note": factor_notes[factor],
        }
    return total, detail



def get_signal(raw_weighted_score: int) -> tuple[str, int]:
    if raw_weighted_score >= 5:
        return "STRONG_BULLISH", 3
    if raw_weighted_score >= 3:
        return "BULLISH", 2
    if raw_weighted_score >= 1:
        return "SLIGHT_BULLISH", 1
    if raw_weighted_score >= -1:
        return "NEUTRAL", 0
    if raw_weighted_score >= -3:
        return "SLIGHT_BEARISH", -1
    if raw_weighted_score >= -5:
        return "BEARISH", -2
    return "STRONG_BEARISH", -3



def get_confidence(symbol: str, raw_weighted_score: int) -> int:
    abs_score = abs(raw_weighted_score)
    if abs_score >= 6:
        confidence = 8
    elif abs_score >= 4:
        confidence = 7
    elif abs_score >= 2:
        confidence = 6
    else:
        confidence = 5

    if symbol in {"GC", "SI", "ES", "NQ", "YM", "RTY"}:
        confidence -= 1

    return max(4, min(9, confidence))



def get_strategy(raw_weighted_score: int, symbol: str) -> tuple[str, str, str]:
    abs_score = abs(raw_weighted_score)

    if symbol in {"GC", "SI", "CL", "6E", "6A", "6J"}:
        if abs_score >= 5:
            return "TREND_FOLLOW", "SWING", "2-5 days"
        if abs_score >= 3:
            return "TREND_FOLLOW", "SWING", "1-2 days"
        if abs_score >= 1:
            return "IB_BREAKOUT", "INTRADAY", "session"
        return "RANGE_TRADE", "INTRADAY", "session"

    if abs_score >= 5:
        return "TREND_FOLLOW", "SWING", "1-2 days"
    if abs_score >= 3:
        return "TREND_FOLLOW", "SWING", "1-2 days"
    if abs_score >= 1:
        return "IB_BREAKOUT", "INTRADAY", "session"
    return "RANGE_TRADE", "INTRADAY", "session"



def get_asset_class_bias(symbols: list[str], results: dict) -> str:
    avg_score = sum(results[s]["score"] for s in symbols) / len(symbols)
    if avg_score >= 2.5:
        return "STRONG_BULLISH"
    if avg_score >= 1.5:
        return "BULLISH"
    if avg_score >= 0.5:
        return "SLIGHT_BULLISH"
    if avg_score >= -0.5:
        return "NEUTRAL"
    if avg_score >= -1.5:
        return "SLIGHT_BEARISH"
    if avg_score >= -2.5:
        return "BEARISH"
    return "STRONG_BEARISH"



def signed_score(value: int) -> str:
    return f"{value:+d}"



def build_markdown(date_label: str, time_label: str, results: dict, asset_class_bias: dict) -> str:
    avg_conf = sum(results[s]["confidence"] for s in results) / len(results)
    top = sorted(
        results.items(),
        key=lambda kv: (kv[1]["confidence"], kv[1]["score"]),
        reverse=True,
    )[:3]

    lines = []
    lines.append("# Matrix Futures Daily Bias Report")
    lines.append(f"**Date:** {date_label} | **Time:** {time_label} UTC")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Overall Market Bias: BULLISH")
    lines.append("")
    lines.append("Macro conditions improved modestly through the April 8 session as dollar weakness and sharply falling equity volatility supported commodities and most risk assets at the margin. The growth signal stabilized rather than worsening further, which reduced recession-style defensiveness, but cross-currents remain visible in FX where euro weakness still contrasts with stronger AUD and JPY divergence themes.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Asset Class Summary")
    lines.append("")
    lines.append("| Asset Class | Bias | Key Driver |")
    lines.append("|-------------|------|------------|")
    lines.append(f"| Commodities | {asset_class_bias['COMMODITIES']} | Weak USD and still-elevated energy and volatility hedging demand keep metals and crude supported |")
    lines.append(f"| Indices | {asset_class_bias['INDICES']} | Falling VIX direction, softer USD, and stable rather than worsening growth conditions improved the index backdrop |")
    lines.append(f"| FX | {asset_class_bias['FX']} | Dollar weakness helps broadly, but policy divergence still clearly favors AUD and JPY over EUR |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Highest Conviction Signals")
    lines.append("")
    lines.append("| Instrument | Score | Signal | Confidence |")
    lines.append("|------------|-------|--------|------------|")
    for symbol, data in top:
        lines.append(f"| {symbol} | {signed_score(data['score'])} | {data['signal']} | {data['confidence']}/10 |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Full Instrument Breakdown")
    lines.append("")
    for symbol in ["GC", "SI", "CL", "ES", "NQ", "YM", "RTY", "6E", "6A", "6J"]:
        data = results[symbol]
        lines.append(f"### {symbol} ({instrument_display[symbol]}): {signed_score(data['score'])} {data['signal']} ({data['confidence']}/10)")
        lines.append(f"**Approach:** {data['recommended_approach']} | **Mode:** {data['recommended_mode']} | **Hold:** {data['hold_expectation']}")
        lines.append(analysis_paragraphs[symbol])
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Key Macro Themes")
    lines.append("")
    lines.append("1. **The dollar is still the main cross-asset tailwind**: TradingView showed DXY at 99.024, down 0.49% on the session, which supported metals, crude, and non-USD FX.")
    lines.append("2. **Volatility improved directionally, but not fully in level terms**: Cboe VIX fell 18.39% to 21.04, which helped equities and risk assets, yet the index still sits above the 20 threshold that keeps the regime defensively tinted.")
    lines.append("3. **Growth stabilized rather than re-accelerated**: Atlanta Fed GDPNow remained at 1.3% for 2026:Q1, leaving the macro picture softer than trend but no worse than the earlier same-day reference point.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Upcoming Catalysts")
    lines.append("")
    lines.append("### Imminent (< 1 Week)")
    lines.append("- Atlanta Fed GDPNow refresh (Apr 9)")
    lines.append("- China inflation data (Apr 10)")
    lines.append("- Ongoing oil-market headlines tied to Strait of Hormuz shipping conditions")
    lines.append("")
    lines.append("### Near-Term (1-4 Weeks)")
    lines.append("- Federal Reserve meeting (Apr 30)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Data Quality")
    lines.append("")
    lines.append("- Live CME FedWatch probabilities were not readable from the public embed during this session, so the neutral-hold classification used a repository-local same-day FedWatch note showing 99.5% no change.")
    lines.append("- FRED DFII10, HY OAS, and T10Y2Y official observations lagged the live session and were treated conservatively where a fresh prior-close comparison could not be fully verified.")
    lines.append("- Several non-core factors, including SOX, MOVE, copper, gold ETF flows, and eurozone and China growth proxies, were carried forward from the repository's previously verified same-day April 8 factor set where direct source access was restricted.")
    lines.append(f"- Average confidence: {avg_conf:.1f}/10")
    lines.append("")
    lines.append("---")
    lines.append("**End of Report**")
    lines.append("")
    return "\n".join(lines)



def main() -> None:
    now_utc = datetime.now(timezone.utc)
    date_str = now_utc.strftime("%Y-%m-%d")
    time_str = now_utc.strftime("%H%M")
    iso_str = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    date_label = now_utc.strftime("%B %-d, %Y")
    time_label = now_utc.strftime("%H:%M")

    results = {}
    scoring_detail = {}
    for symbol, config in instrument_configs.items():
        raw_weighted_score, detail = calculate_score(config)
        signal, pm_score = get_signal(raw_weighted_score)
        confidence = get_confidence(symbol, raw_weighted_score)
        approach, mode, hold = get_strategy(raw_weighted_score, symbol)
        results[symbol] = {
            "score": pm_score,
            "signal": signal,
            "confidence": confidence,
            "recommended_approach": approach,
            "recommended_mode": mode,
            "hold_expectation": hold,
        }
        scoring_detail[symbol] = {
            "name": config["name"],
            "raw_weighted_score": raw_weighted_score,
            "factors": detail,
        }

    asset_class_bias = {
        "COMMODITIES": get_asset_class_bias(["GC", "SI", "CL"], results),
        "INDICES": get_asset_class_bias(["ES", "NQ", "YM", "RTY"], results),
        "FX": get_asset_class_bias(["6E", "6A", "6J"], results),
    }

    output = {
        "date": date_str,
        "generated_at": iso_str,
        "methodology_version": "3.0_STRATEGY",
        "scores": results,
        "asset_class_bias": asset_class_bias,
        "key_drivers": [
            "TradingView showed DXY at 99.024 and down 0.49% on the session, improving the backdrop for commodities and non-USD FX.",
            "Cboe VIX fell 18.39% to 21.04, improving directional risk tone even though the volatility regime remains above the 20 risk-off threshold.",
            "Atlanta Fed GDPNow held at 1.3% for 2026:Q1, which stabilized the U.S. growth signal rather than worsening it further during the session.",
            "Policy divergence remains strongest in FX, with ECB easing bias contrasting against still-supportive RBA and BoJ narratives."
        ],
        "data_quality": {
            "stale_sources": [
                "FRED DFII10 latest official observation available on-page: 2026-04-07",
                "FRED HY OAS latest official observation remained lagged versus the live session",
                "FRED T10Y2Y latest official observation remained 2026-04-07"
            ],
            "fallbacks_used": [
                "Repository-local same-day FedWatch note for neutral-hold classification after the public CME embed failed",
                "Repository's previously verified same-day April 8 factor set for SOX, MOVE, copper, oil inventories, gold ETF flows, China PMI, and eurozone PMI",
                "Cboe VIX product page for live spot level and daily change",
                "TradingView DXY page for live dollar direction"
            ],
            "overnight_changes": [
                "DXY down 0.49% on the day",
                "VIX down 18.39% on the day",
                "GDPNow unchanged at 1.3% versus the earlier same-day repository reference"
            ]
        },
        "catalyst_proximity": {
            "imminent": [
                "Atlanta Fed GDPNow refresh on April 9",
                "China inflation data on April 10",
                "Ongoing Strait of Hormuz and tanker-flow headlines"
            ],
            "near_term": [
                "Federal Reserve meeting on April 30"
            ],
            "background": [
                "Persistent Middle East energy disruption risk",
                "ECB easing bias amid softer euro-area growth",
                "BoJ normalization and post-hike RBA policy divergence"
            ]
        }
    }

    markdown = build_markdown(date_label, time_label, results, asset_class_bias)

    timestamp_json = BIAS_DIR / f"{date_str}_{time_str}.json"
    latest_json = BIAS_DIR / "latest.json"
    timestamp_md = EXEC_DIR / f"{date_str}_{time_str}.md"
    latest_md = EXEC_DIR / "latest.md"
    detail_json = FACTOR_DIR / f"{date_str}_{time_str}_scoring_detail.json"

    timestamp_json.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    latest_json.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    timestamp_md.write_text(markdown, encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")
    detail_json.write_text(
        json.dumps(
            {
                "date": date_str,
                "generated_at": iso_str,
                "macro_data": macro_data,
                "scoring_detail": scoring_detail,
            },
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print(timestamp_json)
    print(latest_json)
    print(timestamp_md)
    print(latest_md)
    print(detail_json)


if __name__ == "__main__":
    main()
