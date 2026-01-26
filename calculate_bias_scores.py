#!/usr/bin/env python3
"""
Macro Bias Scorer - Calculate weighted bias scores for futures instruments
Based on methodology from Macro_Bias_Scorer_Reference.md
Uses WHOLE NUMBER scoring as specified in the reference document
"""

from datetime import datetime
from typing import Dict, List, Tuple

# Core macro indicators (collected data) - WHOLE NUMBER SCORES
CORE_INDICATORS = {
    "fed_stance": +1,  # Dovish hold (CME FedWatch shows rate cut expectations)
    "real_yields": -2,  # Up (10Y TIPS at 2.38%, rising from lows)
    "dxy": +1,  # Down (DXY at 107.39, down 0.52%)
    "risk_mood": +1,  # Risk-off (VIX down = risk-on, inverted for gold/safe havens)
    "vix": +1,  # Down (VIX at 15.88, down 1.31%)
    "growth_narrative": -1,  # Accelerating (GDPNow at 2.3%, positive growth)
    "credit_spreads": +1,  # Narrowing (HY OAS at 2.68%, very tight)
    "yield_curve_2s10s": +1,  # Steepening (0.64%, positive and rising)
}

# Instrument-specific indicators
INSTRUMENT_INDICATORS = {
    "GC": {  # Gold
        "gold_etf_flows": +1,  # Up (record $89B inflows in 2025, $10B in Dec)
        "oil_supply_shock": 0,  # Neutral (no major supply disruptions)
    },
    "SI": {  # Silver
        "gold_etf_flows": +1,  # Up (same as gold)
        "copper": +1,  # Up (Copper at $5.93/lb, +38% YoY)
    },
    "ES": {  # S&P 500
        # Uses core indicators only
    },
    "NQ": {  # Nasdaq
        "sox": +1,  # Up (SOX at 7,960, +46% YoY, near ATH)
        "move": +1,  # Down (MOVE at 56.25, down 32.82% over 6 months)
    },
    "YM": {  # Dow
        # Uses core indicators only
    },
    "CL": {  # Crude Oil
        "oil_supply_shock": 0,  # Neutral (no major supply disruptions)
        "inventories": -1,  # Build (increased by 3.6M barrels, mildly bearish)
        "geopolitical_risk": 0,  # Neutral (no major escalations)
    },
}

# Weights for each instrument (from methodology) - WHOLE NUMBERS
WEIGHTS = {
    "GC": {
        "fed_stance": 1,
        "real_yields": 2,
        "dxy": 1,
        "risk_mood": 1,
        "growth_narrative": 1,
        "oil_supply_shock": 1,
        "gold_etf_flows": 1,
    },
    "SI": {
        "fed_stance": 1,
        "real_yields": 1,
        "dxy": 1,
        "risk_mood": 1,
        "growth_narrative": 1,
        "copper": 1,
        "gold_etf_flows": 1,
    },
    "ES": {
        "fed_stance": 1,
        "real_yields": 2,
        "dxy": 1,
        "risk_mood": 1,
        "growth_narrative": 1,
        "credit_spreads": 1,
        "vix": 1,
    },
    "NQ": {
        "fed_stance": 1,
        "real_yields": 2,
        "dxy": 1,
        "risk_mood": 1,
        "growth_narrative": 1,
        "sox": 1,
        "move": 1,
    },
    "YM": {
        "fed_stance": 1,
        "real_yields": 1,
        "dxy": 1,
        "risk_mood": 1,
        "growth_narrative": 2,
        "credit_spreads": 1,
        "yield_curve_2s10s": 1,
    },
    "CL": {
        "oil_supply_shock": 2,
        "inventories": 1,
        "growth_narrative": 2,
        "geopolitical_risk": 1,
        "dxy": 1,
    },
}


def calculate_bias_score(instrument: str) -> Tuple[int, Dict[str, int]]:
    """
    Calculate weighted bias score for an instrument.
    
    Returns:
        Tuple of (total_score, component_scores_dict)
    """
    weights = WEIGHTS[instrument]
    component_scores = {}
    total_score = 0
    
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


def get_bias_interpretation(score: int) -> str:
    """Convert numerical score to bias interpretation."""
    if score >= 5:
        return "STRONG BULLISH"
    elif score >= 3:
        return "BULLISH"
    elif score >= 1:
        return "SLIGHT BULLISH"
    elif score >= -1:
        return "NEUTRAL"
    elif score >= -3:
        return "SLIGHT BEARISH"
    elif score >= -5:
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
    instrument_names = {
        "GC": "Gold",
        "SI": "Silver",
        "ES": "S&P 500",
        "NQ": "Nasdaq",
        "YM": "Dow",
        "CL": "Crude Oil"
    }
    
    results = {}
    
    for instrument in instruments:
        score, components = calculate_bias_score(instrument)
        bias = get_bias_interpretation(score)
        results[instrument] = {
            "score": score,
            "bias": bias,
            "components": components
        }
        
        print(f"\n{instrument} ({instrument_names[instrument]})")
        print("-" * 80)
        print(f"Weighted Bias Score: {score:+d}")
        print(f"Bias Interpretation: {bias}")
        print(f"\nComponent Breakdown:")
        for indicator, contribution in sorted(components.items(), 
                                             key=lambda x: abs(x[1]), 
                                             reverse=True):
            print(f"  {indicator:20s}: {contribution:+d}")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    for instrument in instruments:
        result = results[instrument]
        print(f"{instrument}: {result['score']:+d} ({result['bias']})")
    
    return results


if __name__ == "__main__":
    results = main()
