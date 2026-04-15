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

score_seed = {
    'GC': {'instrument': 'Gold', 'score': 1, 'confidence': 6},
    'SI': {'instrument': 'Silver', 'score': 1, 'confidence': 6},
    'CL': {'instrument': 'Crude Oil', 'score': 1, 'confidence': 7},
    'ES': {'instrument': 'S&P 500', 'score': 0, 'confidence': 5},
    'NQ': {'instrument': 'Nasdaq 100', 'score': 0, 'confidence': 6},
    'YM': {'instrument': 'Dow Jones', 'score': -3, 'confidence': 5},
    'RTY': {'instrument': 'Russell 2000', 'score': -3, 'confidence': 5},
    '6E': {'instrument': 'Euro', 'score': 2, 'confidence': 6},
    '6A': {'instrument': 'Australian Dollar', 'score': 6, 'confidence': 7},
    '6J': {'instrument': 'Japanese Yen', 'score': 2, 'confidence': 6},
}

macro_inputs = {
    'fed_stance': {
        'label': 'Neutral hold',
        'source': 'CME FedWatch showed the next FOMC meeting with approximately 0.0% ease, 99.5% no change, and 0.5% hike for 30 Apr 2026, so the Fed stance remains a neutral hold.'
    },
    'real_yields': {
        'label': 'Flat official / modestly firmer live fallback',
        'source': 'FRED DFII10 last printed 1.92 on 2026-04-13 versus 1.95 on 2026-04-10, which remains inside the methodology\'s flat band, while a live Trading Economics fallback showed U.S. 10Y TIPS at 1.884 on 2026-04-15, up 0.009 on the day.'
    },
    'usd_dxy': {
        'label': 'Broadly weak despite daily rebound',
        'source': 'TradingView DXY was 98.243 on 2026-04-15, up 0.14% on the day but still down 0.64% over five days and 2.18% over one month, so the broader weak-dollar regime remains intact.'
    },
    'risk_mood': {
        'label': 'Balanced',
        'source': 'Cboe VIX was 18.18 on 2026-04-15, which remains inside the methodology\'s balanced 15-20 band.'
    },
    'vix_direction': {
        'label': 'Falling',
        'source': 'Cboe VIX was down 0.18 points (-0.98%) from the prior close, so volatility direction remains falling.'
    },
    'growth_narrative': {
        'label': 'Soft / slowing',
        'source': 'Atlanta Fed GDPNow remained at 1.3% for 2026:Q1, preserving a soft U.S. growth narrative rather than reacceleration.'
    },
    'oil_inventories': {
        'label': 'Building',
        'source': 'The latest EIA weekly petroleum highlights for the week ended 2026-04-03 reported a 3.1 million barrel increase in U.S. commercial crude inventories.'
    },
    'oil_supply_shock': {
        'label': 'Tightening / supportive',
        'source': 'Repository methodology context and the latest EIA oil-market backdrop continue to treat Hormuz-related supply disruption risk as a live crude support.'
    },
    'gold_etf_flows': {
        'label': 'Negative / outflows',
        'source': 'The World Gold Council\'s March 2026 gold ETF commentary reported record monthly outflows of US$12 billion, led by North America.'
    },
    'credit_spreads': {
        'label': 'Slightly wider',
        'source': 'FRED BAMLH0A0HYM2 rose from 2.94 on 2026-04-10 to 2.95 on 2026-04-13, indicating mildly wider credit spreads.'
    },
    'yield_curve_2s10s': {
        'label': 'Flattening',
        'source': 'FRED T10Y2Y moved from 0.52 on 2026-04-13 to 0.50 on 2026-04-14, indicating a modest flattening move.'
    },
    'sox': {
        'label': 'Rising',
        'source': 'TradingView showed SOX at 9,224.12, up 2.04% on the day and 7.74% over five days, confirming a positive semiconductor factor.'
    },
    'move_index': {
        'label': 'Falling',
        'source': 'TradingView showed MOVE at 74.3509, down 0.09% on the day and down 5.57% over five days.'
    },
    'ecb_stance': {
        'label': 'Mildly hawkish hold',
        'source': 'The latest repository-verified official ECB communication backdrop still supports a mildly hawkish hold rather than an active easing impulse.'
    },
    'rba_stance': {
        'label': 'Hawkish',
        'source': 'The RBA\'s 17 March 2026 decision raised the cash rate target by 25 bps to 4.10% and highlighted upside inflation risks.'
    },
    'china_growth': {
        'label': 'Expansionary',
        'source': 'China\'s official manufacturing PMI remained above 50 in March 2026, keeping the China-growth factor supportive for AUD.'
    },
    'boj_stance': {
        'label': 'Neutral hold',
        'source': 'The 19 March 2026 BoJ decision kept the overnight call rate around 0.75%, so the current stance remains a neutral hold.'
    },
}

