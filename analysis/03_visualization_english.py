"""
英語版図表（投稿用）を生成する。
Figures 1–3 のみ。Figure 4 は revised v6 原稿内の英語版をそのまま使用する。
"""

import sys
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
import yaml

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root / "src"))
import ndb_library.logger as logger_module
from ndb_library.viz import add_watermark

PROJECT = "NDB_XXX_diabetes_unemployment"
config_path = project_root / f"projects/{PROJECT}/config/config.yaml"
with open(config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

log = logger_module.setup_logger(
    name=f"{PROJECT}_phase3_en",
    log_file=project_root / config["logging"]["log_path"] / "phase3_visualization_english.log",
)

PREFECTURE_EN = {
    "沖縄県": "Okinawa",
    "東京都": "Tokyo",
    "大阪府": "Osaka",
    "北海道": "Hokkaido",
}

INTERIM_DIR = project_root / config["output_paths"]["interim"]
FIG_DIR = project_root / config["output_paths"]["figures"] / "en"
FIG_DIR.mkdir(parents=True, exist_ok=True)

DPI = config["visualization"]["dpi"]
EXPERIMENT_MODE = config["experiment_mode"]

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans", "Helvetica"],
        "axes.unicode_minus": False,
    }
)


def load_data() -> pd.DataFrame:
    path = INTERIM_DIR / "analysis_dataset_with_unemployment.csv"
    return pd.read_csv(path, encoding="utf-8-sig")


def plot_scatter_with_regression(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    xlabel: str,
    ylabel: str,
    title: str,
    filename: str,
    highlight_okinawa: bool = True,
    color: str = "#2196F3",
) -> None:
    data = df[[x_col, y_col, "prefecture"]].dropna()
    x = data[x_col].values
    y = data[y_col].values

    fig, ax = plt.subplots(figsize=(8, 6))

    colors = [
        "#F44336" if highlight_okinawa and row["prefecture"] == "沖縄県" else color
        for _, row in data.iterrows()
    ]
    ax.scatter(x, y, c=colors, alpha=0.7, s=50, zorder=3)

    highlight = ["沖縄県", "東京都", "大阪府", "北海道"] if highlight_okinawa else []
    for _, row in data.iterrows():
        if row["prefecture"] in highlight:
            label = PREFECTURE_EN.get(row["prefecture"], row["prefecture"])
            ax.annotate(
                label,
                (row[x_col], row[y_col]),
                textcoords="offset points",
                xytext=(5, 3),
                fontsize=8,
            )

    slope, intercept, r_value, p_value, se = stats.linregress(x, y)
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = intercept + slope * x_line

    n = len(x)
    x_mean = x.mean()
    se_line = se * np.sqrt(1 / n + (x_line - x_mean) ** 2 / np.sum((x - x_mean) ** 2))
    t_crit = stats.t.ppf(0.975, df=n - 2)
    ci_lower = y_line - t_crit * se_line
    ci_upper = y_line + t_crit * se_line

    ax.plot(x_line, y_line, color="#1565C0", linewidth=2, zorder=4)
    ax.fill_between(x_line, ci_lower, ci_upper, alpha=0.15, color="#1565C0")

    p_str = f"p = {p_value:.3f}" if p_value >= 0.001 else "p < 0.001"
    ax.text(
        0.05,
        0.95,
        f"r = {r_value:.3f}\n{p_str}\nN = {n}",
        transform=ax.transAxes,
        va="top",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
    )

    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=13, pad=10)
    ax.grid(alpha=0.3)

    if highlight_okinawa:
        legend = [
            mpatches.Patch(color="#F44336", label="Okinawa (outlier)"),
            mpatches.Patch(color=color, label="Other prefectures"),
        ]
        ax.legend(handles=legend, fontsize=9)

    if EXPERIMENT_MODE:
        add_watermark(fig, "SAMPLE DATA")

    plt.tight_layout()
    out_path = FIG_DIR / filename
    plt.savefig(out_path, dpi=DPI, bbox_inches="tight")
    plt.close()
    log.info("Saved: %s", out_path)


