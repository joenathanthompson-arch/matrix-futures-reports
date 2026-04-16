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
for directory in (BIAS_DIR, EXEC_DIR, FACTOR_DIR, REPORTS_DIR):
    directory.mkdir(parents=True, exist_ok=True)

RUN_TS = datetime.now(timezone.utc)
DATE_STR = RUN_TS.strftime('%Y-%m-%d')
TS_STR = RUN_TS.strftime('%Y-%m-%d_%H%M')
TIME_STR = RUN_TS.strftime('%H:%M UTC')
ISO_TS = RUN_TS.replace(microsecond=0).isoformat().replace('+00:00', 'Z')

INSTRUMENTS = {
    'GC': 'Gold',
    'SI': 'Silver',
    'CL': 'Crude Oil',
    'ES': 'S&P 500',
    'NQ': 'Nasdaq 100',
    'YM': 'Dow Jones',
    'RTY': 'Russell 2000',
    '6E': 'Euro',
    '6A': 'Australian Dollar',
    '6J': 'Japanese Yen',
}

FACTOR_MAP = {
    'fed_stance': {
        'label': 'Fed stance',
        'classification': 'NEUTRAL_HOLD',
        'score': 0,
        'note': 'FedWatch remained centered on no change for the late-April FOMC meeting, so the Fed input stays neutral hold.',
        'source': 'https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html',
    },
    'real_yields': {
        'label': '10Y real yields',
        'classification': 'FLAT',
        'score': 0,
        'note': 'FRED DFII10 printed 1.89 on 2026-04-14 versus 1.92 on 2026-04-13, a 3 bp decline that remains inside the flat band rather than a decisive falling-yield signal.',
        'source': 'https://fred.stlouisfed.org/series/DFII10',
    },
    'usd_dxy': {
        'label': 'USD (DXY)',
        'classification': 'WEAK_FALLING_MULTISESSION',
        'score': 1,
        'note': 'TradingView showed DXY at 98.163, up 0.12% on the day but down 0.71% over five days and down 1.70% over one month, which keeps the usable macro regime weak/falling.',
        'source': 'https://www.tradingview.com/symbols/TVC-DXY/',
    },
    'risk_mood': {
        'label': 'Risk mood',
        'classification': 'BALANCED',
        'score': 0,
        'note': 'Cboe VIX spot was 18.23, which remains in the methodology\'s balanced 15-20 zone.',
        'source': 'https://www.cboe.com/tradable-products/vix/',
    },
    'vix_direction': {
        'label': 'VIX direction',
        'classification': 'RISING',
        'score': -1,
        'note': 'VIX was up 0.33% (+0.06) versus the prior close, so the directional volatility input is mildly negative for equities.',
        'source': 'https://www.cboe.com/tradable-products/vix/',
    },
    'growth_narrative': {
        'label': 'US growth narrative',
        'classification': 'SLOWING',
        'score': 1,
        'note': 'Atlanta Fed GDPNow stayed at 1.3% for 2026:Q1 after stronger earlier-quarter readings, which supports a slowing rather than accelerating growth classification.',
        'source': 'https://www.atlantafed.org/cqer/research/gdpnow',
    },
    'credit_spreads': {
        'label': 'HY credit spreads',
        'classification': 'NARROWING',
        'score': 1,
        'note': 'FRED HY OAS narrowed to 2.84 on 2026-04-14 from 2.95 on 2026-04-13, a supportive tightening in credit conditions.',
        'source': 'https://fred.stlouisfed.org/series/BAMLH0A0HYM2',
    },
    'sox': {
        'label': 'SOX semiconductors',
        'classification': 'RISING',
        'score': 1,
        'note': 'TradingView showed SOX at 9,239.29, up 0.16% on the day, 4.85% over five days, and 17.75% over one month, preserving a rising semiconductor-leadership signal.',
        'source': 'https://www.tradingview.com/symbols/SOX/',
    },
    'move_index': {
        'label': 'MOVE index',
        'classification': 'FALLING',
        'score': 1,
        'note': 'TradingView showed MOVE at 67.9410, down 8.62% on the day and 8.20% over five days, a clear falling rate-volatility input.',
        'source': 'https://www.tradingview.com/symbols/TVC-MOVE/',
    },
    'yield_curve_2s10s': {
        'label': '2s10s curve',
        'classification': 'STEEPENING',
        'score': 1,
        'note': 'FRED T10Y2Y rose to 0.53 on 2026-04-15 from 0.50 on 2026-04-14, which classifies as steepening.',
        'source': 'https://fred.stlouisfed.org/series/T10Y2Y',
    },
    'copper': {
        'label': 'Copper',
        'classification': 'RISING',
        'score': 1,
        'note': 'Recent accessible commodity coverage and repository notes kept copper in a rising trend, supporting both silver and AUD.',
        'source': 'https://www.investing.com/commodities/copper',
    },
    'oil_inventories': {
        'label': 'Oil inventories',
        'classification': 'DRAW',
        'score': 1,
        'note': 'The EIA weekly summary for the week ending April 10, 2026 stated that U.S. commercial crude oil inventories decreased by 0.9 million barrels to 463.8 million.',
        'source': 'https://ir.eia.gov/wpsr/wpsrsummary.pdf',
    },
    'oil_supply_shock': {
        'label': 'Oil supply shock',
        'classification': 'EASING',
        'score': -1,
        'note': 'Cboe\'s volatility commentary stated that fears of significant oil-supply disruption had abated somewhat, so the supply-shock input is easing rather than tightening.',
        'source': 'https://www.cboe.com/tradable-products/vix/',
    },
    'geopolitical_risk': {
        'label': 'Geopolitical risk',
        'classification': 'EASING',
        'score': -1,
        'note': 'The same cross-asset news backdrop points to some easing in the near-term Middle East war premium rather than renewed escalation.',
        'source': 'https://www.cboe.com/tradable-products/vix/',
    },
    'gold_etf_flows': {
        'label': 'Gold ETF flows',
        'classification': 'OUTFLOWS',
        'score': -1,
        'note': 'The World Gold Council gold-ETF page exposed the March 2026 update window, while repository-collected March commentary recorded heavy monthly outflows; this remains a negative flow input.',
        'source': 'https://www.gold.org/goldhub/data/gold-etfs-holdings-and-flows',
    },
    'ecb_stance': {
        'label': 'ECB stance',
        'classification': 'MILDLY_HAWKISH_HOLD',
        'score': 1,
        'note': 'The ECB kept rates unchanged on 19 March 2026 but stressed upside inflation risks from higher energy prices and left the door open to further adjustment, which reads as a mildly hawkish hold.',
        'source': 'https://www.ecb.europa.eu/press/pr/date/2026/html/ecb.mp260319~3057739775.en.html',
    },
    'rba_stance': {
        'label': 'RBA stance',
        'classification': 'HAWKISH',
        'score': 1,
        'note': 'The RBA raised the cash rate 25 bps to 4.10% on 17 March 2026 and explicitly said inflation risks had tilted further to the upside.',
        'source': 'https://www.rba.gov.au/media-releases/2026/mr-26-08.html',
    },
    'boj_stance': {
        'label': 'BoJ stance',
        'classification': 'MILDLY_HAWKISH_HOLD',
        'score': 1,
        'note': 'The BoJ kept the overnight call rate around 0.75% on 19 March 2026, but the normalization narrative remains intact, so the stance is treated as mildly hawkish hold for JPY.',
        'source': 'https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2026/k260319a.pdf',
    },
    'china_growth': {
        'label': 'China growth',
        'classification': 'ACCELERATING',
        'score': 1,
        'note': 'Recent March reporting showed official China manufacturing PMI back in expansion at 50.4, supporting an accelerating China-growth proxy.',
        'source': 'https://www.reuters.com/world/asia-pacific/chinas-factory-activity-returns-expansion-pmi-shows-2026-03-31/',
    },
    'eurozone_growth': {
        'label': 'Eurozone growth',
        'classification': 'STABLE',
        'score': 0,
        'note': 'March euro-area composite PMI slowed to 50.7 from 51.9 but remained above the 50 expansion threshold, so the eurozone growth input is kept stable rather than clearly accelerating.',
        'source': 'https://www.reuters.com/world/europe/euro-zone-growth-slows-nine-month-low-surging-costs-pmi-shows-2026-04-07/',
    },
    'rate_diff_eur_usd': {
        'label': 'EUR-USD rate differential',
        'classification': 'NARROWING_VS_USD',
        'score': 1,
        'note': 'A mildly hawkish ECB hold against a neutral Fed hold makes the policy differential somewhat less USD-positive than before, which is supportive for EUR.',
        'source': 'https://www.ecb.europa.eu/press/pr/date/2026/html/ecb.mp260319~3057739775.en.html',
    },
    'rate_diff_aud_usd': {
        'label': 'AUD-USD rate differential',
        'classification': 'WIDENING_VS_USD',
        'score': 1,
        'note': 'The RBA\'s 4.10% cash rate versus a Fed on hold keeps the AUD-USD rate backdrop supportive.',
        'source': 'https://www.rba.gov.au/media-releases/2026/mr-26-08.html',
    },
    'rate_diff_jpy_usd': {
        'label': 'JPY-USD rate differential',
        'classification': 'NARROWING_VS_USD',
        'score': 1,
        'note': 'BoJ normalization versus a neutral Fed keeps the yen\'s policy-gap story gradually improving, even if the absolute differential is still wide.',
        'source': 'https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2026/k260319a.pdf',
    },
    'risk_sentiment_aud': {
        'label': 'AUD risk sentiment',
        'classification': 'NEUTRAL',
        'score': 0,
        'note': 'VIX remains in the balanced zone, so the broad pro-cyclical risk input for AUD is neutral rather than clearly risk-on.',
        'source': 'https://www.cboe.com/tradable-products/vix/',
    },
}

