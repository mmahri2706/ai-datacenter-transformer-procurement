# Assumptions log

Every assumption in the model goes here, with its source or a note that it is an assumption. A missing public number becomes a documented range, never a single guess.

**Status key:** `PLACEHOLDER` = a made-up number used only so the simulation runs end to end. It has no evidence behind it and must be replaced or justified before any result is reported. The same values live in `simulation/params.py`.

## Project setup

| # | Assumption | Value | Status | Source or reason |
| --- | --- | --- | --- | --- |
| 1 | Transformers a project needs | 10 units | PLACEHOLDER | Round number for the toy project |
| 2 | Planned equipment-ready date, counted from project approval | 18 months | PLACEHOLDER | Delay is measured against this date. Chosen so the toy project has a real chance of delay; replace with a realistic project schedule. |
| 3 | Base lead time (low, most likely, high) | 10, 14, 20 months | PLACEHOLDER | Replace with a range from DOE and industry reports |
| 4 | Lead-time multiplier by demand scenario (low, base, high) | 0.85, 1.0, 1.3 | PLACEHOLDER | Higher demand tightens the market; derive from the IEA scenarios |

## Supplier-wide delay (hits every unit from one supplier at once)

| # | Assumption | Value | Status | Source or reason |
| --- | --- | --- | --- | --- |
| 5 | Chance a supplier is backlogged, by uncertainty level (low, medium, high) | 5%, 15%, 30% | PLACEHOLDER | Link to trade concentration and price spikes in week 3. **The share of supplier-wide versus unit-level delay is the key unknown, tested first in the sensitivity analysis.** |
| 6 | Size of a backlog (low, most likely, high) | 4, 8, 16 months | PLACEHOLDER | Check against 2022-2024 episodes |
| 7 | Month a backlog becomes visible to the buyer | 3 | PLACEHOLDER | Lets diversified sourcing re-route |

## Unit-level problems (one unit, not the whole supplier)

| # | Assumption | Value | Status | Source or reason |
| --- | --- | --- | --- | --- |
| 8 | Average extra delay per unit, by uncertainty level | 0.5, 1.0, 2.0 months | PLACEHOLDER | Assumed |
| 9 | Chance a unit fails inspection, by uncertainty level | 2%, 4%, 8% | PLACEHOLDER | Assumed |
| 10 | Chance the project needs more units than planned, by demand scenario (low, base, high) | 10%, 20%, 35% | PLACEHOLDER | Assumed |
| 11 | Extra units needed if demand rises, and the month it is discovered | 2 units, month 6 | PLACEHOLDER | Assumed |

## Strategy costs (unit price = 1.0)

| # | Assumption | Value | Status | Source or reason |
| --- | --- | --- | --- | --- |
| 12 | Advance procurement: months ordered before approval | 4 | PLACEHOLDER | Assumed |
| 13 | Advance procurement: price premium | 12% | PLACEHOLDER | Assumed |
| 14 | Advance procurement: chance the early order is wasted, and fee if so | 15%, fee 40% of price | PLACEHOLDER | Assumed; added as an expected cost |
| 15 | Diversified sourcing: price premium | 5% | PLACEHOLDER | Extra qualification and coordination |
| 16 | Diversified sourcing: fee for cancelling a re-routed order | 20% of price | PLACEHOLDER | Assumed |
| 17 | Reserved extra capacity: extra units | 10%, 20%, 30% of base need | PLACEHOLDER | Rounded up to whole units |
| 18 | Salvage value of unused spares | 0% | PLACEHOLDER | Conservative: unused spares are a full cost |
| 19 | Spending limit for naming a winner | 15% above the baseline's average cost | PLACEHOLDER | Choose in week 1; the decision map changes with it, so results are also shown at other limits |

## Modeling rules (design choices, not data)

- **One shared world per run.** All strategies are tested on the same random draws, so differences come from the strategy and not from luck.
- **Backlog rule.** An order placed at time t to a backlogged supplier takes its normal lead time plus whatever backlog is left at time t.
- **Baseline cannot switch supplier.** Reactive single sourcing stays with its supplier even when it is backlogged.
- **Extra units from the same supplier do not escape a backlog.** They are delayed along with the rest.
- **The project waits for its slowest needed unit.** Ready date = arrival of the last unit needed. This is why spares help against single late units: they let the project skip the slowest ones.
- **A demand increase is costly without spares.** Without spares, extra units need a fresh order with a full lead time. This one rule drives much of the spares advantage, so test it in the sensitivity analysis.
- **Replacements.** If failures or a demand increase leave too few usable units, a top-up order is placed at the first moment the problem is known, with a fresh lead time.
