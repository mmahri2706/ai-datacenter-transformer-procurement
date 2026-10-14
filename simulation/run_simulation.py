"""Run the simulation for all nine decision-map cells plus the sensitivity sweep.

Usage:  python simulation/run_simulation.py [--runs 5000] [--seed 2026]

Writes (gold layer, not committed):  data/gold/sim_results.parquet
                                     data/gold/sensitivity_delay_type.parquet
Writes (small, committed):           results/sim_results.csv
                                     results/sensitivity_delay_type.csv

ALL INPUTS ARE PLACEHOLDERS (see params.py and docs/assumptions.md).
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from model import run_cell
from params import DEMAND, STRATEGIES, UNCERTAINTY, Params

BACKLOG_SWEEP = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]       # chance a supplier is backlogged
# Scales ALL unit-level problems together: single-unit lateness, inspection failures,
# and the chance the project grows. 0 = none, 1 = the base case (medium uncertainty,
# base demand).
UNIT_SCALE_SWEEP = [0.0, 0.25, 0.5, 1.0, 2.0]

ROOT = Path(__file__).resolve().parent.parent
GOLD = ROOT / "data" / "gold"
RESULTS = ROOT / "results"


def summarize(delays, costs):
    n = len(delays)
    return {
        "mean_delay": delays.mean(),
        "se_delay": delays.std(ddof=1) / np.sqrt(n),
        "mean_cost": costs.mean(),
        "p_on_time": float((delays <= 1e-9).mean()),
        "runs": n,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=5000)
    parser.add_argument("--sweep-runs", type=int, default=3000)
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()

    p = Params()
    GOLD.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)

    # --- The nine-cell grid: demand scenario x uncertainty level ---
    rows = []
    idx = 0
    for d_name, d in DEMAND.items():
        for u_name, u in UNCERTAINTY.items():
            rng = np.random.default_rng([args.seed, idx])
            out, _ = run_cell(rng, args.runs, p, d["lead_mult"], d["p_upsize"],
                              u["p_backlog"], u["unit_delay_mean"], u["p_fail"], STRATEGIES)
            for s, (delays, costs) in out.items():
                rows.append({"demand": d_name, "uncertainty": u_name, "strategy": s,
                             **summarize(delays, costs)})
            idx += 1
            print(f"cell {idx}/9 done: {d_name} demand, {u_name} uncertainty")
    grid = pd.DataFrame(rows)
    grid.to_parquet(GOLD / "sim_results.parquet", index=False)
    grid.round(4).to_csv(RESULTS / "sim_results.csv", index=False)

    # --- Key sensitivity: which kind of delay dominates? (base demand) ---
    # x: how often a supplier is backlogged (supplier-wide delay)
    # y: how severe unit-level problems are (late units, failures, project growth)
    base = DEMAND["base"]
    med = UNCERTAINTY["medium"]
    rows = []
    k = 0
    for p_backlog in BACKLOG_SWEEP:
        for scale in UNIT_SCALE_SWEEP:
            rng = np.random.default_rng([args.seed, 100 + k])
            out, _ = run_cell(rng, args.sweep_runs, p, base["lead_mult"],
                              base["p_upsize"] * scale, p_backlog,
                              med["unit_delay_mean"] * scale, med["p_fail"] * scale,
                              STRATEGIES)
            for s, (delays, costs) in out.items():
                rows.append({"p_backlog": p_backlog, "unit_scale": scale,
                             "strategy": s, **summarize(delays, costs)})
            k += 1
    sens = pd.DataFrame(rows)
    sens.to_parquet(GOLD / "sensitivity_delay_type.parquet", index=False)
    sens.round(4).to_csv(RESULTS / "sensitivity_delay_type.csv", index=False)
    print("Saved results to data/gold/ and results/")


if __name__ == "__main__":
    main()