CONFIGS = {
    'GC': ['fed_stance', 'real_yields', 'usd_dxy', 'risk_mood', 'growth_narrative', 'oil_supply_shock', 'gold_etf_flows'],
    'SI': ['fed_stance', 'real_yields', 'usd_dxy', 'risk_mood', 'growth_narrative', 'copper', 'gold_etf_flows'],
    'CL': ['oil_supply_shock', 'oil_supply_shock', 'oil_inventories', 'growth_narrative', 'growth_narrative', 'geopolitical_risk', 'usd_dxy'],
    'ES': ['fed_stance', 'real_yields', 'real_yields', 'usd_dxy', 'risk_mood', 'growth_narrative', 'credit_spreads', 'vix_direction'],
    'NQ': ['fed_stance', 'real_yields', 'real_yields', 'usd_dxy', 'risk_mood', 'growth_narrative', 'sox', 'move_index'],
    'YM': ['fed_stance', 'real_yields', 'usd_dxy', 'risk_mood', 'growth_narrative', 'growth_narrative', 'credit_spreads', 'yield_curve_2s10s'],
    'RTY': ['fed_stance', 'real_yields', 'usd_dxy', 'risk_mood', 'growth_narrative', 'growth_narrative', 'credit_spreads', 'credit_spreads', 'yield_curve_2s10s'],
    '6E': ['fed_stance', 'ecb_stance', 'rate_diff_eur_usd', 'rate_diff_eur_usd', 'usd_dxy', 'risk_mood', 'eurozone_growth'],
    '6A': ['fed_stance', 'rba_stance', 'rate_diff_aud_usd', 'usd_dxy', 'risk_sentiment_aud', 'risk_sentiment_aud', 'china_growth', 'china_growth', 'copper'],
    '6J': ['fed_stance', 'boj_stance', 'boj_stance', 'rate_diff_jpy_usd', 'rate_diff_jpy_usd', 'usd_dxy', 'risk_mood'],
}

