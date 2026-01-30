#!/usr/bin/env python3
"""
Generates the final JSON and Markdown report files from the calculated bias scores.
"""

import json
from datetime import datetime

# Get the current date for file naming
REPORT_DATE = datetime.now().strftime("%Y-%m-%d")


def generate_markdown_report(data):
    """Generates the full Markdown report content."""
    report_time = data["report_time"]
    instruments = data["instruments"]

    md_content = f"# Matrix Futures Daily Bias Report\n\n"
    md_content += f"**Report Generated:** {report_time}\n\n"
    md_content += "This report provides a quantitative daily bias for 10 key futures instruments based on a weighted analysis of over 14 real-time macroeconomic factors. The bias score indicates the directional pressure on the instrument, with positive scores suggesting bullish sentiment and negative scores suggesting bearish sentiment.\n\n"

    # --- Summary Table ---
    md_content += "## Bias Summary\n\n"
    md_content += "| Instrument | Name                        | Asset Class      | Bias Score | Direction |\n"
    md_content += "|:-----------|:----------------------------|:-----------------|-----------:|:----------|\n"
    for inst in sorted(instruments, key=lambda x: x["instrument"]):
        md_content += f"| {inst['instrument']:<10} | {inst['name']:<27} | {inst['asset_class']:<16} | {inst['bias_score']:>+9.2f} | **{inst['bias_direction']}** |\n"

    md_content += "\n\n"

    # --- Detailed Instrument Breakdown ---
    md_content += "## Detailed Instrument Analysis\n\n"
    for inst in sorted(instruments, key=lambda x: x["instrument"]):
        md_content += f"### {inst['instrument']} - {inst['name']}\n\n"
        md_content += f"**Final Bias Score: {inst['bias_score']:.2f} ({inst['bias_direction']})**\n\n"
        md_content += "| Macro Factor        | Value | Weight | Contribution |\n"
        md_content += "|:--------------------|------:|-------:|-------------:|\n"
        total_contribution = 0
        for factor, details in inst["components"].items():
            value = details["value"]
            weight = details["weight"]
            contribution = details["contribution"]
            total_contribution += contribution
            md_content += f"| {factor:<19} | {value:>5} | {weight:>6.2f} | {contribution:>+12.3f} |\n"
        md_content += f"| **Total**           |       |        | **{total_contribution:>+12.3f}** |\n\n"

    # --- Methodology & Signal Decay ---
    md_content += "## Methodology and Important Notes\n\n"
    md_content += "The bias score is calculated by multiplying the normalized score of each macroeconomic factor (typically -2 to +2) by its assigned weight for a specific instrument. The sum of these weighted scores produces the final bias score. The weights are derived from the reference methodology document and reflect the relative importance of each factor to the instrument.\n\n"
    md_content += "> **Signal Decay Concept:** The conviction level of a signal, particularly for high scores, is time-sensitive. A high bias score suggests a catalyst is expected within a short timeframe (e.g., a few trading sessions). The validity of these signals decays over time. This report is intended for the current trading day and should be re-evaluated with fresh data daily.\n\n"

    # --- Data Sources ---
    md_content += "## Data Sources\n\n"
    md_content += "Data is collected from over 14 sources, including but not limited to: CME Group (FedWatch), FRED (St. Louis Fed), CBOE (VIX), TradingView (DXY, SOX, MOVE), Atlanta Fed (GDPNow), EIA, World Gold Council, and the official websites of the ECB, BoJ, BoE, RBA, and SNB. All data was collected on the report generation date to ensure timeliness.\n\n"

    return md_content


def main():
    """Main function to generate all report files."""
    # Load the calculated data
    with open("/home/ubuntu/matrix-futures-reports/bias_scores_calculated.json", "r") as f:
        data = json.load(f)

    # --- Generate JSON Files ---
    # Timestamped JSON
    timestamped_json_path = f"/home/ubuntu/matrix-futures-reports/reports/{REPORT_DATE}-bias-report.json"
    with open(timestamped_json_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Generated: {timestamped_json_path}")

    # Latest JSON
    latest_json_path = "/home/ubuntu/matrix-futures-reports/reports/latest-bias-report.json"
    with open(latest_json_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Generated: {latest_json_path}")

    # --- Generate Markdown Files ---
    md_report = generate_markdown_report(data)

    # Timestamped Markdown
    timestamped_md_path = f"/home/ubuntu/matrix-futures-reports/reports/{REPORT_DATE}-bias-report.md"
    with open(timestamped_md_path, "w") as f:
        f.write(md_report)
    print(f"Generated: {timestamped_md_path}")

    # Latest Markdown
    latest_md_path = "/home/ubuntu/matrix-futures-reports/reports/latest-bias-report.md"
    with open(latest_md_path, "w") as f:
        f.write(md_report)
    print(f"Generated: {latest_md_path}")

if __name__ == "__main__":
    main()
