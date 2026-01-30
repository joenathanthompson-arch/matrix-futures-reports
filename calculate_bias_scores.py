#!/usr/bin/env python3
"""
Matrix Futures Daily Bias Scorer
Calculates weighted bias scores for 10 instruments based on 14+ macro factors
Updated with fresh data collected on 2026-01-30
"""

from datetime import datetime
import json

# Current date for report
REPORT_DATE = datetime.now().strftime("%Y-%m-%d")
REPORT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

# ===== MACRO FACTOR SCORES (from data collection 2026-01-30) =====

# US Macro Factors
FED_STANCE = 0  # Neutral (on hold, 95% prob of no change in Jan, 76% for March)
REAL_YIELDS = +1  # Rising (2.20% on Jan 29, up from recent lows)
VIX = +1  # Falling (17.43, +3.32% today but still low, score inverted for safe havens)
DXY = +1  # Rising (97.147, +1.02% today)
GDPNOW = +1  # Slowing (4.2% down from 5.4%, still positive growth)
CREDIT_SPREADS = -1  # Widening (2.77%, up from 2.68%, bearish for risk)
SOX = -1  # Falling (-3.87% today at 7,998.47)
MOVE_INDEX = +1  # Falling (59.20, -2.52%, lower rate volatility = bullish for risk)
CURVE_2S10S = +1  # Steepening (0.74%, up from 0.70%, bullish for cyclicals)

# Commodity-Specific Factors
OIL_INVENTORIES = +1  # Draw (-2.3M barrels, bullish for oil)
COPPER = -1  # Falling (-3.75% today to $5.9710/lb)
GOLD_ETF_FLOWS = +1  # Inflows (US$10bn in Dec, record $89bn in 2025)

# FX Central Bank Stances
ECB_STANCE = 0  # Neutral (on hold at 2%, no hikes expected in 2026)
BOJ_STANCE = +1  # Hawkish (held at 0.75% but signaling more hikes, raised forecasts)
BOE_STANCE = -1  # Dovish (cut to 3.75%, more cuts expected in 2026)
RBA_STANCE = +1  # Hawkish (expected to hike to 3.85% in Feb due to inflation)
SNB_STANCE = 0  # Neutral (on hold at 0%, watching strong CHF)

# ===== INSTRUMENT DEFINITIONS WITH WEIGHTS =====

INSTRUMENTS = {
    "ES": {
        "name": "S&P 500 E-mini Futures",
        "asset_class": "Equity Index",
        "weights": {
            "FED_STANCE": 0.20,
            "REAL_YIELDS": 0.15,
            "VIX": 0.15,
            "DXY": 0.10,
            "GDPNOW": 0.10,
            "CREDIT_SPREADS": 0.15,
            "SOX": 0.10,
            "CURVE_2S10S": 0.05
        }
    },
    "NQ": {
        "name": "NASDAQ-100 E-mini Futures",
        "asset_class": "Equity Index",
        "weights": {
            "FED_STANCE": 0.20,
            "REAL_YIELDS": 0.20,
            "VIX": 0.10,
            "DXY": 0.10,
            "SOX": 0.25,
            "CREDIT_SPREADS": 0.10,
            "CURVE_2S10S": 0.05
        }
    },
    "GC": {
        "name": "Gold Futures",
        "asset_class": "Precious Metal",
        "weights": {
            "FED_STANCE": 0.25,
            "REAL_YIELDS": 0.25,
            "DXY": 0.20,
            "VIX": 0.10,
            "GOLD_ETF_FLOWS": 0.15,
            "GDPNOW": 0.05
        }
    },
    "CL": {
        "name": "Crude Oil Futures",
        "asset_class": "Energy",
        "weights": {
            "OIL_INVENTORIES": 0.30,
            "DXY": 0.20,
            "GDPNOW": 0.20,
            "COPPER": 0.15,
            "VIX": 0.10,
            "CREDIT_SPREADS": 0.05
        }
    },
    "HG": {
        "name": "Copper Futures",
        "asset_class": "Industrial Metal",
        "weights": {
            "COPPER": 0.30,
            "GDPNOW": 0.25,
            "DXY": 0.15,
            "SOX": 0.15,
            "CREDIT_SPREADS": 0.10,
            "VIX": 0.05
        }
    },
    "6E": {
        "name": "Euro FX Futures",
        "asset_class": "Currency",
        "weights": {
            "ECB_STANCE": 0.35,
            "FED_STANCE": 0.25,
            "DXY": 0.20,
            "VIX": 0.10,
            "CREDIT_SPREADS": 0.10
        }
    },
    "6J": {
        "name": "Japanese Yen Futures",
        "asset_class": "Currency",
        "weights": {
            "BOJ_STANCE": 0.35,
            "FED_STANCE": 0.25,
            "DXY": 0.15,
            "VIX": 0.15,
            "REAL_YIELDS": 0.10
        }
    },
    "6B": {
        "name": "British Pound Futures",
        "asset_class": "Currency",
        "weights": {
            "BOE_STANCE": 0.35,
            "FED_STANCE": 0.25,
            "DXY": 0.20,
            "CREDIT_SPREADS": 0.10,
            "VIX": 0.10
        }
    },
    "6A": {
        "name": "Australian Dollar Futures",
        "asset_class": "Currency",
        "weights": {
            "RBA_STANCE": 0.35,
            "FED_STANCE": 0.20,
            "COPPER": 0.20,
            "DXY": 0.15,
            "GDPNOW": 0.10
        }
    },
    "6S": {
        "name": "Swiss Franc Futures",
        "asset_class": "Currency",
        "weights": {
            "SNB_STANCE": 0.35,
            "FED_STANCE": 0.25,
            "VIX": 0.20,
            "DXY": 0.15,
            "CREDIT_SPREADS": 0.05
        }
    }
}

