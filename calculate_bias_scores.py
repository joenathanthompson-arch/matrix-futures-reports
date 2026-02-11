#!/usr/bin/env python3
"""
Matrix Futures Daily Bias Report - Bias Score Calculator
Calculates weighted bias scores for 10 instruments based on 14+ macro factors
Data collected: 2026-02-11
"""

from datetime import datetime
import json

# Data collected on 2026-02-11
# All scores are on -2 to +2 scale unless noted

# Core Macro Factors (apply to all instruments with varying weights)
fed_stance = 0  # Neutral hold
real_yields = 0  # Stable around 2.0%
usd = -1  # Weakening (DXY down)
vix = 0  # Balanced (17.80)
growth_narrative = 0  # Stable (GDPNow 3.7%)
credit_spreads = 1  # Narrowing (2.84%)
sox = 1  # Rising (+60% YoY)
move_index = 0  # Flat/mixed signals
curve_2s10s = 1  # Steepening (0.71%)
copper = 1  # Rising (+29% YoY)
oil_inventories = 1  # Draw (-3.5M barrels)
oil_supply_shock = 0  # Neutral
gold_etf_flows = 1  # Inflows (record highs)
geopolitical_risk = 0  # Stable

# FX-specific factors
ecb_stance = 0  # Neutral hold at 2.0%
rba_stance = 2  # Hawkish hike (+25bps to 3.85%)
boj_stance = 1  # Hawkish tilt (gradual normalization)

# Instrument definitions with weights (from methodology)
instruments = {
    "ES": {  # E-mini S&P 500
        "name": "E-mini S&P 500",
        "weights": {
            "fed_stance": 0.20,
            "real_yields": 0.15,
            "credit_spreads": 0.15,
            "growth_narrative": 0.10,
            "vix": 0.10,
            "sox": 0.10,
            "move_index": 0.05,
            "curve_2s10s": 0.05,
            "copper": 0.05,
            "geopolitical_risk": 0.05
        }
    },
    "NQ": {  # E-mini Nasdaq-100
        "name": "E-mini Nasdaq-100",
        "weights": {
            "fed_stance": 0.20,
            "real_yields": 0.20,
            "sox": 0.15,
            "credit_spreads": 0.10,
            "growth_narrative": 0.10,
            "vix": 0.10,
            "move_index": 0.05,
            "curve_2s10s": 0.05,
            "geopolitical_risk": 0.05
        }
    },
    "RTY": {  # E-mini Russell 2000
        "name": "E-mini Russell 2000",
        "weights": {
            "fed_stance": 0.15,
            "credit_spreads": 0.20,
            "curve_2s10s": 0.15,
            "growth_narrative": 0.15,
            "real_yields": 0.10,
            "vix": 0.10,
            "copper": 0.05,
            "sox": 0.05,
            "geopolitical_risk": 0.05
        }
    },
    "YM": {  # E-mini Dow Jones
        "name": "E-mini Dow Jones",
        "weights": {
            "fed_stance": 0.20,
            "growth_narrative": 0.15,
            "credit_spreads": 0.15,
            "real_yields": 0.10,
            "curve_2s10s": 0.10,
            "vix": 0.10,
            "copper": 0.10,
            "geopolitical_risk": 0.05,
            "sox": 0.05
        }
    },
    "GC": {  # Gold Futures
        "name": "Gold Futures",
        "weights": {
            "real_yields": 0.25,
            "usd": 0.20,
            "fed_stance": 0.15,
            "gold_etf_flows": 0.15,
            "geopolitical_risk": 0.10,
            "vix": 0.10,
            "move_index": 0.05
        }
    },
    "CL": {  # Crude Oil Futures
        "name": "Crude Oil Futures",
        "weights": {
            "oil_inventories": 0.25,
            "growth_narrative": 0.20,
            "usd": 0.15,
            "oil_supply_shock": 0.15,
            "geopolitical_risk": 0.15,
            "copper": 0.10
        }
    },
    "M6E": {  # Euro FX
        "name": "Euro FX",
        "weights": {
            "ecb_stance": 0.25,
            "fed_stance": 0.25,
            "usd": 0.20,
            "real_yields": 0.10,
            "geopolitical_risk": 0.10,
            "growth_narrative": 0.10
        }
    },
    "6A": {  # Australian Dollar
        "name": "Australian Dollar",
        "weights": {
            "rba_stance": 0.25,
            "fed_stance": 0.20,
            "copper": 0.20,
            "usd": 0.15,
            "growth_narrative": 0.10,
            "geopolitical_risk": 0.10
        }
    },
    "6J": {  # Japanese Yen
        "name": "Japanese Yen",
        "weights": {
            "boj_stance": 0.25,
            "fed_stance": 0.20,
            "usd": 0.20,
            "vix": 0.15,
            "geopolitical_risk": 0.10,
            "real_yields": 0.10
        }
    },
    "ZN": {  # 10-Year Treasury Note
        "name": "10-Year Treasury Note",
        "weights": {
            "fed_stance": 0.25,
            "real_yields": 0.20,
            "move_index": 0.15,
            "growth_narrative": 0.10,
            "credit_spreads": 0.10,
            "curve_2s10s": 0.10,
            "geopolitical_risk": 0.10
        }
    }
}

