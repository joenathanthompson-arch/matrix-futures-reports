from __future__ import annotations

import re
import json
from pathlib import Path
from typing import Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE = Path('/home/ubuntu/matrix-futures-reports')
PAGE_TEXTS = Path('/home/ubuntu/page_texts')
OUT = BASE / 'macro_snapshot_2026-04-15.json'

HEADERS = {'User-Agent': 'Mozilla/5.0'}


def fred_csv_url(series: str) -> str:
    return f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}'


def load_fred_latest(series: str) -> dict:
    df = pd.read_csv(fred_csv_url(series))
    df = df[df[series] != '.'].copy()
    df[series] = df[series].astype(float)
    date_col = 'observation_date'
    last = df.iloc[-1]
    prev = df.iloc[-2]
    return {
        'series': series,
        'date': str(last[date_col]),
        'value': float(last[series]),
        'prev_date': str(prev[date_col]),
        'prev_value': float(prev[series]),
        'change': float(last[series] - prev[series]),
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8') if path.exists() else ''


def extract_tradingview_value(text: str) -> dict:
    result = {}
    m = re.search(r'\n([A-Z0-9.]+)\n\n([0-9,]+\.?[0-9]*)USD\n\n([+−-][0-9.]+)([+−-][0-9.]+%)', text)
    if m:
        result['symbol'] = m.group(1)
        result['value'] = float(m.group(2).replace(',', ''))
        result['point_change'] = m.group(3).replace('−', '-')
        result['pct_change'] = m.group(4).replace('−', '-')
    for label in ['1 day', '5 days', '1 month', '6 months', 'Year to date', '1 year']:
        mm = re.search(re.escape(label) + r'\s*([+−-]?[0-9.]+%)', text)
        if mm:
            result[label] = mm.group(1).replace('−', '-')
    return result


def get_url(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.text


def simple_extract(pattern: str, text: str, flags: int = 0) -> Optional[str]:
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else None


snapshot = {
    'fred_dfii10': load_fred_latest('DFII10'),
    'fred_hyoas': load_fred_latest('BAMLH0A0HYM2'),
    'fred_t10y2y': load_fred_latest('T10Y2Y'),
}

snapshot['browser_markdown'] = {}
for name in [
    'www.tradingview.com_symbols_TVC-DXY_.md',
    'www.tradingview.com_symbols_TVC-MOVE_.md',
    'www.tradingview.com_symbols_SOX_.md',
    'www.cboe.com_tradable-products_vix_.md',
    'www.atlantafed.org_cqer_research_gdpnow.md',
    'www.eia.gov_petroleum_supply_weekly_.md',
    'www.gold.org_goldhub_data_gold-etfs-holdings-and-flows.md',
    'www.federalreserve.gov_monetarypolicy_fomccalendars.htm.md',
]:
    snapshot['browser_markdown'][name] = read_text(PAGE_TEXTS / name)

snapshot['parsed'] = {
    'dxy': extract_tradingview_value(snapshot['browser_markdown']['www.tradingview.com_symbols_TVC-DXY_.md']),
    'move': extract_tradingview_value(snapshot['browser_markdown']['www.tradingview.com_symbols_TVC-MOVE_.md']),
    'sox': extract_tradingview_value(snapshot['browser_markdown']['www.tradingview.com_symbols_SOX_.md']),
    'vix_spot': simple_extract(r'## \$([0-9.]+)\n\nVIX Spot Price', snapshot['browser_markdown']['www.cboe.com_tradable-products_vix_.md']),
    'vix_change_pct': simple_extract(r'##\s*([+−-]?[0-9.]+%)\s*\([^\)]*\)\n\nChange', snapshot['browser_markdown']['www.cboe.com_tradable-products_vix_.md']),
    'gdpnow_latest': simple_extract(r'([0-9.]+%)\n\n\*\*Latest GDPNow Estimate for 2026:Q1\*\*', snapshot['browser_markdown']['www.atlantafed.org_cqer_research_gdpnow.md']),
    'gdpnow_updated': simple_extract(r'\*\*Updated:\*\* ([A-Za-z]+ \d{2}, \d{4})', snapshot['browser_markdown']['www.atlantafed.org_cqer_research_gdpnow.md']),
    'eia_week': simple_extract(r'Data for week ending ([A-Za-z]+\. \d+, \d{4})', snapshot['browser_markdown']['www.eia.gov_petroleum_supply_weekly_.md']),
    'gold_etf_date': simple_extract(r'# Gold ETFs, holdings and flows\n\n([0-9]{1,2} [A-Za-z]+, 2026)', snapshot['browser_markdown']['www.gold.org_goldhub_data_gold-etfs-holdings-and-flows.md']),
}

for url_name, url in {
    'gold_etf_article': 'https://www.gold.org/goldhub/research/gold-etfs-holdings-and-flows/2026/04',
    'rba_release': 'https://www.rba.gov.au/media-releases/2026/',
    'boj_march_release': 'https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2026/k260319a.pdf',
    'ecb_press': 'https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2026/html/index.en.html',
    'fedwatch': 'https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html',
}.items():
    try:
        html = get_url(url)
        snapshot[url_name] = {'url': url, 'length': len(html)}
        if url_name == 'gold_etf_article':
            snapshot[url_name]['headline'] = simple_extract(r'<title>(.*?)</title>', html, re.I | re.S)
            snapshot[url_name]['snippet'] = simple_extract(r'(?is)<main[\s\S]*?<p>(.*?)</p>', html)
        elif url_name == 'rba_release':
            snapshot[url_name]['headline'] = simple_extract(r'<title>(.*?)</title>', html, re.I | re.S)
            snapshot[url_name]['first_date'] = simple_extract(r'(\d{1,2} [A-Za-z]+ 2026)', html)
        elif url_name == 'ecb_press':
            snapshot[url_name]['headline'] = simple_extract(r'<title>(.*?)</title>', html, re.I | re.S)
            snapshot[url_name]['first_h1'] = simple_extract(r'<h1[^>]*>(.*?)</h1>', html, re.I | re.S)
        elif url_name == 'fedwatch':
            snapshot[url_name]['has_no_change'] = 'no change' in html.lower()
            snapshot[url_name]['has_ease'] = 'ease' in html.lower()
    except Exception as e:
        snapshot[url_name] = {'url': url, 'error': str(e)}

OUT.write_text(json.dumps(snapshot, indent=2), encoding='utf-8')
print(str(OUT))
