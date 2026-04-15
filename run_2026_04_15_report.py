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

MACRO_INPUTS = {
    'fed_stance': {
        'classification': 'NEUTRAL_HOLD',
        'score': 0,
        'note': 'FedWatch remained overwhelmingly centered on no change for the April 28-29 FOMC meeting; yesterday\'s repository-verified read was approximately 99.5% hold.',
        'source': 'https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html',
    },
    'real_yields': {
        'classification': 'FLAT',
        'score': 0,
        'value': 1.92,
        'previous': 1.95,
        'change_bps': -3.0,
        'note': 'FRED DFII10 slipped only 3 bps from 1.95 to 1.92, which stays inside the flat band rather than a decisive falling-real-yield regime.',
        'source': 'https://fred.stlouisfed.org/series/DFII10',
    },
    'dxy': {
        'classification': 'WEAK_ON_5D',
        'score': 1,
        'value': 98.257,
        'day_change_pct': 0.15,
        'five_day_change_pct': -0.62,
        'note': 'DXY bounced modestly intraday but remained lower over the five-day and one-month windows and near six-week lows in Reuters coverage.',
        'source': 'https://www.tradingview.com/symbols/TVC-DXY/',
    },
    'risk_mood': {
        'classification': 'BALANCED',
        'score': 0,
        'vix': 18.19,
        'note': 'VIX stayed in the 15-20 balanced band.',
        'source': 'https://www.cboe.com/tradable-products/vix/',
    },
    'vix_direction': {
        'classification': 'FALLING',
        'score': 1,
        'vix': 18.19,
        'previous_close': 18.36,
        'change_pct': -0.93,
        'note': 'Spot VIX fell versus the prior close, a modest equity tailwind.',
        'source': 'https://www.cboe.com/tradable-products/vix/',
    },
    'growth': {
        'classification': 'STABLE_SOFT',
        'score': 0,
        'gdpnow': 1.3,
        'updated': '2026-04-09',
        'note': 'GDPNow at 1.3% for 2026:Q1 implies a modest growth backdrop rather than clear acceleration.',
        'source': 'https://www.atlantafed.org/cqer/research/gdpnow',
    },
    'credit_spreads': {
        'classification': 'WIDENING',
        'score': -1,
        'value': 2.95,
        'previous': 2.94,
        'change_bps': 1.0,
        'note': 'HY OAS edged 1 bp wider versus the prior observation, so the directional signal is mildly negative even though absolute spread levels remain contained.',
        'source': 'https://fred.stlouisfed.org/series/BAMLH0A0HYM2',
    },
    'curve': {
        'classification': 'FLATTENING',
        'score': -1,
        'value': 0.50,
        'previous': 0.52,
        'change_bps': -2.0,
        'note': 'The 2s10s curve remained positive but flattened by 2 bps versus the prior print.',
        'source': 'https://fred.stlouisfed.org/series/T10Y2Y',
    },
    'move': {
        'classification': 'FALLING',
        'score': 1,
        'one_day_change_pct': -0.09,
        'five_day_change_pct': -5.57,
        'note': 'Rates volatility continues to ease, supporting duration-sensitive equities.',
        'source': 'https://www.tradingview.com/symbols/TVC-MOVE/',
    },
    'sox': {
        'classification': 'RISING',
        'score': 1,
        'one_day_change_pct': 2.04,
        'five_day_change_pct': 7.74,
        'note': 'Semiconductor leadership remains firm.',
        'source': 'https://www.tradingview.com/symbols/SOX/',
    },
    'oil_supply': {
        'classification': 'TIGHTENING',
        'score': 1,
        'note': 'The current EIA weekly package still reflects a disrupted supply backdrop and a domestic production re-benchmarking reduction, although de-escalation headlines have cooled some war premium.',
        'source': 'https://www.eia.gov/petroleum/supply/weekly/',
    },
    'inventories': {
        'classification': 'BUILD',
        'score': -1,
        'note': 'The latest repository-verified weekly petroleum balance was still a crude build, which caps upside for WTI.',
        'source': 'https://www.eia.gov/petroleum/supply/weekly/',
    },
    'geopolitical': {
        'classification': 'EASING_BUT_ELEVATED',
        'score': -1,
        'note': 'Reuters and other same-day coverage highlighted renewed U.S.-Iran diplomacy hopes, implying some easing in near-term war premium even though supply risks have not vanished.',
        'source': 'https://www.reuters.com/markets/back-square-one-markets-bet-iran-war-is-over-2026-04-15/',
    },
    'gold_etf_flows': {
        'classification': 'OUTFLOWS',
        'score': -1,
        'note': 'World Gold Council reported record March outflows of roughly US$12bn, the largest monthly outflow on record.',
        'source': 'https://www.gold.org/goldhub/research/gold-etfs-holdings-and-flows/2026/04',
    },
    'ecb_stance': {
        'classification': 'HAWKISH_HOLD',
        'score': 1,
        'note': 'Recent March reporting still framed the ECB as on hold but discussing further tightening risk given war-led inflation pressure.',
        'source': 'https://www.reuters.com/business/finance/global-markets-central-banks-2026-03-19/',
    },
    'eurozone_growth': {
        'classification': 'STABLE',
        'score': 0,
        'note': 'Euro-area industrial production improved month over month on April 15 releases, but the broader growth backdrop remains subdued rather than decisively reaccelerating.',
        'source': 'https://finance.yahoo.com/calendar/economic?day=2026-04-15',
    },
    'rba_stance': {
        'classification': 'HAWKISH',
        'score': 1,
        'note': 'The RBA raised the cash rate by 25 bps to 4.10% on 17 March and emphasized upside inflation risks.',
        'source': 'https://www.rba.gov.au/media-releases/2026/mr-26-08.html',
    },
    'aud_rate_diff': {
        'classification': 'SUPPORTIVE',
        'score': 1,
        'note': 'The RBA\'s March hike versus a Fed hold keeps the AUD-USD rate backdrop constructive.',
        'source': 'https://www.rba.gov.au/media-releases/2026/mr-26-08.html',
    },
    'china_growth': {
        'classification': 'POSITIVE',
        'score': 1,
        'note': 'China manufacturing PMI remained in expansion territory at 50.8 in March.',
        'source': 'https://tradingeconomics.com/china/manufacturing-pmi',
    },
    'copper': {
        'classification': 'UNVERIFIED_FLAT',
        'score': 0,
        'note': 'Investing.com was blocked in-browser; because no clean same-session alternate quote was fully re-verified, copper is scored flat for conservatism.',
        'source': 'https://www.investing.com/commodities/copper',
    },
    'boj_stance': {
        'classification': 'NEUTRAL_TO_MILDLY_HAWKISH',
        'score': 0,
        'note': 'The BOJ left the overnight rate around 0.75% in March while describing conditions as accommodative; for model purposes this remains a conservative neutral classification.',
        'source': 'https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2026/k260319a.pdf',
    },
    'jpy_rate_diff': {
        'classification': 'NARROWING_SUPPORTIVE',
        'score': 1,
        'note': 'The multi-month path of BOJ normalization versus prior Fed easing still points to a more supportive JPY rate differential than in prior cycles.',
        'source': 'https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2026/k260319a.pdf',
    },
}

