"""Regenerate the PMW-Bernstein post's illustration and two plots."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


DESTINATION = Path(__file__).resolve().parents[1] / "assets/img/posts/pmw-bernstein"
BACKGROUND = "#f7f3ea"
INK = "#203b4b"
TEAL = "#147d7a"
AMBER = "#9b591e"
MUTED = "#51676e"
GRID = "#dddcd2"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 13,
        "text.color": INK,
        "axes.labelcolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "figure.facecolor": BACKGROUND,
        "axes.facecolor": BACKGROUND,
    }
)


def save(fig, name):
    fig.savefig(DESTINATION / f"{name}.png", dpi=150, facecolor=BACKGROUND)
    plt.close(fig)


def variance_header():
    """Illustrate an indicator update with a normalized exponential tilt."""
    x = np.arange(22)
    prior = np.exp(-0.5 * ((x - 8) / 3.6) ** 2) + 0.045
    prior /= prior.sum()
    event = x >= 16
    corrected = prior * np.exp(1.95 * event)
    corrected /= corrected.sum()

    fig, axes = plt.subplots(1, 2, figsize=(10, 5.25), sharey=True)
    fig.subplots_adjust(left=0.065, right=0.935, top=0.86, bottom=0.19, wspace=0.22)
    for ax, weights, title in zip(
        axes, (prior, corrected), ("Before correction", "After correction")
    ):
        ax.set(xlim=(-1, 22), ylim=(0, 0.125))
        ax.axis("off")
        ax.axvspan(15.45, 21.55, color="#efe0cb", lw=0)
        ax.hlines([0, 0.04, 0.08, 0.12], -0.5, 21.5, color=GRID, lw=0.8)
        ax.bar(x, weights, width=0.72, color=np.where(event, AMBER, TEAL), zorder=2)
        ax.text(0.5, -0.08, title, transform=ax.transAxes, ha="center", weight="bold")
    fig.text(0.5, 0.05, "Highlighted bars represent the queried group", ha="center", color=MUTED)
    save(fig, "variance-header")


def step_size():
    error = 0.06
    step = np.linspace(0, 3.04, 600)
    fig, ax = plt.subplots(figsize=(8.2, 5.1))
    fig.subplots_adjust(left=0.16, right=0.94, top=0.81, bottom=0.17)
    fig.text(0.16, 0.92, "Same error, different optimal steps", fontsize=20, weight="bold")
    ax.set(
        xlim=(0, 3),
        ylim=(-0.021, 0.083),
        xlabel=r"Step size $\eta$",
        ylabel="Lower bound on KL decrease",
        yticks=[0, 0.02, 0.04, 0.06, 0.08],
    )
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["bottom", "left"]].set_color("#a9b2ad")
    ax.grid(axis="y", color=GRID)
    ax.axhline(0, color="#a9b2ad", lw=1)

    for variance, color, style, label, position in (
        (0.0099, TEAL, "-", r"Low variance ($v=0.0099$)", (1.40, 0.047)),
        (0.25, AMBER, "--", r"High variance ($v=0.25$)", (0.66, 0.018)),
    ):
        best = np.log1p(error / variance)
        peak = best * error - variance * (np.expm1(best) - best)
        progress = step * error - variance * (np.expm1(step) - step)
        ax.plot(step, progress, color=color, ls=style, lw=2.8)
        ax.plot(best, peak, "o", ms=8, color=color, zorder=4)
        ax.vlines(best, 0, peak, color=color, linestyles=":", lw=1.4)
        ax.annotate(
            f"{label}\nOptimal step {best:.2f}",
            xy=(best, peak),
            xytext=position,
            va="center",
            color=color,
            arrowprops={"arrowstyle": "-", "color": color, "shrinkB": 7},
            bbox={"facecolor": BACKGROUND, "edgecolor": "none", "pad": 2.5},
        )
    save(fig, "step-size")


def simulation_updates():
    """Plot the three noisy rows in Table IV of the paper."""
    labels = ("Low variance", "High variance", "Heterogeneous")
    adaptive = (2.30, 2.60, 35.90)
    fixed = (5.00, 3.00, 60.00)
    group_y = np.arange(len(labels))[::-1] * 1.35
    fig, ax = plt.subplots(figsize=(8.2, 5.3))
    fig.subplots_adjust(left=0.07, right=0.95, top=0.79, bottom=0.16)
    fig.text(0.07, 0.92, "Mean updates in the noisy simulation", fontsize=20, weight="bold")
    ax.set(xlim=(0, 67), ylim=(-0.61, 3.42), yticks=[], xlabel="Number of updates")
    ax.set_xticks(np.arange(0, 61, 10))
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#a9b2ad")
    ax.set_axisbelow(True)
    ax.grid(axis="x", color=GRID)

    ax.axvline(60, color=MUTED, ls="--", lw=1.1)
    ax.text(59.2, 3.25, "60-update cap", color=MUTED, ha="right", va="center")
    for label, y in zip(labels, group_y):
        ax.text(0, y + 0.45, label, va="center", weight="bold")
    for values, offset, color, label in (
        (adaptive, 0.12, TEAL, "Adaptive"),
        (fixed, -0.19, AMBER, "Best fixed step"),
    ):
        ax.barh(group_y + offset, values, height=0.22, color=color, label=label)
        for value, y in zip(values, group_y + offset):
            ax.text(value + 0.75, y, f"{value:.2f}", va="center", color=color, weight="bold")
    ax.legend(loc="lower right", bbox_to_anchor=(1, 1.02), ncols=2, frameon=False)
    save(fig, "simulation-updates")


if __name__ == "__main__":
    DESTINATION.mkdir(parents=True, exist_ok=True)
    variance_header()
    step_size()
    simulation_updates()
