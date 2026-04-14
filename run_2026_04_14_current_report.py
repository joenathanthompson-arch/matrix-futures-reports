from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path('/home/ubuntu/matrix-futures-reports')
BIAS_DIR = BASE_DIR / 'data' / 'bias_scores'
EXEC_DIR = BASE_DIR / 'data' / 'executive_summaries'
FACTOR_DIR = BASE_DIR / 'data' / 'factors'
REPORTS_DIR = BASE_DIR / 'reports'

for path in (BIAS_DIR, EXEC_DIR, FACTOR_DIR, REPORTS_DIR):
    path.mkdir(parents=True, exist_ok=True)

macro_inputs = {
    'fed_stance': {
        'value': 0,
        'label': 'Neutral hold',
        'source': 'CME FedWatch for 30 Apr 2026 showed approximately 0.0% ease, 99.5% no change, and 0.5% hike, so the Fed stance remains a neutral hold.'
    },
    'real_yields': {
        'value': 0,
        'label': 'Flat',
        'source': 'FRED DFII10 showed 1.92 on 2026-04-13, versus 1.95 on 2026-04-10. The 3 bps decline remains inside the methodology\'s ±5 bps flat band.'
    },
    'usd_dxy': {
        'value': 1,
        'label': 'Weak/falling',
        'source': 'TradingView DXY was 98.132, down 0.241 (-0.24%) on the day and down 0.94% over five days, which keeps the dollar factor in weak/falling territory.'
    },
    'risk_mood': {
        'value': 0,
        'label': 'Balanced',
        'source': 'Cboe VIX spot was 18.36, which remains inside the methodology\'s balanced 15-20 band rather than a high-stress regime.'
    },
    'vix_direction': {
        'value': 1,
        'label': 'Falling',
        'source': 'Cboe VIX was down 3.97% (-0.76) from the prior close, so volatility direction is classified as falling.'
    },
    'growth_narrative': {
        'value': 1,
        'label': 'Slowing',
        'source': 'Atlanta Fed GDPNow remained at 1.3% for 2026:Q1, preserving a slowing U.S. growth narrative.'
    },
    'oil_supply_shock': {
        'value': 1,
        'label': 'Tightening',
        'source': 'The EIA\'s recent outlook still treats the Hormuz closure and related outages as key oil-market drivers, so the supply-shock classification remains tightening.'
    },
    'oil_inventories': {
        'value': -1,
        'label': 'Building',
        'source': 'The latest EIA weekly petroleum summary for the week ended 2026-04-03 reported a 3.1 million barrel rise in U.S. commercial crude inventories, which is a bearish inventory build.'
    },
    'gold_etf_flows': {
        'value': -1,
        'label': 'Outflowing',
        'source': 'The World Gold Council reported record March gold-ETF outflows totaling about US$12 billion, so the ETF-flow signal remains negative.'
    },
    'credit_spreads': {
        'value': -1,
        'label': 'Widening',
        'source': 'FRED high-yield OAS showed 2.95 on 2026-04-13, up slightly from 2.94 on the prior official reference, which classifies as widening credit spreads.'
    },
    'sox': {
        'value': 1,
        'label': 'Rising',
        'source': 'The latest repository-verified TradingView check showed SOX still rising on both daily and five-day horizons, so the semiconductor signal remains positive.'
    },
    'move_index': {
        'value': -1,
        'label': 'Rising',
        'source': 'The latest repository-verified TradingView check showed MOVE rising on the day, so the rates-volatility factor remains negative for Nasdaq under the methodology.'
    },
    'yield_curve_2s10s': {
        'value': -1,
        'label': 'Flattening',
        'source': 'FRED T10Y2Y printed 0.50 on 2026-04-14 versus 0.52 on 2026-04-13, which classifies the curve as flattening on the latest official update.'
    },
    'copper': {
        'value': 0,
        'label': 'Unverified / flat',
        'source': 'A clean live copper source was not fully re-verified in-session, so the copper factor is conservatively scored flat rather than guessed.'
    },
    'ecb_stance': {
        'value': 1,
        'label': 'Mildly hawkish hold',
        'source': 'The official ECB page was not cleanly extractable in-browser, but the latest available official ECB communication and repository backdrop still support a mildly hawkish hold classification rather than an easing signal.'
    },
    'rate_diff_eur_usd': {
        'value': 0,
        'label': 'Stable',
        'source': 'With the Fed neutral and the ECB on hold rather than actively easing or hiking in today\'s verified set, the near-term EUR-USD policy differential is best treated as stable.'
    },
    'eurozone_growth': {
        'value': -1,
        'label': 'Slowing / downgraded',
        'source': 'The latest repository-verified ECB growth backdrop still reflects a downgraded euro-area outlook, so eurozone growth remains classified as slowing.'
    },
    'rba_stance': {
        'value': 1,
        'label': 'Hawkish/tightening',
        'source': 'The RBA\'s 17 March 2026 decision raised the cash rate target by 25 bps to 4.10% and highlighted upside inflation risks, so the RBA stance remains hawkish.'
    },
    'rate_diff_aud_usd': {
        'value': 1,
        'label': 'Widening vs USD',
        'source': 'A hawkish 4.10% RBA backdrop against a neutral Fed still leaves the AUD-USD short-rate differential supportive for AUD.'
    },
    'risk_sentiment_aud': {
        'value': 0,
        'label': 'Neutral',
        'source': 'The broad volatility regime is balanced rather than decisively risk-on or risk-off, so the AUD-specific sentiment factor remains neutral.'
    },
    'china_growth': {
        'value': 1,
        'label': 'Accelerating / expanding',
        'source': 'China manufacturing PMI remained above 50 in March 2026, keeping the China-growth factor in positive territory for AUD.'
    },
    'boj_stance': {
        'value': 0,
        'label': 'Neutral hold',
        'source': 'The 19 March 2026 BoJ statement kept the overnight call rate at around 0.75%, so the safer current classification is neutral hold.'
    },
    'rate_diff_jpy_usd': {
        'value': 1,
        'label': 'Widening vs USD',
        'source': 'A neutral Fed combined with Japan\'s post-normalization backdrop still keeps the policy-divergence story favorable for yen futures.'
    },
    'geopolitical_risk': {
        'value': 1,
        'label': 'Elevated',
        'source': 'The EIA continues to frame Hormuz-related disruption as a live oil-market driver, so geopolitical risk for crude remains elevated.'
    },
}