RESULTS = {
    'GC': {
        'score': 0,
        'confidence': 5,
        'recommended_approach': 'RANGE_TRADE',
        'recommended_mode': 'INTRADAY',
        'hold_expectation': 'session',
        'analysis': 'Gold is neutral. The broader dollar trend remains soft enough to prevent a bearish call, but flat real yields and record March ETF outflows leave the metal without a strong fresh macro catalyst. With risk sentiment balanced rather than defensive, the report treats GC as a lower-conviction range trade rather than a momentum long.',
        'factors': [
            ['Fed stance', 'NEUTRAL_HOLD', 0, 1, 0],
            ['Real yields', 'FLAT', 0, 2, 0],
            ['USD (DXY)', 'WEAK_ON_5D', 1, 1, 1],
            ['Risk mood', 'BALANCED', 0, 1, 0],
            ['Growth', 'STABLE_SOFT', 0, 1, 0],
            ['Oil supply / inflation impulse', 'TIGHTENING', 1, 1, 1],
            ['Gold ETF flows', 'OUTFLOWS', -1, 1, -1],
        ],
    },
    'SI': {
        'score': 0,
        'confidence': 5,
        'recommended_approach': 'RANGE_TRADE',
        'recommended_mode': 'INTRADAY',
        'hold_expectation': 'session',
        'analysis': 'Silver is also neutral. A softer multi-session dollar backdrop offsets the drag from heavy gold-ETF outflows, but the copper input has been left flat because the preferred live source was blocked and no clean same-session replacement was fully re-verified. That keeps SI from graduating into a clearer bullish view.',
        'factors': [
            ['Fed stance', 'NEUTRAL_HOLD', 0, 1, 0],
            ['Real yields', 'FLAT', 0, 1, 0],
            ['USD (DXY)', 'WEAK_ON_5D', 1, 1, 1],
            ['Risk mood', 'BALANCED', 0, 1, 0],
            ['Growth', 'STABLE_SOFT', 0, 1, 0],
            ['Copper', 'UNVERIFIED_FLAT', 0, 1, 0],
            ['Gold ETF flows', 'OUTFLOWS', -1, 1, -1],
        ],
    },
    'CL': {
        'score': 1,
        'confidence': 6,
        'recommended_approach': 'IB_BREAKOUT',
        'recommended_mode': 'INTRADAY',
        'hold_expectation': 'session',
        'analysis': 'WTI crude remains slight bullish rather than outright strong. The methodology still gives positive weight to a disrupted supply backdrop and a softer recent dollar trend, but those positives are partly offset by the latest crude-build read and by diplomacy-driven easing in the immediate war premium. The net result is a constructive but not high-conviction oil bias.',
        'factors': [
            ['Oil supply shock', 'TIGHTENING', 1, 2, 2],
            ['Inventories', 'BUILD', -1, 1, -1],
            ['Growth', 'STABLE_SOFT', 0, 2, 0],
            ['Geopolitical risk', 'EASING_BUT_ELEVATED', -1, 1, -1],
            ['USD (DXY)', 'WEAK_ON_5D', 1, 1, 1],
        ],
    },
    'ES': {
        'score': 1,
        'confidence': 6,
        'recommended_approach': 'IB_BREAKOUT',
        'recommended_mode': 'INTRADAY',
        'hold_expectation': 'session',
        'analysis': 'The S&P 500 carries a slight bullish bias. Falling VIX direction and broad dollar softness are supportive, but the gain is capped by a mild widening in high-yield spreads and the absence of a strong growth reacceleration signal. ES therefore looks constructive, though not emphatically so.',
        'factors': [
            ['Fed stance', 'NEUTRAL_HOLD', 0, 1, 0],
            ['Real yields', 'FLAT', 0, 2, 0],
            ['USD (DXY)', 'WEAK_ON_5D', 1, 1, 1],
            ['Risk mood', 'BALANCED', 0, 1, 0],
            ['Growth', 'STABLE_SOFT', 0, 1, 0],
            ['Credit spreads', 'WIDENING', -1, 1, -1],
            ['VIX direction', 'FALLING', 1, 1, 1],
        ],
    },
    'NQ': {
        'score': 3,
        'confidence': 7,
        'recommended_approach': 'TREND_FOLLOW',
        'recommended_mode': 'SWING',
        'hold_expectation': '1-2 days',
        'analysis': 'Nasdaq is the strongest equity-index signal in today\'s basket. Semiconductor leadership remains firm and rates volatility continues to ease, which is materially friendlier for long-duration growth exposure than the prior session. A modestly softer multi-day dollar backdrop adds another tailwind, producing a bullish but still not extreme signal.',
        'factors': [
            ['Fed stance', 'NEUTRAL_HOLD', 0, 1, 0],
            ['Real yields', 'FLAT', 0, 2, 0],
            ['USD (DXY)', 'WEAK_ON_5D', 1, 1, 1],
            ['Risk mood', 'BALANCED', 0, 1, 0],
            ['Growth', 'STABLE_SOFT', 0, 1, 0],
            ['SOX', 'RISING', 1, 1, 1],
            ['MOVE', 'FALLING', 1, 1, 1],
        ],
    },
    'YM': {
        'score': -1,
        'confidence': 5,
        'recommended_approach': 'RANGE_TRADE',
        'recommended_mode': 'INTRADAY',
        'hold_expectation': 'session',
        'analysis': 'Dow futures hold a slight bearish tilt. The model remains cautious on cyclical, value-heavy exposure because credit spreads widened modestly and the 2s10s curve flattened on the latest official prints. Dollar softness provides some offset, but not enough to lift the contract out of a low-conviction defensive stance.',
        'factors': [
            ['Fed stance', 'NEUTRAL_HOLD', 0, 1, 0],
            ['Real yields', 'FLAT', 0, 1, 0],
            ['USD (DXY)', 'WEAK_ON_5D', 1, 1, 1],
            ['Risk mood', 'BALANCED', 0, 1, 0],
            ['Growth', 'STABLE_SOFT', 0, 2, 0],
            ['Credit spreads', 'WIDENING', -1, 1, -1],
            ['2s10s curve', 'FLATTENING', -1, 1, -1],
        ],
    },
    'RTY': {
        'score': -2,
        'confidence': 6,
        'recommended_approach': 'IB_BREAKOUT',
        'recommended_mode': 'INTRADAY',
        'hold_expectation': 'session',
        'analysis': 'Russell 2000 remains the weakest equity setup, though only modestly so. Small caps are the most sensitive sleeve to the direction of credit spreads, and the latest one-basis-point widening receives double weight in the model. Together with a flatter curve, that leaves RTY lagging the tech-led equity tone.',
        'factors': [
            ['Fed stance', 'NEUTRAL_HOLD', 0, 1, 0],
            ['Real yields', 'FLAT', 0, 1, 0],
            ['USD (DXY)', 'WEAK_ON_5D', 1, 1, 1],
            ['Risk mood', 'BALANCED', 0, 1, 0],
            ['Growth', 'STABLE_SOFT', 0, 2, 0],
            ['Credit spreads', 'WIDENING', -1, 2, -2],
            ['2s10s curve', 'FLATTENING', -1, 1, -1],
        ],
    },
    '6E': {
        'score': 2,
        'confidence': 6,
        'recommended_approach': 'RANGE_TRADE',
        'recommended_mode': 'INTRADAY',
        'hold_expectation': 'session',
        'analysis': 'Euro futures are slight bullish. A still-hawkish ECB communication backdrop and a weaker recent dollar trend modestly support EUR, but the report treats euro-area growth as only stable rather than reaccelerating. That leaves 6E constructive but still range-oriented rather than a breakout conviction trade.',
        'factors': [
            ['Fed stance', 'NEUTRAL_HOLD', 0, 1, 0],
            ['ECB stance', 'HAWKISH_HOLD', 1, 1, 1],
            ['Rate differential EUR-USD', 'STABLE', 0, 2, 0],
            ['USD (DXY)', 'WEAK_ON_5D', 1, 1, 1],
            ['Risk mood', 'BALANCED', 0, 1, 0],
            ['Eurozone growth', 'STABLE', 0, 1, 0],
        ],
    },
    '6A': {
        'score': 3,
        'confidence': 7,
        'recommended_approach': 'TREND_FOLLOW',
        'recommended_mode': 'SWING',
        'hold_expectation': '1-2 days',
        'analysis': 'The Australian dollar remains one of the cleaner bullish expressions in the basket. A hawkish RBA, supportive AUD-USD rate differential, and still-expansionary China PMI combine with the broader soft-dollar backdrop to keep the score positive. The signal is capped only by balanced rather than fully risk-on volatility conditions and by a conservative flat copper classification.',
        'factors': [
            ['Fed stance', 'NEUTRAL_HOLD', 0, 1, 0],
            ['RBA stance', 'HAWKISH', 1, 1, 1],
            ['Rate differential AUD-USD', 'SUPPORTIVE', 1, 1, 1],
            ['USD (DXY)', 'WEAK_ON_5D', 1, 1, 1],
            ['Risk sentiment', 'BALANCED', 0, 2, 0],
            ['China growth', 'POSITIVE', 1, 2, 2],
            ['Copper', 'UNVERIFIED_FLAT', 0, 1, 0],
        ],
    },
    '6J': {
        'score': 3,
        'confidence': 6,
        'recommended_approach': 'TREND_FOLLOW',
        'recommended_mode': 'SWING',
        'hold_expectation': '1-2 days',
        'analysis': 'Japanese yen futures are bullish. The main drivers are the still-supportive multi-month rate-differential story and the softer broader dollar backdrop, while balanced risk sentiment prevents a stronger safe-haven tailwind. This keeps 6J positive, but below the highest-conviction tier.',
        'factors': [
            ['Fed stance', 'NEUTRAL_HOLD', 0, 1, 0],
            ['BoJ stance', 'NEUTRAL_TO_MILDLY_HAWKISH', 0, 2, 0],
            ['Rate differential JPY-USD', 'NARROWING_SUPPORTIVE', 1, 2, 2],
            ['USD (DXY)', 'WEAK_ON_5D', 1, 1, 1],
            ['Risk mood', 'BALANCED', 0, 1, 0],
        ],
    },
}


