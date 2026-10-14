# Assumptions log

Every assumption in the model goes here, with its source or a note that it is an assumption. A missing public number becomes a documented range, never a single guess.

**Week 1 status (13 Oct 2026):** definitions, the delay and cost formulas, and the spending limit are now fixed (sections 1-4). The numeric inputs in `simulation/params.py` are **still placeholders** on purpose; section 5 shows, for each one, what the Week 1 data audit found and what range is proposed to replace it in Weeks 2-3. Nothing here is a research finding.

**Status key**

| Tag | Meaning |
| --- | --- |
| `PLACEHOLDER` | The value currently in `params.py`. Made up so the simulation runs. No evidence behind it. |
| `EVIDENCE` | A public source gives a number or range that can anchor the input. Source in `data_sources.md`. |
| `ASSUMPTION` | No public number exists. A deliberate modeling choice, stated as a range and tested in the sensitivity analysis. |

---

## 1. Key variables (plain-language glossary)

| Name in code | Meaning | Unit |
| --- | --- | --- |
| time 0 | The day the project is formally approved. All times are counted from here. | months |
| `n_units` | Transformers the project needs | units |
| `t_plan` | The date the rest of the project needs the transformers installed (set by the construction schedule, **not** by procurement) | months after approval |
| lead time | Months from placing an order to a unit arriving, with no problems. Drawn from a triangular range (low, most likely, high), then multiplied by the demand scenario's `lead_mult` | months |
| supplier-wide backlog | Months added to **every** unit from one supplier. Happens with probability `p_backlog`, size drawn from a triangular range | months |
| unit-level delay | Small extra delay for one unit (exponential, mean `unit_delay_mean`) | months |
| unit failure | A unit fails inspection (probability `p_fail`) and must be replaced by a fresh order | yes/no |
| demand increase | The project turns out to need `upsize_units` more units, found at `upsize_month` (probability `p_upsize`) | yes/no |
| demand scenario | low / base / high. Sets `lead_mult` (how tight the market is) and `p_upsize` | - |
| uncertainty level | low / medium / high. Sets `p_backlog`, `unit_delay_mean`, `p_fail` | - |

## 2. How delay is calculated

For one simulated project under one strategy:

1. Every ordered unit gets an arrival time: `order time + lead time + its supplier's backlog + its own unit delay`.
2. Failed units are dropped. If too few usable units remain (failures, or a demand increase with no spares), a top-up order is placed and arrives after a fresh lead time.
3. `ready date` = arrival of the **last unit that is needed** (spares can let the project skip the slowest ones).
4. **`delay = max(0, ready date - t_plan)`** in months. Early arrival earns no credit.

The reported **expected delay** is the average over thousands of runs. Every strategy is run on the *same* random world each time, so differences come from the strategy, not luck. **Delay reduction** = baseline expected delay minus the strategy's expected delay.

*Worked example (placeholder numbers, no random problems):* lead time 14 months, `t_plan` 18 months. Reactive: ready at 14, delay 0. This is why `t_plan` matters so much; see risk R1 in section 7.

## 3. How cost is calculated

Cost is measured in **units of one transformer's baseline price (= 1.0)**. No dollar price is assumed, because none was verified. A dollar figure can be added later by multiplying by a price the user supplies.

**Total procurement-related cost** = units bought x price per unit (with any premium)
+ expected fee for a wasted advance order
+ fee for cancelling a re-routed order
+ top-up units bought at price 1.0
- salvage value of unused spares.

| Strategy | Cost with no problems (n = 10) | Why |
| --- | --- | --- |
| Reactive single source | 10.0 | 10 units x 1.00 |
| Advance procurement | 11.8 | 10 x 1.12 premium + 10 x 15% chance x 0.40 fee |
| Diversified sourcing | 10.5 | 10 x 1.05 premium (re-route fees added only when a re-route happens) |
| Reserved +10% / +20% / +30% | 11.0 / 12.0 / 13.0 | 11 / 12 / 13 units x 1.00, no salvage |

These match `results/sensitivity_delay_type.csv` for the no-problem row. Under real conditions the baseline also pays for top-up orders, so a reserve strategy's *average* extra cost versus baseline is smaller than its nominal 10/20/30% (the placeholder run shows about +7% to +14%).

**What cost leaves out, on purpose:** the business cost of a delayed data center (lost revenue, penalties, idle crews). That number is project-specific and not public. Instead the results will report a **break-even delay cost**: `(strategy cost - baseline cost) / months of delay saved`, in transformer-prices per month. If a month of delay costs a developer more than that, the strategy pays for itself.

## 4. The spending limit (fixed in Week 1)

> A strategy may be named the winner of a decision-map cell only if its **average total cost is no more than 15% above the baseline's average total cost** in that same cell. Among eligible strategies, the winner is the one with the lowest expected delay. If it saves less than 0.25 months versus the baseline, the cell reads "reactive is enough."