instrument_configs = {
    'GC': {'instrument': 'Gold', 'factors': {'fed_stance': 1, 'real_yields': 2, 'usd_dxy': 1, 'risk_mood': 1, 'growth_narrative': 1, 'oil_supply_shock': 1, 'gold_etf_flows': 1}},
    'SI': {'instrument': 'Silver', 'factors': {'fed_stance': 1, 'real_yields': 1, 'usd_dxy': 1, 'risk_mood': 1, 'growth_narrative': 1, 'copper': 1, 'gold_etf_flows': 1}},
    'CL': {'instrument': 'Crude Oil', 'factors': {'oil_supply_shock': 2, 'oil_inventories': 1, 'growth_narrative': 2, 'geopolitical_risk': 1, 'usd_dxy': 1}},
    'ES': {'instrument': 'S&P 500', 'factors': {'fed_stance': 1, 'real_yields': 2, 'usd_dxy': 1, 'risk_mood': 1, 'growth_narrative': 1, 'credit_spreads': 1, 'vix_direction': 1}},
    'NQ': {'instrument': 'Nasdaq 100', 'factors': {'fed_stance': 1, 'real_yields': 2, 'usd_dxy': 1, 'risk_mood': 1, 'growth_narrative': 1, 'sox': 1, 'move_index': 1}},
    'YM': {'instrument': 'Dow Jones', 'factors': {'fed_stance': 1, 'real_yields': 1, 'usd_dxy': 1, 'risk_mood': 1, 'growth_narrative': 2, 'credit_spreads': 1, 'yield_curve_2s10s': 1}},
    'RTY': {'instrument': 'Russell 2000', 'factors': {'fed_stance': 1, 'real_yields': 1, 'usd_dxy': 1, 'risk_mood': 1, 'growth_narrative': 2, 'credit_spreads': 2, 'yield_curve_2s10s': 1}},
    '6E': {'instrument': 'Euro', 'factors': {'fed_stance': 1, 'ecb_stance': 1, 'rate_diff_eur_usd': 2, 'usd_dxy': 1, 'risk_mood': 1, 'eurozone_growth': 1}},
    '6A': {'instrument': 'Australian Dollar', 'factors': {'fed_stance': 1, 'rba_stance': 1, 'rate_diff_aud_usd': 1, 'usd_dxy': 1, 'risk_sentiment_aud': 2, 'china_growth': 2, 'copper': 1}},
    '6J': {'instrument': 'Japanese Yen', 'factors': {'fed_stance': 1, 'boj_stance': 2, 'rate_diff_jpy_usd': 2, 'usd_dxy': 1, 'risk_mood': 1}},
}