def signal(score: int) -> str:
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


for symbol, payload in RESULTS.items():
    payload['signal'] = signal(payload['score'])


ASSET_CLASS_BIAS = {
    'COMMODITIES': 'SLIGHT_BULLISH',
    'INDICES': 'MIXED',
    'FX': 'BULLISH',
}

KEY_DRIVERS = [
    'The dominant cross-asset input remains a softer multi-session U.S. dollar backdrop, even though DXY bounced modestly intraday on April 15.',
    'U.S. growth remains modest rather than accelerating, with GDPNow at 1.3% and no fresh reacceleration signal to help cyclical equity sleeves.',
    'Tech leadership improved because SOX stayed strong and MOVE continued to fall, lifting NQ above the other index contracts.',
    'AUD and JPY retain support from non-USD FX themes, while record March gold-ETF outflows continue to cap precious-metals conviction.',
]

DATA_QUALITY = {
    'stale_sources': [
        'FRED DFII10 latest official observation: 2026-04-13',
        'FRED HY OAS latest official observation: 2026-04-13',
        'GDPNow last updated: 2026-04-09',
    ],
    'fallbacks_used': [
        'Yahoo Finance economic calendar used as substitute after Forex Factory was blocked in-browser',
        'Previous same-day repository verification used for FedWatch probability detail because the CME page did not expose probabilities cleanly in markdown',
        'Copper scored flat because the preferred live source was blocked and no fully re-verified alternate quote was completed in-session',
        'World Gold Council research article used to confirm the March ETF-flow direction because the public dashboard requires sign-in for detailed charts',
    ],
    'overnight_changes': [
        'VIX fell to 18.19 from 18.36',
        'DXY traded at 98.257, up 0.15% on the day but down 0.62% over five days',
        'MOVE eased another 0.09% on the day and 5.57% over five days',
    ],
}