- **Why relative to the baseline's cost:** the baseline itself pays for top-ups, so comparing all-in expected cost is fairer than comparing purchase prices.
- **Why 15%:** it is a policy choice, not a measured number; no public source defines a normal budget. 15% sits between the +10% and +20% reserve options, so the rule does not mechanically exclude or favor one reserve level. **This is a judgment call for the researcher to confirm.**
- **Required robustness check:** redraw the map at 0%, 5%, 10%, 15%, 20%, and 30%. (`decision_map.py --budget` already does this.) A conclusion that flips between 10% and 20% is reported as sensitive to the budget, not as a clean finding.

## 5. Assumption tables

### Project setup

| # | Assumption | Current value | Status | What the Week 1 audit found, and proposed replacement |
| --- | --- | --- | --- | --- |
| 1 | Transformers a project needs | 10 units | `PLACEHOLDER` / `ASSUMPTION` | No public source for units per data center was verified. Keep 10 as the base toy project; test 6, 10, 20 in sensitivity. State clearly this is a hypothetical project. |
| 2 | `t_plan`: date the transformers are needed, months after approval | 18 months | `PLACEHOLDER` / `ASSUMPTION` | No public schedule data verified. **Most influential design choice** (risk R1). Proposed rule: set `t_plan` from the scenario's typical quoted lead time plus a small float, so delay measures deviation from what the developer was told. Test 3 values. |
| 3 | Base lead time (low, most likely, high) | 10, 14, 20 months | `PLACEHOLDER`; **contradicted by evidence** | See "Lead-time evidence" below. For substation-class power transformers, public sources point to roughly **18 / 28 / 48 months**, not 10 / 14 / 20. |
| 4 | Lead-time multiplier by demand scenario (low, base, high) | 0.85, 1.0, 1.3 | `PLACEHOLDER` | The high value has an anchor: DOE says lead times are "often 36 months," and 36 / 27.6 = 1.3. The low value is `ASSUMPTION`; the 2021 market (about 50 weeks) is 0.4x, so test 0.6 to 0.85. |

**Lead-time evidence (all secondary reports; see `data_sources.md` for caveats).** Weeks are converted at 4.345 weeks per month.

| Evidence | Weeks | Months | Source |
| --- | --- | --- | --- |
| Power transformers, 2021 | about 50 | about 11.5 | Wood Mackenzie (Apr 2024) |
| Power transformers, 2024 average | about 120 | about 27.6 | Wood Mackenzie (Apr 2024) |
| Large power (substation, GSU) range, 2024 | 80 to 210 | 18.4 to 48.3 | Wood Mackenzie (Apr 2024) |
| Power transformers, Q2 2025 survey average | 128 | 29.5 | WoodMac, via POWER Magazine (Jan 2026) |
| Generator step-up, Q2 2025 survey average | 144 | 33.1 | WoodMac, via POWER Magazine (Jan 2026) |
| Large power transformers, "often" and maximum | - | 36 and 60 | U.S. DOE, *Large Power Transformer Resilience* (Jul 2024) |
| Before COVID-19 | - | under 12 | U.S. DOE (Jul 2024) |
| One vendor's claim: 12 to 14 months after drawings approved | - | 12 to 14 | Bolt Electrical, in POWER Magazine (Jan 2026); a single unverified claim that disputes a shortage |