references = {
    '1': {'title': 'TradingView DXY page', 'url': 'https://www.tradingview.com/symbols/TVC-DXY/'},
    '2': {'title': 'Cboe VIX page', 'url': 'https://www.cboe.com/tradable-products/vix/'},
    '3': {'title': 'Atlanta Fed GDPNow', 'url': 'https://www.atlantafed.org/cqer/research/gdpnow'},
    '4': {'title': 'EIA Weekly Petroleum Status Report', 'url': 'https://www.eia.gov/petroleum/supply/weekly/'},
    '5': {'title': 'EIA Hormuz closure press release', 'url': 'https://www.eia.gov/pressroom/releases/press586.php'},
    '6': {'title': 'World Gold Council March 2026 ETF flows', 'url': 'https://www.gold.org/goldhub/research/gold-etfs-holdings-and-flows/2026/04'},
    '7': {'title': 'FRED DFII10', 'url': 'https://fred.stlouisfed.org/series/DFII10'},
    '8': {'title': 'FRED BAMLH0A0HYM2', 'url': 'https://fred.stlouisfed.org/series/BAMLH0A0HYM2'},
    '9': {'title': 'FRED T10Y2Y', 'url': 'https://fred.stlouisfed.org/series/T10Y2Y'},
    '10': {'title': 'TradingView MOVE page', 'url': 'https://www.tradingview.com/symbols/TVC-MOVE/'},
    '11': {'title': 'China PMI source context', 'url': 'http://english.scio.gov.cn/m/pressroom/2026-03/31/content_118411839.html'},
    '12': {'title': 'RBA monetary policy page', 'url': 'https://www.rba.gov.au/monetary-policy/'},
    '13': {'title': 'Bank of Japan Statement on Monetary Policy, March 19 2026', 'url': 'https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2026/k260319a.pdf'},
    '14': {'title': 'ECB Economic Bulletin Issue 2, 2026', 'url': 'https://www.ecb.europa.eu/pub/pdf/ecbu/eb202602.en.pdf'},
}


def signal_from_score(score: int) -> str:
    if score >= 5:
        return 'STRONG_BULLISH'
    if score >= 3:
        return 'BULLISH'
    if score >= 1:
        return 'SLIGHT_BULLISH'
    if score == 0:
        return 'NEUTRAL'
    if score >= -2:
        return 'SLIGHT_BEARISH'
    if score >= -4:
        return 'BEARISH'
    return 'STRONG_BEARISH'


def confidence_from_score(symbol: str, score: int) -> int:
    abs_score = abs(score)
    if abs_score >= 5:
        conf = 7
    elif abs_score >= 3:
        conf = 6
    elif abs_score >= 2:
        conf = 5
    else:
        conf = 5
    if symbol in {'ES', 'NQ', 'YM', 'RTY', 'SI'}:
        conf -= 1
    if symbol in {'6E'}:
        conf = max(conf, 5)
    return max(4, min(9, conf))


def strategy_from_score(symbol: str, score: int) -> tuple[str, str, str]:
    abs_score = abs(score)
    if abs_score >= 5:
        return 'TREND_FOLLOW', 'SWING', '2-5 days'
    if abs_score >= 3:
        return 'TREND_FOLLOW', 'SWING', '1-2 days'
    if abs_score >= 1:
        return 'IB_BREAKOUT', 'INTRADAY', 'session'
    return 'RANGE_TRADE', 'INTRADAY', 'session'


def class_bias(avg_score: float) -> str:
    return signal_from_score(round(avg_score))


def signed(value: int) -> str:
    return f'{value:+d}'