CATALYST_PROXIMITY = {
    'imminent': [
        'EIA Weekly Petroleum Status Report due April 15, 2026',
        'Any further U.S.-Iran diplomacy or Strait of Hormuz flow headlines',
        'April 15 earnings-driven U.S. equity sentiment around large-cap results',
    ],
    'near_term': [
        'Federal Reserve meeting on April 28-29, 2026',
        'Next Atlanta Fed GDPNow update scheduled for April 21, 2026',
        'Potential April ECB debate over renewed tightening after the March hawkish hold',
    ],
    'background': [
        'Record March gold ETF outflows remain a headwind for metals conviction',
        'China manufacturing PMI remained in expansion territory at 50.8 in March',
    ],
}

CALENDAR_ROWS = [
    ('06:45 UTC', 'France CPI final (Mar)', 'French final CPI and harmonised CPI releases printed early in the European session.'),
    ('09:00 UTC', 'Euro area industrial production (Feb)', 'Industrial production rose 0.4% m/m but remained down 0.6% y/y.'),
    ('11:00 UTC', 'U.S. MBA mortgage applications', 'Mortgage-market index data and purchase-index updates hit before the U.S. cash open.'),
    ('All day', '92 scheduled calendar events', 'Yahoo Finance listed 92 economic events for Wednesday, April 15, 2026.'),
]

