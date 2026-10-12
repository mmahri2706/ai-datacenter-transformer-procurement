# Buy Smarter or Build Bigger? A Transformer Supply Study for U.S. AI Data Centers Through 2030

> **Headline result:** _to be added at the week 5 checkpoint (the decision map)._

## Research question

For hypothetical U.S. AI data center projects through 2030, under which demand and supply conditions does smarter transformer procurement reduce delay more than simply reserving extra capacity?

## What this project produces

One **decision map**: three demand scenarios (low, base, high) by three levels of lead-time uncertainty (low, medium, high). Each cell shows which procurement strategy wins, how many months of delay it saves, and what it costs.

## Strategies compared

| Strategy | What the developer does |
| --- | --- |
| Reactive single source | Orders from one supplier when the project is approved (baseline) |
| Advance procurement | Orders earlier, before the project is fully approved |
| Diversified sourcing | Splits the order across two or more suppliers |
| Reserved extra capacity | Locks in surplus transformer capacity from the start, with one supplier |

## Scope

In: electrical transformers for hypothetical U.S. AI data center projects.
Out (future work): cooling equipment, grid interconnection delays, projects outside the U.S.

## Data lake layers

| Layer | Folder | Contents |
| --- | --- | --- |
| Bronze | `data/bronze/` | Raw downloads, untouched, with the download date |
| Silver | `data/silver/` | Cleaned, standardized Parquet tables |
| Gold | `data/gold/` | Simulation inputs and results |

Data files are not committed. Every file is rebuilt by the scripts in `pipelines/`.

## How to run

```bash
pip install -r requirements.txt
python pipelines/01_fetch_fred.py     # bronze: transformer price index from FRED
python pipelines/02_clean_fred.py     # silver: cleaned Parquet table
```

More pipeline steps and the simulation are added in weeks 2-5. See `docs/assumptions.md` for every assumption in the model.

## Status

- [x] Repo skeleton
- [ ] Week 1: data source audit
- [ ] Weeks 2-3: bronze and silver layers, scenarios, lead-time ranges
- [ ] Weeks 4-5: simulation and first decision map
- [ ] Week 6: sensitivity analysis and 2022-2024 sanity check
- [ ] Weeks 7-8: write-up, README headline, optional dashboard

## Limitations

Public data cannot name every supplier or show contract delivery times, so lead times are ranges. The share of transformer demand caused by AI data centers is assumed and stated. Results show how strategies behave under stated scenarios; they are not forecasts of real projects.
