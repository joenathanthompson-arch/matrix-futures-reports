#!/usr/bin/env python3
"""
Matrix Futures Daily Bias Scorer
Calculates weighted bias scores for 10 futures instruments
"""

from datetime import datetime, timezone
import json

# Data from collection (2026-01-29)
fed_stance = 1  # Dovish hold
real_yields = 0  # Flat
usd_dxy = 1  # Weak/Falling
risk_mood = 0  # Balanced (VIX 15-20)
vix_direction = 0  # Flat
growth = -1  # Accelerating
credit_spreads = 1  # Narrowing
sox = 1  # Rising
move = 1  # Falling
curve_2s10s = 1  # Steepening
copper = 1  # Rising
oil_inventories = 1  # Draw
geopolitical = 1  # Rising
gold_etf_flows = 1  # Inflows
ecb_stance = 0  # Neutral hold
rba_stance = 1  # Hawkish
boj_stance = 1  # Hawkish
china_growth = 0  # Stable

# Calculate GC (Gold) - Max Range: -14 to +16
gc_score = (
    fed_stance * 1 +
    real_yields * 2 +  # Weight 2
    usd_dxy * 1 +
    risk_mood * 1 +
    growth * 1 +
    geopolitical * 1 +  # Using geopolitical as proxy for oil supply shock
    gold_etf_flows * 1
)
print(f"GC (Gold): {gc_score}")
print(f"  Fed: {fed_stance}*1={fed_stance}")
print(f"  Real Yields: {real_yields}*2={real_yields*2}")
print(f"  USD: {usd_dxy}*1={usd_dxy}")
print(f"  Risk Mood: {risk_mood}*1={risk_mood}")
print(f"  Growth: {growth}*1={growth}")
print(f"  Geopolitical: {geopolitical}*1={geopolitical}")
print(f"  Gold ETF: {gold_etf_flows}*1={gold_etf_flows}")
print()

# Calculate SI (Silver) - Max Range: -10 to +12
si_score = (
    fed_stance * 1 +
    real_yields * 1 +
    usd_dxy * 1 +
    risk_mood * 1 +
    growth * 1 +
    copper * 1 +
    gold_etf_flows * 1
)
print(f"SI (Silver): {si_score}")
print(f"  Fed: {fed_stance}*1={fed_stance}")
print(f"  Real Yields: {real_yields}*1={real_yields}")
print(f"  USD: {usd_dxy}*1={usd_dxy}")
print(f"  Risk Mood: {risk_mood}*1={risk_mood}")
print(f"  Growth: {growth}*1={growth}")
print(f"  Copper: {copper}*1={copper}")
print(f"  Gold ETF: {gold_etf_flows}*1={gold_etf_flows}")
print()

# Calculate CL (Crude) - Max Range: -9 to +9
cl_score = (
    geopolitical * 2 +  # Weight 2 (oil supply shock)
    oil_inventories * 1 +
    growth * 2 +  # Weight 2
    geopolitical * 1 +  # Geopolitical risk
    usd_dxy * 1
)
print(f"CL (Crude): {cl_score}")
print(f"  Oil Supply Shock: {geopolitical}*2={geopolitical*2}")
print(f"  Inventories: {oil_inventories}*1={oil_inventories}")
print(f"  Growth: {growth}*2={growth*2}")
print(f"  Geopolitical: {geopolitical}*1={geopolitical}")
print(f"  USD: {usd_dxy}*1={usd_dxy}")
print()

# Calculate ES (S&P 500) - Max Range: -12 to +14
es_score = (
    fed_stance * 1 +
    real_yields * 2 +  # Weight 2
    usd_dxy * 1 +
    risk_mood * 1 +
    growth * 1 +
    credit_spreads * 1 +
    vix_direction * 1
)
print(f"ES (S&P 500): {es_score}")
print(f"  Fed: {fed_stance}*1={fed_stance}")
print(f"  Real Yields: {real_yields}*2={real_yields*2}")
print(f"  USD: {usd_dxy}*1={usd_dxy}")
print(f"  Risk Mood: {risk_mood}*1={risk_mood}")
print(f"  Growth: {growth}*1={growth}")
print(f"  Credit Spreads: {credit_spreads}*1={credit_spreads}")
print(f"  VIX Direction: {vix_direction}*1={vix_direction}")
print()

# Calculate NQ (Nasdaq) - Max Range: -12 to +14
nq_score = (
    fed_stance * 1 +
    real_yields * 2 +  # Weight 2
    usd_dxy * 1 +
    risk_mood * 1 +
    growth * 1 +
    sox * 1 +
    move * 1
)
print(f"NQ (Nasdaq): {nq_score}")
print(f"  Fed: {fed_stance}*1={fed_stance}")
print(f"  Real Yields: {real_yields}*2={real_yields*2}")
print(f"  USD: {usd_dxy}*1={usd_dxy}")
print(f"  Risk Mood: {risk_mood}*1={risk_mood}")
print(f"  Growth: {growth}*1={growth}")
print(f"  SOX: {sox}*1={sox}")
print(f"  MOVE: {move}*1={move}")
print()

