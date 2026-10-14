# Next steps (prioritized)

Order matters: each step unblocks the next. Time estimates assume one undergraduate working part-time.

## Do first (this week, before Week 2 begins)

- [ ] **1. Run the pipeline on your own computer.** The Week 1 workspace could not reach FRED. Follow "How to run" in the README, then check that `data/silver/transformer_ppi.parquet` exists and its latest month matches the FRED page. If it fails, copy the error message into the next session. *(30 min)*
- [ ] **2. Confirm the FRED series name.** Open `https://fred.stlouisfed.org/series/PCU335311335311` and check the title reads "Electric Power and Specialty Transformer Manufacturing." *(5 min)*
- [ ] **3. Confirm the spending limit and the transformer-class scope.** These are judgment calls made in Week 1 (`assumptions.md` section 4; `research_proposal.md` section 8). Keep them, or change them and say why. *(15 min)*
- [ ] **4. Read two primary sources yourself:** the DOE *Large Power Transformer Resilience* report (July 2024) and the LBNL *2024 U.S. Data Center Energy Usage Report*. Confirm the numbers quoted in `data_sources.md` against the PDFs, especially whether LBNL's 325-580 TWh is a 2028 total or an increase. Fix the doc if it is wrong. *(1-2 hours)*

## Weeks 2-3: bronze and silver layers, replace placeholders

- [ ] **5. Comtrade or Census import data.** Pick whichever works first. Pull U.S. imports for the transformer HS subheadings (first confirm the code definitions), save raw files to `data/bronze/` with the download date, then clean to `data/silver/`. Add `pipelines/03_fetch_trade.py` and `04_clean_trade.py`. *(Week 2)*
- [ ] **6. Import concentration metric.** From the silver trade table, compute each exporting country's share and a concentration index (HHI) by year. Use it to justify the *range* for supplier backlog probability (assumption row 5). It is evidence for a range, not a measurement of backlog. *(Week 2)*
- [ ] **7. Lead-time table.** Create `data/silver/lead_time_evidence.parquet` (or a small CSV in `docs/`) from the table in `assumptions.md`: one row per published figure, with source, date, class, weeks, months, and a flag for "survey" versus "estimate" versus "claim." Every row needs a citation. *(Week 2)*
- [ ] **8. Demand scenario table.** From IEA and LBNL, define low / base / high demand as growth in data center electricity use relative to 2023-2024. State the extrapolation from 2028 to 2030. Do not call it a transformer forecast. *(Week 3)*
- [ ] **9. Replace the placeholders in `simulation/params.py`, one assumption row at a time.** Start with the lead-time range (row 3) and `t_plan` (row 2), because they move everything. Change `PLACEHOLDER` tags in `assumptions.md` as you go. Re-run `sanity_checks.py` after each change. *(Week 3)*
- [ ] **10. Build the gold input table.** A DuckDB query that joins the silver tables into the scenario table the simulation reads, so one command rebuilds everything. *(Week 3)*

## Weeks 4-5: real-input decision map (the first headline)

- [ ] **11. Add 95% confidence intervals and a near-tie flag** to the winner rule (`decision_map.py`), so a cell is not "won" by noise (risk R4). *(Week 4)*
- [ ] **12. Report break-even delay cost** for each cell: extra cost per month of delay saved. *(Week 4)*
- [ ] **13. Run the nine-cell map and check it against hypotheses H1-H3.** Say plainly which are supported, which are not, and which depend on a stated assumption. *(Week 5)*
- [ ] **14. Update the README headline** with the real result and remove the placeholder warnings only where inputs have truly been replaced. *(Week 5)*

## Week 6: sensitivity and reality check

- [ ] **15. Sensitivity sweeps,** in this order: supplier-wide versus unit-level split (row 5 against rows 8-11); `t_plan`; demand-increase rule (rows 10-11); advance and diversified premiums; salvage; units per project; spending limit 0-30%. Chart which ones change the winner. *(Week 6)*
- [ ] **16. 2022-2024 sanity check.** Does a model run with 2021-style inputs (about 50-week lead times) and 2024-style inputs (about 120 weeks) show delay growing the way the published lead-time rise suggests? Compare with the FRED price series. This checks the *direction* of the model, not its exact numbers. *(Week 6)*

## Weeks 7-8: write-up and polish

- [ ] **17. Write the roughly 5-page paper:** question, data (real versus assumed), method, results, sensitivity, limitations. Use the limitations already drafted. *(Week 7)*
- [ ] **18. Final repo check:** fresh clone, new virtual environment, one command to rebuild everything, results match. *(Week 8)*
- [ ] **19. Optional only:** dashboard. First in line to cut if time runs short (see the fallback order in the proposal).

## Standing rules

- Never present a placeholder result as a finding.
- Every number in a figure needs a source or an `ASSUMPTION` tag.
- Report results as scenarios, not forecasts of real projects.