# ===== FACTOR VALUES DICTIONARY =====
FACTOR_VALUES = {
    "FED_STANCE": FED_STANCE,
    "REAL_YIELDS": REAL_YIELDS,
    "VIX": VIX,
    "DXY": DXY,
    "GDPNOW": GDPNOW,
    "CREDIT_SPREADS": CREDIT_SPREADS,
    "SOX": SOX,
    "MOVE_INDEX": MOVE_INDEX,
    "CURVE_2S10S": CURVE_2S10S,
    "OIL_INVENTORIES": OIL_INVENTORIES,
    "COPPER": COPPER,
    "GOLD_ETF_FLOWS": GOLD_ETF_FLOWS,
    "ECB_STANCE": ECB_STANCE,
    "BOJ_STANCE": BOJ_STANCE,
    "BOE_STANCE": BOE_STANCE,
    "RBA_STANCE": RBA_STANCE,
    "SNB_STANCE": SNB_STANCE
}

# ===== BIAS CALCULATION =====

def calculate_bias(instrument_code, instrument_data):
    """Calculate weighted bias score for an instrument"""
    weights = instrument_data["weights"]
    weighted_sum = 0.0
    components = {}
    
    for factor, weight in weights.items():
        factor_value = FACTOR_VALUES[factor]
        contribution = factor_value * weight
        weighted_sum += contribution
        components[factor] = {
            "value": factor_value,
            "weight": weight,
            "contribution": round(contribution, 3)
        }
    
    # Round to 2 decimal places
    bias_score = round(weighted_sum, 2)
    
    # Determine bias direction
    if bias_score > 0.3:
        bias_direction = "BULLISH"
    elif bias_score < -0.3:
        bias_direction = "BEARISH"
    else:
        bias_direction = "NEUTRAL"
    
    return {
        "instrument": instrument_code,
        "name": instrument_data["name"],
        "asset_class": instrument_data["asset_class"],
        "bias_score": bias_score,
        "bias_direction": bias_direction,
        "components": components
    }

# ===== MAIN CALCULATION =====

def main():
    print("=" * 70)
    print("MATRIX FUTURES DAILY BIAS REPORT")
    print(f"Report Date: {REPORT_DATE}")
    print(f"Report Time: {REPORT_TIME}")
    print("=" * 70)
    print()
    
    results = []
    
    for code, data in INSTRUMENTS.items():
        result = calculate_bias(code, data)
        results.append(result)
        
        print(f"{code:4s} | {result['name']:35s} | Score: {result['bias_score']:+6.2f} | {result['bias_direction']}")
    
    print()
    print("=" * 70)
    print("CALCULATION COMPLETE")
    print("=" * 70)
    
    # Save results to JSON for next script
    output = {
        "report_date": REPORT_DATE,
        "report_time": REPORT_TIME,
        "macro_factors": FACTOR_VALUES,
        "instruments": results
    }
    
    with open("/home/ubuntu/matrix-futures-reports/bias_scores_calculated.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print("\nResults saved to: bias_scores_calculated.json")
    
    return results

if __name__ == "__main__":
    main()
