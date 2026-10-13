"""Draw the decision map and the delay-type map from the simulation results.

Usage:  python simulation/decision_map.py [--budget 0.15]

Reads:   results/sim_results.csv, results/sensitivity_delay_type.csv
Writes:  results/decision_map.png, results/delay_type_map.png,
         results/decision_map_winners.csv

ALL INPUTS ARE PLACEHOLDERS. The figures say so on their face.
"""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Rectangle

from params import Params

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

# Validated categorical colors (blue, orange, aqua, yellow); identity is also
# carried by the text label in every cell, never by color alone.
FAMILY_COLOR = {"reactive": "#2a78d6", "reserved": "#eb6834",
                "diversified": "#1baf7a", "advance": "#eda100"}
FAMILY_NAME = {"reactive": "Reactive is enough", "reserved": "Reserved extra capacity",
               "diversified": "Diversified sourcing", "advance": "Advance procurement"}
SURFACE, INK, INK2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"


def family(strategy):
    return strategy.split("_")[0]


def strategy_label(strategy):
    if strategy.startswith("reserved"):
        return f"Reserved extra capacity (+{strategy.split('_')[1]}%)"
    return FAMILY_NAME[strategy]


def pick_winner(cell, budget, min_gain):
    """Fewest months of delay among strategies within the spending limit."""
    cell = cell.set_index("strategy")
    base = cell.loc["reactive"]
    eligible = cell[cell["mean_cost"] <= (1 + budget) * base["mean_cost"]]
    best = eligible.sort_values(["mean_delay", "mean_cost"]).iloc[0]
    name = best.name
    gain = base["mean_delay"] - best["mean_delay"]
    if name != "reactive" and gain < min_gain:
        name, best, gain = "reactive", base, 0.0
    return {"winner": name, "months_saved": gain,
            "cost_change": best["mean_cost"] / base["mean_cost"] - 1,
            "mean_delay": best["mean_delay"], "baseline_delay": base["mean_delay"]}


def setup_axes(figsize):
    fig = plt.figure(figsize=figsize, facecolor=SURFACE)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(SURFACE)
    ax.axis("off")
    return fig, ax


def draw_cell(ax, x, y, w, h, winner, lines, gap=0.012):
    fam = family(winner)
    color = FAMILY_COLOR[fam]
    ax.add_patch(Rectangle((x + gap, y + gap), w - 2 * gap, h - 2 * gap,
                           facecolor=color, alpha=0.20, edgecolor="none"))
    ax.add_patch(Rectangle((x + gap, y + gap), w - 2 * gap, h - 2 * gap,
                           facecolor="none", edgecolor=color, linewidth=1.4))
    cx, cy = x + w / 2, y + h / 2
    n = len(lines)
    for k, (text, weight, col, size) in enumerate(lines):
        ax.text(cx, cy + (n - 1) / 2 * 0.032 - k * 0.032 + (0.0 if n > 2 else 0.0), text,
                ha="center", va="center", fontsize=size, fontweight=weight, color=col)


def legend(ax, families, x0, y0):
    x = x0
    for fam in families:
        ax.add_patch(Rectangle((x, y0 - 0.008), 0.016, 0.016, facecolor=FAMILY_COLOR[fam],
                               alpha=0.35, edgecolor=FAMILY_COLOR[fam], linewidth=1.2))
        ax.text(x + 0.024, y0, FAMILY_NAME[fam], va="center", fontsize=9.5, color=INK2)
        x += 0.07 + 0.0085 * len(FAMILY_NAME[fam])


def decision_map(grid, budget, min_gain, runs):
    demands = ["low", "base", "high"]
    levels = ["low", "medium", "high"]
    rows = []
    fig, ax = setup_axes((10.4, 7.0))
    left, bottom, cw, ch = 0.16, 0.17, 0.27, 0.215
    ax.text(0.03, 0.955, "Which way of buying transformers cuts delay the most?",
            fontsize=16, fontweight="bold", color=INK, va="center")
    ax.text(0.03, 0.915, "First rough decision map. PLACEHOLDER INPUTS: not real data, "
            "not a finding.", fontsize=10.5, color="#b3261e", va="center", fontweight="bold")
    ax.text(0.03, 0.885, f"Winner = fewest months of delay among strategies costing at most "
            f"{budget:.0%} more than the baseline. Months saved and cost are versus the baseline.",
            fontsize=9.3, color=INK2, va="center")
    for j, lvl in enumerate(levels):
        ax.text(left + cw * (j + 0.5), 0.835, f"{lvl.capitalize()} uncertainty", ha="center",
                fontsize=11, fontweight="bold", color=INK)
    ax.text(left + cw * 1.5, 0.862, "", ha="center")
    used = []
    for i, dem in enumerate(demands):
        y = bottom + ch * (2 - i)
        ax.text(left - 0.015, y + ch / 2, f"{dem.capitalize()}\ndemand", ha="right", va="center",
                fontsize=11, fontweight="bold", color=INK)
        for j, lvl in enumerate(levels):
            cell = grid[(grid.demand == dem) & (grid.uncertainty == lvl)]
            r = pick_winner(cell, budget, min_gain)
            rows.append({"demand": dem, "uncertainty": lvl, **r})
            fam = family(r["winner"])
            used.append(fam)
            if r["winner"] == "reactive":
                lines = [("Reactive is enough", "bold", INK, 11),
                         ("no strategy saves a meaningful", "normal", INK2, 9),
                         ("amount within the spending limit", "normal", INK2, 9)]
            else:
                lines = [(strategy_label(r["winner"]), "bold", INK, 10.5),
                         (f"{r['months_saved']:.1f} months less delay", "normal", INK, 10),
                         (f"+{r['cost_change']:.0%} cost", "normal", INK2, 10),
                         (f"avg delay {r['mean_delay']:.1f} vs {r['baseline_delay']:.1f} months",
                          "normal", INK2, 8.5)]
            draw_cell(ax, left + cw * j, y, cw, ch, r["winner"], lines)
    fams = [f for f in ["reactive", "reserved", "diversified", "advance"] if f in used]
    legend(ax, fams, left, 0.115)
    ax.text(0.03, 0.06, f"Hypothetical U.S. project needing 10 transformers, {runs:,} runs per "
            f"cell. Uncertainty sets how often a supplier is backlogged and how often single "
            f"units are late or fail.", fontsize=8.5, color=MUTED, va="center")
    fig.savefig(RESULTS / "decision_map.png", dpi=170, facecolor=SURFACE)
    plt.close(fig)
    pd.DataFrame(rows).round(4).to_csv(RESULTS / "decision_map_winners.csv", index=False)
    return pd.DataFrame(rows)


