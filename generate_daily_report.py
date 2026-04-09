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

# Refreshed April 9, 2026 UTC inputs collected or confirmed during this session.
# Integer scoring conventions follow docs/Macro_Bias_Scorer_Reference.md.
macro_data = {
    "fed_stance": 0,
    "real_yields": 0,
    "usd_dxy": 1,
    "risk_mood": 0,
    "vix_direction": 1,
    "growth_narrative": 0,
    "credit_spreads": 1,
    "sox": 1,
    "move_index": 1,
    "yield_curve_2s10s": 1,
    "copper": -1,
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
    "risk_sentiment_aud": 0,
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

references = {
    "1": {
        "title": "TradingView DXY page",
        "url": "https://www.tradingview.com/symbols/TVC-DXY/",
    },
    "2": {
        "title": "Cboe VIX product page",
        "url": "https://www.cboe.com/tradable-products/vix/",
    },
    "3": {
        "title": "Atlanta Fed GDPNow",
        "url": "https://www.atlantafed.org/cqer/research/gdpnow",
    },
    "4": {
        "title": "TradingView SOX page",
        "url": "https://www.tradingview.com/symbols/SOX/",
    },
    "5": {
        "title": "TradingView MOVE page",
        "url": "https://www.tradingview.com/symbols/TVC-MOVE/",
    },
    "6": {
        "title": "TradingView Copper continuous futures page",
        "url": "https://www.tradingview.com/symbols/COMEX-HG1!/",
    },
    "7": {
        "title": "CME FedWatch Tool",
        "url": "https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html",
    },
    "8": {
        "title": "ECB key interest rates page",
        "url": "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html",
    },
    "9": {
        "title": "RBA cash rate page",
        "url": "https://www.rba.gov.au/statistics/cash-rate/",
    },
    "10": {
        "title": "FRED DFII10 series",
        "url": "https://fred.stlouisfed.org/series/DFII10",
    },
    "11": {
        "title": "FRED BAMLH0A0HYM2 series",
        "url": "https://fred.stlouisfed.org/series/BAMLH0A0HYM2",
    },
    "12": {
        "title": "FRED T10Y2Y series",
        "url": "https://fred.stlouisfed.org/series/T10Y2Y",
    },
    "13": {
        "title": "World Gold Council weekly markets monitor",
        "url": "https://www.gold.org/goldhub/gold-focus/2026/04/weekly-markets-monitor-21-tonne-salute",
    },
    "14": {
        "title": "Bank of Japan monetary policy schedule page",
        "url": "https://www.boj.or.jp/en/mopo/mpmsche_minu/index.htm",
    },
    "15": {
        "title": "China NBS PMI press release",
        "url": "https://www.stats.gov.cn/english/PressRelease/202604/t20260401_1962920.html",
    },
    "16": {
        "title": "FXStreet eurozone PMI article",
        "url": "https://www.fxstreet.com/news/eurozone-hcob-composite-pmi-above-expectations-505-in-march-actual-507-202604070800",
    },
    "17": {
        "title": "EIA press release on Hormuz closure and production outages",
        "url": "https://www.eia.gov/pressroom/releases/press586.php",
    },
    "18": {
        "title": "Anadolu summary of the latest EIA crude inventory release",
        "url": "https://www.aa.com.tr/en/energy/oil/us-crude-oil-inventories-up-by-07-for-week-ending-april-3/56257",
    },
    "19": {
        "title": "AP market roundup on stocks and oil",
        "url": "https://apnews.com/article/stock-markets-trump-iran-ceasefire-oil-857ae30b3be4441819b2848fd594a33d",
    },
    "20": {
        "title": "Forex.com FX market article",
        "url": "https://www.forex.com/en-us/news-and-analysis/oil-stocks-still-driving-fx-markets-as-ceasefire-hopes-push-into-eow/",
    },
}

factor_notes = {
    "fed_stance": "CME FedWatch showed 98.4% probability of no change and 1.6% probability of a hike for the April 30 FOMC meeting, so the Fed stance remains neutral [7].",
    "real_yields": "FRED DFII10 printed 1.96 on both 2026-04-08 and 2026-04-07, so real yields were flat on the latest official reading [10].",
    "usd_dxy": "TradingView showed DXY at 98.795, down 0.203 points (-0.21%) from a 98.998 prior close, which keeps the dollar factor weak/falling [1].",
    "risk_mood": "Cboe VIX was 19.49, which lies in the methodology's balanced 15-20 zone rather than the defensive above-20 regime [2].",
    "vix_direction": "Cboe VIX fell 7.37% (-1.55) on the day from a 21.04 prior close, so the directional volatility signal remains supportive [2].",
    "growth_narrative": "Atlanta Fed GDPNow held at 1.3% for 2026:Q1 on April 9, leaving the growth narrative stable rather than re-accelerating or deteriorating further [3].",
    "credit_spreads": "FRED HY OAS narrowed to 2.94 on 2026-04-08 from 3.12 on 2026-04-07, which qualifies as tighter credit spreads on the latest official print [11].",
    "sox": "TradingView showed SOX at 8,689.53, up 2.10% on the day from 8,510.92, keeping the semiconductor leadership factor positive [4].",
    "move_index": "TradingView showed MOVE at 74.0129, down 6.00% on the day from 78.7357, reinforcing a friendlier Treasury-volatility backdrop [5].",
    "yield_curve_2s10s": "FRED T10Y2Y remained positive at 0.51 on 2026-04-09 after 0.50 on 2026-04-08, so the curve stays normalized and positively sloped [12].",
    "copper": "TradingView showed COMEX copper at 5.7475, down 0.29% on the day, flipping the copper direction factor to bearish [6].",
    "oil_inventories": "Anadolu's summary of the latest EIA release said U.S. commercial crude inventories rose by 3.1 million barrels to 464.7 million in the week ending April 3, a bearish build for WTI [18].",
    "oil_supply_shock": "EIA said oil flows through the Strait of Hormuz remain limited and estimated production shut-ins rising from 7.5 million b/d in March to 9.1 million b/d in April, preserving a bullish supply-shock factor for crude [17].",
    "geopolitical_risk": "The Middle East energy conflict and continuing tanker-flow uncertainty keep geopolitical risk elevated, which remains supportive for oil risk premium [17] [19].",
    "gold_etf_flows": "The World Gold Council weekly monitor reported a 21-tonne inflow into global gold ETFs at the start of April, preserving a positive investment-flow signal for gold and silver [13].",
    "ecb_stance": "The ECB key rates page continues to show 2.00% deposit, 2.15% MRO, and 2.40% marginal lending, consistent with an easing-biased policy stance [8].",
    "rba_stance": "The RBA cash rate page continues to show a 4.10% cash rate target effective March 18, 2026, preserving a supportive policy stance for AUD [9].",
    "boj_stance": "The BoJ policy schedule still points back to the March 18-19 cycle as the latest completed meeting, consistent with retaining the repository's normalization bias [14].",
    "china_growth": "China's official March manufacturing PMI rebounded to 50.4 from 49.0, confirming an improving China growth proxy [15].",
    "eurozone_growth": "A fallback FXStreet report on the HCOB/S&P Global release put euro area composite PMI at 50.7 in March, below February's 51.9, which keeps the eurozone growth factor negative [16].",
    "rate_diff_eur_usd": "A neutral Fed versus an easing-biased ECB continues to leave the policy-rate differential unfavorable for EUR [7] [8].",
    "rate_diff_aud_usd": "A 4.10% RBA cash rate versus a 3.50%-3.75% Fed target range keeps the rate differential supportive for AUD [7] [9].",
    "rate_diff_jpy_usd": "BoJ normalization still improves the JPY side of the rate-differential narrative against a neutral Fed [7] [14].",
    "risk_sentiment_aud": "With VIX at 19.49, the broad risk tone is balanced rather than clearly adverse or clearly risk-on, so the AUD sentiment factor is neutral [2].",
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
    "GC": "Gold stays constructive because the dollar softened and ETF flows remain positive, while the Hormuz-related energy shock still supports hedging demand. The signal is no longer amplified by a clearly defensive VIX level because spot volatility slipped back below 20, which keeps the setup bullish but not extreme.",
    "SI": "Silver retains only a marginally constructive stance because dollar weakness and gold ETF inflows still help, but the copper signal flipped lower on the day and removes an important industrial tailwind. With real yields flat and the growth narrative stable rather than re-accelerating, the contract is closer to a tactical upside lean than a full trend continuation.",
    "CL": "WTI crude remains bullish because the official EIA supply-shock backdrop is still severe and geopolitical risk stays elevated. The latest U.S. inventory build prevents a stronger classification, but the weaker dollar and persistent Hormuz disruption still leave the net balance positive.",
    "ES": "The S&P 500 remains bullish because a softer dollar, tighter credit spreads, and a falling VIX direction all improved the cross-asset backdrop. Even so, the VIX level itself only moved back into a balanced regime rather than a clearly complacent one, which argues for a moderate rather than aggressive bullish bias.",
    "NQ": "Nasdaq 100 keeps a bullish bias because semiconductor leadership strengthened further and Treasury volatility continued to fall, while the weaker dollar also helped duration-sensitive growth assets. The signal is healthier than earlier in the week, but flat real yields mean the move still lacks a fresh rates-driven acceleration tailwind.",
    "YM": "The Dow Jones contract is bullish because dollar weakness, tighter high-yield spreads, and a still-positive curve leave the cyclical large-cap backdrop more supportive. Stable rather than accelerating growth keeps the score in the middle bullish tier instead of the strongest category.",
    "RTY": "Russell 2000 becomes one of the stronger equity expressions because it benefits most from tighter credit spreads and a normalized curve. The balanced VIX regime is less of a headwind than before, so small caps now screen as a higher-conviction pro-cyclical setup than the other major U.S. index futures.",
    "6E": "Euro FX remains mildly bearish because a softer dollar is still outweighed by the ECB's easing bias, an unfavorable policy differential, and slowing euro-area growth momentum. The contract improved from a more hostile USD backdrop, but not enough to offset Europe-specific macro drag.",
    "6A": "The Australian dollar improves to a clearer bullish configuration because RBA policy remains supportive, China's PMI rebound still helps the regional growth proxy, and the broader market tone is no longer outright risk-off with VIX back below 20. The one notable offset is copper's daily decline, which tempers but does not overturn the positive macro mix.",
    "6J": "Japanese yen futures remain the highest-conviction setup because the contract combines BoJ normalization, a friendlier JPY rate-differential narrative, and ongoing dollar softness. Even though VIX fell back into a balanced rather than overtly defensive regime, the yen still has the cleanest macro alignment in the basket.",
}

futures_news = [
    {
        "headline": "US stocks rise and oil prices trim their gains on hopes for the ceasefire with Iran",
        "url": references["19"]["url"],
    },
    {
        "headline": "US crude oil inventories up by 0.7% for week ending April 3",
        "url": references["18"]["url"],
    },
]

currency_news = [
    {
        "headline": "Oil, Stocks Still Driving FX Markets as Ceasefire Hopes Push into EOW",
        "url": references["20"]["url"],
    },
    {
        "headline": "Eurozone HCOB Composite PMI above expectations: 50.7 in March",
        "url": references["16"]["url"],
    },
]

calendar_notes = [
    "Preferred ForexFactory calendar page access was blocked in-browser during this session, so the schedule below uses confirmed session catalysts and near-dated releases rather than claiming direct calendar extraction.",
    "April 9: U.S. weekly jobless claims and February core PCE-related market digestion remained in focus alongside the Atlanta Fed GDPNow refresh [3] [19].",
    "April 10: China inflation data and the U.S. CPI report are the next immediate macro catalysts for futures and FX positioning [15] [20].",
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

    lines: list[str] = []
    lines.append("# Matrix Futures Daily Bias Report")
    lines.append(f"**Date:** {date_label} | **Time:** {time_label} UTC")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Overall Market Bias: BULLISH")
    lines.append("")
    lines.append("Macro conditions on April 9 remained broadly constructive because the dollar weakened, credit spreads tightened, and both equity and Treasury volatility improved directionally. The regime is no longer clearly defensive after VIX slipped below 20, but it is not yet a full risk-on surge because growth merely stabilized, crude inventories still built, and Europe-specific macro data remain soft [1] [2] [3] [11] [18].")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Main Summary Table")
    lines.append("")
    lines.append("| Instrument | Name | Numeric Bias Score | Signal | Confidence | Approach | Mode | Hold |")
    lines.append("|------------|------|--------------------|--------|------------|----------|------|------|")
    for symbol in ["GC", "SI", "CL", "ES", "NQ", "YM", "RTY", "6E", "6A", "6J"]:
        data = results[symbol]
        lines.append(
            f"| {symbol} | {instrument_display[symbol]} | {signed_score(data['score'])} | {data['signal']} | {data['confidence']}/10 | {data['recommended_approach']} | {data['recommended_mode']} | {data['hold_expectation']} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Asset Class Summary")
    lines.append("")
    lines.append("| Asset Class | Bias | Key Driver |")
    lines.append("|-------------|------|------------|")
    lines.append(f"| Commodities | {asset_class_bias['COMMODITIES']} | Softer USD and continuing Hormuz-related supply stress keep the complex supported even after another bearish U.S. crude inventory build [1] [17] [18] |")
    lines.append(f"| Indices | {asset_class_bias['INDICES']} | Tighter credit spreads, falling VIX direction, and stronger semiconductors improved the risk backdrop [2] [4] [11] |")
    lines.append(f"| FX | {asset_class_bias['FX']} | Dollar weakness helps broadly, but policy divergence still favors JPY and AUD over EUR [1] [7] [8] [9] [14] |")
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
    for item in calendar_notes:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Brief News Summary: Futures")
    lines.append("")
    for item in futures_news:
        lines.append(f"- {item['headline']} | {item['url']}")
    lines.append("")
    lines.append("Futures headlines still revolve around two linked themes: crude remains underpinned by unresolved Strait of Hormuz disruption, while equity benchmarks continue to stabilize as ceasefire hopes reduce the probability of a deeper near-term growth shock [17] [18] [19].")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Brief News Summary: Currency")
    lines.append("")
    for item in currency_news:
        lines.append(f"- {item['headline']} | {item['url']}")
    lines.append("")
    lines.append("Currency headlines continue to emphasize a weaker dollar backdrop, a still-fragile USD/JPY pressure point, and persistent euro underperformance against the backdrop of softer euro-area activity [1] [16] [20].")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Key Macro Themes")
    lines.append("")
    lines.append("1. **The dollar remains a broad cross-asset tailwind** because DXY fell to 98.795, supporting commodities and non-USD FX [1].")
    lines.append("2. **Risk conditions improved without becoming euphoric** because VIX fell sharply to 19.49 and MOVE dropped to 74.0129, yet the growth narrative only held steady at 1.3% GDPNow [2] [3] [5].")
    lines.append("3. **Crude remains uniquely supported by supply stress** because EIA still describes severe Hormuz-related outages even as domestic inventories rose by 3.1 million barrels [17] [18].")
    lines.append("4. **Policy divergence still matters most in FX** because ECB easing bias contrasts with still-supportive RBA settings and the BoJ normalization story [8] [9] [14].")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Upcoming Catalysts")
    lines.append("")
    lines.append("### Imminent (< 1 Week)")
    lines.append("- U.S. CPI on April 10 [20]")
    lines.append("- China inflation data on April 10 [15]")
    lines.append("- Ongoing Strait of Hormuz and tanker-flow headlines [17] [19]")
    lines.append("")
    lines.append("### Near-Term (1-4 Weeks)")
    lines.append("- Federal Reserve meeting on April 30 [7]")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Data Quality")
    lines.append("")
    lines.append("- The preferred ForexFactory calendar page could not be opened directly in-browser because of access restrictions, so the calendar section uses fallback session catalysts and explicitly discloses that limitation.")
    lines.append("- Reuters access to the eurozone PMI article was restricted, so the euro-area growth factor used an accessible FXStreet fallback tied to the HCOB/S&P Global release [16].")
    lines.append("- FRED inputs are official but still slightly lagged relative to the live session; the model therefore uses the latest available official print for DFII10, HY OAS, and T10Y2Y [10] [11] [12].")
    lines.append(f"- Average confidence: {avg_conf:.1f}/10")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## References")
    lines.append("")
    for key in sorted(references, key=lambda x: int(x)):
        ref = references[key]
        lines.append(f"[{key}]: {ref['url']} \"{ref['title']}\"")
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
            "TradingView showed DXY at 98.795 and down 0.21% on the session, improving the backdrop for commodities and non-USD FX [1].",
            "Cboe VIX fell 7.37% to 19.49, moving the volatility regime back to balanced while leaving direction supportive for risk assets [2].",
            "FRED HY OAS tightened from 3.12 to 2.94 on the latest official print, improving the cross-asset credit backdrop [11].",
            "EIA still describes severe Hormuz-related supply disruption even as U.S. crude inventories rose by 3.1 million barrels [17] [18].",
        ],
        "data_quality": {
            "stale_sources": [
                "FRED DFII10 latest official observation used: 2026-04-08 [10]",
                "FRED HY OAS latest official observation used: 2026-04-08 [11]",
                "Preferred ForexFactory calendar page inaccessible in browser during this session",
            ],
            "fallbacks_used": [
                "FXStreet fallback for eurozone PMI after Reuters access restriction [16]",
                "Anadolu summary for the latest EIA crude inventory release [18]",
                "Session catalyst fallback notes for calendar context after ForexFactory access restriction",
            ],
            "overnight_changes": [
                "DXY down 0.21% on the day [1]",
                "VIX down 7.37% on the day [2]",
                "Copper down 0.29% on the day [6]",
            ],
        },
        "catalyst_proximity": {
            "imminent": [
                "U.S. CPI on April 10 [20]",
                "China inflation data on April 10 [15]",
                "Ongoing Strait of Hormuz and tanker-flow headlines [17] [19]",
            ],
            "near_term": [
                "Federal Reserve meeting on April 30 [7]",
            ],
            "background": [
                "Persistent Middle East energy disruption risk [17] [19]",
                "ECB easing bias amid softer euro-area growth [8] [16]",
                "BoJ normalization and post-hike RBA policy divergence [9] [14]",
            ],
        },
        "references": references,
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
        )
        + "\n",
        encoding="utf-8",
    )

    print(timestamp_json)
    print(latest_json)
    print(timestamp_md)
    print(latest_md)
    print(detail_json)


if __name__ == "__main__":
    main()
