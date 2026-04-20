from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import csv
import json

BASE = Path('/home/ubuntu/matrix-futures-reports')
BIAS_DIR = BASE / 'data' / 'bias_scores'
EXEC_DIR = BASE / 'data' / 'executive_summaries'
FACTORS_DIR = BASE / 'data' / 'factors'
REPORTS_DIR = BASE / 'reports'
for d in [BIAS_DIR, EXEC_DIR, FACTORS_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

now = datetime.now(timezone.utc)
date_str = now.strftime('%Y-%m-%d')
time_hhmm = now.strftime('%H%M')
iso_str = now.strftime('%Y-%m-%dT%H:%M:%SZ')
human_date = now.strftime('%B %d, %Y')

# Verified and documented live-source classifications for 2026-04-20 UTC.
# Integer raw scores follow the methodology lookup tables.
factors = {
    'fed_stance': {
        'raw': 0,
        'observation': 'CME FedWatch showed 0.0% ease, 99.5% no change, and 0.5% hike for the visible 30 Apr 2026 meeting row; classified as neutral hold.'
    },
    'real_yields': {
        'raw': 0,
        'observation': 'FRED DFII10 latest official print was 1.93 on 2026-04-16, effectively flat versus the recent 1.90 prior reference used in repository notes.'
    },
    'usd': {
        'raw': 1,
        'observation': 'TradingView DXY was 98.190, down 0.04% on the day, so the USD factor is weak/falling.'
    },
    'risk_mood': {
        'raw': 0,
        'observation': 'Cboe VIX spot was 19.45, which remains in the 15-20 balanced band.'
    },
    'growth_narrative': {
        'raw': 1,
        'observation': 'Atlanta Fed GDPNow remained at 1.3% for 2026:Q1, a soft/slowing growth backdrop.'
    },
    'oil_supply': {
        'raw': 1,
        'observation': 'Official energy-source context remained consistent with a tightening/disruption-prone oil backdrop rather than easing oversupply.'
    },
    'gold_etf_flows': {
        'raw': -1,
        'observation': 'Repository-documented same-month gold flow references indicate March 2026 gold ETF outflows; the WGC page itself was partially gated, so confidence is reduced.'
    },
    'credit_spreads': {
        'raw': -1,
        'observation': 'FRED HY OAS was 2.86 on 2026-04-16 and repository notes indicate a slight widening from the prior reading.'
    },
    'vix_direction': {
        'raw': -1,
        'observation': 'VIX was up 11.27% on the day, so volatility direction is rising.'
    },
    'sox': {
        'raw': 1,
        'observation': 'TradingView SOX closed at 9,555.88, up 2.43% on the session.'
    },
    'move': {
        'raw': 1,
        'observation': 'TradingView MOVE closed at 65.6953, down 0.30% on the session, so rates volatility is falling.'
    },
    'oil_inventories': {
        'raw': 1,
        'observation': 'Same-day repository notes and latest official EIA context continued to point to a crude draw signal in the most recent interpreted report.'
    },
    'geopolitical_risk': {
        'raw': 1,
        'observation': 'The ECB March policy statement explicitly cited the Middle East war and higher energy-price risks, so geopolitical risk remains elevated rather than easing.'
    },
    'curve_2s10s': {
        'raw': 1,
        'observation': 'FRED T10Y2Y was 0.55 on 2026-04-17, with repository notes showing a slight steepening from 0.54.'
    },
    'copper': {
        'raw': -1,
        'observation': 'TradingView copper futures HG1! were 6.0205, down 1.54% on the day.'
    },
    'ecb_stance': {
        'raw': 0,
        'observation': 'The ECB held rates unchanged on 19 Mar 2026, keeping the deposit facility at 2.00%; treated as a neutral hold for scoring.'
    },
    'eur_usd_rate_diff': {
        'raw': 0,
        'observation': 'With both the Fed and ECB on hold, the EUR-USD rate differential is treated as broadly stable rather than clearly widening in the euro\'s favor.'
    },
    'eurozone_growth': {
        'raw': -1,
        'observation': 'The ECB revised 2026 growth down to 0.9%, indicating a softer euro-area growth backdrop.'
    },
    'rba_stance': {
        'raw': 1,
        'observation': 'Repository-verified official RBA context indicates the March 17, 2026 decision was a 25 bp hike to 4.10%, leaving the stance hawkish.'
    },
    'aud_usd_rate_diff': {
        'raw': 1,
        'observation': 'The RBA\'s post-hike 4.10% cash rate versus a steady Fed keeps the AUD-USD differential supportive for AUD.'
    },
    'aud_risk_sentiment': {
        'raw': 0,
        'observation': 'Broader risk sentiment is balanced rather than decisively risk-on or risk-off because VIX remains below 20 but elevated on the day.'
    },
    'china_growth': {
        'raw': 1,
        'observation': 'China\'s official March 2026 manufacturing PMI rose to 50.4 from 49.0, showing an improving growth and demand backdrop.'
    },
    'boj_stance': {
        'raw': 1,
        'observation': 'The BoJ\'s 2026 policy release archive shows ongoing normalization-era statements rather than easing; classified as hawkish/tightening.'
    },
    'jpy_usd_rate_diff': {
        'raw': 1,
        'observation': 'BoJ normalization versus a neutral Fed narrows the JPY-USD policy gap in the yen\'s favor.'
    },
}

weights = {
    'GC': [('fed_stance', 1), ('real_yields', 2), ('usd', 1), ('risk_mood', 1), ('growth_narrative', 1), ('oil_supply', 1), ('gold_etf_flows', 1)],
    'SI': [('fed_stance', 1), ('real_yields', 1), ('usd', 1), ('risk_mood', 1), ('growth_narrative', 1), ('copper', 1), ('gold_etf_flows', 1)],
    'CL': [('oil_supply', 2), ('oil_inventories', 1), ('growth_narrative', 2), ('geopolitical_risk', 1), ('usd', 1)],
    'ES': [('fed_stance', 1), ('real_yields', 2), ('usd', 1), ('risk_mood', 1), ('growth_narrative', 1), ('credit_spreads', 1), ('vix_direction', 1)],
    'NQ': [('fed_stance', 1), ('real_yields', 2), ('usd', 1), ('risk_mood', 1), ('growth_narrative', 1), ('sox', 1), ('move', 1)],
    'YM': [('fed_stance', 1), ('real_yields', 1), ('usd', 1), ('risk_mood', 1), ('growth_narrative', 2), ('credit_spreads', 1), ('curve_2s10s', 1)],
    'RTY': [('fed_stance', 1), ('real_yields', 1), ('usd', 1), ('risk_mood', 1), ('growth_narrative', 2), ('credit_spreads', 2), ('curve_2s10s', 1)],
    '6E': [('fed_stance', 1), ('ecb_stance', 1), ('eur_usd_rate_diff', 2), ('usd', 1), ('risk_mood', 1), ('eurozone_growth', 1)],
    '6A': [('fed_stance', 1), ('rba_stance', 1), ('aud_usd_rate_diff', 1), ('usd', 1), ('aud_risk_sentiment', 2), ('china_growth', 2), ('copper', 1)],
    '6J': [('fed_stance', 1), ('boj_stance', 2), ('jpy_usd_rate_diff', 2), ('usd', 1), ('risk_mood', 1)],
}

instrument_names = {
    'GC': 'Gold', 'SI': 'Silver', 'CL': 'Crude Oil', 'ES': 'S&P 500', 'NQ': 'Nasdaq 100',
    'YM': 'Dow Jones', 'RTY': 'Russell 2000', '6E': 'Euro', '6A': 'Australian Dollar', '6J': 'Japanese Yen'
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
    if score <= -5:
        return 'STRONG_BEARISH'
    if score <= -3:
        return 'BEARISH'
    return 'SLIGHT_BEARISH'


def strategy_for(symbol: str, score: int, confidence: int) -> tuple[str, str, str]:
    magnitude = abs(score)
    signal = signal_from_score(score)
    if signal == 'NEUTRAL':
        return 'RANGE_TRADE', 'INTRADAY', 'session'
    if magnitude >= 5 and confidence >= 6:
        return 'TREND_FOLLOW', 'SWING', '2-5 days' if magnitude >= 6 else '1-2 days'
    if magnitude >= 3:
        if symbol in {'6A', 'YM'}:
            return 'TREND_FOLLOW', 'SWING', '1-2 days'
        return 'IB_BREAKOUT', 'INTRADAY', 'session'
    return 'IB_BREAKOUT', 'INTRADAY', 'session'


def confidence_for(symbol: str) -> int:
    table = {
        'GC': 5, 'SI': 4, 'CL': 7, 'ES': 5, 'NQ': 6,
        'YM': 6, 'RTY': 5, '6E': 4, '6A': 6, '6J': 7,
    }
    return table[symbol]


def calc_score(symbol: str) -> tuple[int, list[dict[str, object]]]:
    total = 0
    breakdown = []
    for factor_name, weight in weights[symbol]:
        raw = factors[factor_name]['raw']
        weighted = raw * weight
        total += weighted
        breakdown.append({
            'factor': factor_name,
            'raw': raw,
            'weight': weight,
            'weighted': weighted,
            'observation': factors[factor_name]['observation'],
        })
    return total, breakdown

scores = {}
full_breakdown = {}
for symbol in instrument_names:
    total, breakdown = calc_score(symbol)
    signal = signal_from_score(total)
    confidence = confidence_for(symbol)
    recommended_approach, recommended_mode, hold_expectation = strategy_for(symbol, total, confidence)
    scores[symbol] = {
        'score': total,
        'signal': signal,
        'confidence': confidence,
        'recommended_approach': recommended_approach,
        'recommended_mode': recommended_mode,
        'hold_expectation': hold_expectation,
    }
    full_breakdown[symbol] = breakdown

asset_avg = {
    'COMMODITIES': round((scores['GC']['score'] + scores['SI']['score'] + scores['CL']['score']) / 3),
    'INDICES': round((scores['ES']['score'] + scores['NQ']['score'] + scores['YM']['score'] + scores['RTY']['score']) / 4),
    'FX': round((scores['6E']['score'] + scores['6A']['score'] + scores['6J']['score']) / 3),
}
asset_class_bias = {k: signal_from_score(v) for k, v in asset_avg.items()}

json_payload = {
    'date': date_str,
    'generated_at': iso_str,
    'methodology_version': '3.0_STRATEGY',
    'scores': scores,
    'asset_class_bias': asset_class_bias,
    'key_drivers': [
        'CME FedWatch still prices essentially no near-term Fed move, while DXY softened modestly on the day, keeping the dollar from overwhelming other cross-asset signals.',
        'Crude has the strongest macro setup because the latest interpreted EIA backdrop still favors a draw/tight-supply reading while geopolitical risk remains elevated.',
        'Equities are supported by strong semiconductor leadership and falling MOVE, but widening HY spreads and a sharply rising VIX cap broad index conviction.',
        'FX divergence remains the cleanest macro theme: the ECB is on hold, the RBA remains post-hike hawkish, and the BoJ stays in normalization mode while the USD is softer.',
        'Gold and silver lose some support because the latest accessible gold-flow evidence points to March ETF outflows and copper turned lower on the day.'
    ],
    'data_quality': {
        'stale_sources': [
            'Atlanta Fed GDPNow remained the April 9, 2026 official update at 1.3% for 2026:Q1.',
            'FRED DFII10, HY OAS, and T10Y2Y reflect official publication lags into April 16-17 rather than intraday April 20 prints.',
            'World Gold Council ETF detail is partially gated; direction used the latest repository-documented March 2026 flow evidence.'
        ],
        'fallbacks_used': [
            'TradingView was used for DXY, SOX, MOVE, and copper because it provided readable live direction within the browser.',
            'Repository same-day notes were used to preserve the latest interpreted EIA inventory direction and March gold-flow sign where page-level extraction was incomplete.',
            'The ECB March 19 policy page, BoJ 2026 release archive, and official China March PMI release were read directly in the browser to anchor policy and growth classifications.'
        ],
        'overnight_changes': [
            'DXY was down 0.04% on the day while VIX was up 11.27%, creating a softer-dollar but less comfortable risk backdrop.',
            'SOX was up 2.43% and MOVE was down 0.30%, which remains supportive for growth-sensitive assets even with the VIX spike.',
            'Copper was down 1.54%, adding an industrial-demand headwind for silver and AUD despite stronger China PMI data.'
        ]
    },
    'catalyst_proximity': {
        'imminent': [
            'Atlanta Fed GDPNow update scheduled for April 21, 2026'
        ],
        'near_term': [
            'FOMC meeting on April 28-29, 2026',
            'ECB decision window on April 30, 2026',
            'BoJ communication remains a live FX catalyst into late April'
        ],
        'background': [
            'RBA post-hike policy divergence still supports AUD on a multi-session basis',
            'Middle East energy-risk headlines remain capable of repricing crude and safe havens quickly'
        ]
    }
}

summary_order = sorted(scores.items(), key=lambda item: (abs(item[1]['score']), item[1]['confidence']), reverse=True)[:3]
avg_conf = round(sum(v['confidence'] for v in scores.values()) / len(scores), 1)

analysis = {
    'GC': 'Gold keeps a mild upside lean because flat real yields are no longer a strong headwind and the dollar softened on the day. The bullish case is capped by the latest accessible March ETF-flow evidence pointing to outflows, so the macro edge is present but not decisive.',
    'SI': 'Silver remains more conflicted than gold because the weaker dollar and soft growth backdrop help, but copper fell sharply on the day and March precious-metals flow evidence was unsupportive. That leaves silver closer to a neutral range than a clean trend signal.',
    'CL': 'Crude has the strongest directional profile in the slate. The latest interpreted EIA backdrop still favors a draw/tightness signal, growth is slowing rather than collapsing, the dollar is softer, and geopolitical energy risk remains elevated.',
    'ES': 'The S&P 500 sits in a balanced macro zone. A softer dollar helps, but widening HY spreads and a rising VIX offset the benefits of falling MOVE and leave the broad index without a clean multi-session edge.',
    'NQ': 'Nasdaq retains better macro support than the broader index complex because SOX is strongly higher and MOVE is lower, both of which favor duration-sensitive growth. Even so, the VIX jump argues for tactical breakout trading rather than complacent trend chasing.',
    'YM': 'The Dow is firmer than ES because the 2s10s curve is still steepening and the growth factor remains positive in the methodology. Credit spreads still limit conviction, but the balance of factors points modestly upward rather than flat.',
    'RTY': 'Russell 2000 is constructive but fragile. A steeper curve, softer dollar, and positive growth factor help, but the index remains highly exposed to HY-spread widening, which prevents a stronger swing-grade score.',
    '6E': 'The euro lacks a strong standalone policy edge because both the Fed and ECB are effectively on hold and euro-area growth projections have softened. The weaker dollar stops the outlook from turning bearish, but the setup remains mostly range-bound.',
    '6A': 'AUD benefits from one of the clearest macro combinations in the report: a softer dollar, a still-hawkish RBA, a supportive policy-rate differential, and an improving official China PMI backdrop. The main restraint is the sharp one-day copper drop, which keeps the score bullish rather than outright strong-bullish.',
    '6J': 'JPY remains one of the cleanest expressions of policy divergence. BoJ normalization and narrowing JPY-USD rate differentials combine with a softer dollar to keep the yen supported, even though the balanced VIX regime prevents an even larger safe-haven boost.',
}

overall_bias = 'MIXED' if len({asset_class_bias['COMMODITIES'], asset_class_bias['INDICES'], asset_class_bias['FX']}) > 1 else asset_class_bias['INDICES']

md_lines = [
    '# Matrix Futures Daily Bias Report',
    f'**Date:** {human_date} | **Time:** {now.strftime("%H:%M")} UTC',
    '',
    '---',
    '',
    f'## Overall Market Bias: {overall_bias}',
    '',
    'The current cross-asset regime is **constructive but uneven**. Crude and FX carry the clearest macro tailwinds because the dollar softened, policy divergence remains active, and energy risk is still elevated, while U.S. equity index conviction is tempered by wider credit spreads and a sharp same-day VIX jump. Precious metals are supported by the weaker USD but remain constrained by stale-to-negative ETF flow evidence and a softer industrial-metals signal.',
    '',
    '---',
    '',
    '## Asset Class Summary',
    '',
    '| Asset Class | Bias | Key Driver |',
    '|-------------|------|------------|',
    f"| Commodities | {asset_class_bias['COMMODITIES']} | Crude supply tightness and geopolitical risk outweigh neutral-to-soft precious-metals flow support |",
    f"| Indices | {asset_class_bias['INDICES']} | Strong SOX and lower MOVE help, but wider HY spreads and a rising VIX cap broad risk appetite |",
    f"| FX | {asset_class_bias['FX']} | Softer USD and persistent central-bank divergence favor JPY and AUD more than EUR |",
    '',
    '---',
    '',
    '## Highest Conviction Signals',
    '',
    '| Instrument | Score | Signal | Confidence |',
    '|------------|-------|--------|------------|',
]
for sym, payload in summary_order:
    score_fmt = f"{payload['score']:+d}"
    md_lines.append(f"| {sym} | {score_fmt} | {payload['signal']} | {payload['confidence']}/10 |")

md_lines.extend(['', '---', '', '## Full Instrument Breakdown', ''])
for sym in ['GC', 'SI', 'CL', 'ES', 'NQ', 'YM', 'RTY', '6E', '6A', '6J']:
    payload = scores[sym]
    md_lines.append(f"### {sym} ({instrument_names[sym]}): {payload['score']:+d} {payload['signal']} ({payload['confidence']}/10)")
    md_lines.append(f"**Approach:** {payload['recommended_approach']} | **Mode:** {payload['recommended_mode']} | **Hold:** {payload['hold_expectation']}")
    md_lines.append(analysis[sym])
    md_lines.append('')

md_lines.extend([
    '---',
    '',
    '## Key Macro Themes',
    '',
    '1. **FX divergence still matters:** The Fed remains in a no-change regime, while the RBA and BoJ still carry relatively firmer policy narratives and the USD softened on the day.',
    '2. **Risk appetite is selective, not broad:** SOX strength and lower MOVE support growth assets, but wider HY spreads and a VIX jump argue against treating the whole equity complex as cleanly risk-on.',
    '3. **Energy remains the strongest commodity theme:** Tight-supply interpretation and elevated geopolitical risk continue to make crude the highest-conviction macro expression among commodities.',
    '',
    '---',
    '',
    '## Upcoming Catalysts',
    '',
    '### Imminent (< 1 Week)',
    '- Atlanta Fed GDPNow update (April 21, 2026)',
    '',
    '### Near-Term (1-4 Weeks)',
    '- FOMC meeting (April 28-29, 2026)',
    '- ECB decision window (April 30, 2026)',
    '- BoJ communication and normalization messaging (late April 2026)',
    '',
    '---',
    '',
    '## Data Quality',
    f'- All report inputs were refreshed or cross-checked on April 20, 2026, with normal publication-lag caveats for official macro series.',
    '- Stale or partially gated sources were explicitly documented and reflected in lower confidence where appropriate.',
    f'- Average confidence: {avg_conf}/10',
    '',
    '---',
    '**End of Report**',
])

markdown_text = '\n'.join(md_lines) + '\n'

json_path = BIAS_DIR / f'{date_str}_{time_hhmm}.json'
json_latest = BIAS_DIR / 'latest.json'
md_path = EXEC_DIR / f'{date_str}_{time_hhmm}.md'
md_latest = EXEC_DIR / 'latest.md'
csv_path = FACTORS_DIR / f'{date_str}_{time_hhmm}.csv'

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(json_payload, f, indent=2)
    f.write('\n')
with open(json_latest, 'w', encoding='utf-8') as f:
    json.dump(json_payload, f, indent=2)
    f.write('\n')
with open(md_path, 'w', encoding='utf-8') as f:
    f.write(markdown_text)
with open(md_latest, 'w', encoding='utf-8') as f:
    f.write(markdown_text)

with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['symbol', 'factor', 'raw', 'weight', 'weighted', 'observation'])
    for symbol, rows in full_breakdown.items():
        for row in rows:
            writer.writerow([symbol, row['factor'], row['raw'], row['weight'], row['weighted'], row['observation']])

print(json_path)
print(md_path)
print(csv_path)