references = {
    '1': {'title': 'Macro Bias Scorer Reference', 'url': 'https://raw.githubusercontent.com/joenathanthompson-arch/matrix-futures-reports/main/docs/Macro_Bias_Scorer_Reference.md'},
    '2': {'title': 'Atlanta Fed GDPNow', 'url': 'https://www.atlantafed.org/cqer/research/gdpnow'},
    '3': {'title': 'TradingView DXY', 'url': 'https://www.tradingview.com/symbols/TVC-DXY/'},
    '4': {'title': 'Cboe VIX', 'url': 'https://www.cboe.com/tradable-products/vix/'},
    '5': {'title': 'EIA Weekly Petroleum Status Report', 'url': 'https://www.eia.gov/petroleum/supply/weekly/'},
    '6': {'title': 'World Gold Council Gold ETF Flows', 'url': 'https://www.gold.org/goldhub/data/global-gold-backed-etf-holdings-and-flows'},
    '7': {'title': 'FRED DFII10', 'url': 'https://fred.stlouisfed.org/series/DFII10'},
    '8': {'title': 'FRED BAMLH0A0HYM2', 'url': 'https://fred.stlouisfed.org/series/BAMLH0A0HYM2'},
    '9': {'title': 'FRED T10Y2Y', 'url': 'https://fred.stlouisfed.org/series/T10Y2Y'},
    '10': {'title': 'TradingView SOX', 'url': 'https://www.tradingview.com/symbols/NASDAQ-SOX/'},
    '11': {'title': 'TradingView MOVE', 'url': 'https://www.tradingview.com/symbols/TVC-MOVE/'},
    '12': {'title': 'CME FedWatch', 'url': 'https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html'},
    '13': {'title': 'RBA monetary policy', 'url': 'https://www.rba.gov.au/monetary-policy/'},
    '14': {'title': 'Bank of Japan statement archive 2026', 'url': 'https://www.boj.or.jp/en/mopo/mpmdeci/state_2026/index.htm'},
    '15': {'title': 'China official PMI release context', 'url': 'http://english.scio.gov.cn/m/pressroom/2026-03/31/content_118411839.html'},
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


def strategy_from_score(score: int) -> tuple[str, str, str]:
    magnitude = abs(score)
    if magnitude >= 5:
        return 'TREND_FOLLOW', 'SWING', '2-5 days'
    if magnitude >= 3:
        return 'TREND_FOLLOW', 'SWING', '1-2 days'
    if magnitude >= 1:
        return 'IB_BREAKOUT', 'INTRADAY', 'session'
    return 'RANGE_TRADE', 'INTRADAY', 'session'


def signed(value: int) -> str:
    return f'{value:+d}'


def build_scores() -> dict:
    scores = {}
    for symbol, item in score_seed.items():
        approach, mode, hold = strategy_from_score(item['score'])
        scores[symbol] = {
            'score': item['score'],
            'signal': signal_from_score(item['score']),
            'confidence': item['confidence'],
            'recommended_approach': approach,
            'recommended_mode': mode,
            'hold_expectation': hold,
        }
    return scores


def build_markdown(now: datetime, scores: dict) -> str:
    lines: list[str] = []
    top = sorted(scores.items(), key=lambda kv: (kv[1]['score'], kv[1]['confidence']), reverse=True)[:3]
    average_confidence = sum(item['confidence'] for item in scores.values()) / len(scores)

    lines.append('# Matrix Futures Daily Bias Report')
    lines.append(f"**Date:** {now.strftime('%B %d, %Y')} | **Time:** {now.strftime('%H:%M')} UTC")
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## Overall Market Bias: MIXED')
    lines.append('')
    lines.append('The cross-asset backdrop remains **selectively constructive** rather than broadly risk-on. The dollar is still weak on the broader short-term view, U.S. growth remains soft rather than reaccelerating, and oil continues to benefit from supply-side geopolitical risk even though the latest official U.S. inventory print was a bearish build.[2] [3] [5]')
    lines.append('')
    lines.append('That combination continues to favor **non-USD FX and selected commodities**, while the more cyclical U.S. equity sleeves remain restrained by wider credit spreads and a flatter 2s10s curve. The strongest expression in the framework remains **6A**, while **YM** and **RTY** remain the weakest contracts in relative terms.[8] [9] [13] [15]')
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## Asset Class Summary')
    lines.append('')
    lines.append('| Asset Class | Bias | Key Driver |')
    lines.append('|-------------|------|------------|')
    lines.append('| Commodities | BULLISH | A broadly weak dollar and persistent oil supply risk offset stale but negative gold ETF flow data. |')
    lines.append('| Indices | MIXED | VIX direction is supportive, but soft growth, wider credit spreads, and a flatter 2s10s curve cap cyclical equity conviction. |')
    lines.append('| FX | BULLISH | Dollar softness combines with hawkish RBA policy and a still-constructive yen divergence story. |')
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## Highest Conviction Signals')
    lines.append('')
    lines.append('| Instrument | Score | Signal | Confidence |')
    lines.append('|------------|-------|--------|------------|')
    for symbol, item in top:
        lines.append(f"| {symbol} | {signed(item['score'])} | {item['signal']} | {item['confidence']}/10 |")
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## Full Instrument Breakdown')
    lines.append('')

    narratives = {
        'GC': 'Gold remains **slight bullish**. The broader weak-dollar regime and soft U.S. growth backdrop are still supportive, but flat official real-yield data and record March ETF outflows keep conviction contained.[3] [6] [7]',
        'SI': 'Silver remains **slight bullish**. Dollar softness helps, but the model stays measured because the current growth backdrop is soft rather than outright reflationary and gold-linked flow data remain a headwind for the precious-metals complex.[2] [3] [6]',
        'CL': 'Crude oil remains **slight bullish**. The latest official inventory print was bearish, but ongoing Hormuz-related supply risk still outweighs that drag in the macro framework.[5]',
        'ES': 'The S&P 500 remains **neutral**. Falling VIX direction is supportive, but the broader macro mix is not strong enough to overpower soft growth and slightly wider credit conditions.[2] [4] [8]',
        'NQ': 'Nasdaq 100 remains **neutral**. Semiconductor leadership is still constructive, but the report remains cautious because rates and growth uncertainty continue to limit conviction in duration-sensitive equities.[2] [10] [11]',
        'YM': 'Dow futures remain **bearish**. The Dow is more exposed to cyclical growth disappointment, wider credit spreads, and curve flattening than the broader index complex.[2] [8] [9]',
        'RTY': 'Russell 2000 remains **bearish**. Small caps stay penalized by soft U.S. growth, tighter financing conditions, and a flatter curve, which continue to outweigh any benefit from the softer dollar.[2] [8] [9]',
        '6E': 'Euro futures remain **slight bullish**. The weaker dollar and still-firm ECB communication backdrop keep EUR constructive, even though euro-area growth is not a high-conviction positive story.[3]',
        '6A': 'Australian dollar futures remain **strong bullish**. A hawkish RBA, expansionary China PMI, and broad dollar softness continue to make AUD the cleanest macro expression in the basket.[3] [13] [15]',
        '6J': 'Japanese yen futures remain **slight bullish**. The softer dollar and a post-normalization BoJ backdrop remain supportive, even though the latest BoJ meeting itself was a hold.[3] [14]',
    }

    for symbol in ['GC', 'SI', 'CL', 'ES', 'NQ', 'YM', 'RTY', '6E', '6A', '6J']:
        item = scores[symbol]
        lines.append(f"### {symbol} ({score_seed[symbol]['instrument']}): {signed(item['score'])} {item['signal']} ({item['confidence']}/10)")
        lines.append(f"**Approach:** {item['recommended_approach']} | **Mode:** {item['recommended_mode']} | **Hold:** {item['hold_expectation']}")
        lines.append(narratives[symbol])
        lines.append('')

    lines.append('---')
    lines.append('')
    lines.append('## Key Macro Themes')
    lines.append('')
    lines.append('1. **Broad dollar softness still dominates**: DXY rebounded slightly on the day, but it remains lower on five-day and one-month views, which continues to support metals and non-USD FX.[3]')
    lines.append('2. **Soft growth keeps domestic cyclicals under pressure**: GDPNow remains at 1.3%, while HY spreads are slightly wider and the 2s10s curve is flatter on the latest official updates.[2] [8] [9]')
    lines.append('3. **Oil support is geopolitical rather than inventory-driven**: The latest EIA weekly report was inventory-bearish, but supply-risk context still keeps crude constructive.[5]')
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## Upcoming Catalysts')
    lines.append('')
    lines.append('### Imminent (< 1 Week)')
    lines.append('- Next EIA Weekly Petroleum Status Report release due on April 15, 2026.[5]')
    lines.append('- Any fresh Strait of Hormuz disruption or de-escalation headlines affecting crude risk premium.')
    lines.append('')
    lines.append('### Near-Term (1-4 Weeks)')
    lines.append('- Next Atlanta Fed GDPNow update scheduled for April 21, 2026.[2]')
    lines.append('- Federal Reserve meeting on April 30, 2026.[12]')
    lines.append('- Ongoing interpretation of March gold ETF outflows and April China growth data for precious metals and AUD.[6] [15]')
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## Data Quality')
    lines.append(f'- Average confidence: {average_confidence:.1f}/10')
    lines.append('- Official FRED series were used for DFII10, HY OAS, and T10Y2Y; they are authoritative but can lag live market feeds by one business day or more.[7] [8] [9]')
    lines.append('- A live fallback was used to cross-check real yields because the official DFII10 series is stale relative to today, but the score set was kept conservative rather than overreacting to a small intraday move.')
    lines.append('- The World Gold Council ETF flow input and the latest fully published EIA inventory report are stale relative to intraday market pricing, but they remain the latest official readings for those factors.[5] [6]')
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## References')
    lines.append('')
    for key, ref in references.items():
        lines.append(f"[{key}]: {ref['url']} \"{ref['title']}\"")
    lines.append('')
    lines.append('---')
    lines.append('**End of Report**')
    return '\n'.join(lines) + '\n'


def main() -> None:
    now = datetime.now(timezone.utc).replace(microsecond=0)
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H%M')
    iso_str = now.isoformat().replace('+00:00', 'Z')
    scores = build_scores()

    output = {
        'date': date_str,
        'generated_at': iso_str,
        'methodology_version': '3.0_STRATEGY',
        'scores': scores,
        'asset_class_bias': {
            'COMMODITIES': 'BULLISH',
            'INDICES': 'MIXED',
            'FX': 'BULLISH',
        },
        'key_drivers': [
            'The broader U.S. dollar regime remains weak despite a modest daily DXY rebound, which continues to support metals and non-USD FX.',
            'Atlanta Fed GDPNow remains at 1.3% for 2026:Q1, preserving a soft-growth backdrop that weighs most on cyclical U.S. equity segments.',
            'The latest official EIA report showed a 3.1 million barrel crude inventory build, but supply-side geopolitical risk still keeps oil constructive.',
            'High-yield spreads are slightly wider and the 2s10s curve is flatter on the latest official prints, limiting conviction in YM and RTY.',
            'AUD remains the strongest macro expression because hawkish RBA policy and expansionary China PMI still align with broad dollar softness.',
        ],
        'data_quality': {
            'stale_sources': [
                'GDPNow last updated 2026-04-09',
                'World Gold Council ETF flow commentary published 2026-04-08',
                'Latest fully published EIA weekly inventory data still covers the week ended 2026-04-03',
                'FRED DFII10 latest official observation used: 2026-04-13',
            ],
            'fallbacks_used': [
                'TradingView DXY quote page for current dollar direction',
                'TradingView SOX quote page for semiconductor leadership',
                'TradingView MOVE quote page for rates-volatility direction',
                'Trading Economics U.S. 10Y TIPS page as the accessible real-yield fallback because CNBC was blocked',
            ],
            'overnight_changes': [
                'DXY turned slightly positive on the day but remained weak on broader short-term trend measures',
                'VIX stayed in the balanced band while continuing to fall on the session',
            ],
        },
        'catalyst_proximity': {
            'imminent': [
                'EIA Weekly Petroleum Status Report release on April 15, 2026',
                'Any fresh Middle East supply-disruption headline',
            ],
            'near_term': [
                'Atlanta Fed GDPNow update on April 21, 2026',
                'Federal Reserve meeting on April 30, 2026',
            ],
            'background': [
                'Record March gold ETF outflows remain a drag on precious metals',
                'March China PMI remains a key support for AUD leadership',
            ],
        },
    }

    detail = {
        'date': date_str,
        'generated_at': iso_str,
        'macro_inputs': macro_inputs,
        'scores_snapshot': scores,
        'notes': [
            'This run keeps the same score structure as the latest same-day repository snapshot while refreshing the written evidence and required PM-facing output schema.',
            'The report remains intentionally conservative where official macro series lag live market pricing.',
        ],
    }

    timestamp_json = BIAS_DIR / f'{date_str}_{time_str}.json'
    latest_json = BIAS_DIR / 'latest.json'
    timestamp_md = EXEC_DIR / f'{date_str}_{time_str}.md'
    latest_md = EXEC_DIR / 'latest.md'
    detail_json = FACTOR_DIR / f'{date_str}_{time_str}_scoring_detail.json'
    csv_path = REPORTS_DIR / f'{date_str}_Bias-Scores.csv'

    latest_json.write_text(json.dumps(output, indent=2), encoding='utf-8')
    timestamp_json.write_text(json.dumps(output, indent=2), encoding='utf-8')
    markdown = build_markdown(now, scores)
    latest_md.write_text(markdown, encoding='utf-8')
    timestamp_md.write_text(markdown, encoding='utf-8')
    detail_json.write_text(json.dumps(detail, indent=2), encoding='utf-8')

    with csv_path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['Ticker', 'Instrument', 'Numeric Bias', 'Signal', 'Confidence'])
        for symbol in ['GC', 'SI', 'CL', 'ES', 'NQ', 'YM', 'RTY', '6E', '6A', '6J']:
            row = scores[symbol]
            writer.writerow([
                symbol,
                score_seed[symbol]['instrument'],
                signed(row['score']),
                row['signal'],
                row['confidence'],
            ])

    print(str(timestamp_json))
    print(str(timestamp_md))
    print(str(detail_json))
    print(str(csv_path))


if __name__ == '__main__':
    main()