NEWS_FUTURES = (
    'Futures trade opened in a calmer tone after a strong risk rebound, with Reuters and other market coverage describing U.S. index futures as broadly steady while investors waited for earnings and assessed whether the Middle East relief rally had run its course. In energy, oil gave back part of its earlier war premium as diplomacy headlines improved, but the market remained supported by an only partially resolved supply-risk backdrop.'
)

NEWS_FX = (
    'In currencies, the dollar hovered near six-week lows on hopes that renewed U.S.-Iran talks could erase more of the prior safe-haven premium. That left the broader FX picture supportive for non-USD contracts, especially where domestic policy remains comparatively firm, such as the Australian dollar, while the yen continued to benefit from a more constructive medium-term rate-differential narrative.'
)

REFERENCES = [
    ('Yahoo Finance Economic Calendar', 'https://finance.yahoo.com/calendar/economic?day=2026-04-15'),
    ('CBOE VIX', 'https://www.cboe.com/tradable-products/vix/'),
    ('TradingView DXY', 'https://www.tradingview.com/symbols/TVC-DXY/'),
    ('FRED DFII10', 'https://fred.stlouisfed.org/series/DFII10'),
    ('FRED HY OAS', 'https://fred.stlouisfed.org/series/BAMLH0A0HYM2'),
    ('FRED 2s10s', 'https://fred.stlouisfed.org/series/T10Y2Y'),
    ('Atlanta Fed GDPNow', 'https://www.atlantafed.org/cqer/research/gdpnow'),
    ('TradingView MOVE', 'https://www.tradingview.com/symbols/TVC-MOVE/'),
    ('TradingView SOX', 'https://www.tradingview.com/symbols/SOX/'),
    ('World Gold Council ETF flows', 'https://www.gold.org/goldhub/research/gold-etfs-holdings-and-flows/2026/04'),
    ('Reuters dollar update', 'https://www.reuters.com/world/middle-east/safe-haven-dollar-near-six-week-lows-hopes-fresh-iran-talks-2026-04-15/'),
    ('Reuters central-bank roundup', 'https://www.reuters.com/business/finance/global-markets-central-banks-2026-03-19/'),
    ('RBA March 17 decision', 'https://www.rba.gov.au/media-releases/2026/mr-26-08.html'),
    ('BOJ March 19 statement', 'https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2026/k260319a.pdf'),
]


