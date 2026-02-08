#!/usr/bin/env python3
"""
Matrix Futures Bias Scorer
Calculates weighted bias scores for 10 futures instruments
"""
import json
from datetime import datetime, timezone

# Data collected from sources (2026-02-08)
macro_data = {
    "fed_stance": 0,  # Neutral hold (3.5-3.75%, on hold, no changes expected)
    "real_yields": +2,  # Falling (1.98% on 2/3, down from previous)
    "usd_dxy": -1,  # Weak/Falling (97.51, down -0.19%)
    "risk_mood": 0,  # Balanced (VIX 17.76, in 15-20 range)
    "vix_direction": +1,  # Falling (down -18.42%)
    "growth_narrative": 0,  # Stable (GDPNow 4.2%, unchanged)
    "credit_spreads": +1,  # Narrowing (2.97%, near multi-year lows, downtrend)
    "sox": +1,  # Rising (8048.62, +5.70% 1d, +6.54% 1m, +58.99% 1y)
    "move_index": +1,  # Falling (63.62, down -32.81% 1y, -20.62% 6m)
    "yield_curve_2s10s": +1,  # Steepening (0.72%, up from deeply inverted)
    "copper": +1,  # Rising (5.8820, +18.66% 3m, +28.18% 1y)
    "oil_inventories": +1,  # Draw (-3.5M barrels)
    "oil_supply_shock": 0,  # Neutral (no major disruptions)
    "geopolitical_risk": 0,  # Stable (no major new escalations)
    "gold_etf_flows": +1,  # Inflows ($4.39B in Jan, 8th consecutive month)
    "ecb_stance": 0,  # Neutral hold (2%, on hold)
    "rba_stance": 0,  # Neutral hold
    "boj_stance": +1,  # Hawkish/Tightening (normalizing policy)
    "china_growth": 0,  # Stable (~5% target)
    "rate_diff_eur_usd": 0,  # Stable (both on hold)
    "rate_diff_aud_usd": 0,  # Stable (both on hold)
    "rate_diff_jpy_usd": +1,  # Widening vs USD (BoJ normalizing, Fed on hold)
    "risk_sentiment_aud": 0,  # Neutral (VIX balanced)
    "eurozone_growth": 0,  # Stable (inflation 1.7%, below target)
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
            "oil_supply_shock": 1,
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
    "M6E": {
        "name": "Micro Euro FX",
        "factors": {
            "fed_stance": 1,
            "ecb_stance": 1,
            "rate_diff_eur_usd": 2,  # Double weight
            "usd_dxy": 1,
            "risk_mood": 1,
            "eurozone_growth": 1,
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
    if score >= 5:
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
    if abs_score >= 5:
        return 8  # High conviction
    elif abs_score >= 3:
        return 7  # Good conviction
    elif abs_score >= 1:
        return 6  # Moderate conviction
    else:
        return 5  # Low conviction (neutral)

# Calculate scores for all instruments
results = {}
for symbol, config in instruments.items():
    score = calculate_score(symbol, config)
    signal, pm_code = get_signal(score)
    confidence = get_confidence(score, signal)
    
    results[symbol] = {
        "score": pm_code,
        "signal": signal,
        "confidence": confidence,
        "raw_weighted_score": score
    }

# Determine asset class bias
def get_asset_class_bias(symbols):
    """Determine bias for a group of symbols"""
    bullish = sum(1 for s in symbols if results[s]["score"] > 0)
    bearish = sum(1 for s in symbols if results[s]["score"] < 0)
    
    if bullish > len(symbols) / 2:
        return "BULLISH"
    elif bearish > len(symbols) / 2:
        return "BEARISH"
    elif bullish == bearish:
        return "NEUTRAL"
    else:
        return "MIXED"

asset_class_bias = {
    "COMMODITIES": get_asset_class_bias(["GC", "SI", "CL"]),
    "INDICES": get_asset_class_bias(["ES", "NQ", "YM", "RTY"]),
    "FX": get_asset_class_bias(["M6E", "6A", "6J"])
}

# Generate output
now_utc = datetime.now(timezone.utc)
date_str = now_utc.strftime("%Y-%m-%d")
time_str = now_utc.strftime("%H%M")
iso_str = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

output = {
    "date": date_str,
    "generated_at": iso_str,
    "scores": {k: {kk: vv for kk, vv in v.items() if kk != "raw_weighted_score"} 
               for k, v in results.items()},
    "asset_class_bias": asset_class_bias,
    "key_drivers": [
        "Falling real yields (+2 weight) supporting gold and tech",
        "Weak USD (-1) benefiting commodities and risk assets",
        "Narrowing credit spreads (+1) and falling VIX (+1) supporting equities",
        "BoJ policy normalization (+1) supporting JPY strength"
    ],
    "data_quality": {
        "stale_sources": ["T10Y2Y (2 days old)", "BAMLH0A0HYM2 (3 days old)"],
        "fallbacks_used": []
    }
}

# Print results for verification
print("=" * 80)
print("MATRIX FUTURES BIAS SCORES")
print(f"Generated: {iso_str}")
print("=" * 80)
print()
for symbol, data in results.items():
    print(f"{symbol:6s} | Score: {data['raw_weighted_score']:+3d} → {data['signal']:20s} | Confidence: {data['confidence']}/10")
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
