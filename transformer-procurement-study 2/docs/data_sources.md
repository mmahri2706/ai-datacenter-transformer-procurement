# Data sources

Status key: **Not verified** (named in the plan, not yet checked), **Verified** (opened, confirmed it contains what we need, access works), **Rejected** (checked, not suitable; reason noted).

All of these are filled in during the week 1 data audit.

| Source | Intended use | Status | Exact dataset or series | Access method | Notes |
| --- | --- | --- | --- | --- | --- |
| International Energy Agency (IEA) | Data center electricity demand scenarios | Not verified | TBD | TBD | Check which scenarios are free to use and cite |
| UN Comtrade | Transformer trade flows and import concentration | Not verified | TBD (choose the product codes for transformers) | TBD | Confirm code definitions and whether the free tier covers the years needed |
| FRED / Bureau of Labor Statistics | Transformer producer price index history | Not verified | `PCU335311335311` (from memory, confirm the series title) | CSV download from FRED | Used by `pipelines/01_fetch_fred.py` |
| U.S. Department of Energy | Published transformer supply constraints and lead-time evidence | Not verified | TBD | TBD | Lead times are entered as ranges in `assumptions.md` |
| Company filings and industry reports | Procurement assumptions, only where disclosed | Not verified | TBD | TBD | Cite page and date for every number used |

## Rule for missing data

Where no public number exists, the input is a documented range (low, likely, high) in `assumptions.md`, never a single guess. The sensitivity analysis shows how much each range matters.