def signed(value: int) -> str:
    return f'+{value}' if value > 0 else str(value)


now = datetime.now(timezone.utc).replace(microsecond=0)
date_str = now.strftime('%Y-%m-%d')
time_str = now.strftime('%H%M')
iso_str = now.isoformat().replace('+00:00', 'Z')

output_scores = {}
for symbol in INSTRUMENTS:
    item = RESULTS[symbol]
    output_scores[symbol] = {
        'score': item['score'],
        'signal': item['signal'],
        'confidence': item['confidence'],
        'recommended_approach': item['recommended_approach'],
        'recommended_mode': item['recommended_mode'],
        'hold_expectation': item['hold_expectation'],
    }

output = {
    'date': date_str,
    'generated_at': iso_str,
    'methodology_version': '3.0_STRATEGY',
    'scores': output_scores,
    'asset_class_bias': ASSET_CLASS_BIAS,
    'key_drivers': KEY_DRIVERS,
    'data_quality': DATA_QUALITY,
    'catalyst_proximity': CATALYST_PROXIMITY,
}

avg_conf = sum(item['confidence'] for item in RESULTS.values()) / len(RESULTS)

top_three = sorted(RESULTS.items(), key=lambda kv: (kv[1]['score'], kv[1]['confidence']), reverse=True)[:3]
ordered_symbols = ['GC', 'SI', 'CL', 'ES', 'NQ', 'YM', 'RTY', '6E', '6A', '6J']