# Calculate YM (Dow) - Max Range: -10 to +12
ym_score = (
    fed_stance * 1 +
    real_yields * 1 +
    usd_dxy * 1 +
    risk_mood * 1 +
    growth * 2 +  # Weight 2
    credit_spreads * 1 +
    curve_2s10s * 1
)
print(f"YM (Dow): {ym_score}")
print(f"  Fed: {fed_stance}*1={fed_stance}")
print(f"  Real Yields: {real_yields}*1={real_yields}")
print(f"  USD: {usd_dxy}*1={usd_dxy}")
print(f"  Risk Mood: {risk_mood}*1={risk_mood}")
print(f"  Growth: {growth}*2={growth*2}")
print(f"  Credit Spreads: {credit_spreads}*1={credit_spreads}")
print(f"  2s10s: {curve_2s10s}*1={curve_2s10s}")
print()

# Calculate RTY (Russell 2000) - Max Range: -12 to +14
rty_score = (
    fed_stance * 1 +
    real_yields * 1 +
    usd_dxy * 1 +
    risk_mood * 1 +
    growth * 2 +  # Weight 2
    credit_spreads * 2 +  # Weight 2
    curve_2s10s * 1
)
print(f"RTY (Russell 2000): {rty_score}")
print(f"  Fed: {fed_stance}*1={fed_stance}")
print(f"  Real Yields: {real_yields}*1={real_yields}")
print(f"  USD: {usd_dxy}*1={usd_dxy}")
print(f"  Risk Mood: {risk_mood}*1={risk_mood}")
print(f"  Growth: {growth}*2={growth*2}")
print(f"  Credit Spreads: {credit_spreads}*2={credit_spreads*2}")
print(f"  2s10s: {curve_2s10s}*1={curve_2s10s}")
print()

# Calculate M6E (Euro) - Max Range: -10 to +10
# For EUR/USD: Bullish M6E = Bullish EUR = Bearish USD
# Fed dovish (+1) vs ECB neutral (0) = slight EUR advantage
# USD weak (+1) = EUR strong = bullish M6E
m6e_score = (
    fed_stance * 1 +  # Dovish Fed = bullish EUR
    ecb_stance * 1 +  # Neutral
    (fed_stance - ecb_stance) * 2 +  # Rate differential (Fed dovish vs ECB neutral) Weight 2
    usd_dxy * 1 +  # Weak USD = strong EUR
    risk_mood * 1 +
    growth * 1  # Using US growth as proxy for Eurozone
)
print(f"M6E (Euro): {m6e_score}")
print(f"  Fed: {fed_stance}*1={fed_stance}")
print(f"  ECB: {ecb_stance}*1={ecb_stance}")
print(f"  Rate Differential: ({fed_stance}-{ecb_stance})*2={(fed_stance-ecb_stance)*2}")
print(f"  USD: {usd_dxy}*1={usd_dxy}")
print(f"  Risk Mood: {risk_mood}*1={risk_mood}")
print(f"  Growth: {growth}*1={growth}")
print()

# Calculate 6A (Australian Dollar) - Max Range: -12 to +12
# Risk-on sentiment: VIX low = risk-on, but VIX is balanced (0)
# For risk sentiment, use inverse of risk_mood for AUD (risk-off = -1 for AUD)
risk_sentiment = -risk_mood  # Risk-off (VIX >20) = -1 for AUD, Risk-on (VIX <15) = +1 for AUD
# Currently VIX balanced = 0
aud_6a_score = (
    fed_stance * 1 +  # Dovish Fed = bullish AUD
    rba_stance * 1 +  # Hawkish RBA = bullish AUD
    (rba_stance - fed_stance) * 1 +  # Rate differential (RBA hawkish vs Fed dovish)
    usd_dxy * 1 +  # Weak USD = strong AUD
    risk_sentiment * 2 +  # Weight 2 - AUD is risk currency
    china_growth * 2 +  # Weight 2 - China is major trade partner
    copper * 1  # Commodity proxy
)
print(f"6A (Australian Dollar): {aud_6a_score}")
print(f"  Fed: {fed_stance}*1={fed_stance}")
print(f"  RBA: {rba_stance}*1={rba_stance}")
print(f"  Rate Differential: ({rba_stance}-{fed_stance})*1={(rba_stance-fed_stance)*1}")
print(f"  USD: {usd_dxy}*1={usd_dxy}")
print(f"  Risk Sentiment: {risk_sentiment}*2={risk_sentiment*2}")
print(f"  China Growth: {china_growth}*2={china_growth*2}")
print(f"  Copper: {copper}*1={copper}")
print()