A distribution or pad-mount transformer is a different, faster product. **Scope decision:** the primary model covers **substation-class power transformers** (the units that gate a data center's grid connection); medium-voltage distribution transformers are a possible secondary run. This narrows "electrical transformers" in the original scope but does not change the research question.

### Supplier-wide delay (hits every unit from one supplier at once)

| # | Assumption | Current value | Status | Audit finding / proposed replacement |
| --- | --- | --- | --- | --- |
| 5 | Chance a supplier is backlogged, by uncertainty level (low, medium, high) | 5%, 15%, 30% | `PLACEHOLDER` / `ASSUMPTION` | **Not observable in public data.** WoodMac reports a 30% supply deficit for power transformers in 2025, and DOE reports about 40% domestic factory utilization, but neither gives a per-supplier backlog probability. Keep as a range; **testing the supplier-wide versus unit-level split is the first sensitivity analysis.** |
| 6 | Size of a backlog (low, most likely, high) | 4, 8, 16 months | `PLACEHOLDER` | The 2021 to 2024 lead-time rise (about 16 months) is a rough yardstick for a market-wide episode. Use for the 2022-2024 sanity check. |
| 7 | Month a backlog becomes visible to the buyer | 3 | `PLACEHOLDER` / `ASSUMPTION` | No public data. Test 1, 3, 6. |

### Unit-level problems (one unit, not the whole supplier)

| # | Assumption | Current value | Status | Audit finding / proposed replacement |
| --- | --- | --- | --- | --- |
| 8 | Average extra delay per unit, by uncertainty level | 0.5, 1.0, 2.0 months | `PLACEHOLDER` / `ASSUMPTION` | No public data found. |
| 9 | Chance a unit fails inspection, by uncertainty level | 2%, 4%, 8% | `PLACEHOLDER` / `ASSUMPTION` | No public data found. |
| 10 | Chance the project needs more units than planned, by demand scenario | 10%, 20%, 35% | `PLACEHOLDER` / `ASSUMPTION` | No public data. Demand growth (IEA, LBNL) is about electricity use, not unit counts, so the link is an assumption. |
| 11 | Extra units needed if demand rises, and the month it is discovered | 2 units, month 6 | `PLACEHOLDER` / `ASSUMPTION` | No public data. |

### Strategy costs (unit price = 1.0)

| # | Assumption | Current value | Status | Audit finding / proposed replacement |
| --- | --- | --- | --- | --- |
| 12 | Advance procurement: months ordered before approval | 4 | `PLACEHOLDER` / `ASSUMPTION` | POWER Magazine (Jan 2026) reports utilities treating early procurement as a competitive lever, but gives no durations. Test 2, 4, 8, 12 months. |
| 13 | Advance procurement: price premium | 12% | `PLACEHOLDER` / `ASSUMPTION` | No sourced premium. One broker says he adds 12-15% to factory cost (a single claim, not a market figure). Test 0% to 25%. |
| 14 | Advance: chance the early order is wasted, and fee if so | 15%, fee 40% | `PLACEHOLDER` / `ASSUMPTION` | No public data on cancellation terms. Never state as fact. |
| 15 | Diversified sourcing: price premium | 5% | `PLACEHOLDER` / `ASSUMPTION` | Extra qualification and coordination. Test 0% to 15%. |
| 16 | Diversified: fee for cancelling a re-routed order | 20% | `PLACEHOLDER` / `ASSUMPTION` | No public data. |
| 17 | Reserved extra capacity: extra units | 10%, 20%, 30% | **Fixed by the research design** | Rounded up to whole units. Not an assumption; part of the strategy definition. |
| 18 | Salvage value of unused spares | 0% | `ASSUMPTION` | Conservative. DOE describes shared spare pools (e.g. Grid Assurance) as an alternative, so test 0%, 25%, 50% salvage as a stand-in for resale or reuse. |
| 19 | Spending limit | 15% above baseline average cost | **Decided in Week 1** (see section 4) | A policy parameter; robustness shown at 0-30%. |

## 6. Modeling rules (design choices, not data)

- **One shared world per run.** All strategies are tested on the same random draws.
- **Backlog rule.** An order placed at time t to a backlogged supplier takes its normal lead time plus whatever backlog is left at time t.
- **Baseline cannot switch supplier.** Reactive single sourcing stays with its supplier even when it is backlogged.
- **Extra units from the same supplier do not escape a backlog.** They are delayed along with the rest. (Sanity check 1 proves this.)
- **The project waits for its slowest needed unit.** Spares help against single late units because the project can skip the slowest ones.
- **A demand increase is costly without spares.** Without spares, extra units need a fresh order with a full lead time. This one rule drives much of the spares advantage; test it.
- **Replacements.** If failures or a demand increase leave too few usable units, a top-up order is placed at the first moment the problem is known, with a fresh lead time.
- **Advance procurement removes no risk.** It shifts the order earlier by `advance_months`, at a premium plus an expected waste fee.
- **Diversified sourcing uses two suppliers** and re-routes only when exactly one is backlogged and re-routing is expected to arrive sooner.

## 7. Known modeling risks to test (found in the Week 1 review)

| ID | Risk | Why it matters | Planned test |
| --- | --- | --- | --- |
| R1 | **`t_plan` is arbitrary.** Delay is clipped at zero, so the whole map moves with it. With the placeholder 18-month plan and the evidence-based 28-month lead time, every project would be late. | Could decide which strategy wins | Week 3: choose the rule in row 2; Week 6: sweep 3 values |
| R2 | **Reserved capacity wins all nine cells in the placeholder run,** including low demand and low uncertainty. This may come from rows 10-11 (a demand increase forces a full fresh lead time) and not from anything real. It contradicts hypothesis H2 only because of placeholder inputs. | Do not report as a finding | Sweep rows 10, 11 and 14 before trusting any cell |
| R3 | **Evidence-based lead times are 2x longer than the placeholders,** so backlog sizes (4/8/16) and advance months (4) are now small in comparison. | Changes how much each strategy can help | Re-scale after row 3 is updated |
| R4 | **Winner is picked on the mean alone.** Differences smaller than the simulation noise (see `se_delay`) can look like wins. | Overconfident map | Week 5: add 95% intervals and flag near-ties |
| R5 | **One project, 10 units, two suppliers.** Real developers order many units and may have more suppliers. | Limits generality | State in limitations; sweep `n_units` |
| R6 | **Trade concentration is not yet used.** Row 5 is meant to be linked to import concentration in Week 3. | Backlog probability stays unsupported | Week 3 |
