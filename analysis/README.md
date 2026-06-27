# Analysis Scripts / 解析スクリプト解説

This folder contains the four sequential analysis scripts for the study:
> *Not All Social Determinants Travel: A Prefectural Ecological Analysis of Unemployment Rate and Diabetes Prevalence in Japan*

このフォルダには論文の全解析を再現するための4本のスクリプトが含まれます。

---

## Execution order / 実行順序

```bash
# Step 1: Build integrated prefecture-level dataset
python analysis/01_fetch_unemployment_data.py

# Step 2: OLS regression and sensitivity analyses
python analysis/02_regression_analysis.py

# Step 3: Figures (Japanese labels, for internal use)
python analysis/03_visualization.py

# Step 3b: Figures (English labels, for journal submission)
python analysis/03_visualization_english.py

# Step 4: Insert figures into DOCX (optional)
python analysis/04_insert_figures.py
```

For reviewers who wish to skip NDB download, start from **Step 2** using `data/release/analysis_dataset_prefecture_n47.csv`.

---

## Script descriptions / スクリプト詳細

### `01_fetch_unemployment_data.py`

**Purpose (EN):** Retrieves prefecture-level unemployment rates from the Statistics Bureau Labour Force Survey (2022 annual) and merges them with the existing HbA1c and antidiabetic drug data from NDB Open Data to produce the integrated analysis dataset.

**目的（日本語）:** 総務省統計局「労働力調査 都道府県別結果（2022年平均）」から都道府県別完全失業率を取得し、NDB Open Dataから得たHbA1c高値割合・抗糖尿病薬処方量データと統合して解析用データセットを構築する。

**Inputs:**
- NDB Open Data 10th edition: HbA1c checkup (FY2022), antidiabetic drug prescriptions (FY2023)
- Labour Force Survey unemployment rates 2022 (embedded dictionary, source verified)
- e-Stat census covariates (aging rate, population density)
- Cabinet Office per-capita prefectural income FY2022

**Outputs:**
- `data/interim/analysis_dataset_with_unemployment.csv` (47 rows × 13 columns)

**Logs:** `analysis/logs/phase1_unemployment.log`

---

### `02_regression_analysis.py`

**Purpose (EN):** Estimates Pearson correlations and six sequential OLS regression models with the HbA1c high rate as the primary outcome and unemployment rate as the main exposure. Includes HC3 robust standard errors (Model 5) and outlier exclusion sensitivity analysis (Model 6, Okinawa excluded). Also runs secondary analysis with antidiabetic drug prescriptions as outcome.

**目的（日本語）:** HbA1c高値割合を従属変数、失業率を主要曝露変数とした6段階のOLS回帰モデルを推定する。感度分析としてHC3頑健標準誤差（Model 5）・外れ値除外（Model 6、沖縄県除外）を実施。副次解析として抗糖尿病薬処方量を従属変数とした解析も実施。

**Inputs:** `data/interim/analysis_dataset_with_unemployment.csv` or `data/release/analysis_dataset_prefecture_n47.csv`

**Outputs:**
- `results/regression_coefficients.csv` — β, SE, t, p, 95%CI for all models
- `results/model_fit_statistics.csv` — R², adj-R², F-stat, AIC, BIC

**Key results (from manuscript):**

| Model | Unemployment β | p | R² |
|-------|---------------|---|-----|
| Model 1 (univariate) | −0.103 | 0.490 | 0.011 |
| Model 3 (primary) | −0.007 | 0.966 | 0.41 |
| Model 5 (HC3) | −0.007 | 0.967 | 0.41 |
| Model 6 (−Okinawa) | −0.020 | 0.900 | 0.43 |

**Logs:** `analysis/logs/phase2_regression.log`

---

### `03_visualization.py`

**Purpose (EN):** Generates the four main figures with Japanese axis labels.

**目的（日本語）:** 日本語ラベルで4種類の主要図を生成する。

**Outputs (300 dpi PNG):**
- `results/figures/Fig1_unemployment_hba1c_scatter.png` — Scatter plot: unemployment × HbA1c
- `results/figures/Fig2_unemployment_drug_scatter.png` — Scatter plot: unemployment × antidiabetic drug
- `results/figures/Fig3_forest_sensitivity_hba1c.png` — Forest plot: β across 6 models
- `results/figures/Fig4_prefecture_ranking.png` — Prefecture ranking chart

**Logs:** `analysis/logs/phase3_visualization.log`

---

### `03_visualization_english.py`

**Purpose (EN):** Same figures as `03_visualization.py` but with English labels, suitable for international journal submission.

**目的（日本語）:** `03_visualization.py` と同内容だが、英語ラベルで生成（国際誌投稿用）。

**Outputs:** `results/figures/en/Fig1_*_en.png`, `Fig2_*_en.png`, `Fig3_*_en.png`

---

### `04_insert_figures.py`

**Purpose (EN):** Inserts figure image files into a DOCX manuscript template at the appropriate locations (after each Figure legend paragraph).

**目的（日本語）:** FigureレジェンドのDOCX段落直後に図を挿入するユーティリティ。

---

## Common settings / 共通設定

All scripts load `config/config.yaml` for file paths and project settings.  
全スクリプトは `config/config.yaml` からパスと設定を読み込みます。

```yaml
# config/config.yaml (excerpt)
output_paths:
  interim: "data/interim"
  results: "results"
logging:
  log_path: "analysis/logs"
```

Scripts use `ndb_library.logger` from the NDB Research Hub shared library. If running outside the monorepo, install the library or adjust the `sys.path` at the top of each script.

スクリプトはNDB Research Hubの共有ライブラリ `ndb_library.logger` を使用します。モノレポ外で実行する場合は、スクリプト冒頭の `sys.path` を調整してください。

---

**Last updated:** 2026-06-27
