> **正本リポジトリ (GitHub):** https://github.com/haruki00430/ndb-unemployment-diabetes-japan  
> **再現・公開:** [`REPRODUCE.md`](REPRODUCE.md) · [`DATA_SOURCES.md`](DATA_SOURCES.md) · [`analysis/README.md`](analysis/README.md) · [`CITATION.cff`](CITATION.cff)

# Not All Social Determinants Travel

## Unemployment Rate and Diabetes Prevalence in Japan — Prefecture-Level Ecological Analysis

**論文タイトル（日本語）**: 失業率は糖尿病指標の地域差を予測しない——社会的決定因の文脈依存性：全国47都道府県の生態学的研究

**Manuscript status**: ~~*Primary Care Diabetes* (PCD-D-26-00735, desk rejected 2026-06-30)~~ → **Submitted** to *Journal of Preventive Medicine and Hygiene* (JPMH) on 2026-06-30  
**運用メモ**: [`MEMORY.md`](MEMORY.md)（投稿後ステータス・次アクション）  
**Repository:** https://github.com/haruki00430/ndb-unemployment-diabetes-japan  
**Zenodo DOI:** https://doi.org/10.5281/zenodo.20949288

---

## Abstract / 研究概要

We conducted a prefecture-level ecological study to examine whether regional unemployment rates predict diabetes prevalence across Japan's 47 prefectures. Using NDB Open Data (10th edition, FY2022 health checkups), we found that unemployment rate showed virtually no ecological association with the proportion of residents with HbA1c ≥ 6.5% (Pearson r = −0.016, p = 0.916), robust across six OLS model specifications. By contrast, per-capita prefectural income was a strong inverse predictor (r = −0.570, p < 0.001). These findings suggest that social determinants of diabetes may not transfer universally across different socioeconomic and institutional contexts.

失業率と都道府県別HbA1c高値割合の間に有意な関連は認められなかった（r = −0.016, p = 0.916）。一方、1人当たり県民所得は強い逆相関を示した（r = −0.570, p < 0.001）。社会的決定因の予測力は制度・労働市場の文脈に依存することを示唆する。

---

## Submission / 投稿情報

