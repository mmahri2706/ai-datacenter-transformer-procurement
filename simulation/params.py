"""All model inputs in one place.

EVERY NUMBER IN THIS FILE IS A PLACEHOLDER.
They exist so the simulation runs end to end and the pipeline can be tested.
They have no evidence behind them. Replace or justify each one (see
docs/assumptions.md) before any result is reported as a finding.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Params:
    # Project setup
    n_units: int = 10            # transformers the project needs
    # Planned equipment-ready date, months after approval. Chosen so the toy project
    # has a real chance of delay; otherwise there is nothing to compare.
    t_plan: float = 18.0

    # Base lead time (months): triangular(low, most likely, high), shared by all suppliers
    lead_low: float = 10.0
    lead_mode: float = 14.0
    lead_high: float = 20.0

    # Supplier-wide backlog (months added to every unit from that supplier)
    backlog_low: float = 4.0
    backlog_mode: float = 8.0
    backlog_high: float = 16.0
    backlog_detect_month: float = 3.0   # when the buyer can see the backlog

    # Demand increase mid-project
    upsize_units: int = 2
    upsize_month: float = 6.0

    # Strategy costs (unit price = 1.0)
    advance_months: float = 4.0         # how early advance procurement orders
    advance_premium: float = 0.12
    advance_cancel_prob: float = 0.15   # chance the early order is wasted
    advance_cancel_fee: float = 0.40    # fee as a share of price if wasted
    diversified_premium: float = 0.05
    reroute_fee: float = 0.20           # fee for cancelling a re-routed order
    spare_salvage: float = 0.0          # value of unused spares (0 = full cost)

    # Fair-comparison rule: a strategy may only win if its average cost is within
    # this share above the baseline's average cost
    spending_limit: float = 0.15
    # A winner must save at least this many months versus the baseline,
    # otherwise the cell says the baseline is enough
    min_gain_months: float = 0.25


# Demand scenarios: how tight the transformer market is, and how likely a project grows
DEMAND = {
    "low":  {"lead_mult": 0.85, "p_upsize": 0.10},
    "base": {"lead_mult": 1.00, "p_upsize": 0.20},
    "high": {"lead_mult": 1.30, "p_upsize": 0.35},
}

# Uncertainty levels: chance a supplier is backlogged, and unit-level problems
UNCERTAINTY = {
    "low":    {"p_backlog": 0.05, "unit_delay_mean": 0.5, "p_fail": 0.02},
    "medium": {"p_backlog": 0.15, "unit_delay_mean": 1.0, "p_fail": 0.04},
    "high":   {"p_backlog": 0.30, "unit_delay_mean": 2.0, "p_fail": 0.08},
}

STRATEGIES = [
    "reactive",
    "advance",
    "diversified",
    "reserved_10",
    "reserved_20",
    "reserved_30",
]
