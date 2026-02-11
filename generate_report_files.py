#!/usr/bin/env python3
"""
Matrix Futures Daily Bias Report - File Generator
Generates all 4 required output files from the bias_scores.json data
"""

import json
from datetime import datetime
import pandas as pd

# Get current date for filenames
report_date = datetime.now().strftime('%Y-%m-%d')

def generate_markdown_report(data):
    """Generates the main report in Markdown format"""
    filename = f"/home/ubuntu/matrix-futures-reports/{report_date}_Matrix-Futures-Daily-Bias-Report.md"
    
    with open(filename, 'w') as f:
        f.write(f"# Matrix Futures Daily Bias Report\n\n")
        f.write(f"**Report Date:** {data['report_date']}\n")
        f.write(f"**Generated At:** {data['generated_at']}\n\n")
        f.write("## I. Executive Summary\n\n")
        f.write("This report provides a quantitative, macro-driven daily bias for 10 key futures instruments across equities, commodities, and foreign exchange. The bias is derived from a weighted model of over 14 macroeconomic factors, designed to provide a directional perspective for the upcoming trading session.\n\n")
        
        # Summary Table
        f.write("### Bias Summary\n\n")
        summary_df = pd.DataFrame([
            {
                "Instrument": code,
                "Name": details["name"],
                "Bias Score": details["score"],
                "Bias": details["bias"]
            } for code, details in data["instruments"].items()
        ])
        f.write(summary_df.to_markdown(index=False))
        f.write("\n\n")
        
        f.write("## II. Detailed Instrument Breakdown\n\n")
        for code, details in data["instruments"].items():
            f.write(f"### {code} - {details['name']}\n\n")
            f.write(f"- **Final Bias Score:** {details['score']:+.2f}\n")
            f.write(f"- **Directional Bias:** {details['bias']}\n\n")
            f.write("#### Factor Contribution Breakdown\n\n")
            breakdown_df = pd.DataFrame([
                {
                    "Factor": factor,
                    "Value": f_details["value"],
                    "Weight": f_details["weight"],
                    "Contribution": f_details["contribution"]
                } for factor, f_details in details["breakdown"].items()
            ])
            f.write(breakdown_df.to_markdown(index=False))
            f.write("\n\n")
            
        f.write("## III. Macro Factor Inputs\n\n")
        f.write("The following table details the raw scores assigned to each macroeconomic factor based on the data collected for this report.\n\n")
        factors_df = pd.DataFrame(list(data['macro_factors'].items()), columns=['Factor', 'Score'])
        f.write(factors_df.to_markdown(index=False))
        f.write("\n\n")
        
        f.write("## IV. Methodology & Disclaimer\n\n")
        f.write("The bias scores are calculated using a proprietary weighted model. The weights for each instrument are defined in the project's methodology document. The model is intended to provide a directional bias and is not a trading signal or financial advice. All data is sourced from publicly available information and is subject to change. The concept of 'signal decay' should be considered, as the relevance of this report diminishes over time.\n")

    print(f"Markdown report generated: {filename}")

def generate_csv_summary(data):
    """Generates a summary of the scores in CSV format"""
    filename = f"/home/ubuntu/matrix-futures-reports/{report_date}_Matrix-Futures-Daily-Bias-Summary.csv"
    summary_df = pd.DataFrame([
        {
            "Instrument": code,
            "Name": details["name"],
            "Bias Score": details["score"],
            "Bias": details["bias"]
        } for code, details in data["instruments"].items()
    ])
    summary_df.to_csv(filename, index=False)
    print(f"CSV summary generated: {filename}")

def generate_conviction_txt(data):
    """Generates a plain text file with the conviction scores"""
    filename = f"/home/ubuntu/matrix-futures-reports/{report_date}_Matrix-Futures-Daily-Bias-Conviction.txt"
    with open(filename, 'w') as f:
        f.write(f"Matrix Futures Daily Bias Conviction - {data['report_date']}\n")
        f.write("="*50 + "\n")
        for code, details in data["instruments"].items():
            f.write(f"{code:<5} | {details['bias']:<16} | Score: {details['score']:+.2f}\n")
    print(f"Conviction text file generated: {filename}")

def main():
    """Load data and generate all report files"""
    try:
        with open('/home/ubuntu/matrix-futures-reports/bias_scores.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: bias_scores.json not found. Please run the calculation script first.")
        return

    # Rename the JSON file to the final dated format
    json_filename = f"/home/ubuntu/matrix-futures-reports/{report_date}_Matrix-Futures-Daily-Bias-Scores.json"
    with open(json_filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"JSON report generated: {json_filename}")

    # Generate other report formats
    generate_markdown_report(data)
    generate_csv_summary(data)
    generate_conviction_txt(data)

    print("\nAll report files generated successfully.")

if __name__ == "__main__":
    main()