# Calculate 6J (Japanese Yen) - Max Range: -10 to +10
# IMPORTANT: 6J quotes are inverted - Bullish 6J = Bullish JPY = Bearish USD/JPY
# Risk-off = bullish JPY, so we use inverse of risk_mood
jpy_risk_mood = -risk_mood  # Risk-off (VIX >20) = +1 for JPY
jpy_6j_score = (
    fed_stance * 1 +  # Dovish Fed = bullish JPY (narrows differential)
    boj_stance * 2 +  # Weight 2 - Hawkish BoJ = bullish JPY
    (boj_stance - fed_stance) * 2 +  # Weight 2 - Rate differential
    usd_dxy * 1 +  # Weak USD = strong JPY
    jpy_risk_mood * 1  # Risk-off = bullish JPY
)
print(f"6J (Japanese Yen): {jpy_6j_score}")
print(f"  Fed: {fed_stance}*1={fed_stance}")
print(f"  BoJ: {boj_stance}*2={boj_stance*2}")
print(f"  Rate Differential: ({boj_stance}-{fed_stance})*2={(boj_stance-fed_stance)*2}")
print(f"  USD: {usd_dxy}*1={usd_dxy}")
print(f"  Risk Mood (JPY): {jpy_risk_mood}*1={jpy_risk_mood}")
print()

# Map scores to signals
def map_signal(score):
    if score >= 5:
        return "STRONG_BULLISH"
    elif score >= 3:
        return "BULLISH"
    elif score >= 1:
        return "SLIGHT_BULLISH"
    elif score >= -1:
        return "NEUTRAL"
    elif score >= -3:
        return "SLIGHT_BEARISH"
    elif score >= -5:
        return "BEARISH"
    else:
        return "STRONG_BEARISH"

# Assign confidence scores (1-10)
# Based on data freshness, signal clarity, and catalyst proximity
scores = {
    "GC": {"score": gc_score, "signal": map_signal(gc_score), "confidence": 8},
    "SI": {"score": si_score, "signal": map_signal(si_score), "confidence": 7},
    "CL": {"score": cl_score, "signal": map_signal(cl_score), "confidence": 7},
    "ES": {"score": es_score, "signal": map_signal(es_score), "confidence": 7},
    "NQ": {"score": nq_score, "signal": map_signal(nq_score), "confidence": 7},
    "YM": {"score": ym_score, "signal": map_signal(ym_score), "confidence": 7},
    "RTY": {"score": rty_score, "signal": map_signal(rty_score), "confidence": 7},
    "M6E": {"score": m6e_score, "signal": map_signal(m6e_score), "confidence": 6},
    "6A": {"score": aud_6a_score, "signal": map_signal(aud_6a_score), "confidence": 7},
    "6J": {"score": jpy_6j_score, "signal": map_signal(jpy_6j_score), "confidence": 7}
}

# Asset class bias aggregation
commodities_bullish = sum(1 for sym in ["GC", "SI", "CL"] if "BULLISH" in scores[sym]["signal"])
indices_bullish = sum(1 for sym in ["ES", "NQ", "YM", "RTY"] if "BULLISH" in scores[sym]["signal"])
fx_bullish = sum(1 for sym in ["M6E", "6A", "6J"] if "BULLISH" in scores[sym]["signal"])

def aggregate_bias(bullish_count, total_count, threshold):
    if bullish_count >= threshold:
        return "BULLISH"
    elif bullish_count == 0:
        return "BEARISH"
    else:
        return "MIXED"

asset_class_bias = {
    "COMMODITIES": aggregate_bias(commodities_bullish, 3, 2),
    "INDICES": aggregate_bias(indices_bullish, 4, 3),
    "FX": aggregate_bias(fx_bullish, 3, 2)
}

# Generate timestamp
now = datetime.now(timezone.utc)
date_str = now.strftime("%Y-%m-%d")
timestamp_str = now.strftime("%Y-%m-%dT%H:%M:%SZ")
filename_timestamp = now.strftime("%Y-%m-%d_%H%M")

# Create JSON output
output = {
    "date": date_str,
    "generated_at": timestamp_str,
    "scores": scores,
    "asset_class_bias": asset_class_bias,
    "key_drivers": [
        "Fed dovish hold supporting risk assets",
        "Geopolitical tensions (Iran-US) elevating gold and oil",
        "USD weakness benefiting commodities and FX"
    ],
    "data_quality": {
        "stale_sources": ["DFII10", "BAMLH0A0HYM2", "T10Y2Y"],
        "fallbacks_used": ["CNBC for real yields confirmation"]
    }
}

print("\n=== FINAL SCORES ===")
for symbol, data in scores.items():
    print(f"{symbol}: {data['score']:+d} ({data['signal']}) - Confidence: {data['confidence']}/10")

print(f"\n=== ASSET CLASS BIAS ===")
for asset_class, bias in asset_class_bias.items():
    print(f"{asset_class}: {bias}")

print(f"\n=== OUTPUT ===")
print(f"Filename: {filename_timestamp}.json")
print(json.dumps(output, indent=2))