def delay_type_map(sens, budget, min_gain, runs):
    ps = sorted(sens.p_backlog.unique())
    us = sorted(sens.unit_scale.unique())
    scale_label = {0.0: "None", 0.25: "0.25x", 0.5: "0.5x", 1.0: "1x (base)", 2.0: "2x"}
    fig, ax = setup_axes((10.4, 7.0))
    left, bottom = 0.15, 0.17
    cw, ch = 0.80 / len(ps), 0.62 / len(us)
    ax.text(0.03, 0.955, "Which strategy wins as the kind of delay changes?",
            fontsize=16, fontweight="bold", color=INK, va="center")
    ax.text(0.03, 0.915, "Supplier-wide delay versus unit-level problems. PLACEHOLDER "
            "INPUTS: not real data, not a finding.", fontsize=10.5, color="#b3261e",
            va="center", fontweight="bold")
    ax.text(0.03, 0.885, f"Base demand. Winner = fewest months of delay among strategies costing "
            f"at most {budget:.0%} more than the baseline.", fontsize=9.3, color=INK2, va="center")
    used = []
    for i, u in enumerate(reversed(us)):          # largest unit-level delay on top
        y = bottom + ch * i
        ax.text(left - 0.012, y + ch / 2, scale_label.get(u, f"{u:g}x"), ha="right",
                va="center", fontsize=10, color=INK2)
        for j, pb in enumerate(ps):
            cell = sens[(sens.p_backlog == pb) & (sens.unit_scale == u)]
            r = pick_winner(cell, budget, min_gain)
            fam = family(r["winner"])
            used.append(fam)
            if r["winner"] == "reactive":
                lines = [("Baseline", "bold", INK, 9.5)]
            else:
                short = {"reserved": f"Spares +{r['winner'].split('_')[-1]}%",
                         "diversified": "Diversify", "advance": "Advance"}[fam]
                lines = [(short, "bold", INK, 9.5), (f"-{r['months_saved']:.1f} mo", "normal",
                                                     INK2, 9)]
            draw_cell(ax, left + cw * j, y, cw, ch, r["winner"], lines, gap=0.006)
    for j, pb in enumerate(ps):
        ax.text(left + cw * (j + 0.5), bottom - 0.025, f"{pb:.0%}", ha="center", fontsize=10,
                color=INK2)
    ax.text(left + 0.40, bottom - 0.065, "More supplier-wide delay: chance a supplier is "
            "backlogged  →", ha="center", fontsize=10.5, color=INK, fontweight="bold")
    ax.text(0.03, bottom + ch * len(us) + 0.05, "Unit-level problems: none at the top, more going "
            "down ↓", ha="left", va="center", fontsize=10.5, color=INK, fontweight="bold")
    ax.text(0.03, bottom + ch * len(us) + 0.02, "(late single units, failed units, project "
            "growth, scaled together)", ha="left", va="center", fontsize=8.8, color=INK2)
    fams = [f for f in ["reactive", "reserved", "diversified", "advance"] if f in used]
    legend(ax, fams, left, 0.085)
    ax.text(0.03, 0.04, f"{runs:,} runs per cell. 1x = base case: 4% unit failure chance, 20% "
            f"chance the project grows by 2 units. 'Spares +X%' = X% extra units from the same "
            f"supplier.", fontsize=8.5, color=MUTED, va="center")
    fig.savefig(RESULTS / "delay_type_map.png", dpi=170, facecolor=SURFACE)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--budget", type=float, default=Params().spending_limit)
    args = parser.parse_args()
    min_gain = Params().min_gain_months

    grid = pd.read_csv(RESULTS / "sim_results.csv")
    sens = pd.read_csv(RESULTS / "sensitivity_delay_type.csv")
    winners = decision_map(grid, args.budget, min_gain, int(grid.runs.iloc[0]))
    delay_type_map(sens, args.budget, min_gain, int(sens.runs.iloc[0]))
    print(winners[["demand", "uncertainty", "winner", "months_saved", "cost_change"]]
          .round(2).to_string(index=False))


if __name__ == "__main__":
    main()
