# Browser Verification Notes - 2026-04-14

The methodology document was read in full from the repository's raw GitHub URL before any other report-generation step. The document confirms that all raw scores and weights must remain integers, that four output files must be created on every run, and that `latest.json` plus `latest.md` must be explicitly written rather than copied by shell command.

The CME FedWatch page loaded successfully and visually displayed the next meeting probability table, although the markdown extraction did not expose the row cleanly. The repository's same-day April 14 run script and supporting verification notes indicate that the 30 April 2026 meeting was priced at approximately 0.0% ease, 99.5% no change, and 0.5% hike, which supports a **neutral hold** Fed classification.

The FRED DFII10 page was directly verified in-browser. It showed a latest observation of **1.92** for **2026-04-13**, updated **Apr 14, 2026 3:16 PM CDT**. Relative to the prior official repository reference of 1.95 on 2026-04-10, this is a decline of 3 basis points, which remains within the methodology's flat band of plus or minus 5 basis points and therefore supports a **flat** real-yield classification.

The CNBC VIX page was blocked, so the Cboe VIX page was used as the permitted fallback. Cboe showed **VIX spot at 18.36** as of **April 14, 2026**, with a daily change of **-3.97% (-0.76)** and prior close **19.12**. That leaves the volatility regime in the methodology's **balanced** 15-20 band while also classifying VIX direction as **falling**.

The TradingView DXY page was directly verified in-browser. It showed **DXY at 98.132**, down **0.241 (-0.24%)** on the day, with **98.373** as the previous close and five-day performance of **-0.94%**. That supports a **weak/falling U.S. dollar** classification for the current run.

The Atlanta Fed GDPNow page was directly verified. It showed a **1.3%** latest GDPNow estimate for **2026:Q1**, updated **April 09, 2026**, with the next update scheduled for **April 21, 2026**. Relative to stronger prior repository baselines, this supports a **slowing growth narrative**.

The FRED ICE BofA US High Yield OAS page was directly verified. It showed a latest observation of **2.95** for **2026-04-13**, updated **Apr 14, 2026 9:21 AM CDT**. Compared with the recent prior reference of 2.94, credit spreads have **widened slightly**, which remains a negative risk signal under the methodology.

The FRED T10Y2Y page was directly verified. It showed a latest observation of **0.50** for **2026-04-14**, updated **Apr 14, 2026 4:02 PM CDT**. This is back down from **0.52** on 2026-04-13, so the curve signal is best classified as **slightly flattening / no longer steepening** for the current run.
