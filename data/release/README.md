# data/release — Prefecture-Level Aggregated Dataset / 都道府県別集計データ

This folder contains the **prefecture-level aggregated analysis dataset** (N = 47) used in:

> Saito H, Ohira T. "Not All Social Determinants Travel: A Prefectural Ecological Analysis of Unemployment Rate and Diabetes Prevalence in Japan." *Primary Care Diabetes* (under review, 2026).

## Files / ファイル一覧

| File | Description |
|------|-------------|
| `analysis_dataset_prefecture_n47.csv` | Main analysis table (47 rows × 7 columns) |

## Column dictionary / 変数辞書

| Column | Unit | Description (EN) | 説明（日本語） |
|--------|------|-------------------|--------------|
| `prefecture_jp` | — | Prefecture name (Japanese) | 都道府県名 |
| `hba1c_high_rate_pct` | % | Proportion of specific health checkup participants with HbA1c ≥ 6.5%, FY2022 | 特定健診参加者中HbA1c≥6.5%の割合（R4年度） |
| `antidiabetic_drug_per10k` | count/10,000 pop | Antidiabetic drug prescriptions (code 396) per 10,000 population, FY2023 | 抗糖尿病薬処方量（薬効コード396）人口10万対（R5年度レセプト） |
| `unemployment_rate_pct` | % | Complete unemployment rate (2022 annual average, Labour Force Survey) | 完全失業率（2022年平均、労働力調査） |
| `aging_rate_pct` | % | Proportion of population aged ≥ 65 years (2020 Census) | 高齢化率（65歳以上人口割合、2020国勢調査） |
| `income_per_capita_kyen` | thousand yen | Per-capita prefectural income, FY2022 | 都道府県民所得（1人当たり、千円、R4年度） |
| `pop_density_per_km2` | persons/km² | Population density (2020 Census) | 人口密度（人/km²、2020国勢調査） |

## Data provenance / データの出典

All values are derived solely from **publicly available** aggregate statistics:

- NDB Open Data 10th edition: https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177182.html
- Statistics Bureau Labour Force Survey: https://www.stat.go.jp/data/roudou/pref/index.html
- e-Stat / 2020 Population Census: https://www.e-stat.go.jp/
- Cabinet Office Prefectural Income Statistics: https://www.esri.cao.go.jp/jp/sna/data/data_list/kenmin/files/contents/main_r04.html

**NDB raw Excel files are NOT included** in this repository and cannot be redistributed (MHLW terms). They must be downloaded from the portal above.

## License / ライセンス

`data/release/` files are released under **CC BY 4.0** (see `LICENSE-DATA` in repository root).  
Cite the Zenodo DOI, this repository, and the original data sources listed above.

## Headline values (from manuscript) / 主要統計値（論文掲載値）

| Quantity | Value |
|----------|-------|
| N (prefectures) | 47 |
| Unemployment rate range | 1.5–5.8% (mean 2.6%, SD 0.7%) |
| HbA1c high rate range | 6.0–9.7% (mean 7.7%, SD 0.8%) |
| Pearson r (unemployment × HbA1c) | −0.016 (p = 0.916) |
| Pearson r (income × HbA1c) | −0.570 (p < 0.001) |
