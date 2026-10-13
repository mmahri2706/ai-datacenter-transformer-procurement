# Simulation

A Monte Carlo model of transformer procurement for one hypothetical data center project. **All inputs are placeholders** (see `params.py` and `docs/assumptions.md`), so the outputs show how the machinery behaves, not findings.

| File | What it does |
| --- | --- |
| `params.py` | Every model input in one place, each marked as a placeholder |
| `model.py` | The simulation: two kinds of delay (supplier-wide and unit-level), four strategies, one shared random world per run |
| `run_simulation.py` | Runs the nine decision-map cells and the delay-type sweep; writes the gold layer and `results/*.csv` |
| `decision_map.py` | Picks winners under the spending limit and draws `results/decision_map.png` and `results/delay_type_map.png` |
| `sanity_checks.py` | Five tests that the model behaves as the research design says it should |

## Run it

```bash
python simulation/sanity_checks.py      # about 1 second
python simulation/run_simulation.py     # about 10 seconds
python simulation/decision_map.py       # redraw the maps; try --budget 0.25
```

## What the sanity checks prove

1. Ordering 12 transformers instead of 10 from a backlogged supplier saves 0 months (and costs 20% more).
2. When single units fail, extra units do cut delay.
3. When backlogs are common, diversified sourcing cuts delay.
4. With no random problems, advance ordering shifts the ready date by exactly the advance months.
5. The same seed gives identical results.