SYMBOL_NOTES = {
    'GC': 'Gold has only a slight bullish bias because dollar weakness and a softer U.S. growth narrative are offset by easing oil-risk inflation pressure and still-negative ETF flows. With real yields flat rather than falling, the metal has a supportive backdrop but not a clean momentum impulse.',
    'SI': 'Silver is slight bullish. The weaker multi-session dollar trend, softer macro growth impulse, and rising copper backdrop outweigh the drag from negative gold-ETF flow data. The signal is constructive, but the absence of a falling-real-yield tailwind keeps conviction moderate.',
    'CL': 'WTI crude is only slight bullish. A fresh EIA crude draw and weaker dollar help, but the supply-shock and geopolitical-risk inputs both eased, preventing oil from moving into a high-conviction trend regime. This remains a constructive but headline-sensitive contract.',
    'ES': 'The S&P 500 carries a slight bullish bias. Narrower credit spreads and a softer dollar support risk assets, but the day\'s rising VIX direction and only-balanced volatility regime cap upside conviction. ES still favors directional long setups, though mainly for intraday expansion rather than multi-day swing follow-through.',
    'NQ': 'Nasdaq 100 is bullish. Falling rate volatility, strong semiconductor leadership, and a weaker dollar all align positively, while flat real yields stop the signal from moving into the strongest bucket. Among the equity indices, NQ remains the cleanest quality-growth expression.',
    'YM': 'Dow futures register a strong bullish bias. A slowing-growth narrative, tighter credit conditions, and a steepening curve combine into a favorable cyclical value backdrop. The broad risk regime is not euphoric, but macro conditions now skew clearly constructive for YM.',
    'RTY': 'Russell 2000 is strong bullish and one of the highest-conviction contracts in the basket. Small caps benefit most from narrowing credit spreads and a steeper curve, while the softer dollar adds to the constructive domestic-risk tone. This signal also carries signal-decay risk if financial conditions reverse quickly.',
    '6E': 'Euro futures are bullish. Mild ECB hawkishness and a somewhat less USD-favorable rate-differential narrative now reinforce the broader weak-dollar backdrop. Euro-area growth is only stable, so the conviction is solid rather than extreme.',
    '6A': 'Australian dollar futures are strong bullish. A hawkish RBA, supportive rate differential, expansionary China PMI signal, and rising copper trend all align with the weaker-dollar backdrop. The only restraint is that broad risk sentiment remains balanced rather than fully risk-on.',
    '6J': 'Japanese yen futures are strong bullish. Mild BoJ tightening bias and a gradually improving rate-differential story pair with broad dollar weakness to keep the yen favored. Because 6J is an inverted quote, this remains a bearish-USD/JPY macro expression.',
}