| 項目 | 内容 |
|------|------|
| Journal | [Journal of Preventive Medicine and Hygiene](https://www.jpmh.org) (Pacini Editore) |
| Submitted | 2026-06-30 |
| Status | Under review |
| Portal | https://www.jpmh.org |
| Previous submission | Primary Care Diabetes (PCD-D-26-00735, 2026-06-27; desk rejected 2026-06-30) |

Post-submission tracking: **[MEMORY.md](MEMORY.md)**

---

```
ndb-unemployment-diabetes-japan/
├── analysis/                  # Analysis scripts (01–04) / 解析スクリプト
│   ├── README.md              # Script guide / スクリプト解説
│   ├── 01_fetch_unemployment_data.py
│   ├── 02_regression_analysis.py
│   ├── 03_visualization.py
│   └── 04_insert_figures.py
├── config/
│   └── config.yaml            # Project settings / プロジェクト設定
├── data/
│   └── release/               # Public aggregated data (N = 47) / 公開集計データ
│       ├── analysis_dataset_prefecture_n47.csv
│       └── README.md          # Column dictionary / 変数辞書
├── results/
│   └── figures/               # Output figures (PNG, 300 dpi)
├── 04_Manuscripts/
│   ├── Manuscript_PCD.qmd              # Quarto source (PCD-specific)
│   └── submission_package_PCD/         # PCD submission package (DOCX, figures, approved PDF)
│       ├── Manuscript_PCD.docx
│       ├── PCD-S-26-00913 (2).pdf      # Final approved submission PDF
│       └── README_UPLOAD_ORDER.md
├── MEMORY.md                           # Post-submission ops log / 投稿後運用メモ
├── references.bib             # BibTeX references
├── vancouver.csl              # Citation style
├── REPRODUCE.md               # Reproduction guide / 再現手順書
├── DATA_SOURCES.md            # Data download instructions / データ取得先
├── CITATION.cff               # Machine-readable citation
├── LICENSE                    # MIT (code)
├── LICENSE-DATA               # CC BY 4.0 (data/release/)
└── requirements.txt           # Python dependencies
```

---

## Quick start / クイックスタート

```bash
git clone https://github.com/haruki00430/ndb-unemployment-diabetes-japan.git
cd ndb-unemployment-diabetes-japan

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### Minimal reproduction (no NDB download required) / 最小再現（NDBダウンロード不要）

```bash
# Uses data/release/analysis_dataset_prefecture_n47.csv
python analysis/02_regression_analysis.py
python analysis/03_visualization.py
```

For full pipeline instructions, see **[REPRODUCE.md](REPRODUCE.md)**.

---

## Data sources / データソース

| Source | Description | URL |
|--------|-------------|-----|
| NDB Open Data (10th edition) | HbA1c, antidiabetic drug prescriptions | https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177182.html |
| Statistics Bureau Labour Force Survey | Prefecture-level unemployment rate 2022 | https://www.stat.go.jp/data/roudou/pref/index.html |
| e-Stat / 2020 Population Census | Aging rate, population density | https://www.e-stat.go.jp/ |
| Cabinet Office Prefectural Income | Per-capita prefectural income FY2022 | https://www.esri.cao.go.jp/jp/sna/data/data_list/kenmin/ |

**NDB raw Excel files are NOT included** in this repository (MHLW redistribution terms). See [DATA_SOURCES.md](DATA_SOURCES.md) for download instructions.

---

## Key results / 主要結果

| Indicator | Pearson r | p value |
|-----------|-----------|---------|
| Unemployment rate × HbA1c high rate | −0.016 | 0.916 |
| Per-capita income × HbA1c high rate | −0.570 | <0.001 |
| Unemployment: OLS β (6 models) | all near 0 | all ≥ 0.495 |

---

## Authors / 著者

| Name | Affiliation | ORCID |
|------|-------------|-------|
| **Haruki Saito** (Corresponding) | Department of Epidemiology, Fukushima Medical University School of Medicine | [0009-0009-7890-6068](https://orcid.org/0009-0009-7890-6068) |
| Tetsuya Ohira | Department of Epidemiology, Fukushima Medical University School of Medicine, Fukushima, Japan; Radiation Medical Science Center for the Fukushima Health Management Survey, Fukushima Medical University, Fukushima, Japan | [0000-0003-4532-7165](https://orcid.org/0000-0003-4532-7165) |

---

## Citation / 引用

If you use this code or data, please cite:

```
Saito H, Ohira T. Not All Social Determinants Travel: A Prefectural Ecological 
Analysis of Unemployment Rate and Diabetes Prevalence in Japan.
Journal of Preventive Medicine and Hygiene (submitted 2026-06-30).
GitHub: https://github.com/haruki00430/ndb-unemployment-diabetes-japan
Zenodo DOI: https://doi.org/10.5281/zenodo.20949288
```

See also [`CITATION.cff`](CITATION.cff) for machine-readable metadata.

---

## License / ライセンス

- **Code** (`analysis/`, `config/`, scripts): [MIT License](LICENSE)
- **Aggregated data** (`data/release/`): [CC BY 4.0](LICENSE-DATA)
- **NDB raw data**: Not included; subject to MHLW portal terms

---

## Notes / 注意事項

- NDB生データは本リポジトリに含まれていません（厚生労働省利用規約上の再配布禁止）
- 公開集計データ（`data/release/`）のみ CC BY 4.0 で公開
- 個人識別可能なデータは一切含まれていません

**Last updated**: 2026-06-30 (Re-submitted to JPMH; PCD desk rejected 2026-06-30)
