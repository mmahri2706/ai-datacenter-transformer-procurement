# Data sources

**Week 1 audit, 13 Oct 2026.**

**Status key**

| Status | Meaning |
| --- | --- |
| **Verified** | Page or document opened, and it contains what the project needs |
| **Partly verified** | Exists and looks right, but a key detail is unconfirmed (named in the notes) |
| **Not tested** | Candidate only. Nothing opened or run yet |
| **Rejected** | Checked and not suitable |

**How this audit was done, and its limit.** The cloud workspace used for Week 1 cannot reach FRED, BLS, Comtrade, DOE, or IEA directly (its network is restricted to package registries and GitHub). Sources were therefore opened with a web-reading tool that returns a *summary* of each page. Every number below came from such a read and should be **re-checked against the original page or PDF when you cite it in the write-up**. The scripts in `pipelines/` have not yet been run against the live sites. Your first task is to run them on your own computer (see `next_steps.md`).

---

## A. Data the model will use directly

| Source | Intended use | Status | Exact dataset | Access | What it contains | Key limitations |
| --- | --- | --- | --- | --- | --- | --- |
| **FRED / BLS** | Transformer price history; 2022-2024 sanity check | **Verified** (page); download **not tested** | Series `PCU335311335311`, "Producer Price Index by Industry: Electric Power and Specialty Transformer Manufacturing". Monthly, not seasonally adjusted, index Jun 1981 = 100, from Jan 1967. Page showed a latest value of 475.065 for Aug 2026. Not discontinued. | `https://fred.stlouisfed.org/graph/fredgraph.csv?id=PCU335311335311` (used by `pipelines/01_fetch_fred.py`); backup: BLS API | Producer prices received by U.S. manufacturers | **Prices only, not lead times.** Industry-wide: mixes power, distribution, and specialty transformers and is not specific to data centers. Measures manufacturers' selling prices, which can lag spot or expedited prices. One correction: the script docstring named the series "Power, Distribution, and Specialty Transformer Manufacturing" (the NAICS name). The FRED title is as shown here. |
| **U.S. DOE, *Large Power Transformer Resilience*** (Report to Congress, July 2024) | Lead-time range; import dependence; reserve options | **Verified** (content read) | Official report PDF on energy.gov | Free PDF | Lead times "often 36 months," maximum 60 (Sec. II.1, p. 3); before COVID-19, under a year. In 2019, imports supplied 82% of large power transformers (617 units) versus 18% domestic (137). Domestic capacity about 343 units a year at about 40% utilization. Grain-oriented electrical steel and copper each about 25% of production cost. Discusses shared spare pools (e.g. Grid Assurance). | Not a time series, so it gives a snapshot not a trend. Covers *large* power transformers (above about 60 MVA in the report's import figures), so it may overstate lead times for smaller substation units. |
| **Wood Mackenzie** (public press and articles only) | Lead-time anchors; supply deficit; import share | **Partly verified** | (a) Opinion piece, 2 Apr 2024: lead times about 50 weeks (2021) to about 120 weeks (2024); large power transformers 80 to 210 weeks. (b) Press release, 14 Aug 2025: 2025 supply deficit 30% power and 10% distribution transformers; import share 80% and 50%. (c) Q2 2025 survey, as reported by POWER Magazine (2 Jan 2026): power 128 weeks, generator step-up 144 weeks; unit prices since 2019 up 77% (power), 45% (GSU), up to 95% (some distribution). | Free public pages; full reports are paid and **not used** | Best public lead-time anchors available | **Proprietary data, methodology not disclosed** in what is public. The 2024 piece does not say whether its figures are a survey or an estimate. Cite as "Wood Mackenzie, as reported by...", never as raw data. |
| **UN Comtrade** | Import concentration by supplier country (to inform backlog probability and diversification feasibility) | **Not tested** | HS 8504 subheadings for transformers (liquid-dielectric 8504.21-.23 and other 8504.31-.34, from the HS nomenclature; **confirm code definitions in Comtrade before use**) | `comtradeapicall` Python package. Per its documentation, the keyless preview returns up to 500 records a call and a free subscription key allows up to 250,000. **Confirm the current free-tier terms on the Comtrade site.** | Trade value, weight, quantity by partner country | Records which *countries* sold, not which *firms*, and nothing about delivery times. HS codes do not separate data-center-class units. Recent months can be revised or missing. |
| **U.S. Census Bureau, International Trade API** (added candidate) | Same use as Comtrade; may be easier for U.S. imports at finer HS detail | **Not tested** | Dataset "Time Series International Trade: Monthly U.S. Imports by Harmonized System (HS) Code" | `api.census.gov/data/timeseries/intltrade/imports/hs` (listed in the data.gov catalog; **key requirement not confirmed**) | U.S. imports by HS code and country | Same limits as Comtrade. Added because the original plan lists only Comtrade; use whichever works first and cite the choice. |
| **IEA, *Energy and AI*** (2025) | Demand scenarios | **Verified** (summary page) | Report and its scenarios | Free IEA account needed to download. Licence CC BY 4.0. Cite as IEA (2025). | Data centres used about 415 TWh in 2024 (about 1.5% of world electricity; the U.S. about 45% of that). Global demand about 945 TWh by 2030 (more than double). Cases: Base, Lift-Off, Headwinds, High Efficiency. | Measures **electricity (TWh), not transformers or MW.** Mostly global. The 2030 U.S. figure and the downloadable dataset were not found on the summary page; confirm in the full report. The page shows both 2025 and 2026 as the year; check before citing. |
| **LBNL / DOE, *2024 United States Data Center Energy Usage Report*** (19 Dec 2024) (added candidate) | U.S.-specific demand range | **Partly verified** | Report by Shehabi et al., DOI 10.71468/P1WC7Q; announced by DOE on 20 Dec 2024 | Free; licence not stated on the landing page | As reported by DOE: data centers used about 4.4% of U.S. electricity (176 TWh) in 2023, and a projected 6.7% to 12% in 2028. | Ends in **2028**; the study runs to 2030, so extrapolation must be stated. A DOE summary lists "325 to 580 TWh" as an *increase*, but 325 / 176 and the 6.7% to 12% share suggest these are *total* 2028 use. **Open the PDF and confirm before using.** Added because it is the U.S.-specific DOE-sponsored source. |

## B. Context and secondary sources (cite carefully, not used as model inputs)

| Source | Use | Status | Caution |
| --- | --- | --- | --- |
| POWER Magazine, "Transformers in 2026" (2 Jan 2026) | Reports Wood Mackenzie 2025 numbers; presents the opposing view that "there is not a shortage" (one vendor claims 12 to 14 month delivery and a 12-15% markup) | **Verified** (read) | Secondary; the dissenting vendor claim is unverified. It is useful as the **low end** of the lead-time range and as a reminder the evidence is contested. |
| NIAC draft report, "Addressing the Critical Shortage of Power Transformers..." (June 2024) | Repeats Wood Mackenzie's 120-week average and 80-210 week range; says U.S. domestic share of large power transformers is about 20%; prices up about 80% since the pandemic | **Verified** (read) | **Marked "DRAFT // PRE-DECISIONAL."** Contains an apparent typo ("2 to 41 years"). **Do not cite that number.** |
| Company filings and industry reports (manufacturers, utilities, data center developers) | Procurement behavior, advance-order practice | **Not tested** | Not checked in Week 1. Cite page and date for any number used. Optional in Weeks 2-3. |

## C. What is real data and what is assumed

| Model input | Real data available? | Where it comes from |
| --- | --- | --- |
| Transformer price history | **Yes** | FRED PPI series |
| Lead-time level and trend (2021-2025) | **Yes, as secondary-reported ranges** | Wood Mackenzie (via public pages), DOE |
| Import dependence | **Yes, as of 2019 and 2025 estimates** | DOE, Wood Mackenzie |
| U.S. data center electricity demand | **Yes, to 2028** | LBNL/DOE (confirm figures) |
| Global data center demand to 2030 and 2035 | **Yes** | IEA |
| Number of transformers per data center | **No** | Assumption |
| Project schedule (`t_plan`) | **No** | Assumption |
| Supplier backlog probability, size, and visibility | **No** | Assumption, tested in sensitivity analysis |
| Unit failure and unit-delay rates | **No** | Assumption |
| Chance a demand increase hits a project | **No** | Assumption |
| Advance-order premium and cancellation terms | **No** | Assumption |
| Diversified-sourcing premium and cancellation fee | **No** | Assumption |
| Supplier contracts, actual delivery times of any company | **No** | Not used. Never invented. |

## D. Overall conclusions of the audit

1. **The placeholder lead times are too short.** Public sources point to about 18 / 28 / 48 months for substation-class units, versus the placeholders of 10 / 14 / 20. Updating them is the top Week 2-3 task.
2. **Prices and lead times are well supported; backlog and unit-level behavior are not.** The decision map's central unknown (supplier-wide versus unit-level delay) has no public data, so it must remain a tested range.
3. **Demand data measures electricity, not transformers.** Turning TWh growth into transformer scarcity needs an explicit, stated assumption.
4. **Nothing here is data-center-specific.** All transformer evidence is for the U.S. grid in general.

## Rule for missing data

Where no public number exists, the input is a documented range (low, likely, high) in `assumptions.md`, never a single guess. The sensitivity analysis shows how much each range matters.
