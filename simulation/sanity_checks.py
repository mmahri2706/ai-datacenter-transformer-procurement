"""Sanity checks for the model. Run: python simulation/sanity_checks.py

These test that the model behaves the way the research design says it should,
before any result is trusted. They use the placeholder parameters.
"""

from dataclasses import replace

import numpy as np

from model import run_cell
from params import Params

P = Params()
RUNS = 4000


def cell(seed, **kw):
    args = dict(lead_mult=1.0, p_upsize=0.0, p_backlog=0.0, unit_delay_mean=0.0, p_fail=0.0)
    args.update(kw)
    rng = np.random.default_rng(seed)
    return run_cell(rng, RUNS, P,
                    args["lead_mult"], args["p_upsize"], args["p_backlog"],
                    args["unit_delay_mean"], args["p_fail"],
                    ["reactive", "advance", "diversified", "reserved_20"])


def check_extra_units_do_not_beat_a_supplier_wide_backlog():
    # Every supplier is always backlogged; nothing else goes wrong.
    out, _ = cell(1, p_backlog=1.0)
    d_react, c_react = out["reactive"]
    d_res, c_res = out["reserved_20"]
    assert np.allclose(d_react, d_res), "extra units must not reduce a supplier-wide delay"
    assert c_res.mean() > c_react.mean(), "extra units must cost more"
    print("PASS 1: ordering 12 instead of 10 from a backlogged supplier saves 0 months "
          f"(and costs {100 * (c_res.mean() / c_react.mean() - 1):.0f}% more)")


def check_extra_units_help_with_unit_level_problems():
    out, _ = cell(2, p_fail=0.2)
    d_react = out["reactive"][0].mean()
    d_res = out["reserved_20"][0].mean()
    assert d_res < d_react, "spares should help when single units fail"
    print(f"PASS 2: with failing units, reserved +20% cuts average delay "
          f"from {d_react:.2f} to {d_res:.2f} months")


def check_diversifying_helps_against_a_one_sided_backlog():
    out, _ = cell(3, p_backlog=0.3)
    d_react = out["reactive"][0].mean()
    d_div = out["diversified"][0].mean()
    assert d_div < d_react, "diversified should help when backlogs are common"
    print(f"PASS 3: with 30% backlog chance, diversified cuts average delay "
          f"from {d_react:.2f} to {d_div:.2f} months")


def check_advance_is_a_pure_time_shift():
    # No randomness except the shared lead time: advance ordering should shift
    # the ready date earlier by exactly the advance months.
    p = replace(P, t_plan=10.0)
    rng = np.random.default_rng(4)
    out, w = run_cell(rng, RUNS, p, 1.0, 0.0, 0.0, 0.0, 0.0, ["reactive", "advance"])
    lead = w["lead"]
    expect_react = np.maximum(0.0, lead - p.t_plan)
    expect_adv = np.maximum(0.0, lead - p.advance_months - p.t_plan)
    assert np.allclose(out["reactive"][0], expect_react)
    assert np.allclose(out["advance"][0], expect_adv)
    print("PASS 4: with no random problems, advance ordering shifts delay by exactly "
          f"{p.advance_months:.0f} months")


def check_same_seed_same_result():
    a, _ = cell(5, p_backlog=0.15, unit_delay_mean=1.0, p_fail=0.04, p_upsize=0.2)
    b, _ = cell(5, p_backlog=0.15, unit_delay_mean=1.0, p_fail=0.04, p_upsize=0.2)
    for s in a:
        assert np.array_equal(a[s][0], b[s][0]) and np.array_equal(a[s][1], b[s][1])
    print("PASS 5: the same seed gives identical results")


if __name__ == "__main__":
    check_extra_units_do_not_beat_a_supplier_wide_backlog()
    check_extra_units_help_with_unit_level_problems()
    check_diversifying_helps_against_a_one_sided_backlog()
    check_advance_is_a_pure_time_shift()
    check_same_seed_same_result()
    print("All sanity checks passed.")
