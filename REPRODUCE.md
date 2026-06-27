# Reproduction Guide / 再現手順書

**Project:** `NDB_XXX_diabetes_unemployment`  
**Manuscript:** *Not All Social Determinants Travel: A Prefectural Ecological Analysis of Unemployment Rate and Diabetes Prevalence in Japan*  
**Repository:** https://github.com/haruki00430/NDB_XXX_diabetes_unemployment  
**Zenodo DOI:** `10.5281/zenodo.XXXXXXX` — *replace before public release*

This guide describes how to reproduce the **prefecture-level aggregated analysis (N = 47)** reported in the manuscript.  
本書は論文に報告した **47都道府県の集計解析** を再現する手順です。

---

## What this repository includes / 含むもの・含まないもの

| Included | Not included (download separately) |
|----------|-----------------------------------|
| Analysis scripts (`analysis/`) | NDB raw Excel (MHLW portal) |
| `data/release/analysis_dataset_prefecture_n47.csv` (N = 47) | Individual-level claims |
| `REPRODUCE.md`, `DATA_SOURCES.md` | Files > 100 MB (GitHub limit) |
| Result summaries under `results/` | Private HbA1c/drug intermediate CSVs |

Under MHLW rules, **individual-level claims and prefecture-level raw NDB Excel cannot be redistributed**. The `data/release/` CSV is derived from public open data only and is sufficient to reproduce all regression and visualization outputs.

---

## System requirements / システム要件

| Item | Requirement |
|------|-------------|
| Python | 3.10 or later (3.11+ tested on Windows 11) |
| OS | Windows 10/11, macOS 12+, Ubuntu 20.04+ |
| RAM | 4 GB minimum |
| Disk | ~200 MB (without NDB raw files) |

---

## Step 0: Clone and environment / 環境構築

```bash
git clone https://github.com/haruki00430/NDB_XXX_diabetes_unemployment.git
cd NDB_XXX_diabetes_unemployment

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Route 1 — Minimal reproduction (recommended for reviewers) / 最小再現（推奨）

Uses the committed **`data/release/analysis_dataset_prefecture_n47.csv`** only. **No NDB download required.**

### 1.1 Verify release file

```bash
python -c "
import pandas as pd
df = pd.read_csv('data/release/analysis_dataset_prefecture_n47.csv')
print('N rows:', len(df))
print('Columns:', df.columns.tolist())
print(df.describe().round(3))
"
```

Expected: 47 rows, 7 columns. See `data/release/README.md` for column definitions.

### 1.2 Run regression analysis

```bash
python analysis/02_regression_analysis.py
```

**Expected headline values (tolerance):**

| Quantity | Expected | Tolerance |
|----------|----------|-----------|
| N prefectures | 47 | exact |
| Pearson r (unemployment × HbA1c) | −0.016 | ±0.001 |
| Pearson r (income × HbA1c) | −0.570 | ±0.001 |
| Model 3 β (unemployment) | −0.007 | ±0.001 |
| Model 3 p (unemployment) | 0.966 | ±0.01 |
| Model 3 R² | 0.41 | ±0.01 |

Outputs written to: `results/regression_coefficients.csv`, `results/model_fit_statistics.csv`

### 1.3 Reproduce figures

```bash
python analysis/03_visualization.py
```

Outputs: `results/figures/Fig1_unemployment_hba1c_scatter.png`, `Fig2_*`, `Fig3_*`

---

## Route 2 — Full rebuild from public sources / フル再構築

Follow **[`DATA_SOURCES.md`](DATA_SOURCES.md)** to download:

1. NDB Open Data No.10 — HbA1c checkup results (特定健診 検査項目)
2. NDB Open Data No.10 — Antidiabetic drug prescriptions (処方薬 薬効コード396)
3. Statistics Bureau — Prefecture unemployment rates 2022 (Labour Force Survey)
4. e-Stat — 2020 census aging rates, population density
5. Cabinet Office — Per-capita prefectural income FY2022

### 2.1 Full pipeline entry point

```bash
python analysis/01_fetch_unemployment_data.py   # Build integrated dataset
python analysis/02_regression_analysis.py       # OLS regression + sensitivity
python analysis/03_visualization.py             # Figures (Japanese labels)
python analysis/03_visualization_english.py     # Figures (English labels, for submission)
```

Each script writes its output to `data/interim/` or `results/` and logs to `analysis/logs/`.

### 2.2 Manuscript DOCX

The submission DOCX (`04_Manuscripts/Not_All_Social_Determinants_Travel_20260627.docx`) was produced by modifying the Quarto output via python-docx. To generate a fresh DOCX from the QMD source:

```bash
quarto render 04_Manuscripts/Manuscript_PCD.qmd --to docx
```

---

## Zenodo ↔ GitHub release workflow / リリース手順

1. Pass pre-release checklist (see `04_Manuscripts/submission_package_PCD/submission_workflow_PCD.md`)
2. Tag `v1.0.0` on GitHub after confirming no secrets/raw NDB in tracked files
3. Enable **Zenodo–GitHub integration** at https://zenodo.org/account/settings/github/
4. Replace `10.5281/zenodo.XXXXXXX` in this file and in manuscript Data Availability section
5. Publish Zenodo record (may follow journal acceptance per MHLW policy)

---

## Troubleshooting / トラブルシューティング

| Issue | Action |
|-------|--------|
| `ModuleNotFoundError: ndb_library` | Run from Hub root or adjust `sys.path`; see script header for path setup |
| `UnicodeEncodeError` on Windows console | Run `chcp 65001` or use VS Code terminal; scripts use UTF-8 throughout |
| CSV not tracked by git | Only `data/release/*.csv` is whitelisted; `data/interim/` CSVs are gitignored |
| Headline β slightly different | Confirm you are using `data/release/analysis_dataset_prefecture_n47.csv` exactly |

---

## Citation / 引用

If you use this repository or the Zenodo archive, please cite:

- **Paper**: Saito H, Ohira T. "Not All Social Determinants Travel..." *Primary Care Diabetes* (2026).
- **Software/data**: See `CITATION.cff` and the Zenodo DOI above.
- **Primary data**: MHLW NDB Open Data, Statistics Bureau (see `DATA_SOURCES.md`).

---

## Document map / 関連ドキュメント

| File | Purpose |
|------|---------|
| [`DATA_SOURCES.md`](DATA_SOURCES.md) | Official download URLs and file locations |
| [`data/release/README.md`](data/release/README.md) | Column-level dictionary for N = 47 CSV |
| [`analysis/README.md`](analysis/README.md) | Plain-English guide to each Python script |
| [`CITATION.cff`](CITATION.cff) | Machine-readable citation metadata |
| [`config/config.yaml`](config/config.yaml) | Project settings and paths |

**Last updated:** 2026-06-27