def plot_forest_sensitivity(coef_csv: Path, outcome_filter: str, x_label: str, filename: str) -> None:
    df = pd.read_csv(coef_csv, encoding="utf-8-sig")
    df = df[(df["variable"] == "unemployment_rate") & (df["model"].str.contains(outcome_filter))]
    if df.empty:
        log.warning("No data for forest plot: %s", outcome_filter)
        return

    label_map = {
        "M1_HbA1c_Univariate": "M1: Univariate",
        "M2_HbA1c_AgeAdj": "M2: + Aging rate",
        "M3_HbA1c_FullModel": "M3: + Income adjustment",
        "M4_HbA1c_PopDensity": "M4: + Population density",
        "M3_HbA1c_HC3": "M3: HC3 robust SE",
        "M3_HbA1c_ExclOkinawa": "M3: Excluding Okinawa",
    }
    order = list(label_map.keys())
    df["label"] = df["model"].map(label_map).fillna(df["model"])
    df["sort_key"] = df["model"].map({name: i for i, name in enumerate(order)})
    df = df.sort_values("sort_key", ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    y_pos = range(len(df))
    colors = ["#F44336" if not sig else "#2196F3" for sig in df["significant"]]

    ax.errorbar(
        df["beta"],
        list(y_pos),
        xerr=[df["beta"] - df["ci_lower"], df["ci_upper"] - df["beta"]],
        fmt="o",
        capsize=5,
        color="black",
        markersize=6,
        elinewidth=1.5,
    )

    for i, (_, row) in enumerate(df.iterrows()):
        ax.scatter(row["beta"], i, color=colors[i], zorder=5, s=80)

    ax.axvline(0, color="gray", linestyle="--", linewidth=1)
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(df["label"].tolist(), fontsize=10)
    ax.set_xlabel(x_label, fontsize=11)
    ax.grid(axis="x", alpha=0.3)

    for i, (_, row) in enumerate(df.iterrows()):
        p_str = f"p={row['p']:.3f}" if row["p"] >= 0.001 else "p<0.001"
        ax.text(
            ax.get_xlim()[1] * 0.98,
            i,
            p_str,
            ha="right",
            va="center",
            fontsize=8,
            color="red" if row["significant"] else "gray",
        )

    sig_n = int(df["significant"].sum())
    total_n = len(df)
    ax.set_title(
        f"Sensitivity analysis: unemployment rate regression coefficients (95% CI)\n"
        f"({sig_n}/{total_n} models significant)",
        fontsize=12,
    )

    if EXPERIMENT_MODE:
        add_watermark(fig, "SAMPLE DATA")

    plt.tight_layout()
    out_path = FIG_DIR / filename
    plt.savefig(out_path, dpi=DPI, bbox_inches="tight")
    plt.close()
    log.info("Saved: %s", out_path)


def main() -> None:
    log.info("Generating English manuscript figures")
    df = load_data()
    coef_csv = project_root / config["output_paths"]["results"] / "regression_coefficients.csv"

    plot_scatter_with_regression(
        df,
        "unemployment_rate",
        "hba1c_high_rate",
        xlabel="Unemployment rate (%)",
        ylabel="HbA1c high rate (≥6.5%, %)",
        title="Association between unemployment rate and HbA1c high rate\n"
        "(by prefecture, N=47, NDB Open Data No.10)",
        filename="Fig1_unemployment_hba1c_scatter_en.png",
    )

    if "dm_drug_per_10k" in df.columns:
        plot_scatter_with_regression(
            df,
            "unemployment_rate",
            "dm_drug_per_10k",
            xlabel="Unemployment rate (%)",
            ylabel="Antidiabetic drug prescriptions (per 10,000 population)",
            title="Association between unemployment rate and antidiabetic drug prescriptions\n"
            "(by prefecture, N=47, NDB Open Data No.10)",
            filename="Fig2_unemployment_drug_scatter_en.png",
            color="#4CAF50",
        )

    if coef_csv.exists():
        plot_forest_sensitivity(
            coef_csv,
            "HbA1c",
            x_label="Regression coefficient β (change in HbA1c high rate per 1% increase in unemployment)",
            filename="Fig3_forest_sensitivity_hba1c_en.png",
        )
    else:
        log.warning("Coefficient file not found: %s", coef_csv)


if __name__ == "__main__":
    main()
