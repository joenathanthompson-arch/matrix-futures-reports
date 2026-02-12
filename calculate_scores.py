#!/usr/bin/env python3
"""
Matrix Futures Bias Scorer
Calculates weighted bias scores for 10 futures instruments
Updated: 2026-02-12 with fresh macro data
"""
import json
from datetime import datetime, timezone

# Data collected from sources (2026-02-12)
macro_data = {
    "fed_stance": 0,  # Neutral (Fed on hold, 4.25-4.50%, next meeting March 19)
    "real_yields": +1,  # Rising (2.36% 10Y TIPS, up from recent lows)
    "usd_dxy": 0,  # Flat (96.908, +0.02%, range-bound)
    "risk_mood": +1,  # Positive (VIX 17.64, down -0.90%, low vol)
    "vix_direction": +1,  # Falling (down -0.90%)
    "growth_narrative": 0,  # Stable (GDPNow 3.7%, solid but not accelerating)
    "credit_spreads": +1,  # Narrowing (2.86%, tightening trend)
    "sox": +1,  # Rising (8,291.86, +2.28% day, +6.82% week, +13.76% YTD)
    "move_index": +1,  # Falling (61.35, down -4.96%, bond vol declining)
    "yield_curve_2s10s": +1,  # Steepening (0.66%, positive for growth)
    "copper": +1,  # Rising (5.9878, +2.85% week, +17.27% 3mo, +27.26% 1y)
    "oil_inventories": -1,  # Build (+8.5M barrels = bearish)
    "oil_supply_shock": 0,  # Neutral (no major disruptions)
    "geopolitical_risk": +1,  # Elevated (US-Europe tensions, Iran, trade)
    "gold_etf_flows": +1,  # Inflows (record $19bn in January)
    "ecb_stance": 0,  # Neutral hold
    "rba_stance": 0,  # Neutral hold
    "boj_stance": +1,  # Hawkish/Tightening (normalizing policy)
    "china_growth": 0,  # Stable
    "rate_diff_eur_usd": 0,  # Stable (both on hold)
    "rate_diff_aud_usd": 0,  # Stable (both on hold)
    "rate_diff_jpy_usd": +1,  # Widening vs USD (BoJ normalizing, Fed on hold)
    "risk_sentiment_aud": +1,  # Positive (risk-on environment)
}

# Instrument scoring configurations
instruments = {
    "GC": {
        "name": "Gold Futures",
        "factors": {
            "fed_stance": 1,
            "real_yields": 2,  # Double weight
            "usd_dxy": 1,
            "risk_mood": 1,
            "growth_narrative": 1,
            "geopolitical_risk": 1,
            "gold_etf_flows": 1,
        }
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
        }
    },
    "CL": {
        "name": "WTI Crude Oil",
        "factors": {
            "oil_supply_shock": 2,  # Double weight
            "oil_inventories": 1,
            "growth_narrative": 2,  # Double weight
            "geopolitical_risk": 1,
            "usd_dxy": 1,
        }
    },
    "ES": {
        "name": "S&P 500 E-mini",
        "factors": {
            "fed_stance": 1,
            "real_yields": 2,  # Double weight
            "usd_dxy": 1,
            "risk_mood": 1,
            "growth_narrative": 1,
            "credit_spreads": 1,
            "vix_direction": 1,
        }
    },
    "NQ": {
        "name": "Nasdaq 100 E-mini",
        "factors": {
            "fed_stance": 1,
            "real_yields": 2,  # Double weight
            "usd_dxy": 1,
            "risk_mood": 1,
            "growth_narrative": 1,
            "sox": 1,
            "move_index": 1,
        }
    },
    "YM": {
        "name": "Dow Jones E-mini",
        "factors": {
            "fed_stance": 1,
            "real_yields": 1,
            "usd_dxy": 1,
            "risk_mood": 1,
            "growth_narrative": 2,  # Double weight
            "credit_spreads": 1,
            "yield_curve_2s10s": 1,
        }
    },
    "RTY": {
        "name": "Russell 2000 E-mini",
        "factors": {
            "fed_stance": 1,
            "real_yields": 1,
            "usd_dxy": 1,
            "risk_mood": 1,
            "growth_narrative": 2,  # Double weight
            "credit_spreads": 2,  # Double weight
            "yield_curve_2s10s": 1,
        }
    },
    "6E": {
        "name": "Euro FX",
        "factors": {
            "fed_stance": 1,
            "ecb_stance": 1,
            "rate_diff_eur_usd": 2,  # Double weight
            "usd_dxy": 1,
            "risk_mood": 1,
            "geopolitical_risk": 1,
        }
    },
    "6A": {
        "name": "Australian Dollar",
        "factors": {
            "fed_stance": 1,
            "rba_stance": 1,
            "rate_diff_aud_usd": 1,
            "usd_dxy": 1,
            "risk_sentiment_aud": 2,  # Double weight
            "china_growth": 2,  # Double weight
            "copper": 1,
        }
    },
    "6J": {
        "name": "Japanese Yen",
        "factors": {
            "fed_stance": 1,
            "boj_stance": 2,  # Double weight
            "rate_diff_jpy_usd": 2,  # Double weight
            "usd_dxy": 1,
            "risk_mood": 1,
        }
    },
}

