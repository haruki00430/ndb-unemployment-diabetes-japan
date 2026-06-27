"""
Phase 2: OLS regression analysis — unemployment rate and diabetes prevalence.

Estimates six sequential OLS models with HbA1c high rate (≥6.5%) as primary
outcome and unemployment rate as main exposure. Sensitivity analyses include
HC3 heteroscedasticity-consistent standard errors (Model 5) and outlier
exclusion of Okinawa (Model 6). Secondary analysis uses antidiabetic drug
prescriptions per 10,000 population as outcome.

Phase 2: OLS回帰分析（失業率 → 糖尿病有病率）。
HbA1c高値割合（≥6.5%）を主要アウトカムとした6モデルのOLS回帰。
感度分析: HC3頑健標準誤差（Model 5）、沖縄除外（Model 6）。

Models:
  Model 1: Unemployment rate only (univariate)
  Model 2: + Aging rate
  Model 3: + Aging rate + Per-capita income (primary model)
  Model 4: + Aging rate + Per-capita income + Population density (full model)
  Model 5: Model 3 with HC3 robust standard errors
  Model 6: Model 3 excluding Okinawa (high-unemployment outlier)

Outputs:
  results/regression_coefficients.csv
  results/model_fit_statistics.csv
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import yaml
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root / "src"))
import ndb_library.logger as logger_module

PROJECT = "NDB_XXX_diabetes_unemployment"
config_path = project_root / f"projects/{PROJECT}/config/config.yaml"
with open(config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

log = logger_module.setup_logger(
    name=f"{PROJECT}_phase2",
    log_file=project_root / config["logging"]["log_path"] / "phase2_regression.log"
)

INTERIM_DIR = project_root / config["output_paths"]["interim"]
RESULTS_DIR = project_root / config["output_paths"]["results"]
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

ALPHA = config["analysis_parameters"]["alpha"]
VIF_THRESHOLD = config["analysis_parameters"]["vif_threshold"]
SEED = config["reproducibility"]["random_seed"]
np.random.seed(SEED)


def load_data():
    path = INTERIM_DIR / "analysis_dataset_with_unemployment.csv"
    df = pd.read_csv(path, encoding="utf-8-sig")
    log.info(f"Loaded: {df.shape}, columns: {df.columns.tolist()}")
    return df


def check_vif(X_df):
    """VIF（多重共線性）チェック"""
    vif_data = pd.DataFrame()
    vif_data["Variable"] = X_df.columns
    vif_data["VIF"] = [variance_inflation_factor(X_df.values, i) for i in range(X_df.shape[1])]
    return vif_data


def run_ols(df, outcome, predictors, model_name, robust_se=False):
    """OLS回帰を実行し結果を返す"""
    valid_preds = [p for p in predictors if p in df.columns]
    if outcome not in df.columns:
        log.error(f"Outcome '{outcome}' not in data")
        return None

    data = df[[outcome] + valid_preds].dropna()
    if len(data) < 10:
        log.warning(f"Too few observations for {model_name}: {len(data)}")
        return None

    y = data[outcome]
    X = sm.add_constant(data[valid_preds])

    model = sm.OLS(y, X).fit()
    if robust_se:
        result = model.get_robustcov_results(cov_type="HC3")
    else:
        result = model

    log.info(f"\n{'='*50}")
    log.info(f"{model_name} (N={len(data)})")
    log.info(f"R2 = {result.rsquared:.4f}, Adj R2 = {result.rsquared_adj:.4f}")
    log.info(f"F = {result.fvalue:.3f}, p = {result.f_pvalue:.4f}")
    log.info(result.summary().tables[1].as_text())

    return {
        "model_name": model_name,
        "outcome": outcome,
        "n": len(data),
        "r2": result.rsquared,
        "adj_r2": result.rsquared_adj,
        "f_stat": result.fvalue,
        "f_pvalue": result.f_pvalue,
        "result": result,
        "X": data[valid_preds],
    }


def extract_coef_table(model_result):
    """回帰係数テーブルを抽出"""
    if model_result is None:
        return None
    res = model_result["result"]
    # HC3 robust SE時はparams.indexが存在しないためmodel.exog_namesを使う
    try:
        param_names = list(res.params.index)
    except AttributeError:
        param_names = list(res.model.exog_names)
    params = np.array(res.params).flatten()
    bse = np.array(res.bse).flatten()
    tvalues = np.array(res.tvalues).flatten()
    pvalues = np.array(res.pvalues).flatten()
    conf_int = np.array(res.conf_int())
    rows = []
    for i, var in enumerate(param_names):
        rows.append({
            "model": model_result["model_name"],
            "variable": var,
            "beta": params[i],
            "se": bse[i],
            "t": tvalues[i],
            "p": pvalues[i],
            "ci_lower": conf_int[i, 0],
            "ci_upper": conf_int[i, 1],
            "significant": pvalues[i] < ALPHA,
        })
    return pd.DataFrame(rows)


def main():
    log.info("=" * 60)
    log.info("Phase 2: OLS Regression Analysis")
    log.info("=" * 60)

    df = load_data()
    results_list = []
    coef_tables = []

    # ============================================================
    # OUTCOME 1: HbA1c高値率
    # ============================================================
    log.info("\n### OUTCOME: HbA1c高値率 ###")
    outcome = "hba1c_high_rate"

    models_hba1c = [
        ("M1_HbA1c_Univariate",    [                                             "unemployment_rate"]),
        ("M2_HbA1c_AgeAdj",        ["aging_rate",                                "unemployment_rate"]),
        ("M3_HbA1c_FullModel",     ["aging_rate", "income_per_capita",            "unemployment_rate"]),
        ("M4_HbA1c_PopDensity",    ["aging_rate", "income_per_capita", "pop_density", "unemployment_rate"]),
    ]

    for mname, preds in models_hba1c:
        r = run_ols(df, outcome, preds, mname)
        if r:
            results_list.append(r)
            ct = extract_coef_table(r)
            if ct is not None:
                coef_tables.append(ct)

    # HC3 頑健SE（Model 3）
    r_hc3 = run_ols(df, outcome,
                    ["aging_rate", "income_per_capita", "unemployment_rate"],
                    "M3_HbA1c_HC3", robust_se=True)
    if r_hc3:
        results_list.append(r_hc3)
        ct = extract_coef_table(r_hc3)
        if ct is not None:
            coef_tables.append(ct)

    # 外れ値除外（沖縄：失業率5.8%は突出）
    df_excl_okinawa = df[df["prefecture"] != "沖縄県"].copy()
    r_excl = run_ols(df_excl_okinawa, outcome,
                     ["aging_rate", "income_per_capita", "unemployment_rate"],
                     "M3_HbA1c_ExclOkinawa")
    if r_excl:
        results_list.append(r_excl)
        ct = extract_coef_table(r_excl)
        if ct is not None:
            coef_tables.append(ct)

    # ============================================================
    # OUTCOME 2: 糖尿病用剤処方量
    # ============================================================
    if "dm_drug_per_10k" in df.columns:
        log.info("\n### OUTCOME: 糖尿病用剤処方量 ###")
        outcome2 = "dm_drug_per_10k"

        models_drug = [
            ("M1_Drug_Univariate",  ["unemployment_rate"]),
            ("M2_Drug_AgeAdj",      ["aging_rate", "unemployment_rate"]),
            ("M3_Drug_FullModel",   ["aging_rate", "income_per_capita", "unemployment_rate"]),
        ]

        for mname, preds in models_drug:
            r = run_ols(df, outcome2, preds, mname)
            if r:
                results_list.append(r)
                ct = extract_coef_table(r)
                if ct is not None:
                    coef_tables.append(ct)

    # ============================================================
    # VIF チェック（フルモデル）
    # ============================================================
    full_preds = ["aging_rate", "income_per_capita", "pop_density", "unemployment_rate"]
    available = [p for p in full_preds if p in df.columns]
    vif_df = check_vif(df[available].dropna())
    log.info(f"\nVIF Check:\n{vif_df.to_string(index=False)}")
    high_vif = vif_df[vif_df["VIF"] > VIF_THRESHOLD]
    if len(high_vif) > 0:
        log.warning(f"High VIF detected: {high_vif['Variable'].tolist()}")
    else:
        log.info("VIF check passed: no multicollinearity issues")

    # ============================================================
    # 結果サマリー保存
    # ============================================================
    if coef_tables:
        df_coef = pd.concat(coef_tables, ignore_index=True)
        coef_path = RESULTS_DIR / "regression_coefficients.csv"
        df_coef.to_csv(coef_path, index=False, encoding="utf-8-sig")
        log.info(f"Saved coefficients: {coef_path}")

    # モデルフィット統計
    fit_rows = []
    for r in results_list:
        fit_rows.append({
            "model": r["model_name"],
            "outcome": r["outcome"],
            "n": r["n"],
            "r2": round(r["r2"], 4),
            "adj_r2": round(r["adj_r2"], 4),
            "f_stat": round(r["f_stat"], 3),
            "f_pvalue": round(r["f_pvalue"], 4),
            "aic": round(r["result"].aic, 2),
            "bic": round(r["result"].bic, 2),
        })
    df_fit = pd.DataFrame(fit_rows)
    fit_path = RESULTS_DIR / "model_fit_statistics.csv"
    df_fit.to_csv(fit_path, index=False, encoding="utf-8-sig")
    log.info(f"\nModel fit statistics:\n{df_fit.to_string(index=False)}")
    log.info(f"Saved: {fit_path}")

    # 失業率係数の感度分析サマリー（HbA1c）
    unemp_sens = df_coef[
        (df_coef["variable"] == "unemployment_rate") &
        (df_coef["model"].str.contains("HbA1c"))
    ][["model", "beta", "se", "p", "significant"]].copy()
    log.info(f"\n=== 感度分析サマリー（unemployment_rate → HbA1c高値率）===")
    log.info(unemp_sens.to_string(index=False))

    sig_count = unemp_sens["significant"].sum()
    total_count = len(unemp_sens)
    log.info(f"\n頑健性: {sig_count}/{total_count} モデルで失業率が有意 (p<0.05)")
    if sig_count >= int(total_count * 0.6):
        log.info("→ 結果は頑健: 主要モデルで一貫した有意性")
    else:
        log.info("→ 結果は不安定: 調整変数・外れ値に感応的")

    log.info("Phase 2 complete.")


if __name__ == "__main__":
    main()
