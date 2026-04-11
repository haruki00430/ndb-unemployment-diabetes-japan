# NDB_XXX_diabetes_unemployment

失業率等と糖尿病関連指標の地域関連（NDB オープンデータ＋ e-Stat 等）。

## ステータス（2026-04-05 リポジトリ照合）

- **原稿**: `04_Manuscripts/Manuscript_diabetes_unemployment.qmd`（HTML 出力あり）
- **参考文献**: ルート `references.bib`、同 `vancouver.csl`
- **解析**: `analysis/01_fetch_unemployment_data.py`〜`04_insert_figures.py`、`analysis/logs/` にログ
- **結果**: `results/` に回帰・モデル適合等
- **設定**: `config/config.yaml`
- プロジェクト直下に README が無かったため新設。

## 注意

- NDB 生データは読取専用。実データを外部 AI に送信しない（`CLAUDE.md` 準拠）。