# Factor values dictionary
factors = {
    "fed_stance": fed_stance,
    "real_yields": real_yields,
    "usd": usd,
    "vix": vix,
    "growth_narrative": growth_narrative,
    "credit_spreads": credit_spreads,
    "sox": sox,
    "move_index": move_index,
    "curve_2s10s": curve_2s10s,
    "copper": copper,
    "oil_inventories": oil_inventories,
    "oil_supply_shock": oil_supply_shock,
    "gold_etf_flows": gold_etf_flows,
    "geopolitical_risk": geopolitical_risk,
    "ecb_stance": ecb_stance,
    "rba_stance": rba_stance,
    "boj_stance": boj_stance
}

def calculate_bias_score(instrument_code):
    """Calculate weighted bias score for an instrument"""
    instrument = instruments[instrument_code]
    weights = instrument["weights"]
    
    score = 0.0
    breakdown = {}
    
    for factor_name, weight in weights.items():
        factor_value = factors[factor_name]
        contribution = factor_value * weight
        score += contribution
        breakdown[factor_name] = {
            "value": factor_value,
            "weight": weight,
            "contribution": round(contribution, 3)
        }
    
    return round(score, 2), breakdown

def get_bias_label(score):
    """Convert numeric score to bias label"""
    if score >= 0.75:
        return "Bullish"
    elif score >= 0.25:
        return "Slightly Bullish"
    elif score >= -0.25:
        return "Neutral"
    elif score >= -0.75:
        return "Slightly Bearish"
    else:
        return "Bearish"

def main():
    """Calculate and display bias scores for all instruments"""
    print("=" * 80)
    print("MATRIX FUTURES DAILY BIAS REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 80)
    print()
    
    results = {}
    
    for code in instruments.keys():
        score, breakdown = calculate_bias_score(code)
        bias = get_bias_label(score)
        
        results[code] = {
            "name": instruments[code]["name"],
            "score": score,
            "bias": bias,
            "breakdown": breakdown
        }
        
        print(f"{code:6s} | {instruments[code]['name']:25s} | Score: {score:+.2f} | {bias}")
    
    print()
    print("=" * 80)
    
    # Save results to JSON
    output = {
        "report_date": datetime.now().strftime('%Y-%m-%d'),
        "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
        "macro_factors": factors,
        "instruments": results
    }
    
    with open('/home/ubuntu/matrix-futures-reports/bias_scores.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("Results saved to bias_scores.json")
    
    return results

if __name__ == "__main__":
    main()