lines = []
lines.append('# Matrix Futures Daily Bias Report')
lines.append(f'**Date:** {now.strftime("%B %d, %Y")} | **Time:** {now.strftime("%H:%M")} UTC')
lines.append('')
lines.append('---')
lines.append('')
lines.append('## Economic Calendar')
lines.append('')
lines.append('| Time (UTC) | Event | Why It Matters |')
lines.append('|---|---|---|')
for row in CALENDAR_ROWS:
    lines.append(f'| {row[0]} | {row[1]} | {row[2]} |')
lines.append('')
lines.append('---')
lines.append('')
lines.append('## News Snapshot')
lines.append('')
lines.append(f'**Futures:** {NEWS_FUTURES}')
lines.append('')
lines.append(f'**Currency:** {NEWS_FX}')
lines.append('')
lines.append('---')
lines.append('')
lines.append('## Overall Market Bias: MIXED')
lines.append('')
lines.append('The cross-asset picture is constructive in selective areas rather than uniformly bullish. A softer recent U.S. dollar trend, balanced volatility conditions, and easing rates volatility support Nasdaq and the non-USD FX complex, but a mild widening in credit spreads and a flatter 2s10s curve continue to restrain the more cyclical U.S. equity contracts. Commodities are not outright weak, yet precious metals remain capped by heavy ETF outflows and crude is only modestly positive as diplomacy headlines partially offset supply-risk support.')
lines.append('')
lines.append('---')
lines.append('')
lines.append('## Asset Class Summary')
lines.append('')
lines.append('| Asset Class | Bias | Key Driver |')
lines.append('|-------------|------|------------|')
lines.append('| Commodities | SLIGHT_BULLISH | Crude retains a modest supply-driven bid, but gold and silver are capped by ETF outflows and flat real yields. |')
lines.append('| Indices | MIXED | Nasdaq benefits from SOX strength and falling MOVE, while YM and RTY remain restrained by wider credit spreads and a flatter curve. |')
lines.append('| FX | BULLISH | The softer multi-session USD backdrop and firmer non-U.S. policy themes keep EUR, AUD, and JPY biased higher. |')
lines.append('')
lines.append('---')
lines.append('')
lines.append('## Highest Conviction Signals')
lines.append('')
lines.append('| Instrument | Score | Signal | Confidence |')
lines.append('|------------|-------|--------|------------|')
for symbol, item in top_three:
    lines.append(f"| {symbol} | {signed(item['score'])} | {item['signal']} | {item['confidence']}/10 |")
lines.append('')
lines.append('---')
lines.append('')
lines.append('## Full Instrument Breakdown')
lines.append('')
for symbol in ordered_symbols:
    item = RESULTS[symbol]
    lines.append(f"### {symbol} ({INSTRUMENTS[symbol]}): {signed(item['score'])} {item['signal']} ({item['confidence']}/10)")
    lines.append(f"**Approach:** {item['recommended_approach']} | **Mode:** {item['recommended_mode']} | **Hold:** {item['hold_expectation']}")
    lines.append(item['analysis'])
    lines.append('')
lines.append('---')
lines.append('')
lines.append('## Key Macro Themes')
lines.append('')
lines.append('1. **Dollar weakness still matters more than the intraday bounce.** DXY traded higher on the day, but remained lower over the five-day and one-month windows and near six-week lows in same-day market coverage.')
lines.append('2. **Rates volatility is easing even as credit and curve signals stay less friendly.** Falling MOVE and a lower VIX help NQ and ES, but a one-basis-point widening in HY OAS and a flatter 2s10s curve continue to pressure YM and RTY.')
lines.append('3. **Commodity conviction has narrowed.** Crude still benefits from an only partially resolved supply backdrop, yet diplomacy headlines have reduced urgency, while record March ETF outflows keep GC and SI from producing stronger bullish scores.')
lines.append('')
lines.append('---')
lines.append('')
lines.append('## Upcoming Catalysts')
lines.append('')
lines.append('### Imminent (< 1 Week)')
for item in CATALYST_PROXIMITY['imminent']:
    lines.append(f'- {item}')