def score_to_signal(score: int) -> str:
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


def confidence_for(symbol: str, score: int) -> int:
    abs_score = abs(score)
    base = 5
    if abs_score >= 5:
        base = 8
    elif abs_score >= 3:
        base = 7
    elif abs_score >= 1:
        base = 6
    penalties = 0
    if symbol in {'GC', 'SI'}:
        penalties += 1  # ETF flow detail remains partially gated.
    if symbol in {'6E', '6A'}:
        penalties += 1  # Growth proxies rely on latest headline-level reporting.
    if symbol == '6J':
        penalties += 1  # BoJ stance remains a mildly hawkish-hold interpretation.
    return max(5, min(8, base - penalties))


def approach_mode_hold(score: int, confidence: int) -> tuple[str, str, str]:
    if score == 0:
        return 'RANGE_TRADE', 'INTRADAY', 'session'
    if abs(score) >= 3 and confidence >= 7:
        hold = '2-5 days' if abs(score) >= 5 else '1-2 days'
        return 'TREND_FOLLOW', 'SWING', hold
    return 'IB_BREAKOUT', 'INTRADAY', 'session'


def signed(n: int) -> str:
    return f'{n:+d}'


results = {}
factor_rows: list[list[str]] = []
for symbol, factors in CONFIGS.items():
    total = 0
    breakdown = []
    counts: dict[str, int] = {}
    for factor in factors:
        counts[factor] = counts.get(factor, 0) + 1
    seen: set[tuple[str, int]] = set()
    for factor in factors:
        score = FACTOR_MAP[factor]['score']
        total += score
        occurrence = sum(1 for f in factors[: factors.index(factor) + 1] if f == factor)
        key = (factor, occurrence)
        if key in seen:
            continue
        seen.add(key)
    detailed = []
    local_counts: dict[str, int] = {}
    for factor in factors:
        local_counts[factor] = local_counts.get(factor, 0) + 1
        weight = counts[factor]
        if local_counts[factor] > 1:
            continue
        raw = FACTOR_MAP[factor]['score']
        weighted = raw * weight
        detailed.append({
            'factor': FACTOR_MAP[factor]['label'],
            'classification': FACTOR_MAP[factor]['classification'],
            'raw': raw,
            'weight': weight,
            'weighted': weighted,
            'note': FACTOR_MAP[factor]['note'],
            'source': FACTOR_MAP[factor]['source'],
        })
        factor_rows.append([
            symbol,
            FACTOR_MAP[factor]['label'],
            FACTOR_MAP[factor]['classification'],
            str(raw),
            str(weight),
            str(weighted),
            FACTOR_MAP[factor]['note'],
            FACTOR_MAP[factor]['source'],
        ])
    signal = score_to_signal(total)
    confidence = confidence_for(symbol, total)
    approach, mode, hold = approach_mode_hold(total, confidence)
    results[symbol] = {
        'score': total,
        'signal': signal,
        'confidence': confidence,
        'recommended_approach': approach,
        'recommended_mode': mode,
        'hold_expectation': hold,
        'analysis': SYMBOL_NOTES[symbol],
        'factors': detailed,
    }

