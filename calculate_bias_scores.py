#!/usr/bin/env python3
"""
Macro Bias Scorer - Calculate weighted bias scores for futures instruments
Based on methodology from Macro_Bias_Scorer_Reference.md
"""

from datetime import datetime
from typing import Dict, List, Tuple

# Core macro indicators (collected data)
CORE_INDICATORS = {
    "fed_stance": +1,  # Dovish (CME FedWatch shows rate cut expectations)
    "real_yields": -1,  # Rising (10Y TIPS at 2.38%, up from lows)
    "dxy": -1,  # Down (DXY at 107.39, down 0.52%)
    "vix": +1,  # Down (VIX at 15.88, down 1.31%)
    "gdpnow": +1,  # Positive (Atlanta Fed GDPNow at 2.3%)
    "credit_spreads": +1,  # Narrowing (HY OAS at 2.68%, very tight)
    "yield_curve_2s10s": +1,  # Steepening (0.64%, positive and rising)
}

# Instrument-specific indicators
INSTRUMENT_INDICATORS = {
    "GC": {  # Gold
        "gold_etf_flows": +1,  # Up (record $89B inflows in 2025, $10B in Dec)
        "sox": +1,  # Up (SOX at 7,960, +46% YoY, near ATH)
        "move": +1,  # Down (MOVE at 56.25, down 32.82% over 6 months)
    },
    "SI": {  # Silver
        "gold_etf_flows": +1,  # Up (same as gold)
        "sox": +1,  # Up
        "copper": +1,  # Up (Copper at $5.93/lb, +38% YoY)
    },
    "ES": {  # S&P 500
        "sox": +1,  # Up
        "move": +1,  # Down
    },
    "NQ": {  # Nasdaq
        "sox": +1,  # Up
        "move": +1,  # Down
    },
    "YM": {  # Dow
        "sox": +1,  # Up
        "move": +1,  # Down
    },
    "CL": {  # Crude Oil
        "oil_supply_shock": 0,  # Neutral (no major supply disruptions)
        "oil_inventories": -1,  # Build (increased by 3.6M barrels, mildly bearish)
    },
}

# Additional instrument-specific indicators (not in core set)
ADDITIONAL_INDICATORS = {
    "NG": {  # Natural Gas (not in our 6, but for reference)
        "ng_storage": -1,  # Above average (3,065 Bcf, 6.1% above 5-yr avg)
    },
    "ZC": {  # Corn (not in our 6, but for reference)
        "corn_stocks": -1,  # Above average (13.3B bushels, +10% YoY)
    },
    "CC": {  # Cocoa (not in our 6, but for reference)
        "cocoa_supply_shock": 0,  # Neutral (recovering production, surplus forecast)
    },
}

# Weights for each instrument (from methodology)
WEIGHTS = {
    "GC": {
        "fed_stance": 0.20,
        "real_yields": 0.20,
        "dxy": 0.15,
        "vix": 0.10,
        "gdpnow": 0.05,
        "credit_spreads": 0.05,
        "gold_etf_flows": 0.15,
        "sox": 0.05,
        "move": 0.05,
    },
    "SI": {
        "fed_stance": 0.15,
        "real_yields": 0.15,
        "dxy": 0.10,
        "vix": 0.10,
        "gdpnow": 0.05,
        "credit_spreads": 0.05,
        "gold_etf_flows": 0.15,
        "sox": 0.15,
        "copper": 0.10,
    },
    "ES": {
        "fed_stance": 0.15,
        "real_yields": 0.10,
        "dxy": 0.05,
        "vix": 0.20,
        "gdpnow": 0.15,
        "credit_spreads": 0.15,
        "sox": 0.10,
        "move": 0.10,
    },
    "NQ": {
        "fed_stance": 0.15,
        "real_yields": 0.10,
        "dxy": 0.05,
        "vix": 0.20,
        "gdpnow": 0.10,
        "credit_spreads": 0.10,
        "sox": 0.20,
        "move": 0.10,
    },
    "YM": {
        "fed_stance": 0.15,
        "real_yields": 0.10,
        "dxy": 0.05,
        "vix": 0.20,
        "gdpnow": 0.20,
        "credit_spreads": 0.15,
        "sox": 0.05,
        "move": 0.10,
    },
    "CL": {
        "fed_stance": 0.10,
        "real_yields": 0.05,
        "dxy": 0.15,
        "vix": 0.10,
        "gdpnow": 0.20,
        "credit_spreads": 0.05,
        "oil_supply_shock": 0.20,
        "oil_inventories": 0.15,
    },
}


def calculate_bias_score(instrument: str) -> Tuple[float, Dict[str, float]]:
    """
    Calculate weighted bias score for an instrument.
    
    Returns:
        Tuple of (total_score, component_scores_dict)
    """
    weights = WEIGHTS[instrument]
    component_scores = {}
    total_score = 0.0
    
    for indicator, weight in weights.items():
        # Get indicator value from core or instrument-specific
        if indicator in CORE_INDICATORS:
            value = CORE_INDICATORS[indicator]
        elif indicator in INSTRUMENT_INDICATORS.get(instrument, {}):
            value = INSTRUMENT_INDICATORS[instrument][indicator]
        else:
            value = 0  # Default if not found
        
        contribution = value * weight
        component_scores[indicator] = contribution
        total_score += contribution
    
    return total_score, component_scores


def get_bias_interpretation(score: float) -> str:
    """Convert numerical score to bias interpretation."""
    if score >= 0.30:
        return "STRONG BULLISH"
    elif score >= 0.10:
        return "BULLISH"
    elif score >= -0.10:
        return "NEUTRAL"
    elif score >= -0.30:
        return "BEARISH"
    else:
        return "STRONG BEARISH"


def main():
    """Calculate and display bias scores for all instruments."""
    print("=" * 80)
    print("MACRO BIAS SCORER - DAILY REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 80)
    print()
    
    instruments = ["GC", "SI", "ES", "NQ", "YM", "CL"]
    results = {}
    
    for instrument in instruments:
        score, components = calculate_bias_score(instrument)
        bias = get_bias_interpretation(score)
        results[instrument] = {
            "score": score,
            "bias": bias,
            "components": components
        }
        
        print(f"\n{instrument} (Gold)" if instrument == "GC" else 
              f"\n{instrument} (Silver)" if instrument == "SI" else
              f"\n{instrument} (S&P 500)" if instrument == "ES" else
              f"\n{instrument} (Nasdaq)" if instrument == "NQ" else
              f"\n{instrument} (Dow)" if instrument == "YM" else
              f"\n{instrument} (Crude Oil)")
        print("-" * 80)
        print(f"Weighted Bias Score: {score:+.3f}")
        print(f"Bias Interpretation: {bias}")
        print(f"\nComponent Breakdown:")
        for indicator, contribution in sorted(components.items(), 
                                             key=lambda x: abs(x[1]), 
                                             reverse=True):
            print(f"  {indicator:20s}: {contribution:+.3f}")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    for instrument in instruments:
        result = results[instrument]
        print(f"{instrument}: {result['score']:+.3f} ({result['bias']})")
    
    return results


if __name__ == "__main__":
    results = main()
