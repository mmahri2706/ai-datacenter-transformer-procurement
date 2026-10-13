"""Monte Carlo model of transformer procurement for one data center project.

Two kinds of delay are modeled separately:
  * supplier-wide backlog: hits every unit ordered from one supplier at once
  * unit-level problems: one unit arrives late or fails inspection

All strategies are tested on the SAME random world in each run, so differences
come from the strategy and not from luck. See docs/assumptions.md for every rule.
"""

import math

import numpy as np

from params import Params

MAX_UNITS = 24


def draw_worlds(rng, n_runs, p, lead_mult, p_upsize, p_backlog, unit_delay_mean, p_fail):
    """Draw every random event for n_runs independent runs."""
    def tri(lo, mo, hi, size):
        return rng.triangular(lo, mo, hi, size)

    return {
        "lead_mult": lead_mult,
        "backlog": rng.random((n_runs, 2)) < p_backlog,
        "backlog_size": tri(p.backlog_low, p.backlog_mode, p.backlog_high, (n_runs, 2)),
        "lead": tri(p.lead_low, p.lead_mode, p.lead_high, n_runs) * lead_mult,
        "unit_delay": rng.exponential(unit_delay_mean, (n_runs, MAX_UNITS)),
        "fail": rng.random((n_runs, MAX_UNITS)) < p_fail,
        "upsize": rng.random(n_runs) < p_upsize,
        # fresh draws for re-sourced orders and replacement orders
        "new_lead": tri(p.lead_low, p.lead_mode, p.lead_high, (n_runs, 2)) * lead_mult,
        "new_unit_delay": rng.exponential(unit_delay_mean, (n_runs, 2 * MAX_UNITS)),
    }


def run_one(w, i, strategy, p):
    """Simulate one project under one strategy. Returns (delay_months, cost)."""
    n = p.n_units
    lead = float(w["lead"][i])
    lead_mult = w["lead_mult"]
    backlogged = [bool(w["backlog"][i, 0]), bool(w["backlog"][i, 1])]
    size = [float(w["backlog_size"][i, k]) if backlogged[k] else 0.0 for k in (0, 1)]
    unit_delay = w["unit_delay"][i]
    fail = w["fail"][i]
    new_lead = w["new_lead"][i]
    new_unit_delay = w["new_unit_delay"][i]
    need = n + (p.upsize_units if w["upsize"][i] else 0)

    # --- Strategy setup ---
    t0 = 0.0          # when the first order is placed (months after approval)
    price = 1.0
    spares = 0
    if strategy == "advance":
        t0 = -p.advance_months
        price = 1.0 + p.advance_premium
    elif strategy == "diversified":
        price = 1.0 + p.diversified_premium
    elif strategy.startswith("reserved"):
        spares = math.ceil(n * int(strategy.split("_")[1]) / 100)

    ordered = n + spares
    if strategy == "diversified":
        half = n // 2
        supplier = [0] * half + [1] * (n - half)
    else:
        supplier = [0] * ordered

    # A unit arrives after the shared lead time, plus its supplier's backlog,
    # plus its own small delay.
    arrivals = [t0 + lead + size[supplier[j]] + unit_delay[j] for j in range(ordered)]
    cost = ordered * price
    if strategy == "advance":
        cost += n * p.advance_cancel_prob * p.advance_cancel_fee

    # A supplier's backlog clears this long after the order was placed.
    backlog_end = [t0 + size[0], t0 + size[1]]

    # --- Diversified sourcing: re-route when exactly one supplier is backlogged ---
    if strategy == "diversified" and backlogged[0] != backlogged[1]:
        bad = 0 if backlogged[0] else 1
        good = 1 - bad
        group = [j for j in range(ordered) if supplier[j] == bad]
        d = p.backlog_detect_month
        expected_new_arrival = d + p.lead_mode * lead_mult
        original_arrival = lead + size[bad]
        if expected_new_arrival < original_arrival:
            wait = max(0.0, backlog_end[good] - d)
            for k, j in enumerate(group):
                arrivals[j] = d + new_lead[0] + wait + new_unit_delay[k]
            cost += len(group) * p.reroute_fee

    # --- Failures and demand increase: top up if spares do not cover it ---
    usable = [arrivals[j] for j in range(ordered) if not fail[j]]
    failed = [arrivals[j] for j in range(ordered) if fail[j]]
    shortfall = need - len(usable)
    if shortfall > 0:
        triggers = failed + ([p.upsize_month] if need > n else [])
        t_place = min(triggers)
        if strategy == "diversified":
            sup = 0 if backlog_end[0] <= backlog_end[1] else 1
        else:
            sup = 0
        lead_top = new_lead[1] + max(0.0, backlog_end[sup] - t_place)
        for k in range(shortfall):
            usable.append(t_place + lead_top + new_unit_delay[MAX_UNITS + k % MAX_UNITS])
        cost += shortfall * 1.0

    usable.sort()
    ready = usable[need - 1]
    unused = max(0, len(usable) - need)
    cost -= unused * p.spare_salvage
    return max(0.0, ready - p.t_plan), cost


def run_cell(rng, n_runs, p, lead_mult, p_upsize, p_backlog, unit_delay_mean, p_fail,
             strategies):
    """Run every strategy on the same worlds. Returns {strategy: (delays, costs)}."""
    w = draw_worlds(rng, n_runs, p, lead_mult, p_upsize, p_backlog, unit_delay_mean, p_fail)
    out = {}
    for s in strategies:
        delays = np.empty(n_runs)
        costs = np.empty(n_runs)
        for i in range(n_runs):
            delays[i], costs[i] = run_one(w, i, s, p)
        out[s] = (delays, costs)
    return out, w