asset_class_bias = {
    'COMMODITIES': 'SLIGHT_BULLISH',
    'INDICES': 'BULLISH',
    'FX': 'STRONG_BULLISH',
}

json_payload = {
    'date': DATE_STR,
    'generated_at': ISO_TS,
    'methodology_version': '3.0_STRATEGY',
    'scores': {
        symbol: {
            'score': results[symbol]['score'],
            'signal': results[symbol]['signal'],
            'confidence': results[symbol]['confidence'],
            'recommended_approach': results[symbol]['recommended_approach'],
            'recommended_mode': results[symbol]['recommended_mode'],
            'hold_expectation': results[symbol]['hold_expectation'],
        }
        for symbol in INSTRUMENTS
    },
    'asset_class_bias': asset_class_bias,
    'key_drivers': [
        'The multi-session U.S. dollar trend remains soft even after a small intraday DXY rebound.',
        'Financial conditions improved through narrower HY credit spreads, lower MOVE, and a steeper 2s10s curve.',
        'Oil lost part of its war-premium support because supply-disruption fears eased, even though the latest EIA report showed a modest crude draw.',
        'FX leadership strengthened because the ECB, RBA, and BoJ all screen at least mildly hawkish relative to a neutral Fed.',
    ],
    'data_quality': {
        'stale_sources': ['Detailed WGC ETF-flow chart remained login-gated; March flow direction was carried from the latest accessible repository note.'],
        'fallbacks_used': ['EIA weekly summary PDF for crude inventory headline', 'BoJ statement PDF for policy stance', 'Reuters headline coverage for China PMI and euro-area PMI growth proxies'],
        'overnight_changes': ['VIX direction flipped mildly negative on the day while DXY remained weak on five-day and one-month horizons.'],
    },
    'catalyst_proximity': {
        'imminent': ['U.S. weekly jobless claims and housing data on 2026-04-16', 'RBA monetary policy decision on 2026-04-17'],
        'near_term': ['Atlanta Fed GDPNow update on 2026-04-21', 'FOMC meeting on 2026-04-28 to 2026-04-29'],
        'background': ['BoJ normalization path remains active after the March 19 hold at 0.75%'],
    },
}

avg_conf = sum(item['confidence'] for item in results.values()) / len(results)
highest = sorted(results.items(), key=lambda kv: (kv[1]['confidence'], kv[1]['score']), reverse=True)[:3]

md_lines = []
md_lines.append('# Matrix Futures Daily Bias Report')
md_lines.append(f'**Date:** {DATE_STR} | **Time:** {TIME_STR}')
md_lines.append('')
md_lines.append('---')
md_lines.append('')
md_lines.append('## Overall Market Bias: BULLISH')
md_lines.append('')
md_lines.append('Macro conditions on April 16, 2026 remain constructive, but leadership has rotated. The weaker multi-session dollar trend, tighter credit backdrop, lower rate volatility, and steeper curve now support equities and non-USD FX more clearly than precious metals or crude. Commodities still lean positive overall, yet gold remains capped by ETF outflows and crude has lost part of its geopolitical premium even after the latest EIA crude draw.')
md_lines.append('')
md_lines.append('---')
md_lines.append('')
md_lines.append('## Asset Class Summary')
md_lines.append('')
md_lines.append('| Asset Class | Bias | Key Driver |')
md_lines.append('|-------------|------|------------|')
md_lines.append('| Commodities | SLIGHT_BULLISH | Weak USD and a fresh crude draw help, but gold ETF outflows and easing oil-supply fears cap conviction. |')
md_lines.append('| Indices | BULLISH | Narrower HY spreads, falling MOVE, and a steeper 2s10s curve improved the domestic risk backdrop. |')
md_lines.append('| FX | STRONG_BULLISH | Soft USD conditions now align with mildly hawkish ECB and BoJ narratives plus a clearly hawkish RBA. |')
md_lines.append('')
md_lines.append('---')
md_lines.append('')
md_lines.append('## Highest Conviction Signals')
md_lines.append('')
md_lines.append('| Instrument | Score | Signal | Confidence |')
md_lines.append('|------------|-------|--------|------------|')
for symbol, data in highest:
    md_lines.append(f"| {symbol} | {signed(data['score'])} | {data['signal']} | {data['confidence']}/10 |")
