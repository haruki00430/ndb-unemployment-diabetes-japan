# Data Sources / データソース

This repository does **not** include NDB raw Excel files.  
All primary inputs are **publicly available** administrative open data.

本リポジトリは NDB 生 Excel ファイルを含みません。  
一次データはすべて公開情報から取得できます。

---

## 1. NDB Open Data / NDB オープンデータ（第10回）

| Item | Details |
|------|---------|
| Provider | Ministry of Health, Labour and Welfare (MHLW) / 厚生労働省 |
| Portal | https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177182.html |
| Round used | **第10回**（FY2022 specific health checkup; FY2023 medical claims） |
| Format | Excel (`.xlsx`) |
| Redistribution | **Raw files cannot be redistributed**; must be downloaded from portal |

### 1.1 Primary outcome: HbA1c high rate / 主要アウトカム：HbA1c高値割合

| Item | Value |
|------|-------|
| Category | `07_特定健診 検査` |
| Subfolder | `01_公費レセプトを含まないデータ` |
| File | HbA1c（ヘモグロビンA1c） 都道府県別性年齢階級別分布 (FY2022) |
| Definition | Proportion with HbA1c ≥ 6.5% among specific health checkup participants |
| Manuscript label | HbA1c high rate (%) |

**Calculation:**  
Sum counts with HbA1c ≥ 6.5% across all age–sex strata per prefecture → divide by total checkup participants.

### 1.2 Secondary outcome: Antidiabetic drug prescriptions / 副次アウトカム：抗糖尿病薬処方

| Item | Value |
|------|-------|
| Category | `05_処方薬 / 01_処方薬（内服）` |
| Subfolder | `01_公費レセプトを含まないデータ` |
| File | 薬効分類コード別都道府県別処方量 (FY2023) |
| Code | 薬効分類コード **396**（糖尿病用剤, including oral hypoglycemics and GLP-1 RAs） |
| Unit | Total quantity per 10,000 population |

---

## 2. Unemployment rate / 完全失業率

| Item | Details |
|------|---------|
| Provider | Statistics Bureau of Japan / 総務省統計局 |
| Survey | 労働力調査（基本集計）都道府県別結果 |
| Year | 2022 annual average |
| URL | https://www.stat.go.jp/data/roudou/pref/index.html |
| Variable | Complete unemployment rate (%) by prefecture |

**Note:** Values for FY2022 used in this study are embedded in `analysis/01_fetch_unemployment_data.py` as a dictionary (verified against the official table, retrieved 2026-03).

---

## 3. Population and area statistics / 人口・面積（2020年国勢調査）

| Item | Details |
|------|---------|
| Provider | Statistics Bureau of Japan / 総務省統計局 |
| Portal | https://www.e-stat.go.jp/ |
| Dataset | 2020 Population Census — prefecture-level totals |
| Variables | `aging_rate` (≥65 / total), `pop_density` (persons/km²) |
| e-Stat table ID | 国勢調査 2020 基本集計 都道府県別 |

---

## 4. Per-capita prefectural income / 1人当たり県民所得

| Item | Details |
|------|---------|
| Provider | Cabinet Office / 内閣府経済社会総合研究所 |
| Dataset | 県民経済計算 (Prefectural Accounts) FY2022 |
| URL | https://www.esri.cao.go.jp/jp/sna/data/data_list/kenmin/files/contents/main_r04.html |
| Unit | Thousand yen per person (千円/人) |

---

## 5. What we deposit vs. what you download / デポジットと取得の分担

| Data product | In `data/release/` | In Zenodo `v1.0.0` | User must download |
|--------------|:------------------:|:------------------:|:-----------------:|
| `analysis_dataset_prefecture_n47.csv` (N = 47) | ✅ Yes | ✅ Yes | — |
| NDB raw `.xlsx` | ❌ No | ❌ No | ✅ Yes (MHLW portal) |
| Census microdata | ❌ No | ❌ No | ✅ Yes (e-Stat) |

---

## 6. Licenses and attribution / ライセンス・引用

| Source | Condition |
|--------|-----------|
| NDB Open Data | Free for research; cite MHLW portal and round; no re-sharing of raw files |
| e-Stat | Follow portal terms; cite table name and retrieval date |
| Cabinet Office Prefectural Accounts | Follow terms; cite publication title and fiscal year |
| Statistics Bureau Labour Force Survey | Follow terms; cite survey name and year |

---

## 7. Local path configuration / ローカルパス設定

If running the full pipeline with NDB raw Excel, set paths in `config/config.yaml`:

```yaml
paths:
  ndb_hba1c_xlsx: "../../02_Data/raw/NDB_OpenData/No.10/07_特定健診 検査/..."
  ndb_drug_xlsx: "../../02_Data/raw/NDB_OpenData/No.10/05_処方薬/..."
  interim_dir: "data/interim"
  release_dir: "data/release"
```

Paths may point to a sibling `NDB_Research_Hub/02_Data/raw/` tree if you use the Hub monorepo layout.

---

**Last updated:** 2026-06-27