lines.append('')
lines.append('### Near-Term (1-4 Weeks)')
for item in CATALYST_PROXIMITY['near_term']:
    lines.append(f'- {item}')
lines.append('')
lines.append('---')
lines.append('')
lines.append('## Data Quality')
lines.append(f'- Average confidence: {avg_conf:.1f}/10')
lines.append('- Official FRED series were used for real yields, HY OAS, and the 2s10s curve; these are authoritative but not fully intraday.')
lines.append('- Forex Factory was blocked in-browser, so the economic-calendar section uses Yahoo Finance as an accessible substitute source.')
lines.append('- Copper was scored flat because the preferred live quote source was blocked and no fully re-verified substitute quote was completed in-session.')
lines.append('- Gold ETF direction was confirmed through the World Gold Council research article because the public dashboard requires sign-in for the detailed chart values.')
lines.append('')
lines.append('---')
lines.append('')
lines.append('## References')
lines.append('')
for title, url in REFERENCES:
    lines.append(f'- [{title}]({url})')
lines.append('')
lines.append('---')
lines.append('**End of Report**')
markdown = '\n'.join(lines) + '\n'

scoring_detail = {
    'date': date_str,
    'generated_at': iso_str,
    'macro_inputs': MACRO_INPUTS,
    'instrument_scoring': {
        symbol: {
            'instrument': INSTRUMENTS[symbol],
            'score': RESULTS[symbol]['score'],
            'signal': RESULTS[symbol]['signal'],
            'confidence': RESULTS[symbol]['confidence'],
            'recommended_approach': RESULTS[symbol]['recommended_approach'],
            'recommended_mode': RESULTS[symbol]['recommended_mode'],
            'hold_expectation': RESULTS[symbol]['hold_expectation'],
            'factor_breakdown': [
                {
                    'factor': factor,
                    'classification': classification,
                    'raw_score': raw_score,
                    'weight': weight,
                    'weighted_score': weighted,
                }
                for factor, classification, raw_score, weight, weighted in RESULTS[symbol]['factors']
            ],
            'analysis': RESULTS[symbol]['analysis'],
        }
        for symbol in ordered_symbols
    },
}

timestamp_json = BIAS_DIR / f'{date_str}_{time_str}.json'
latest_json = BIAS_DIR / 'latest.json'
timestamp_md = EXEC_DIR / f'{date_str}_{time_str}.md'
latest_md = EXEC_DIR / 'latest.md'
detail_json = FACTOR_DIR / f'{date_str}_{time_str}_scoring_detail.json'
csv_path = REPORTS_DIR / f'{date_str}_Bias-Scores.csv'

for path in (timestamp_json, latest_json):
    path.write_text(json.dumps(output, indent=2), encoding='utf-8')
for path in (timestamp_md, latest_md):
    path.write_text(markdown, encoding='utf-8')
detail_json.write_text(json.dumps(scoring_detail, indent=2), encoding='utf-8')

with csv_path.open('w', newline='', encoding='utf-8') as handle:
    writer = csv.writer(handle)
    writer.writerow(['Ticker', 'Instrument', 'Numeric Bias', 'Signal', 'Confidence'])
    for symbol in ordered_symbols:
        item = RESULTS[symbol]
        writer.writerow([symbol, INSTRUMENTS[symbol], signed(item['score']), item['signal'], item['confidence']])

print(json.dumps({
    'timestamp_json': str(timestamp_json),
    'latest_json': str(latest_json),
    'timestamp_md': str(timestamp_md),
    'latest_md': str(latest_md),
    'detail_json': str(detail_json),
    'csv_path': str(csv_path),
    'scores': {symbol: RESULTS[symbol]['score'] for symbol in ordered_symbols},
    'asset_class_bias': ASSET_CLASS_BIAS,
}, indent=2))
