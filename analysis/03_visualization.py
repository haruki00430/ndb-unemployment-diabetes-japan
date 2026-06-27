"""
Phase 3: Generate main figures with Japanese labels.

Produces four main figures reported in the manuscript (300 dpi PNG):
  Fig 1: Scatter plot — unemployment rate × HbA1c high rate (with regression line)
  Fig 2: Scatter plot — unemployment rate × antidiabetic drug prescriptions
  Fig 3: Forest plot — unemployment rate β across six sensitivity analysis models
  Fig 4: Prefecture ranking chart — HbA1c high rate and unemployment rate

Phase 3: 日本語ラベルで主要図を生成する（300dpi PNG）。
国際誌投稿用英語版は 03_visualization_english.py を参照。

Output directory: results/figures/
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import yaml
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy.stats as stats

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root / "src"))
from ndb_library.viz import set_japanese_font, add_watermark
import ndb_library.logger as logger_module

PROJECT = "NDB_XXX_diabetes_unemployment"
config_path = project_root / f"projects/{PROJECT}/config/config.yaml"
with open(config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

log = logger_module.setup_logger(
    name=f"{PROJECT}_phase3",
    log_file=project_root / config["logging"]["log_path"] / "phase3_visualization.log"
)

set_japanese_font()

INTERIM_DIR = project_root / config["output_paths"]["interim"]
FIG_DIR = project_root / config["output_paths"]["figures"]
FIG_DIR.mkdir(parents=True, exist_ok=True)

DPI = config["visualization"]["dpi"]
EXPERIMENT_MODE = config["experiment_mode"]


def load_data():
    path = INTERIM_DIR / "analysis_dataset_with_unemployment.csv"
    return pd.read_csv(path, encoding="utf-8-sig")


def plot_scatter_with_regression(df, x_col, y_col, xlabel, ylabel, title, filename,
                                  highlight_okinawa=True, color="#2196F3"):
    """散布図 + 回帰直線 + 95%CI"""
    data = df[[x_col, y_col, "prefecture"]].dropna()
    x = data[x_col].values
    y = data[y_col].values

    fig, ax = plt.subplots(figsize=(8, 6))

    # 散布
    colors = []
    for _, row in data.iterrows():
        if highlight_okinawa and row["prefecture"] == "沖縄県":
            colors.append("#F44336")  # 赤（外れ値）
        else:
            colors.append(color)

    ax.scatter(x, y, c=colors, alpha=0.7, s=50, zorder=3)

    # 都道府県ラベル（外れ値のみ）
    highlight = ["沖縄県", "東京都", "大阪府", "北海道"] if highlight_okinawa else []
    for _, row in data.iterrows():
        if row["prefecture"] in highlight:
            ax.annotate(row["prefecture"], (row[x_col], row[y_col]),
                        textcoords="offset points", xytext=(5, 3), fontsize=8)

    # 回帰直線 + 95%CI
    slope, intercept, r_value, p_value, se = stats.linregress(x, y)
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = intercept + slope * x_line

    # 95%CI（標準誤差から計算）
    n = len(x)
    x_mean = x.mean()
    se_line = se * np.sqrt(1/n + (x_line - x_mean)**2 / np.sum((x - x_mean)**2))
    t_crit = stats.t.ppf(0.975, df=n-2)
    ci_lower = y_line - t_crit * se_line
    ci_upper = y_line + t_crit * se_line

    ax.plot(x_line, y_line, color="#1565C0", linewidth=2, zorder=4)
    ax.fill_between(x_line, ci_lower, ci_upper, alpha=0.15, color="#1565C0")

    # 統計情報
    p_str = f"p = {p_value:.3f}" if p_value >= 0.001 else "p < 0.001"
    ax.text(0.05, 0.95, f"r = {r_value:.3f}\n{p_str}\nN = {n}",
            transform=ax.transAxes, va="top", fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=13, pad=10)
    ax.grid(alpha=0.3)

    if highlight_okinawa:
        legend = [mpatches.Patch(color="#F44336", label="沖縄県（外れ値）"),
                  mpatches.Patch(color=color, label="その他")]
        ax.legend(handles=legend, fontsize=9)

    if EXPERIMENT_MODE:
        add_watermark(fig, "SAMPLE DATA")

    plt.tight_layout()
    out_path = FIG_DIR / filename
    plt.savefig(out_path, dpi=DPI, bbox_inches="tight")
    plt.close()
    log.info(f"Saved: {out_path}")


def plot_forest_sensitivity(coef_csv, outcome_filter, x_label, filename):
    """感度分析 Forest Plot"""
    df = pd.read_csv(coef_csv, encoding="utf-8-sig")
    df = df[(df["variable"] == "unemployment_rate") & (df["model"].str.contains(outcome_filter))]
    if df.empty:
        log.warning(f"No data for forest plot: {outcome_filter}")
        return

    # モデル名を短縮
    label_map = {
        "M1_HbA1c_Univariate": "M1: 単変量",
        "M2_HbA1c_AgeAdj": "M2: +高齢化率",
        "M3_HbA1c_FullModel": "M3: +所得調整",
        "M4_HbA1c_PopDensity": "M4: +人口密度",
        "M3_HbA1c_HC3": "M3: HC3頑健SE",
        "M3_HbA1c_ExclOkinawa": "M3: 沖縄除外",
    }
    df["label"] = df["model"].map(label_map).fillna(df["model"])

    fig, ax = plt.subplots(figsize=(8, 5))

    y_pos = range(len(df))
    colors = ["#F44336" if not sig else "#2196F3" for sig in df["significant"]]

    ax.errorbar(df["beta"], list(y_pos), xerr=[df["beta"] - df["ci_lower"],
                                                 df["ci_upper"] - df["beta"]],
                fmt="o", capsize=5, color="black", markersize=6, elinewidth=1.5)

    for i, (idx, row) in enumerate(df.iterrows()):
        ax.scatter(row["beta"], i, color=colors[i], zorder=5, s=80)

    ax.axvline(0, color="gray", linestyle="--", linewidth=1)
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(df["label"].tolist(), fontsize=10)
    ax.set_xlabel(x_label, fontsize=11)
    ax.set_title(f"感度分析：失業率の回帰係数 (95% CI)\n（アウトカム: {outcome_filter}）", fontsize=12)
    ax.grid(axis="x", alpha=0.3)

    # p値を右側に表示
    for i, (idx, row) in enumerate(df.iterrows()):
        p_str = f"p={row['p']:.3f}" if row["p"] >= 0.001 else "p<0.001"
        ax.text(ax.get_xlim()[1] * 0.98, i, p_str, ha="right", va="center", fontsize=8,
                color="red" if row["significant"] else "gray")

    sig_n = df["significant"].sum()
    total_n = len(df)
    ax.set_title(f"感度分析：失業率の回帰係数 (95% CI)\n({sig_n}/{total_n}モデルで有意)", fontsize=12)

    if EXPERIMENT_MODE:
        add_watermark(fig, "SAMPLE DATA")

    plt.tight_layout()
    out_path = FIG_DIR / filename
    plt.savefig(out_path, dpi=DPI, bbox_inches="tight")
    plt.close()
    log.info(f"Saved: {out_path}")


def plot_dual_map(df, filename):
    """都道府県ランキング棒グラフ（地図代替）"""
    df_sorted = df.sort_values("unemployment_rate", ascending=False)

    fig, axes = plt.subplots(1, 2, figsize=(16, 10))

    # 失業率
    ax = axes[0]
    colors = ["#F44336" if v > 4.0 else "#FF9800" if v > 3.0 else "#4CAF50"
              for v in df_sorted["unemployment_rate"]]
    ax.barh(df_sorted["prefecture"], df_sorted["unemployment_rate"], color=colors)
    ax.set_xlabel("完全失業率 (%)", fontsize=11)
    ax.set_title("都道府県別完全失業率（2022年）", fontsize=12)
    ax.axvline(df_sorted["unemployment_rate"].mean(), color="navy", linestyle="--",
               linewidth=1.5, label=f"全国平均 {df_sorted['unemployment_rate'].mean():.1f}%")
    ax.legend(fontsize=9)
    ax.grid(axis="x", alpha=0.3)

    # HbA1c高値率
    if "hba1c_high_rate" in df.columns:
        df_sorted2 = df.sort_values("hba1c_high_rate", ascending=False)
        ax2 = axes[1]
        colors2 = ["#F44336" if v > 9 else "#FF9800" if v > 7.5 else "#4CAF50"
                   for v in df_sorted2["hba1c_high_rate"]]
        ax2.barh(df_sorted2["prefecture"], df_sorted2["hba1c_high_rate"], color=colors2)
        ax2.set_xlabel("HbA1c≥6.5%割合 (%)", fontsize=11)
        ax2.set_title("都道府県別HbA1c高値率（NDB No.10）", fontsize=12)
        ax2.axvline(df_sorted2["hba1c_high_rate"].mean(), color="navy", linestyle="--",
                    linewidth=1.5,
                    label=f"全国平均 {df_sorted2['hba1c_high_rate'].mean():.1f}%")
        ax2.legend(fontsize=9)
        ax2.grid(axis="x", alpha=0.3)

    if EXPERIMENT_MODE:
        add_watermark(fig, "SAMPLE DATA")

    plt.suptitle("都道府県別 失業率・HbA1c高値率の分布", fontsize=14, y=1.01)
    plt.tight_layout()
    out_path = FIG_DIR / filename
    plt.savefig(out_path, dpi=DPI, bbox_inches="tight")
    plt.close()
    log.info(f"Saved: {out_path}")


def main():
    log.info("=" * 60)
    log.info("Phase 3: Visualization")
    log.info("=" * 60)

    df = load_data()
    coef_csv = project_root / config["output_paths"]["results"] / "regression_coefficients.csv"

    # 1. 散布図: 失業率 × HbA1c高値率
    plot_scatter_with_regression(
        df, "unemployment_rate", "hba1c_high_rate",
        xlabel="完全失業率 (%)",
        ylabel="HbA1c≥6.5%割合 (%)",
        title="失業率とHbA1c高値率の関連\n（都道府県別、N=47、NDB No.10）",
        filename="Fig1_unemployment_hba1c_scatter.png",
    )

    # 2. 散布図: 失業率 × 糖尿病用剤処方量
    if "dm_drug_per_10k" in df.columns:
        plot_scatter_with_regression(
            df, "unemployment_rate", "dm_drug_per_10k",
            xlabel="完全失業率 (%)",
            ylabel="糖尿病用剤処方量 (/1万人)",
            title="失業率と糖尿病用剤処方量の関連\n（都道府県別、N=47、NDB No.10）",
            filename="Fig2_unemployment_drug_scatter.png",
            color="#4CAF50",
        )

    # 3. Forest plot（感度分析）
    if coef_csv.exists():
        plot_forest_sensitivity(
            coef_csv, "HbA1c",
            x_label="回帰係数 β（失業率1%増加あたりのHbA1c高値率変化）",
            filename="Fig3_forest_sensitivity_hba1c.png",
        )
    else:
        log.warning(f"Coefficient file not found: {coef_csv} — run Phase 2 first")

    # 4. 棒グラフ（都道府県ランキング）
    plot_dual_map(df, filename="Fig4_prefecture_ranking.png")

    log.info("Phase 3 complete. All figures saved.")


if __name__ == "__main__":
    main()
