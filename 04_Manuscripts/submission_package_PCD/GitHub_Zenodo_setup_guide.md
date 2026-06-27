# GitHub・Zenodo 公開手順ガイド

**プロジェクト**: NDB_XXX_diabetes_unemployment  
**論文**: Not All Social Determinants Travel  
**作成日**: 2026-06-27  

---

## 概要

PCD投稿に際し、再現性のためにコードとデータ（集計値のみ）をGitHub + Zenodo で公開する。  
**NDB生データは絶対に含めない**（NDBデータ利用規約・研究倫理上の禁止事項）。

---

## Section 1: GitHub リポジトリ準備

### 1-1. 既存リポジトリ名の確認・リネーム

現在のリポジトリ名が `NDB_XXX_diabetes_unemployment` のままであれば、論文タイトルに合わせてリネームを検討する。

**候補名（どちらか選択）**:
```
haruki00430/not-all-sdh-travel-diabetes-japan
haruki00430/ndb-unemployment-diabetes-ecological-japan
```

**リネーム手順（GitHub.com上）**:
1. https://github.com/haruki00430/NDB_XXX_diabetes_unemployment にアクセス
2. "Settings" タブ → "General" → "Repository name"
3. 新しいリポジトリ名を入力 → "Rename"
4. ⚠️ **リネーム後はローカルの remote URL を更新**:
   ```bash
   git remote set-url origin https://github.com/haruki00430/<新しいリポジトリ名>.git
   git remote -v   # 確認
   ```

> **参考**: 類似プロジェクトの命名例
> - `haruki00430/NDB_pollen_allergy_ecological_japan`（pollen_allergy_v2）
> - `haruki00430/social_isolation_bz_ndb_japan`（social_isolation_bz）

### 1-2. リポジトリの公開（Private → Public）

**手順**:
1. リポジトリ → Settings → General → Danger Zone
2. "Change repository visibility" → **"Make public"**
3. 確認ダイアログで "I understand, make this repository public" と入力

### 1-3. 公開前チェックリスト

- [ ] `02_Data/raw/` がリポジトリに**含まれていない**（.gitignore で除外確認）
- [ ] `.env`, APIキー, パスワードが含まれていない
- [ ] `02_Data/interim/` の大容量ファイルが除外されている
- [ ] `README.md` が存在し、内容が最新か確認
- [ ] ライセンスファイルが存在するか確認（MIT推奨）

### 1-4. README.md の最小構成

```markdown
# Not All Social Determinants Travel

Replication code for: Saito H, Ohira T. "Not All Social Determinants Travel: 
A Prefectural Ecological Analysis of Unemployment Rate and Diabetes Prevalence in Japan." 
*Primary Care Diabetes* (under review, 2026).

## Data sources
- NDB Open Data (10th edition, FY2022): https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177182.html
- Statistics Bureau Labour Force Survey: https://www.stat.go.jp/data/roudou/pref/index.html

## Reproduction
```bash
pip install -r requirements.txt
python 03_Analysis/analysis/00_aggregate_real_data.py
python 03_Analysis/analysis/02_visualization_eda.py
```

## License
MIT
```

---

## Section 2: Zenodo アーカイブ

### 2-1. GitHub-Zenodo 連携（推奨）

**メリット**: GitHub Release を作るだけで自動的にDOIが発行される。

**初回設定手順**:
1. https://zenodo.org にサインイン（GitHub OAuth連携）
2. 右上メニュー → "GitHub" タブ
3. リポジトリ一覧から `NDB_XXX_diabetes_unemployment`（またはリネーム後の名前）を **ON** に切り替え
4. "Save" をクリック

### 2-2. DOI取得（GitHub Release作成）

1. GitHubリポジトリ → "Releases" → "Draft a new release"
2. **Tag**: `v1.0.0`
3. **Title**: `v1.0.0 – Initial release for Primary Care Diabetes submission`
4. **Description**:
   ```
   Replication code for: Saito H, Ohira T. "Not All Social Determinants Travel: 
   A Prefectural Ecological Analysis of Unemployment Rate and Diabetes Prevalence in Japan."
   Primary Care Diabetes (under review, 2026).
   
   ## Contents
   - Analysis scripts (03_Analysis/)
   - Integrated dataset (aggregate only, no NDB raw data)
   - Manuscript source (04_Manuscripts/)
   ```
5. **"Publish release"** をクリック
6. 数分後、Zenodo で DOI が発行される（例: `10.5281/zenodo.XXXXXXX`）

### 2-3. Zenodo メタデータ入力

Zenodo側で自動作成されたメタデータを確認・編集:

| 項目 | 内容 |
|------|------|
| **Title** | Not All Social Determinants Travel: A Prefectural Ecological Analysis of Unemployment Rate and Diabetes Prevalence in Japan – Analysis Code |
| **Authors** | Saito, Haruki; Ohira, Tetsuya |
| **Description** | Replication code for the ecological study of unemployment rate and diabetes prevalence across 47 Japanese prefectures using NDB Open Data. |
| **Keywords** | diabetes; unemployment; social determinants; ecological study; Japan; NDB Open Data |
| **License** | MIT |
| **Related publication** | （受理後にDOIを入力） |

### 2-4. DOI を原稿に反映

Zenodo DOI発行後:
1. `04_Manuscripts/Not_All_Social_Determinants_Travel_20260627.docx` の Data Availability セクションを更新:
   - `"DOI to be assigned upon repository release"` → `"https://doi.org/10.5281/zenodo.XXXXXXX"`
2. 投稿前に最終版DOCXを再確認

---

## Section 3: 参考プロジェクトとの比較

| プロジェクト | GitHubリポジトリ | Zenodo DOI |
|------------|----------------|-----------|
| slope_fracture | Public公開済み | 10.5281/zenodo.20452953 |
| social_isolation_bz | Public公開済み | 10.5281/zenodo.20713830 |
| pollen_allergy_v2 | Public公開済み | GitHub/Zenodo公開済み |
| **diabetes_unemployment** | **要公開** | **要取得** |

---

## タイムライン

| 作業 | タイミング |
|------|-----------|
| GitHub公開前チェック | 投稿前日 |
| リポジトリ Public 化 | 投稿当日 |
| GitHub Release → Zenodo DOI取得 | 投稿当日 |
| DOCXのData Availability更新 | DOI取得直後 |
| Editorial Manager に投稿 | DOI確認後 |

---

*作成: Claude Sonnet 4.6 支援 / 2026-06-27*
