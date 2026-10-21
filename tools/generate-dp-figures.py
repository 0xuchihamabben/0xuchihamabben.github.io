"""Reproduce the introductory DP post's two original explanatory figures.

Requires matplotlib and numpy. The second figure plots exact Laplace densities,
rather than samples or empirical results.
Run from any directory: python tools/generate-dp-figures.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np


DESTINATION = (
    Path(__file__).resolve().parents[1]
    / "assets/img/posts/differential-privacy-introduction"
)
BACKGROUND = "#f7f3ea"
INK = "#203b4b"
TEAL = "#147d7a"
AMBER = "#b8792f"
MUTED = "#576b72"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 14,
        "text.color": INK,
        "axes.labelcolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "savefig.facecolor": BACKGROUND,
    }
)


def record_linkage():
    fig, ax = plt.subplots(figsize=(12, 7), facecolor=BACKGROUND)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")
    ax.text(
        0.05, 0.94, "Removing a name leaves other clues",
        fontsize=25, weight="bold", va="center",
    )
    ax.text(
        0.05, 0.875, "Shared attributes can reconnect two separate releases.",
        fontsize=16, color=MUTED,
    )

    left_rows = [
        ("Birth date", "14 Jun 1990"),
        ("ZIP code", "02138"),
        ("Sex", "F"),
        ("Diagnosis", "Condition X"),
    ]
    right_rows = left_rows[:3] + [("Name", "Alex")]

    for x, title, subtitle, rows in (
        (0.05, "Medical release", "Direct identifiers removed", left_rows),
        (0.53, "Public directory", "Names remain available", right_rows),
    ):
        ax.add_patch(
            FancyBboxPatch(
                (x, 0.28), 0.42, 0.52,
                boxstyle="round,pad=0.008,rounding_size=0.014",
                facecolor="white", edgecolor="#d4dedc", linewidth=1.5,
            )
        )
        ax.text(x + 0.025, 0.745, title, fontsize=20, weight="bold")
        ax.text(x + 0.025, 0.695, subtitle, fontsize=12, color=MUTED)
        for i, (label, value) in enumerate(rows):
            y = 0.605 - 0.083 * i
            ax.add_patch(
                FancyBboxPatch(
                    (x + 0.018, y - 0.029), 0.384, 0.064,
                    boxstyle="round,pad=0.003,rounding_size=0.006",
                    facecolor="#e8f2ef" if i < 3 else "#fbefdb",
                    edgecolor="none",
                )
            )
            ax.text(x + 0.031, y, label, va="center", fontsize=14, color=MUTED)
            ax.text(
                x + 0.387, y, value, va="center", ha="right",
                fontsize=15, weight="bold", color=TEAL if i < 3 else AMBER,
            )

    for y in (0.605, 0.522, 0.439):
        ax.annotate(
            "", xy=(0.523, y), xytext=(0.477, y),
            arrowprops={"arrowstyle": "<->", "color": TEAL, "lw": 1.6},
        )

    ax.text(
        0.5, 0.194, "If the shared combination is unique,",
        ha="center", fontsize=18,
    )
    ax.text(
        0.5, 0.139, "a name can be linked to a diagnosis.",
        ha="center", fontsize=20, weight="bold",
    )
    fig.savefig(DESTINATION / "record-linkage.png", dpi=160)
    plt.close(fig)


def neighboring_distributions():
    fig, ax = plt.subplots(figsize=(12, 7), facecolor=BACKGROUND)
    fig.subplots_adjust(left=0.10, right=0.96, bottom=0.29, top=0.75)
    ax.set_facecolor(BACKGROUND)
    fig.text(
        0.06, 0.93, "One patient, two nearby output distributions",
        fontsize=24, weight="bold",
    )
    fig.text(
        0.06, 0.865,
        r"Laplace mechanism: sensitivity $\Delta f=1$, privacy $\varepsilon=0.5$, noise scale $b=2$",
        fontsize=16, color=MUTED,
    )

    x = np.linspace(13, 32, 2401)
    scale = 2.0
    for count, color, label in (
        (22, TEAL, "Without patient: true count 22"),
        (23, AMBER, "With patient: true count 23"),
    ):
        density = np.exp(-np.abs(x - count) / scale) / (2 * scale)
        ax.plot(x, density, color=color, lw=3, label=label)
        ax.fill_between(x, density, color=color, alpha=0.10)
        ax.vlines(count, 0, 0.25, color=color, ls="--", lw=1.1, alpha=0.7)

    ax.set(
        xlim=(13, 32), ylim=(0, 0.295),
        xlabel="Released count (real-valued)", ylabel="Probability density",
        xticks=[14, 18, 22, 23, 27, 31],
        yticks=[0, 0.05, 0.10, 0.15, 0.20, 0.25],
    )
    ax.grid(axis="y", color="#dce1d9", alpha=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#abb9b5")
    ax.legend(
        loc="upper right", fontsize=12, framealpha=0.95,
        facecolor=BACKGROUND, edgecolor="none",
    )
    ax.xaxis.labelpad = 12
    ax.yaxis.labelpad = 10
    fig.text(
        0.10, 0.105,
        r"Likelihood ratio bounded by $e^{0.5}$ in either direction.",
        fontsize=15, weight="bold",
    )
    fig.text(
        0.10, 0.05,
        "Illustrative parameters. Scale 2 is not a maximum error; both distributions have unbounded tails.",
        fontsize=11, color=MUTED,
    )
    fig.savefig(DESTINATION / "neighboring-distributions.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    DESTINATION.mkdir(parents=True, exist_ok=True)
    record_linkage()
    neighboring_distributions()
    print(f"Saved both figures to {DESTINATION}")