def calculate_score(symbol, config):
    """Calculate weighted bias score for an instrument"""
    total_score = 0
    for factor, weight in config["factors"].items():
        raw_score = macro_data[factor]
        weighted_score = raw_score * weight
        total_score += weighted_score
    return total_score

def get_signal(score):
    """Map score to signal label"""
    if score >= 7:
        return "STRONG_BULLISH", 3
    elif score >= 5:
        return "STRONG_BULLISH", 3
    elif score >= 3:
        return "BULLISH", 2
    elif score >= 1:
        return "SLIGHT_BULLISH", 1
    elif score >= -1:
        return "NEUTRAL", 0
    elif score >= -3:
        return "SLIGHT_BEARISH", -1
    elif score >= -5:
        return "BEARISH", -2
    else:
        return "STRONG_BEARISH", -3

def get_confidence(score, signal):
    """Estimate confidence based on score magnitude and data quality"""
    # Data is fresh (collected today), signals are relatively clear
    abs_score = abs(score)
    if abs_score >= 7:
        return 9  # Very high conviction
    elif abs_score >= 5:
        return 8  # High conviction
    elif abs_score >= 3:
        return 7  # Good conviction
    elif abs_score >= 1:
        return 6  # Moderate conviction
    else:
        return 5  # Low conviction (neutral)

def get_strategy(score, symbol):
    """Determine recommended approach, mode, and hold expectation"""
    abs_score = abs(score)
    
    # Commodities (GC, SI, CL) tend to be swing trades
    if symbol in ["GC", "SI", "CL"]:
        if abs_score >= 5:
            return "TREND_FOLLOW", "SWING", "2-5 days"
        elif abs_score >= 3:
            return "TREND_FOLLOW", "SWING", "1-2 days"
        elif abs_score >= 1:
            return "IB_BREAKOUT", "INTRADAY", "session"
        else:
            return "RANGE_TRADE", "INTRADAY", "session"
    
    # FX (6E, 6A, 6J) can be swing or intraday
    elif symbol in ["6E", "6A", "6J"]:
        if abs_score >= 5:
            return "TREND_FOLLOW", "SWING", "2-5 days"
        elif abs_score >= 3:
            return "TREND_FOLLOW", "SWING", "1-2 days"
        elif abs_score >= 1:
            return "IB_BREAKOUT", "INTRADAY", "session"
        else:
            return "RANGE_TRADE", "INTRADAY", "session"
    
    # Indices (ES, NQ, YM, RTY) are often intraday unless strong conviction
    else:
        if abs_score >= 5:
            return "TREND_FOLLOW", "SWING", "1-2 days"
        elif abs_score >= 3:
            return "TREND_FOLLOW", "SWING", "1-2 days"
        elif abs_score >= 1:
            return "IB_BREAKOUT", "INTRADAY", "session"
        else:
            return "RANGE_TRADE", "INTRADAY", "session"

