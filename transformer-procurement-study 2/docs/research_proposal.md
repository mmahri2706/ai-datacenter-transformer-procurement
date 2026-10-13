# Buy Smarter or Build Bigger? A Transformer Supply Study for U.S. AI Data Centers Through 2030

**Duration:** 8 weeks (first research prototype)
**Area:** Operations research, supply chain management, business analytics

This study builds one result: a decision map that tells a data center developer, for each demand scenario and level of supplier uncertainty, whether buying transformers smarter or reserving extra capacity cuts delay more.

## 1. Research question and hypotheses

**Question:** For hypothetical U.S. AI data center projects through 2030, under which demand and supply conditions does smarter transformer procurement reduce delay more than simply reserving extra capacity?

- **H1:** When transformer lead times are long and unpredictable, diversified and advance procurement beat both reactive buying and extra capacity.
- **H2:** When lead times are short and stable, extra capacity is enough, and smarter procurement only adds cost.
- **H3:** Reserved extra capacity beats the other strategies only when unit-level problems (single late or failed units, demand increases) outweigh supplier-wide delay. Against a supplier-wide backlog, extra units from the same supplier do not help.

**The finish line is one figure, the decision map.** Its rows are three demand scenarios (low, base, high) and its columns are three levels of lead-time uncertainty (low, medium, high). Each of the nine cells shows which strategy wins, how many months of delay it saves, and what it costs.

## 2. Scope

- **In:** electrical transformers for hypothetical U.S. AI data center projects, each with a commissioning date and a transformer order.
- **Out (future work):** cooling equipment, grid interconnection delays, projects outside the U.S.
- **Why narrow:** one component and one country is what makes this finishable in eight weeks and keeps the data problem honest.

## 3. Strategies compared

The same simulated projects run under each strategy, so the only thing that changes is how transformers are bought.

| Strategy | What the developer does | Why it is in the study |
| --- | --- | --- |
| Reactive single source | Orders from one supplier when the project is approved | Baseline: how most projects behave without planning |
| Advance procurement | Orders earlier, before the project is fully approved | Tests buying time with money |
| Diversified sourcing | Splits the order across two or more suppliers | Tests protection against one supplier slipping |
| Reserved extra capacity | Orders a fixed share of extra transformers (10%, 20%, or 30% above the base need) from one supplier at approval, held as spares | The expansion option: the main rival to smarter buying |

**Fair comparison rule:** every strategy is scored on both delay and total cost. The map names a winner only among strategies that stay within a spending limit, a parameter chosen in week 1, so strategies are compared at similar cost.

**Why extra units help, and when they do not.** More transformers do not automatically mean faster completion. If all 10 units from one supplier are held in the same six-month backlog, ordering 12 from that supplier gives 12 late units. The model separates three kinds of problem:

| Problem | What happens | Which strategy helps |
| --- | --- | --- |
| Supplier-wide delay | A backlog hits every unit from one supplier at once | Diversified sourcing, by re-sourcing from a healthy supplier. Extra units do not help. |
| Unit-level problems | One unit arrives late or fails inspection while the others are fine | Reserved extra capacity |
| Demand increase | The project needs more units than planned | Reserved extra capacity |

The share of delay that is supplier-wide versus unit-level cannot be read directly from public data. It is entered as a documented range and is the first sensitivity test. Advance procurement removes no risk; it starts the clock earlier at a higher cost.

## 4. Data and how gaps are handled

See `data_sources.md` for the status of each source. Where no public number exists, such as exact lead times, the input is a documented range (low, likely, high), never a single guess. The sensitivity analysis then shows how much each range matters, so a data gap becomes a finding instead of a flaw.

## 5. Methods

1. **Build the scenarios.** Turn published low, base, and high demand projections into the number of transformers a set of hypothetical projects would need each year.
2. **Measure supply risk.** From trade and price data, describe how concentrated transformer imports are and how prices moved. Use this to set the supply and lead-time ranges.
3. **Simulate.** A Monte Carlo simulation in Python runs each strategy thousands of times per scenario. Each run draws supplier-wide delays and unit-level problems separately, so every strategy faces the same randomly generated world.
4. **Score and map.** For each run, record delay in months, total cost, and whether the deadline was met. Average the runs and fill the decision map.

**Data lake:** Python, DuckDB, and Parquet, with bronze (raw downloads), silver (cleaned tables), and gold (simulation inputs and results) layers. One command rebuilds everything from scratch.

## 6. Definition of done and fallback

The project counts as finished when all four of these exist:

- The decision map, with all nine cells filled and confidence intervals
- A sensitivity chart showing which input ranges change the winner
- A GitHub repo that rebuilds the data lake and the map with one command
- A README plus a short write-up (about 5 pages) that states findings and limits

**If time runs short,** cut in this order: the dashboard first, then the price-trend analysis, then the high-uncertainty column. The map and the repo are never cut.

**Check against reality:** test whether the model reproduces the 2022-2024 period, when transformer lead times stretched, as a sanity check on the delay behavior.

## 7. Limitations

- Public data cannot name every supplier or show contract delivery times, so lead times are ranges.
- The share of transformer demand caused by AI data centers must be assumed, and the assumption is stated.
- Results show how strategies behave under stated scenarios. They are not forecasts of real projects.
- Findings cover transformers only and say nothing about total data center completion time.

## 8. Timeline

The first version of the decision map is due by the end of week 5.

| Weeks | Objective | Deliverable |
| --- | --- | --- |
| 1 | Lock the question, scope, and strategy definitions; audit data sources | One-page plan and source list |
| 2-3 | Build the bronze and silver layers; set demand scenarios and lead-time ranges | Cleaned data and scenario tables |
| 4-5 | Build the simulation and run all four strategies | First decision map (checkpoint) |
| 6 | Sensitivity analysis and the 2022-2024 sanity check | Sensitivity chart |
| 7 | Fix problems found; write the limitations and findings | Draft write-up |
| 8 | Finish the repo, README, and write-up; optional dashboard | Final portfolio piece |
