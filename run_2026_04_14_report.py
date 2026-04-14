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
        'source': 'FRED DFII10 showed 1.95 on 2026-04-10, and the latest official move remains too small to qualify as a directional real-yield shift under the methodology.'
    },
    'usd_dxy': {
        'value': 1,
        'label': 'Weak/falling',
        'source': 'TradingView DXY was 98.079, down 0.30% on the day and down 0.99% over five days, which keeps the dollar factor in weak/falling territory.'
    },
    'risk_mood': {
        'value': 0,
        'label': 'Balanced',
        'source': 'Cboe VIX spot was 18.31, which remains inside the methodology\'s balanced 15-20 band rather than a high-stress regime.'
    },
    'vix_direction': {
        'value': 1,
        'label': 'Falling',
        'source': 'The VIX was down 4.24% (-0.81) from the prior close, so volatility direction is classified as falling.'
    },
    'growth_narrative': {
        'value': 1,
        'label': 'Slowing',
        'source': 'Atlanta Fed GDPNow remained at 1.3% for 2026:Q1 after having been higher in the prior repository baseline, so the U.S. growth narrative remains slowing.'
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
        'source': 'FRED high-yield OAS moved from 2.90 to 2.94 on the latest official print, which classifies as widening credit spreads in this run.'
    },
    'sox': {
        'value': 1,
        'label': 'Rising',
        'source': 'TradingView showed SOX at 9,039.52, up 1.68% on the day and 6.37% over five days, preserving a rising semiconductor signal.'
    },
    'move_index': {
        'value': -1,
        'label': 'Rising',
        'source': 'TradingView showed MOVE at 74.4185, up 3.14% on the day, so the rates-volatility factor is rising and therefore negative for Nasdaq under the methodology.'
    },
    'yield_curve_2s10s': {
        'value': 1,
        'label': 'Steepening',
        'source': 'FRED T10Y2Y increased to 0.52 on 2026-04-13 from 0.50 on 2026-04-10, which classifies the curve as steepening.'
    },
    'copper': {
        'value': 0,
        'label': 'Unverified / flat',
        'source': 'Live copper pages remained incomplete in this session, so the copper factor is conservatively scored flat rather than guessed.'
    },
    'ecb_stance': {
        'value': 1,
        'label': 'Mildly hawkish hold',
        'source': 'The ECB page was not cleanly extractable in-browser, but the latest available official ECB communication and repository backdrop still support a mildly hawkish hold classification rather than an easing signal.'
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
        'label': 'Improving but slowing',
        'source': 'China manufacturing PMI was 50.8 in March 2026, down from 52.1 in February but still above 50, which supports a conservative positive classification.'
    },
    'boj_stance': {
        'value': 0,
        'label': 'Neutral hold',
        'source': 'The 19 March 2026 BoJ statement kept the uncollateralized overnight call rate at around 0.75% and described financial conditions as accommodative, so the safer classification for this run is neutral hold.'
    },
    'rate_diff_jpy_usd': {
        'value': 1,
        'label': 'Improving for JPY',
        'source': 'A neutral Fed combined with the post-normalization BoJ backdrop still keeps the policy-divergence story favorable for yen futures.'
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
    if abs_score >= 6:
        conf = 8
    elif abs_score >= 4:
        conf = 7
    elif abs_score >= 2:
        conf = 6
    else:
        conf = 5
    if symbol in {'GC', 'SI', 'ES', 'NQ', 'YM', 'RTY'}:
        conf -= 1
    return max(4, min(9, conf))


def strategy_from_score(symbol: str, score: int) -> tuple[str, str, str]:
    abs_score = abs(score)
    if abs_score >= 5:
        if symbol in {'GC', 'SI', 'CL', '6E', '6A', '6J'}:
            return 'TREND_FOLLOW', 'SWING', '2-5 days'
        return 'TREND_FOLLOW', 'SWING', '1-2 days'
    if abs_score >= 3:
        return 'TREND_FOLLOW', 'SWING', '1-2 days'
    if abs_score >= 1:
        return 'IB_BREAKOUT', 'INTRADAY', 'session'
    return 'RANGE_TRADE', 'INTRADAY', 'session'


def class_bias(avg_score: float) -> str:
    rounded = round(avg_score)
    return signal_from_score(rounded)


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
    top = sorted(results.items(), key=lambda kv: (kv[1]['confidence'], kv[1]['score']), reverse=True)[:3]
    lines = []
    lines.append('# Matrix Futures Daily Bias Report')
    lines.append(f"**Date:** {now.strftime('%B %d, %Y')} | **Time:** {now.strftime('%H:%M')} UTC")
    lines.append('')
    lines.append('## Overall Market Bias')
    lines.append('')
    lines.append('The broad backdrop remains **constructive but uneven**. The U.S. dollar is still weak, the Fed is effectively on hold, China manufacturing remains above 50, and the RBA continues to run a hawkish stance, which supports commodities ex-gold, selected equities, and pro-cyclical FX. At the same time, record March gold-ETF outflows, widening credit spreads, rising MOVE, and a still-soft euro-area growth backdrop limit conviction outside crude oil and the strongest non-USD currency trades.')
    lines.append('')
    lines.append('## Main Summary Table')
    lines.append('')
    lines.append('| Instrument | Name | Numeric Bias Score | Signal | Confidence | Approach | Mode | Hold |')
    lines.append('|------------|------|--------------------|--------|------------|----------|------|------|')
    ordered = ['GC', 'SI', 'CL', 'ES', 'NQ', 'YM', 'RTY', '6E', '6A', '6J']
    for symbol in ordered:
        item = results[symbol]
        lines.append(f"| {symbol} | {instrument_configs[symbol]['instrument']} | {signed(item['score'])} | {item['signal']} | {item['confidence']}/10 | {item['recommended_approach']} | {item['recommended_mode']} | {item['hold_expectation']} |")
    lines.append('')
    lines.append('## Asset Class Summary')
    lines.append('')
    lines.append('| Asset Class | Bias | Interpretation |')
    lines.append('|-------------|------|----------------|')
    lines.append(f"| Commodities | {asset_class_bias['COMMODITIES']} | Oil remains structurally supported by the Hormuz disruption backdrop, while precious metals are capped by negative ETF-flow data. |")
    lines.append(f"| Indices | {asset_class_bias['INDICES']} | A softer dollar and falling VIX direction help, but widening credit spreads and higher MOVE keep the index sleeve from reaching stronger conviction. |")
    lines.append(f"| FX | {asset_class_bias['FX']} | The weaker dollar combines with hawkish RBA policy and a still-favorable JPY divergence story to keep FX the strongest aggregate sleeve. |")
    lines.append('')
    lines.append('## Highest Conviction Signals')
    lines.append('')
    lines.append('| Instrument | Score | Signal | Confidence |')
    lines.append('|------------|-------|--------|------------|')
    for symbol, item in top:
        lines.append(f"| {symbol} | {signed(item['score'])} | {item['signal']} | {item['confidence']}/10 |")
    lines.append('')
    lines.append('## Economic Calendar')
    lines.append('')
    lines.append('The preferred ForexFactory calendar could not be cleanly accessed in this environment, so the session timetable below uses an accessible fallback and should be cross-checked on ForexFactory before execution.')
    lines.append('')
    lines.append('| Time (UTC) | Region | Event | Source |')
    lines.append('|------------|--------|-------|--------|')
    lines.append('| 04:30 | JPY | Industrial Production m/m (final) | https://www.actionforex.com/economic-calendar/636584-eco-data-4-14-26-2/ |')
    lines.append('| 10:00 | USD | NFIB Business Optimism Index | https://www.actionforex.com/economic-calendar/636584-eco-data-4-14-26-2/ |')
    lines.append('| 12:30 | USD | PPI m/m and PPI y/y | https://www.actionforex.com/economic-calendar/636584-eco-data-4-14-26-2/ |')
    lines.append('')
    lines.append('## News Summary')
    lines.append('')
    lines.append('### Futures')
    lines.append('')
    lines.append('- Hormuz closure and related production outages remain key drivers in the latest EIA outlook | https://www.eia.gov/pressroom/releases/press586.php')
    lines.append('- Record March gold-ETF outflows offset otherwise supportive macro conditions for bullion | https://www.gold.org/goldhub/research/gold-etfs-holdings-and-flows/2026/04')
    lines.append('')
    lines.append('### Currency')
    lines.append('')
    lines.append('- China manufacturing PMI stayed in expansion at 50.8 in March, though momentum cooled from February | https://tradingeconomics.com/china/manufacturing-pmi')
    lines.append('- The RBA raised the cash rate target to 4.10% in March and continued to emphasize upside inflation risks | https://www.rba.gov.au/media-releases/2026/mr-26-08.html')
    lines.append('')
    lines.append('## Detailed Instrument Analysis')
    lines.append('')
    paragraphs = {
        'GC': 'Gold remains only slight bullish. The weaker dollar, slowing U.S. growth impulse, and persistent oil-supply-risk backdrop are supportive, but those positives are offset by record March ETF outflows and the absence of a fresh drop in real yields.',
        'SI': 'Silver also screens slight bullish. USD weakness and the softer U.S. growth narrative help, but the complex is capped by negative ETF-flow data and by the decision to keep copper neutral until a fully readable live source is recovered.',
        'CL': 'WTI crude remains the clearest high-conviction long in this run. The official EIA backdrop still centers on the Hormuz disruption, geopolitical risk remains elevated, and a softer dollar adds support even after the latest inventory build.',
        'ES': 'The S&P 500 improves modestly to slight bullish. A softer dollar, a slowing-growth policy backdrop, and a falling VIX direction are supportive, but widening credit spreads keep the signal from upgrading into the stronger part of the bullish range.',
        'NQ': 'Nasdaq futures remain constructive but not high-conviction. Semiconductor leadership is positive and the dollar remains weak, yet rising MOVE says rates volatility is no longer helping growth stocks the way it was in the prior report.',
        'YM': 'Dow futures stay bullish because the steepening curve and softer dollar more than offset the drag from wider credit spreads. The score is stronger than ES because the Dow benefits more directly from the curve signal.',
        'RTY': 'Russell 2000 remains slight bullish. The small-cap basket benefits from the weaker dollar, slowing-growth backdrop, and a steeper curve, but widening in high-yield spreads prevents a full bullish upgrade.',
        '6E': 'Euro futures are only slight bullish. The weaker dollar and mildly hawkish ECB hold help, but the near-term policy differential is still stable rather than improving and the euro-area growth backdrop remains soft.',
        '6A': 'Australian dollar futures remain strongly bullish. The AUD continues to benefit from the hawkish RBA backdrop, a supportive rate differential versus the Fed, a still-expansionary China PMI, and broad USD weakness, while copper was intentionally left neutral to keep the score conservative.',
        '6J': 'Japanese yen futures stay bullish. The ongoing policy-divergence narrative versus a neutral Fed combines with dollar weakness to support JPY, even though the immediate BoJ decision itself is classified conservatively as a neutral hold in this run.',
    }
    for symbol in ordered:
        item = results[symbol]
        lines.append(f"### {symbol} — {instrument_configs[symbol]['instrument']}")
        lines.append('')
        lines.append(f"**Final Bias Score:** {signed(item['score'])} ({item['signal']})")
        lines.append('')
        lines.append(f"**Approach:** {item['recommended_approach']} | **Mode:** {item['recommended_mode']} | **Hold:** {item['hold_expectation']}")
        lines.append('')
        lines.append(paragraphs[symbol])
        lines.append('')
    lines.append('## Key Macro Themes')
    lines.append('')
    lines.append('1. **The dollar remains the main cross-asset tailwind** because DXY is still below 98.1 and falling on both a daily and five-day basis.')
    lines.append('2. **Volatility conditions improved only at the margin** because VIX fell on the day, but MOVE rose and credit spreads widened.')
    lines.append('3. **Oil keeps its strongest macro support** because inventories built, yet the EIA still frames Hormuz-related disruption as a meaningful supply driver.')
    lines.append('')
    lines.append('## Upcoming Catalysts')
    lines.append('')
    lines.append('### Imminent (< 1 Week)')
    lines.append('- U.S. PPI and NFIB releases on April 14, 2026')
    lines.append('- Any revision to the Hormuz outage narrative in oil markets')
    lines.append('')
    lines.append('### Near-Term (1-4 Weeks)')
    lines.append('- Next Atlanta Fed GDPNow refresh scheduled for April 21, 2026')
    lines.append('- Federal Reserve meeting on April 30, 2026')
    lines.append('')
    lines.append('## Data Quality and Verification Notes')
    lines.append('')
    lines.append('| Area | Status | Note |')
    lines.append('|------|--------|------|')
    lines.append('| Copper | Manual verification needed | The live copper page was blocked or incomplete, so the factor was scored flat rather than guessed. |')
    lines.append('| ECB stance | Partially carried | The official ECB page did not render cleanly in-browser, so the repository\'s latest verified policy backdrop was retained. |')
    lines.append('| FRED series | Official but lagged | DFII10, HY OAS, and T10Y2Y use the latest official observations, which can lag live market moves. |')
    lines.append(f'| Average confidence | Current run | {avg_conf:.1f}/10 |')
    lines.append('')
    lines.append('**End of Report**')
    lines.append('')
    return '\n'.join(lines)


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
            'DXY stayed weak at 98.079 and the next FOMC meeting still prices an overwhelming no-change outcome, which keeps the cross-asset USD backdrop constructive.',
            'VIX fell 4.24% on the day, but credit spreads widened and MOVE rose 3.14%, so financial conditions improved only partially.',
            'The EIA still frames Hormuz-related disruption as a live supply issue, while the latest weekly petroleum report separately showed a bearish crude inventory build.',
            'RBA hawkishness, expansionary China PMI, and persistent dollar weakness continue to make AUD the strongest pro-cyclical FX expression in the basket.',
        ],
        'data_quality': {
            'stale_sources': [
                'FRED DFII10 latest official observation used: 2026-04-10',
                'FRED BAMLH0A0HYM2 latest official observation used: 2026-04-10',
                'FRED T10Y2Y latest official observation used: 2026-04-13',
            ],
            'fallbacks_used': [
                'ActionForex calendar fallback because ForexFactory was not accessible in-session',
                'Repository-verified ECB growth and stance backdrop retained because the official ECB page did not render cleanly',
                'Copper scored flat because a clean live source could not be verified in-session',
            ],
            'overnight_changes': [
                'DXY down 0.30% on the day',
                'VIX down 4.24% on the day',
                'SOX up 1.68% on the day',
                'MOVE up 3.14% on the day',
            ],
        },
        'catalyst_proximity': {
            'imminent': [
                'U.S. PPI and NFIB releases on April 14, 2026',
                'Any fresh Strait of Hormuz disruption headlines',
            ],
            'near_term': [
                'Atlanta Fed GDPNow update on April 21, 2026',
                'Federal Reserve meeting on April 30, 2026',
            ],
            'background': [
                'RBA hawkish stance versus neutral Fed',
                'Record March gold-ETF outflows as a drag on precious metals',
            ],
        },
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
        writer.writerow(['symbol', 'instrument', 'score', 'signal', 'confidence'])
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