md_lines.append('')
md_lines.append('---')
md_lines.append('')
md_lines.append('## Full Instrument Breakdown')
md_lines.append('')
for symbol in INSTRUMENTS:
    data = results[symbol]
    md_lines.append(f"### {symbol} ({INSTRUMENTS[symbol]}): {signed(data['score'])} {data['signal']} ({data['confidence']}/10)")
    md_lines.append(f"**Approach:** {data['recommended_approach']} | **Mode:** {data['recommended_mode']} | **Hold:** {data['hold_expectation']}")
    md_lines.append(data['analysis'])
    md_lines.append('')
md_lines.append('---')
md_lines.append('')
md_lines.append('## Key Macro Themes')
md_lines.append('')
md_lines.append('1. **Dollar softness still matters most**: DXY rose modestly intraday, but the five-day and one-month trend remained negative, which continues to support metals and non-USD FX.')
md_lines.append('2. **Financial conditions improved materially**: HY spreads narrowed, MOVE fell sharply, and the 2s10s curve steepened, which lifted NQ, YM, and especially RTY.')
md_lines.append('3. **Oil support shifted from supply shock to inventory flow**: The latest EIA report showed a small crude draw, but broader supply-disruption fears eased, preventing a stronger bullish crude signal.')
md_lines.append('')
md_lines.append('---')
md_lines.append('')
md_lines.append('## Upcoming Catalysts')
md_lines.append('')
md_lines.append('### Imminent (< 1 Week)')
md_lines.append('- U.S. weekly jobless claims and housing data (2026-04-16)')
md_lines.append('- RBA monetary policy decision (2026-04-17)')
md_lines.append('')
md_lines.append('### Near-Term (1-4 Weeks)')
md_lines.append('- Atlanta Fed GDPNow update (2026-04-21)')
md_lines.append('- FOMC meeting (2026-04-28 to 2026-04-29)')
md_lines.append('')
md_lines.append('---')
md_lines.append('')
md_lines.append('## Data Quality')
md_lines.append(f'- Average confidence: {avg_conf:.1f}/10')
md_lines.append('- The EIA crude inventory headline was refreshed from the latest weekly summary PDF.')
md_lines.append('- Detailed World Gold Council chart data remained gated, so ETF-flow direction used the latest accessible March outflow note already stored in the repository.')
md_lines.append('')
md_lines.append('---')
md_lines.append('**End of Report**')
markdown = '\n'.join(md_lines) + '\n'

bias_path = BIAS_DIR / f'{TS_STR}.json'
latest_bias = BIAS_DIR / 'latest.json'
exec_path = EXEC_DIR / f'{TS_STR}.md'
latest_exec = EXEC_DIR / 'latest.md'
factor_path = FACTOR_DIR / f'{TS_STR}.csv'
report_csv = REPORTS_DIR / f'{DATE_STR}_Bias-Scores.csv'

bias_path.write_text(json.dumps(json_payload, indent=2) + '\n', encoding='utf-8')
latest_bias.write_text(json.dumps(json_payload, indent=2) + '\n', encoding='utf-8')
exec_path.write_text(markdown, encoding='utf-8')
latest_exec.write_text(markdown, encoding='utf-8')

with factor_path.open('w', newline='', encoding='utf-8') as fh:
    writer = csv.writer(fh)
    writer.writerow(['symbol', 'factor', 'classification', 'raw_score', 'weight', 'weighted_score', 'note', 'source'])
    writer.writerows(factor_rows)

with report_csv.open('w', newline='', encoding='utf-8') as fh:
    writer = csv.writer(fh)
    writer.writerow(['Ticker', 'Instrument', 'Numeric Bias', 'Signal', 'Confidence'])
    for symbol, name in INSTRUMENTS.items():
        writer.writerow([symbol, name, signed(results[symbol]['score']), results[symbol]['signal'], results[symbol]['confidence']])

print(bias_path)
print(exec_path)
print(factor_path)
print(report_csv)