# Calculate scores for all instruments
results = {}
for symbol, config in instruments.items():
    score = calculate_score(symbol, config)
    signal, pm_code = get_signal(score)
    confidence = get_confidence(score, signal)
    approach, mode, hold = get_strategy(score, symbol)
    
    results[symbol] = {
        "score": pm_code,
        "signal": signal,
        "confidence": confidence,
        "recommended_approach": approach,
        "recommended_mode": mode,
        "hold_expectation": hold,
        "raw_weighted_score": score
    }

# Determine asset class bias
def get_asset_class_bias(symbols):
    """Determine bias for a group of symbols"""
    total_score = sum(results[s]["score"] for s in symbols)
    avg_score = total_score / len(symbols)
    
    if avg_score >= 2.5:
        return "STRONG_BULLISH"
    elif avg_score >= 1.5:
        return "BULLISH"
    elif avg_score >= 0.5:
        return "SLIGHT_BULLISH"
    elif avg_score >= -0.5:
        return "NEUTRAL"
    elif avg_score >= -1.5:
        return "SLIGHT_BEARISH"
    elif avg_score >= -2.5:
        return "BEARISH"
    else:
        return "STRONG_BEARISH"

asset_class_bias = {
    "COMMODITIES": get_asset_class_bias(["GC", "SI", "CL"]),
    "INDICES": get_asset_class_bias(["ES", "NQ", "YM", "RTY"]),
    "FX": get_asset_class_bias(["6E", "6A", "6J"])
}

# Generate output
now_utc = datetime.now(timezone.utc)
date_str = now_utc.strftime("%Y-%m-%d")
time_str = now_utc.strftime("%H%M")
iso_str = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

output = {
    "date": date_str,
    "generated_at": iso_str,
    "methodology_version": "3.0_STRATEGY",
    "scores": {k: {kk: vv for kk, vv in v.items() if kk != "raw_weighted_score"} 
               for k, v in results.items()},
    "asset_class_bias": asset_class_bias,
    "key_drivers": [
        "Narrowing credit spreads (+1) and falling VIX (+1) supporting equities",
        "Rising SOX (+1) and strong tech momentum",
        "Elevated geopolitical risk (+1) supporting safe havens",
        "Record gold ETF inflows (+1) supporting precious metals",
        "BoJ policy normalization (+1) supporting JPY strength"
    ],
    "data_quality": {
        "stale_sources": [],
        "fallbacks_used": [],
        "overnight_changes": []
    },
    "catalyst_proximity": {
        "imminent": [],
        "near_term": ["Fed meeting March 19"],
        "background": ["US-Europe trade tensions", "BoJ policy normalization"]
    }
}

# Print results for verification
print("=" * 80)
print("MATRIX FUTURES BIAS SCORES")
print(f"Generated: {iso_str}")
print("=" * 80)
print()
for symbol, data in results.items():
    print(f"{symbol:6s} | Score: {data['raw_weighted_score']:+3d} → {data['signal']:20s} | Confidence: {data['confidence']}/10 | {data['recommended_mode']:8s} {data['recommended_approach']}")
print()
print("ASSET CLASS BIAS:")
for asset_class, bias in asset_class_bias.items():
    print(f"  {asset_class:15s}: {bias}")
print()
print("=" * 80)

# Save to file
output_file = f"data/bias_scores/{date_str}_{time_str}.json"
print(f"Saving to: {output_file}")
with open(output_file, 'w') as f:
    json.dump(output, f, indent=2)

# Also save as latest.json
latest_file = "data/bias_scores/latest.json"
print(f"Copying to: {latest_file}")
with open(latest_file, 'w') as f:
    json.dump(output, f, indent=2)

print("✓ Bias scores calculated successfully")