def calculate_results() -> tuple[dict, dict]:
    results = {}
    detail = {}
    for symbol, config in instrument_configs.items():
        total = 0
        factors = []
        for factor, weight in config['factors'].items():
            raw = macro_inputs[factor]['value']
            weighted = raw * weight
            total += weighted
            factors.append({
                'factor': factor,
                'raw': raw,
                'weight': weight,
                'weighted': weighted,
                'source': macro_inputs[factor]['source'],
            })
        approach, mode, hold = strategy_from_score(symbol, total)
        results[symbol] = {
            'score': total,
            'signal': signal_from_score(total),
            'confidence': confidence_from_score(symbol, total),
            'recommended_approach': approach,
            'recommended_mode': mode,
            'hold_expectation': hold,
        }
        detail[symbol] = {
            'instrument': config['instrument'],
            'raw_weighted_score': total,
            'factors': factors,
        }
    return results, detail


def build_markdown(now: datetime, results: dict, asset_class_bias: dict) -> str:
    avg_conf = sum(item['confidence'] for item in results.values()) / len(results)
    top = sorted(results.items(), key=lambda kv: (kv[1]['score'], kv[1]['confidence']), reverse=True)[:3]
    ordered = ['GC', 'SI', 'CL', 'ES', 'NQ', 'YM', 'RTY', '6E', '6A', '6J']
    paragraphs = {
        'GC': 'Gold remains **slight bullish**. The weaker dollar and slowing U.S. growth backdrop help, while real yields are no longer falling enough to add fresh upside and record March ETF outflows continue to cap conviction.',
        'SI': 'Silver is also **slight bullish**. USD weakness and softer U.S. growth are supportive, but the model deliberately keeps copper neutral because a clean live source was not fully re-verified in-session, and ETF-flow data remains a drag.',
        'CL': 'WTI crude remains the clearest **strong bullish** signal in the basket. The EIA still frames Hormuz-related disruption as a meaningful supply constraint, geopolitical risk remains elevated, and dollar weakness offsets the bearish inventory build.',
        'ES': 'The S&P 500 remains **slight bullish**. Falling VIX direction and a weaker dollar help, but wider credit spreads keep the index sleeve from moving into a higher-conviction bullish regime.',
        'NQ': 'Nasdaq futures remain **slight bullish**. Semiconductor leadership is still supportive and the dollar is weak, but rising MOVE says rates volatility is still a headwind for growth stocks.',
        'YM': 'Dow futures are **slight bullish** rather than outright bullish on the latest official curve update. The softer dollar and slowing-growth policy backdrop help, but widening credit spreads and a flattening 2s10s curve reduce conviction.',
        'RTY': 'Russell 2000 shifts to **neutral** in this run. The weaker dollar and softer growth backdrop help, but Russell\'s double-weighted exposure to wider credit spreads plus a flatter curve offsets those positives.',
        '6E': 'Euro futures remain **slight bullish**. The weaker dollar and mildly hawkish ECB hold help, but the near-term policy differential remains stable and euro-area growth stays soft.',
        '6A': 'Australian dollar futures remain **bullish**. The AUD continues to benefit from the hawkish RBA stance, a supportive rate differential versus the Fed, an expansionary China PMI backdrop, and broad USD weakness.',
        '6J': 'Japanese yen futures remain **bullish**. The policy-divergence story versus a neutral Fed and a softer U.S. dollar continue to support JPY, even though the immediate BoJ stance is kept at neutral hold in this run.',
    }

    lines = []
    lines.append('# Matrix Futures Daily Bias Report')
    lines.append(f"**Date:** {now.strftime('%B %d, %Y')} | **Time:** {now.strftime('%H:%M')} UTC")
    lines.append('')
    lines.append('## Overall Market Bias')
    lines.append('')
    lines.append('The broad backdrop remains **constructive but selective**. The U.S. dollar is still weak, the Fed remains on hold, China\'s manufacturing backdrop stays expansionary, and the RBA continues to run a hawkish stance, which supports crude oil and selected G10 FX. At the same time, record March gold-ETF outflows, slightly wider credit spreads, and a flatter 2s10s curve limit conviction in precious metals and small-cap equities.')
    lines.append('')
    lines.append('## Asset Class Summary')
    lines.append('')
    lines.append('| Asset Class | Bias | Key Driver |')
    lines.append('|-------------|------|------------|')
    lines.append(f"| Commodities | {asset_class_bias['COMMODITIES']} | Oil remains structurally supported by Hormuz disruption risk, while gold and silver are capped by negative ETF-flow data. |")
    lines.append(f"| Indices | {asset_class_bias['INDICES']} | A softer dollar and falling VIX direction help, but widening credit spreads and a flatter 2s10s curve restrain conviction. |")
    lines.append(f"| FX | {asset_class_bias['FX']} | Dollar weakness combines with hawkish RBA policy and a favorable yen divergence story to keep FX constructive overall. |")
    lines.append('')
    lines.append('## Highest Conviction Signals')
    lines.append('')
    lines.append('| Instrument | Score | Signal | Confidence |')
    lines.append('|------------|-------|--------|------------|')
    for symbol, item in top:
        lines.append(f"| {symbol} | {signed(item['score'])} | {item['signal']} | {item['confidence']}/10 |")
    lines.append('')
    lines.append('## Full Instrument Breakdown')
    lines.append('')
    for symbol in ordered:
        item = results[symbol]
        lines.append(f"### {symbol} ({instrument_configs[symbol]['instrument']}): {signed(item['score'])} {item['signal']} ({item['confidence']}/10)")
        lines.append(f"**Approach:** {item['recommended_approach']} | **Mode:** {item['recommended_mode']} | **Hold:** {item['hold_expectation']}")
        lines.append(paragraphs[symbol])
        lines.append('')
    lines.append('## Key Macro Themes')
    lines.append('')
    lines.append('1. **The dollar remains the main cross-asset tailwind** because DXY is still below 98.2 and lower on both a daily and five-day basis.')
    lines.append('2. **Volatility conditions improved only partially** because VIX fell on the day, but credit spreads widened slightly and the 2s10s curve flattened on the latest official print.')
    lines.append('3. **Oil keeps the strongest macro support** because inventories built, yet the EIA still frames Hormuz-related disruption as a meaningful supply driver.')
    lines.append('')
    lines.append('## Upcoming Catalysts')
    lines.append('')
    lines.append('### Imminent (< 1 Week)')
    lines.append('- Next EIA Weekly Petroleum Status Report due April 15, 2026')
    lines.append('- Any fresh Strait of Hormuz disruption headlines')
    lines.append('')
    lines.append('### Near-Term (1-4 Weeks)')
    lines.append('- Next Atlanta Fed GDPNow update scheduled for April 21, 2026')
    lines.append('- Federal Reserve meeting on April 30, 2026')
    lines.append('')
    lines.append('## Data Quality')
    lines.append(f'- Average confidence: {avg_conf:.1f}/10')
    lines.append('- Official FRED series were used for DFII10, HY OAS, and T10Y2Y; these are authoritative but can lag live market feeds by one business day or more.')
    lines.append('- ECB stance and eurozone-growth context were carried from the latest repository-verified official materials because the live ECB page did not render cleanly in-session.')
    lines.append('- Copper was scored flat because a clean live source was not fully re-verified in-session.')
    lines.append('')
    lines.append('## References')
    lines.append('')
    for key, ref in references.items():
        lines.append(f"- [{key}] {ref['title']}: {ref['url']}")
    lines.append('')
    lines.append('**End of Report**')
    return '\n'.join(lines) + '\n'


