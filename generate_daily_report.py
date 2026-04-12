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

# Verified session inputs for the April 12, 2026 UTC report run.
# Signs follow the methodology lookup already used by the repository.
macro_data = {
    "fed_stance": 0,
    "real_yields": 0,
    "usd_dxy": 1,
    "risk_mood": 0,
    "vix_direction": 1,
    "growth_narrative": 1,
    "credit_spreads": 1,
    "sox": 1,
    "move_index": 1,
    "yield_curve_2s10s": -1,
    "copper": 1,
    "oil_inventories": -1,
    "oil_supply_shock": -1,
    "geopolitical_risk": -1,
    "gold_etf_flows": -1,
    "ecb_stance": 1,
    "rba_stance": 1,
    "boj_stance": 1,
    "china_growth": 1,
    "eurozone_growth": 1,
    "rate_diff_eur_usd": 1,
    "rate_diff_aud_usd": 1,
    "rate_diff_jpy_usd": 1,
    "risk_sentiment_aud": 0,
}

instrument_configs = {
    "GC": {"name": "Gold Futures", "factors": {"fed_stance": 1, "real_yields": 2, "usd_dxy": 1, "risk_mood": 1, "growth_narrative": 1, "oil_supply_shock": 1, "gold_etf_flows": 1}},
    "SI": {"name": "Silver Futures", "factors": {"fed_stance": 1, "real_yields": 1, "usd_dxy": 1, "risk_mood": 1, "growth_narrative": 1, "copper": 1, "gold_etf_flows": 1}},
    "CL": {"name": "WTI Crude Oil", "factors": {"oil_supply_shock": 2, "oil_inventories": 1, "growth_narrative": 2, "geopolitical_risk": 1, "usd_dxy": 1}},
    "ES": {"name": "S&P 500 E-mini", "factors": {"fed_stance": 1, "real_yields": 2, "usd_dxy": 1, "risk_mood": 1, "growth_narrative": 1, "credit_spreads": 1, "vix_direction": 1}},
    "NQ": {"name": "Nasdaq 100 E-mini", "factors": {"fed_stance": 1, "real_yields": 2, "usd_dxy": 1, "risk_mood": 1, "growth_narrative": 1, "sox": 1, "move_index": 1}},
    "YM": {"name": "Dow Jones E-mini", "factors": {"fed_stance": 1, "real_yields": 1, "usd_dxy": 1, "risk_mood": 1, "growth_narrative": 2, "credit_spreads": 1, "yield_curve_2s10s": 1}},
    "RTY": {"name": "Russell 2000 E-mini", "factors": {"fed_stance": 1, "real_yields": 1, "usd_dxy": 1, "risk_mood": 1, "growth_narrative": 2, "credit_spreads": 2, "yield_curve_2s10s": 1}},
    "6E": {"name": "Euro FX", "factors": {"fed_stance": 1, "ecb_stance": 1, "rate_diff_eur_usd": 2, "usd_dxy": 1, "risk_mood": 1, "eurozone_growth": 1}},
    "6A": {"name": "Australian Dollar", "factors": {"fed_stance": 1, "rba_stance": 1, "rate_diff_aud_usd": 1, "usd_dxy": 1, "risk_sentiment_aud": 2, "china_growth": 2, "copper": 1}},
    "6J": {"name": "Japanese Yen", "factors": {"fed_stance": 1, "boj_stance": 2, "rate_diff_jpy_usd": 2, "usd_dxy": 1, "risk_mood": 1}},
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

references = {
    "1": {"title": "TradingView DXY page", "url": "https://www.tradingview.com/symbols/TVC-DXY/"},
    "2": {"title": "Cboe VIX product page", "url": "https://www.cboe.com/tradable-products/vix/"},
    "3": {"title": "Atlanta Fed GDPNow", "url": "https://www.atlantafed.org/cqer/research/gdpnow"},
    "4": {"title": "CME FedWatch Tool", "url": "https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html"},
    "5": {"title": "World Gold Council ETF flows page", "url": "https://www.gold.org/goldhub/data/global-gold-backed-etf-holdings-and-flows"},
    "6": {"title": "FRED DFII10 series", "url": "https://fred.stlouisfed.org/series/DFII10"},
    "7": {"title": "FRED BAMLH0A0HYM2 series", "url": "https://fred.stlouisfed.org/series/BAMLH0A0HYM2"},
    "8": {"title": "FRED T10Y2Y series", "url": "https://fred.stlouisfed.org/series/T10Y2Y"},
    "9": {"title": "Swissinfo central bank roundup", "url": "https://www.swissinfo.ch/eng/global-rate-path-veers-higher-in-wake-of-another-trump-shock/91234542"},
    "10": {"title": "FXStreet eurozone PMI article", "url": "https://www.fxstreet.com/news/eurozone-hcob-composite-pmi-above-expectations-505-in-march-actual-507-202604070800"},
    "11": {"title": "SCIO China PMI article", "url": "https://english.scio.gov.cn/m/pressroom/2026-03/31/content_118411839.html"},
    "12": {"title": "TradingView SOX page", "url": "https://www.tradingview.com/symbols/SOX/"},
    "13": {"title": "TradingView MOVE page", "url": "https://www.tradingview.com/symbols/TVC-MOVE/"},
    "14": {"title": "EIA Weekly Petroleum Status Report PDF", "url": "https://www.eia.gov/petroleum/supply/weekly/pdf/wpsrall.pdf"},
    "15": {"title": "Yahoo Finance market report on US-Iran ceasefire", "url": "https://finance.yahoo.com/news/live/stock-market-today-dow-sp-500-nasdaq-surge-oil-plunges-after-us-iran-ceasefire-sparks-relief-rally-200305068.html"},
    "16": {"title": "TradingEconomics copper coverage", "url": "https://tradingeconomics.com/commodity/copper"},
}

factor_notes = {
    "fed_stance": "CME FedWatch showed April 30, 2026 probabilities of 97.9% no change, 2.1% hike, and 0.0% ease with the current target range at 350-375, so the Fed factor remains neutral [4].",
    "real_yields": "FRED DFII10 printed 1.95 on 2026-04-09 versus 1.96 on 2026-04-08, a 1bp move that still classifies as flat under the methodology [6].",
    "usd_dxy": "TradingView showed DXY at 98.697, down 0.098 points (-0.10%) on the session, so the dollar signal remains weak/falling [1].",
    "risk_mood": "Cboe VIX closed at 19.23, which stays inside the methodology's balanced 15-20 zone rather than a high-stress regime [2].",
    "vix_direction": "VIX fell 1.33% (-0.26) from the prior session, leaving the volatility-direction factor supportive [2].",
    "growth_narrative": "GDPNow stood at 1.3% on April 9, unchanged from April 7 and down from 1.6% on April 2, so the growth narrative is classified as slowing on a sequential basis [3].",
    "credit_spreads": "FRED high-yield OAS narrowed to 2.90 on 2026-04-09 from 2.94 on 2026-04-08, which counts as tighter credit spreads [7].",
    "sox": "TradingView source inspection returned a positive daily change of roughly +2.31% for SOX, so semiconductor leadership remains supportive [12].",
    "move_index": "TradingView source inspection returned a negative daily change of roughly -2.51% for MOVE, indicating falling rate volatility [13].",
    "yield_curve_2s10s": "FRED T10Y2Y slipped to 0.50 on 2026-04-10 from 0.51 on 2026-04-09, so the curve signal is classified as flattening [8].",
    "copper": "An accessible copper market page stated that copper rose to about 5.81 USD/lb and reached the highest level since March, so the industrial-metals direction remains positive [16].",
    "oil_inventories": "The latest EIA weekly report window showed U.S. crude inventories rising by about 3.1 million barrels to 464.7 million, which is a bearish inventory build for WTI [14].",
    "oil_supply_shock": "Session reporting shifted from acute disruption toward reopening expectations around Hormuz, so the oil supply-shock factor is now classified as easing rather than intensifying [14] [15].",
    "geopolitical_risk": "Yahoo Finance reported that a US-Iran two-week ceasefire helped oil plunge and improved risk appetite, so the crude-specific geopolitical-risk factor is best classified as easing [15].",
    "gold_etf_flows": "The World Gold Council page described March as a record month for global gold ETF outflows totaling about US$12 billion, leaving the flow signal negative [5].",
    "ecb_stance": "The Swissinfo/Bloomberg roundup said the ECB deposit rate is 2.0% and markets are pricing two to three 25bp hikes in 2026, which supports a hawkish ECB classification [9].",
    "rba_stance": "The same roundup said the RBA cash rate is 4.1% after back-to-back hikes and that markets still price further tightening, so the RBA stance remains hawkish [9].",
    "boj_stance": "The Swissinfo/Bloomberg roundup said markets continue to price further BoJ tightening with some probability of action as soon as this month, supporting a hawkish BoJ classification [9].",
    "china_growth": "China's official March manufacturing PMI rose to 50.4 from 49.0, returning to expansionary territory and supporting an accelerating China-growth classification [11].",
    "eurozone_growth": "FXStreet reported the euro area composite PMI at 50.7 in March versus 50.5 expected, which supports an improving euro-area growth classification [10].",
    "rate_diff_eur_usd": "A neutral Fed combined with a newly hawkish ECB narrative improves the EUR-USD policy differential from the euro's perspective [4] [9].",
    "rate_diff_aud_usd": "A 4.10% RBA cash rate versus the Fed's 3.50%-3.75% target range keeps the AUD-USD rate differential supportive [4] [9].",
    "rate_diff_jpy_usd": "BoJ normalization against a neutral Fed continues to improve the JPY-USD rate-differential narrative [4] [9].",
    "risk_sentiment_aud": "Although ceasefire headlines improved sentiment, VIX at 19.23 still leaves the broad risk backdrop balanced rather than clearly risk-on, so AUD sentiment stays neutral [2] [15].",
}

analysis_paragraphs = {
    "GC": "Gold moves back to a neutral macro stance because the weaker dollar and a slowing U.S. growth narrative are now offset by heavy March ETF outflows and an easing oil-and-geopolitics backdrop. With real yields still effectively flat and VIX only balanced rather than defensive, the model no longer shows a decisive precious-metals impulse.",
    "SI": "Silver retains a slight bullish edge because the softer dollar and rising copper price offset the drag from negative gold ETF flows. The signal is constructive rather than aggressive because real yields remain flat and the broader risk regime is balanced.",
    "CL": "WTI crude drops back to a neutral reading because an inventory build, easing Hormuz disruption expectations, and ceasefire-driven geopolitical relief offset the still-supportive weak-dollar backdrop. The model no longer sees the acute supply shock that had driven the earlier bullish oil bias.",
    "ES": "The S&P 500 stays bullish because the dollar is softer, credit spreads have narrowed again, and VIX direction continues to improve even though the volatility regime itself is only balanced. The setup is positive, but not strong enough to justify a high-conviction momentum classification.",
    "NQ": "Nasdaq 100 remains bullish as falling rate volatility and renewed semiconductor leadership reinforce the weaker-dollar backdrop. The signal is solid rather than extreme because real yields are flat and the broader growth picture is slowing rather than surging.",
    "YM": "Dow futures remain bullish because tighter credit spreads and a weaker dollar continue to support cyclical large caps. A modest flattening in the curve prevents a stronger classification, but the aggregate macro mix still leans positive.",
    "RTY": "Russell 2000 keeps a bullish bias because it benefits most from tighter credit spreads and still-supportive domestic financial conditions, even after the latest curve flattening. Small caps are not as cleanly aligned as the strongest FX setups, but the macro basket still leans constructive.",
    "6E": "Euro FX flips into a strong bullish configuration because the softer dollar is now joined by a hawkish ECB signal, a more favorable policy-differential read, and a modest improvement in euro-area PMI data. This is the largest positive change versus the prior report.",
    "6A": "The Australian dollar remains one of the strongest contracts in the basket because hawkish RBA expectations, a supportive rate differential, rebounding China PMI, and higher copper prices all point in the same direction. The only restraint is that the broader risk backdrop is balanced rather than euphoric.",
    "6J": "Japanese yen futures remain strongly bullish because BoJ normalization and a friendlier rate-differential narrative continue to align with a softer U.S. dollar. Even without a fully defensive VIX regime, the macro mix still favors JPY over USD.",
}

futures_news = [
    {"headline": "US crude stocks rise to near three-year high as EIA reports another inventory build", "url": "https://www.reuters.com/business/energy/us-crude-stocks-rise-gasoline-distillate-inventories-fall-eia-says-2026-04-08/"},
    {"headline": "Oil plunges after the US-Iran ceasefire sparks a relief rally", "url": references["15"]["url"]},
]

currency_news = [
    {"headline": "Eurozone HCOB Composite PMI above expectations: 50.7 in March", "url": references["10"]["url"]},
    {"headline": "China's PMI returns to expansionary territory in March", "url": references["11"]["url"]},
]

calendar_notes = [
    "Preferred ForexFactory calendar extraction was not available in-browser during this session, so the schedule below focuses on directly verified catalysts and near-term macro events.",
    "The next major U.S. macro catalyst remains the April 30 FOMC meeting, where FedWatch still implies an overwhelmingly unchanged outcome [4].",
    "Near-term macro attention also remains on follow-through from the April 9 GDPNow update, China inflation data, and any fresh Strait of Hormuz or ceasefire headlines [3] [11] [15].",
]


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



def get_signal(score: int) -> str:
    if score >= 5:
        return "STRONG_BULLISH"
    if score >= 3:
        return "BULLISH"
    if score >= 1:
        return "SLIGHT_BULLISH"
    if score >= -1:
        return "NEUTRAL"
    if score >= -3:
        return "SLIGHT_BEARISH"
    if score >= -5:
        return "BEARISH"
    return "STRONG_BEARISH"



def get_confidence(symbol: str, score: int) -> int:
    abs_score = abs(score)
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



def get_strategy(score: int, symbol: str) -> tuple[str, str, str]:
    abs_score = abs(score)
    if abs_score >= 5:
        if symbol in {"GC", "SI", "CL", "6E", "6A", "6J"}:
            return "TREND_FOLLOW", "SWING", "2-5 days"
        return "TREND_FOLLOW", "SWING", "1-2 days"
    if abs_score >= 3:
        return "TREND_FOLLOW", "SWING", "1-2 days"
    if abs_score >= 1:
        return "IB_BREAKOUT", "INTRADAY", "session"
    return "RANGE_TRADE", "INTRADAY", "session"



def class_bias_from_score(score: int) -> str:
    return get_signal(score)



def signed_score(value: int) -> str:
    return f"{value:+d}"



def build_markdown(date_label: str, time_label: str, results: dict, asset_class_bias: dict) -> str:
    avg_conf = sum(v["confidence"] for v in results.values()) / len(results)
    top = sorted(results.items(), key=lambda kv: (kv[1]["confidence"], kv[1]["score"]), reverse=True)[:3]

    lines: list[str] = []
    lines.append("# Matrix Futures Daily Bias Report")
    lines.append(f"**Date:** {date_label} | **Time:** {time_label} UTC")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Overall Market Bias: MIXED")
    lines.append("")
    lines.append("Macro conditions on April 12 are no longer one-directional. The dollar remains softer, credit spreads are tighter, and both equity and Treasury volatility continue to improve, which keeps the equity and FX backdrop constructive. However, gold lost ETF support and crude lost its earlier supply-shock premium as ceasefire headlines and reopening expectations weighed on oil, leaving commodities much less uniformly bullish than in the prior run [1] [2] [3] [5] [7] [15].")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Main Summary Table")
    lines.append("")
    lines.append("| Instrument | Name | Numeric Bias Score | Signal | Confidence | Approach | Mode | Hold |")
    lines.append("|------------|------|--------------------|--------|------------|----------|------|------|")
    for symbol in ["GC", "SI", "CL", "ES", "NQ", "YM", "RTY", "6E", "6A", "6J"]:
        data = results[symbol]
        lines.append(f"| {symbol} | {instrument_display[symbol]} | {signed_score(data['score'])} | {data['signal']} | {data['confidence']}/10 | {data['recommended_approach']} | {data['recommended_mode']} | {data['hold_expectation']} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Asset Class Summary")
    lines.append("")
    lines.append("| Asset Class | Bias | Key Driver |")
    lines.append("|-------------|------|------------|")
    lines.append(f"| Commodities | {asset_class_bias['COMMODITIES']} | Gold ETF outflows and an easing crude risk premium offset the weaker USD backdrop [1] [5] [14] [15] |")
    lines.append(f"| Indices | {asset_class_bias['INDICES']} | Tighter credit spreads, falling VIX direction, and stronger semiconductors keep the risk backdrop constructive [2] [7] [12] [13] |")
    lines.append(f"| FX | {asset_class_bias['FX']} | The softer dollar now aligns with hawkish ECB, RBA, and BoJ narratives plus improving China and euro-area growth proxies [1] [9] [10] [11] |")
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
    lines.append("## Economic Calendar Context")
    lines.append("")
    for note in calendar_notes:
        lines.append(f"- {note}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Brief News Summary: Futures")
    lines.append("")
    for item in futures_news:
        lines.append(f"- {item['headline']} | {item['url']}")
    lines.append("")
    lines.append("Futures positioning is now dominated by the contrast between easier geopolitical conditions for oil and still-improving financial conditions for equities. That combination softens crude conviction while preserving a positive index backdrop [2] [7] [14] [15].")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Brief News Summary: Currency")
    lines.append("")
    for item in currency_news:
        lines.append(f"- {item['headline']} | {item['url']}")
    lines.append("")
    lines.append("Currency markets remain centered on a weaker dollar and widening policy divergence in favor of EUR, AUD, and JPY. The euro improved the most because its growth proxy and central-bank narrative both turned more supportive in the current session's evidence set [1] [4] [9] [10] [11].")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Key Macro Themes")
    lines.append("")
    lines.append("1. **The dollar remains a cross-asset tailwind** because DXY fell to 98.697 and stayed directionally weak [1].")
    lines.append("2. **Volatility conditions improved without turning euphoric** because VIX stayed in the balanced zone at 19.23 while MOVE also declined [2] [13].")
    lines.append("3. **Oil lost its strongest macro support** because inventories built and ceasefire headlines eased the supply-risk narrative [14] [15].")
    lines.append("4. **FX leadership strengthened further** because the ECB, RBA, and BoJ narratives all screened hawkish enough to complement the weaker dollar backdrop [4] [9] [10] [11].")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Upcoming Catalysts")
    lines.append("")
    lines.append("### Imminent (< 1 Week)")
    lines.append("- Follow-through from the April 9 GDPNow slowdown signal [3]")
    lines.append("- China inflation and post-PMI macro follow-up [11]")
    lines.append("- Any fresh Strait of Hormuz or ceasefire headlines [15]")
    lines.append("")
    lines.append("### Near-Term (1-4 Weeks)")
    lines.append("- Federal Reserve meeting on April 30 [4]")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Data Quality")
    lines.append("")
    lines.append("- FRED inputs are official but lag live markets; the model therefore uses the latest available official DFII10, HY OAS, and T10Y2Y prints [6] [7] [8].")
    lines.append("- Some market sites blocked direct browser extraction, so programmatic page-source checks and accessible alternatives were used for SOX, MOVE, copper, and parts of the oil narrative [12] [13] [14] [16].")
    lines.append("- Gold ETF flows use the latest directly viewed World Gold Council summary and are therefore monthly rather than intraday [5].")
    lines.append(f"- Average confidence: {avg_conf:.1f}/10")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## References")
    lines.append("")
    for key, ref in references.items():
        lines.append(f"[{key}]: {ref['url']} \"{ref['title']}\"")
    lines.append("")
    lines.append("---")
    lines.append("**End of Report**")
    lines.append("")
    return "\n".join(lines)



def main() -> None:
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H%M")
    iso_str = now.replace(microsecond=0).isoformat().replace("+00:00", "Z")
    date_label = now.strftime("%B %d, %Y")
    time_label = now.strftime("%H:%M")

    results = {}
    scoring_detail = {}
    for symbol, config in instrument_configs.items():
        score, detail = calculate_score(config)
        signal = get_signal(score)
        confidence = get_confidence(symbol, score)
        approach, mode, hold = get_strategy(score, symbol)
        results[symbol] = {
            "score": score,
            "signal": signal,
            "confidence": confidence,
            "recommended_approach": approach,
            "recommended_mode": mode,
            "hold_expectation": hold,
        }
        scoring_detail[symbol] = {
            "name": config["name"],
            "raw_weighted_score": score,
            "factors": detail,
        }

    asset_class_bias = {
        "COMMODITIES": class_bias_from_score(round(sum(results[s]["score"] for s in ["GC", "SI", "CL"]) / 3)),
        "INDICES": class_bias_from_score(round(sum(results[s]["score"] for s in ["ES", "NQ", "YM", "RTY"]) / 4)),
        "FX": class_bias_from_score(round(sum(results[s]["score"] for s in ["6E", "6A", "6J"]) / 3)),
    }

    output = {
        "date": date_str,
        "generated_at": iso_str,
        "methodology_version": "3.0_STRATEGY",
        "scores": results,
        "asset_class_bias": asset_class_bias,
        "key_drivers": [
            "DXY remained weak at 98.697 and down 0.10%, preserving a constructive backdrop for non-USD assets [1].",
            "VIX stayed balanced at 19.23 while falling on the day, and MOVE also declined, keeping financial conditions friendly for equity futures [2] [13].",
            "Gold ETF flows turned into a headwind while oil inventories built and crude's geopolitical premium eased after ceasefire headlines [5] [14] [15].",
            "The ECB, RBA, and BoJ all screened hawkish enough relative to a neutral Fed to strengthen the FX complex, with euro-area and China PMI data also improving [4] [9] [10] [11].",
        ],
        "data_quality": {
            "stale_sources": [
                "FRED DFII10 latest official observation used: 2026-04-09 [6]",
                "FRED HY OAS latest official observation used: 2026-04-09 [7]",
                "FRED T10Y2Y latest official observation used: 2026-04-10 [8]",
            ],
            "fallbacks_used": [
                "Programmatic page-source checks for SOX and MOVE after market-site blocking [12] [13]",
                "Accessible copper market page after browser blocks on MarketWatch and Investing.com [16]",
                "Swissinfo/Bloomberg central-bank roundup after Reuters access restrictions [9]",
            ],
            "overnight_changes": [
                "DXY down 0.10% on the session [1]",
                "VIX down 1.33% on the session [2]",
                "SOX up about 2.31% on the session [12]",
                "MOVE down about 2.51% on the session [13]",
            ],
        },
        "catalyst_proximity": {
            "imminent": [
                "Ceasefire durability and Strait of Hormuz reopening headlines [15]",
                "Post-PMI China macro follow-through [11]",
                "Any fresh GDPNow revision after the slowdown from 1.6% to 1.3% [3]",
            ],
            "near_term": [
                "Federal Reserve meeting on April 30 [4]",
            ],
            "background": [
                "Hawkish ECB, RBA, and BoJ divergence versus a neutral Fed [4] [9]",
                "Gold ETF outflows as a drag on the precious-metals complex [5]",
            ],
        },
        "references": references,
    }

    timestamp_json = BIAS_DIR / f"{date_str}_{time_str}.json"
    latest_json = BIAS_DIR / "latest.json"
    timestamp_md = EXEC_DIR / f"{date_str}_{time_str}.md"
    latest_md = EXEC_DIR / "latest.md"
    detail_json = FACTOR_DIR / f"{date_str}_{time_str}_scoring_detail.json"

    with open(timestamp_json, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    with open(latest_json, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    markdown = build_markdown(date_label, time_label, results, asset_class_bias)
    timestamp_md.write_text(markdown, encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")

    detail_json.write_text(json.dumps({
        "date": date_str,
        "generated_at": iso_str,
        "macro_data": macro_data,
        "scoring_detail": scoring_detail,
    }, indent=2), encoding="utf-8")

    print(json.dumps({
        "date": date_str,
        "generated_at": iso_str,
        "timestamp_json": str(timestamp_json),
        "latest_json": str(latest_json),
        "timestamp_md": str(timestamp_md),
        "latest_md": str(latest_md),
        "detail_json": str(detail_json),
        "scores": {k: v["score"] for k, v in results.items()},
        "asset_class_bias": asset_class_bias,
    }, indent=2))


if __name__ == "__main__":
    main()
