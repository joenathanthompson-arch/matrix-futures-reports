"""
Matrix Futures Bias Scorer
Calculates weighted bias scores for 10 futures instruments using the V3.0 methodology.
Updated: 2026-04-08 with verified same-session macro inputs.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
BIAS_DIR = BASE_DIR / "data" / "bias_scores"
BIAS_DIR.mkdir(parents=True, exist_ok=True)

# Verified macro inputs gathered on 2026-04-08 UTC.
# Integer scoring conventions follow docs/Macro_Bias_Scorer_Reference.md.
macro_data = {
    "fed_stance": 0,              # Neutral hold; Apr meeting still overwhelmingly priced for no change
    "real_yields": 0,             # DFII10 at 1.98%; conservatively scored FLAT absent >5bp verified move
    "usd_dxy": 1,                 # DXY 98.726, down 0.79% on day = Weak/Falling
    "risk_mood": 1,               # VIX 20.27 > 20 = Risk-off per methodology lookup
    "vix_direction": 1,           # VIX down 21.37% on day = Falling
    "growth_narrative": 1,        # GDPNow 1.3% = Slowing / softer growth impulse
    "credit_spreads": 0,          # HY OAS 3.05%; mild headwind but not decisively widening enough for -1
    "sox": 1,                     # SOX rising
    "move_index": 1,              # MOVE falling
    "yield_curve_2s10s": 1,       # 2s10s positive and still normalizing / steepening
    "copper": 1,                  # Copper rising
    "oil_inventories": -1,        # EIA crude inventory build +5.5M bbl
    "oil_supply_shock": 1,        # Strait of Hormuz disruption tightening global supply
    "geopolitical_risk": 1,       # Middle East energy conflict keeps risk elevated
    "gold_etf_flows": 1,          # WGC reports 21-tonne inflow to start April
    "ecb_stance": -1,             # ECB easing bias after sequence of rate reductions
    "rba_stance": 1,              # RBA hiked to 4.10% on 18 Mar 2026
    "boj_stance": 1,              # BoJ normalization / hawkish tilt at 0.75%
    "china_growth": 1,            # Official China PMI improved to 50.4 in March
    "eurozone_growth": -1,        # Euro zone Composite PMI slowed to 50.7, nine-month low
    "rate_diff_eur_usd": -1,      # EUR-USD rate differential moving against EUR vs neutral Fed / easing ECB
    "rate_diff_aud_usd": 1,       # AUD-USD rate differential favors AUD after RBA hike
    "rate_diff_jpy_usd": 1,       # JPY-USD differential improving for JPY as BoJ normalizes
    "risk_sentiment_aud": -1,     # AUD risk-sentiment input = risk-off while VIX remains above 20
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
    "fed_stance": "CME FedWatch: Apr 2026 meeting shows 98.4% no change at 350-375, with only 1.6% hike pricing.",
    "real_yields": "FRED DFII10: 1.98% on 2026-04-06; treated as FLAT because a >5bp verified directional move was not confirmed.",
    "usd_dxy": "TradingView DXY: 98.726, down 0.790 points (-0.79%) on the day.",
    "risk_mood": "Cboe VIX: 20.27 on 2026-04-08, which remains above the 20 threshold for a risk-off regime.",
    "vix_direction": "Cboe VIX daily change: -21.37% (-5.51), so the directional signal is falling.",
    "growth_narrative": "Atlanta Fed GDPNow: 1.3% for 2026:Q1, consistent with a slowing rather than accelerating growth impulse.",
    "credit_spreads": "FRED HY OAS: 3.05% on 2026-04-06; classified as flat / only modestly wider rather than decisively widening.",
    "sox": "TradingView SOX: 8,003.87, up 1.11% on the day and 6.08% over five days.",
    "move_index": "TradingView MOVE: 83.1452, down 3.24% in 24h and down 27.04% over the past week.",
    "yield_curve_2s10s": "FRED T10Y2Y: 0.52% on 2026-04-07; curve remains positively sloped and normalized from inversion.",
    "copper": "TradingView HG1!: 5.7490 USD/lb, up 3.34% on the day and 2.20% over five days.",
    "oil_inventories": "EIA Weekly Petroleum Status Report: commercial crude inventories rose by 5.5 million barrels to 461.6 million.",
    "oil_supply_shock": "Anadolu/EIA STEO report: Strait of Hormuz disruption tightened supply, with outages estimated at 7.5m bpd in March and peaking near 9.1m bpd in April.",
    "geopolitical_risk": "Middle East conflict and Hormuz disruption keep geopolitical and energy-market risk elevated.",
    "gold_etf_flows": "World Gold Council Weekly Markets Monitor: global gold ETFs recorded a 21-tonne inflow to start April.",
    "ecb_stance": "ECB key policy rates remain at 2.00% deposit / 2.15% MRO / 2.40% marginal lending after a sequence of cuts, reflecting an easing bias.",
    "rba_stance": "RBA cash rate target is 4.10% as of 18 March 2026 following a 25bp increase.",
    "boj_stance": "BoJ statement dated 19 March 2026 maintained the overnight call rate around 0.75%, still a normalization-oriented stance.",
    "china_growth": "China official NBS manufacturing PMI rose to 50.4 in March from 49.0 in February, returning to expansion.",
    "eurozone_growth": "Reuters-syndicated PMI coverage: euro zone composite PMI fell to 50.7 in March from 51.9 in February, a nine-month low.",
    "rate_diff_eur_usd": "A neutral Fed versus an easing-biased ECB points to a differential moving against EUR.",
    "rate_diff_aud_usd": "RBA 4.10% versus Fed 3.50-3.75% leaves the AUD rate differential supportive.",
    "rate_diff_jpy_usd": "BoJ normalization improves the JPY side of the rate differential versus a neutral Fed.",
    "risk_sentiment_aud": "AUD remains a pro-cyclical risk currency; VIX above 20 implies a risk-off input for this factor.",
}


def calculate_score(config):
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
            "note": factor_notes.get(factor, ""),
        }
    return total, detail


def get_signal(score):
    if score >= 5:
        return "STRONG_BULLISH", 3
    if score >= 3:
        return "BULLISH", 2
    if score >= 1:
        return "SLIGHT_BULLISH", 1
    if score >= -1:
        return "NEUTRAL", 0
    if score >= -3:
        return "SLIGHT_BEARISH", -1
    if score >= -5:
        return "BEARISH", -2
    return "STRONG_BEARISH", -3


def get_confidence(symbol, raw_weighted_score):
    abs_score = abs(raw_weighted_score)
    if abs_score >= 6:
        confidence = 8
    elif abs_score >= 4:
        confidence = 7
    elif abs_score >= 2:
        confidence = 6
    else:
        confidence = 5

    # Reduce for symbols that rely more heavily on lagged FRED prints.
    if symbol in {"GC", "SI", "ES", "NQ", "YM", "RTY"}:
        confidence -= 1
    if symbol in {"YM", "RTY", "6E"}:
        confidence -= 0

    # Keep within the required 1-10 range.
    return max(4, min(9, confidence))


def get_strategy(raw_weighted_score, symbol):
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


def get_asset_class_bias(symbols, results):
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


def main():
    now_utc = datetime.now(timezone.utc)
    date_str = now_utc.strftime("%Y-%m-%d")
    time_str = now_utc.strftime("%H%M")
    iso_str = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

    results = {}
    scoring_detail = {}
    for symbol, config in instrument_configs.items():
        raw_weighted_score, detail = calculate_score(config)
        signal, pm_code = get_signal(raw_weighted_score)
        confidence = get_confidence(symbol, raw_weighted_score)
        approach, mode, hold = get_strategy(raw_weighted_score, symbol)

        results[symbol] = {
            "score": pm_code,
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
            "The U.S. dollar weakened to 98.726 while CME FedWatch still shows a near-certain neutral Fed hold, improving the backdrop for commodities and non-USD FX.",
            "Macro volatility is easing at the margin: VIX fell 21.37% on the day and MOVE fell 3.24%, while SOX advanced 1.11% and copper rose 3.34%.",
            "Growth signals remain mixed but softer in the U.S. and euro area: GDPNow is 1.3% and euro zone composite PMI fell to 50.7, while China PMI rebounded to 50.4.",
            "Energy-market stress remains structurally elevated despite ceasefire headlines, with EIA-linked reporting pointing to ongoing Strait of Hormuz supply disruptions and rising geopolitical risk."
        ],
        "data_quality": {
            "stale_sources": [
                "FRED DFII10 latest official print 2026-04-06",
                "FRED BAMLH0A0HYM2 latest official print 2026-04-06",
                "FRED T10Y2Y latest official print 2026-04-07",
                "EIA weekly inventory detail reflects week ended 2026-03-27"
            ],
            "fallbacks_used": [
                "TradingView for DXY, MOVE, SOX, and copper live direction",
                "WHBL Reuters syndication for euro zone PMI detail after Reuters direct access was restricted",
                "FocusEconomics summary of official China PMI release",
                "Anadolu Agency report summarizing EIA STEO and Hormuz disruption effects"
            ],
            "overnight_changes": [
                "DXY down 0.79% on the day",
                "VIX down 21.37% on the day",
                "MOVE down 3.24% over 24 hours",
                "SOX up 1.11% on the day",
                "Copper up 3.34% on the day"
            ]
        },
        "catalyst_proximity": {
            "imminent": [
                "Atlanta Fed GDPNow refresh on April 9",
                "China inflation data on April 10",
                "Ongoing oil-market headlines around Strait of Hormuz reopening or renewed disruption"
            ],
            "near_term": [
                "Federal Reserve meeting on April 30"
            ],
            "background": [
                "Middle East energy disruption and tanker-flow uncertainty",
                "ECB easing bias versus slowing euro-area growth",
                "RBA hike aftermath and BoJ normalization versus a neutral Fed"
            ]
        }
    }

    timestamped_path = BIAS_DIR / f"{date_str}_{time_str}.json"
    latest_path = BIAS_DIR / "latest.json"
    detail_path = BASE_DIR / "data" / "factors" / f"{date_str}_{time_str}_scoring_detail.json"
    detail_path.parent.mkdir(parents=True, exist_ok=True)

    with open(timestamped_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    with open(detail_path, "w", encoding="utf-8") as f:
        json.dump({
            "date": date_str,
            "generated_at": iso_str,
            "macro_data": macro_data,
            "scoring_detail": scoring_detail,
        }, f, indent=2)

    print("=" * 88)
    print("MATRIX FUTURES BIAS SCORES")
    print(f"Generated: {iso_str}")
    print("=" * 88)
    for symbol, data in results.items():
        raw_score = scoring_detail[symbol]["raw_weighted_score"]
        print(
            f"{symbol:6s} | raw {raw_score:+3d} -> {data['signal']:16s} | "
            f"PM {data['score']:+2d} | Conf {data['confidence']}/10 | "
            f"{data['recommended_mode']:8s} {data['recommended_approach']}"
        )
    print()
    print("ASSET CLASS BIAS:")
    for asset_class, bias in asset_class_bias.items():
        print(f"  {asset_class:15s}: {bias}")
    print()
    print(f"Saved: {timestamped_path}")
    print(f"Saved: {latest_path}")
    print(f"Saved: {detail_path}")


if __name__ == "__main__":
    main()