def main() -> None:
    now = datetime.now(timezone.utc).replace(microsecond=0)
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H%M')
    iso_str = now.isoformat().replace('+00:00', 'Z')

    results, detail = calculate_results()
    asset_class_bias = {
        'COMMODITIES': class_bias(sum(results[s]['score'] for s in ['GC', 'SI', 'CL']) / 3),
        'INDICES': class_bias(sum(results[s]['score'] for s in ['ES', 'NQ', 'YM', 'RTY']) / 4),
        'FX': class_bias(sum(results[s]['score'] for s in ['6E', '6A', '6J']) / 3),
    }

    output = {
        'date': date_str,
        'generated_at': iso_str,
        'methodology_version': '3.0_STRATEGY',
        'scores': results,
        'asset_class_bias': asset_class_bias,
        'key_drivers': [
            'DXY traded at 98.132 and was down 0.24% on the day, preserving a weaker-USD backdrop across metals, equities, and G10 FX [1].',
            'VIX printed 18.36 and fell 3.97%, leaving the regime balanced by level but supportive for equities through falling volatility [2].',
            'Atlanta Fed GDPNow stood at 1.3% for 2026:Q1, implying a softer U.S. growth backdrop that helps defensives but complicates domestic cyclicals [3].',
            'The EIA still treats Hormuz-related disruption as a material bullish supply shock for oil, even though the latest weekly inventory data showed a 3.1 million barrel crude build [4] [5].',
            'FRED HY OAS widened slightly to 2.95 and the 2s10s curve slipped to 0.50, which restrains index conviction despite the softer dollar [8] [9].',
        ],
        'data_quality': {
            'stale_sources': [
                'FRED DFII10 latest official observation used: 2026-04-13 [7]',
                'FRED BAMLH0A0HYM2 latest official observation used: 2026-04-13 [8]',
            ],
            'fallbacks_used': [
                'Fed stance retained from same-day repository-verified FedWatch extraction because the CME page did not expose the probability row cleanly in markdown',
                'ECB stance and eurozone growth backdrop retained from the latest repository-verified official materials because the live ECB page did not render cleanly in-session [14]',
                'Copper scored flat because a clean live source was not fully re-verified in-session',
                'SOX and MOVE retained from latest repository-verified same-day checks rather than re-opening both live pages in this run [10]',
            ],
            'uncertainties': [
                'Official FRED series are authoritative but not fully real-time market feeds',
                'Japan and Australia policy factors were carried from the latest official central-bank decisions because no newer policy meeting has superseded them [12] [13]',
            ],
        },
        'catalyst_proximity': {
            'imminent': [
                'Next EIA Weekly Petroleum Status Report due April 15, 2026 [4]',
                'Any fresh Strait of Hormuz flow or outage update [5]',
            ],
            'near_term': [
                'Next Atlanta Fed GDPNow update scheduled for April 21, 2026 [3]',
                'Federal Reserve meeting on April 30, 2026',
            ],
            'background': [
                'Record March gold ETF outflows remain a drag on precious metals [6]',
                'China manufacturing remained in expansion in March, supporting AUD and commodity-linked risk [11]',
            ],
        },
        'references': references,
    }

    timestamp_json = BIAS_DIR / f'{date_str}_{time_str}.json'
    latest_json = BIAS_DIR / 'latest.json'
    timestamp_md = EXEC_DIR / f'{date_str}_{time_str}.md'
    latest_md = EXEC_DIR / 'latest.md'
    detail_json = FACTOR_DIR / f'{date_str}_{time_str}_scoring_detail.json'
    csv_path = REPORTS_DIR / f'{date_str}_Bias-Scores.csv'

    timestamp_json.write_text(json.dumps(output, indent=2), encoding='utf-8')
    latest_json.write_text(json.dumps(output, indent=2), encoding='utf-8')
    markdown = build_markdown(now, results, asset_class_bias)
    timestamp_md.write_text(markdown, encoding='utf-8')
    latest_md.write_text(markdown, encoding='utf-8')
    detail_json.write_text(json.dumps({
        'date': date_str,
        'generated_at': iso_str,
        'macro_inputs': macro_inputs,
        'instrument_scoring': detail,
    }, indent=2), encoding='utf-8')

    with csv_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Ticker', 'Instrument', 'Numeric Bias', 'Signal', 'Confidence'])
        for symbol in ['GC', 'SI', 'CL', 'ES', 'NQ', 'YM', 'RTY', '6E', '6A', '6J']:
            row = results[symbol]
            writer.writerow([symbol, instrument_configs[symbol]['instrument'], signed(row['score']), row['signal'], row['confidence']])

    print(json.dumps({
        'timestamp_json': str(timestamp_json),
        'latest_json': str(latest_json),
        'timestamp_md': str(timestamp_md),
        'latest_md': str(latest_md),
        'detail_json': str(detail_json),
        'csv_path': str(csv_path),
        'scores': {k: v['score'] for k, v in results.items()},
        'asset_class_bias': asset_class_bias,
    }, indent=2))


if __name__ == '__main__':
    main()
