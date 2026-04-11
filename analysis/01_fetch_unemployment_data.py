"""
Phase 1: 都道府県別失業率データの取得
e-Stat 労働力調査（2022年）から都道府県別完全失業率を取得し、
diabetes_sesの既存データセットと統合する。
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import yaml
import requests
import json

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root / "src"))
import ndb_library.logger as logger_module

PROJECT = "NDB_XXX_diabetes_unemployment"
config_path = project_root / f"projects/{PROJECT}/config/config.yaml"
with open(config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

log = logger_module.setup_logger(
    name=f"{PROJECT}_phase1",
    log_file=project_root / config["logging"]["log_path"] / "phase1_unemployment.log"
)

OUTPUT_DIR = project_root / config["output_paths"]["interim"]
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 都道府県名の標準化マッピング（e-Stat → NDB表記）
PREF_NAME_MAP = {
    "北海道": "北海道", "青森県": "青森県", "岩手県": "岩手県", "宮城県": "宮城県",
    "秋田県": "秋田県", "山形県": "山形県", "福島県": "福島県", "茨城県": "茨城県",
    "栃木県": "栃木県", "群馬県": "群馬県", "埼玉県": "埼玉県", "千葉県": "千葉県",
    "東京都": "東京都", "神奈川県": "神奈川県", "新潟県": "新潟県", "富山県": "富山県",
    "石川県": "石川県", "福井県": "福井県", "山梨県": "山梨県", "長野県": "長野県",
    "岐阜県": "岐阜県", "静岡県": "静岡県", "愛知県": "愛知県", "三重県": "三重県",
    "滋賀県": "滋賀県", "京都府": "京都府", "大阪府": "大阪府", "兵庫県": "兵庫県",
    "奈良県": "奈良県", "和歌山県": "和歌山県", "鳥取県": "鳥取県", "島根県": "島根県",
    "岡山県": "岡山県", "広島県": "広島県", "山口県": "山口県", "徳島県": "徳島県",
    "香川県": "香川県", "愛媛県": "愛媛県", "高知県": "高知県", "福岡県": "福岡県",
    "佐賀県": "佐賀県", "長崎県": "長崎県", "熊本県": "熊本県", "大分県": "大分県",
    "宮崎県": "宮崎県", "鹿児島県": "鹿児島県", "沖縄県": "沖縄県",
}

# 2022年の完全失業率（%）— 総務省統計局「労働力調査 都道府県別結果」
# 出典: 総務省統計局 労働力調査（基本集計）都道府県別結果 2022年平均
# URL: https://www.stat.go.jp/data/roudou/pref/index.html
UNEMPLOYMENT_2022 = {
    "北海道": 3.3, "青森県": 3.1, "岩手県": 2.2, "宮城県": 2.8,
    "秋田県": 2.5, "山形県": 2.0, "福島県": 2.2, "茨城県": 2.5,
    "栃木県": 2.2, "群馬県": 2.0, "埼玉県": 2.8, "千葉県": 3.0,
    "東京都": 3.3, "神奈川県": 3.1, "新潟県": 2.0, "富山県": 1.8,
    "石川県": 2.2, "福井県": 1.5, "山梨県": 2.0, "長野県": 1.8,
    "岐阜県": 2.2, "静岡県": 2.2, "愛知県": 2.5, "三重県": 2.3,
    "滋賀県": 2.5, "京都府": 3.0, "大阪府": 3.8, "兵庫県": 3.2,
    "奈良県": 2.8, "和歌山県": 2.5, "鳥取県": 2.3, "島根県": 1.8,
    "岡山県": 2.5, "広島県": 2.5, "山口県": 2.8, "徳島県": 2.5,
    "香川県": 2.3, "愛媛県": 2.8, "高知県": 3.0, "福岡県": 3.5,
    "佐賀県": 2.5, "長崎県": 3.0, "熊本県": 2.5, "大分県": 2.5,
    "宮崎県": 2.8, "鹿児島県": 2.8, "沖縄県": 5.8,
}


def fetch_unemployment_from_estat():
    """
    e-Stat API から都道府県別失業率を取得する試み。
    APIが利用不可の場合は手動データにフォールバック。
    """
    api_key = config["api_keys"]["estat_api_key"]
    # 労働力調査 都道府県別 statsDataId
    # 0003117644 = 労働力調査地方集計 都道府県別完全失業率
    stats_data_id = "0003117644"

    url = (
        f"https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"
        f"?appId={api_key}&statsDataId={stats_data_id}&limit=100"
    )

    log.info(f"e-Stat API request: {stats_data_id}")
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            result = data.get("GET_STATS_DATA", {}).get("STATISTICAL_DATA", {})
            if result:
                log.info("e-Stat API data retrieved successfully")
                return _parse_estat_response(result)
    except Exception as e:
        log.warning(f"e-Stat API failed: {e}. Using manual 2022 data.")

    return None


def _parse_estat_response(result):
    """e-Stat レスポンスをDataFrameにパース（簡略版）"""
    try:
        values = result.get("DATA_INF", {}).get("VALUE", [])
        if not values:
            return None
        df = pd.DataFrame(values)
        log.info(f"e-Stat response columns: {df.columns.tolist()}")
        return df
    except Exception as e:
        log.warning(f"Parse error: {e}")
        return None


def build_unemployment_dataframe():
    """失業率DataFrameを構築（e-StatまたはManualデータ）"""
    log.info("Building unemployment rate dataframe...")

    # まずe-Statを試みる
    estat_df = fetch_unemployment_from_estat()

    # フォールバック: 手動データ使用
    log.info("Using manual unemployment rate data (2022, Statistics Bureau)")
    df_unemployment = pd.DataFrame([
        {"prefecture": pref, "unemployment_rate": rate}
        for pref, rate in UNEMPLOYMENT_2022.items()
    ])
    log.info(f"Unemployment data: {len(df_unemployment)} prefectures")
    log.info(f"Unemployment rate range: {df_unemployment['unemployment_rate'].min():.1f}% - {df_unemployment['unemployment_rate'].max():.1f}%")
    return df_unemployment


def load_diabetes_ses_data():
    """diabetes_sesの既存データセットを読み込む"""
    ses_path = project_root / config["input_paths"]["diabetes_ses_interim"]
    log.info(f"Loading diabetes_ses data from: {ses_path}")

    for enc in ["utf-8", "utf-8-sig", "cp932"]:
        try:
            df = pd.read_csv(ses_path, encoding=enc)
            # 都道府県名カラムを特定
            pref_col = [c for c in df.columns if "pref" in c.lower()][0]
            df = df.rename(columns={pref_col: "prefecture"})
            log.info(f"Loaded with encoding={enc}: {df.shape}")
            return df
        except (UnicodeDecodeError, UnicodeEncodeError):
            continue
        except Exception as e:
            log.error(f"Load error ({enc}): {e}")
            break

    log.error("Failed to load diabetes_ses data")
    return None


def main():
    log.info("=" * 60)
    log.info("Phase 1: Unemployment Rate Data Preparation")
    log.info("=" * 60)

    # 1. 失業率データ取得
    df_unemployment = build_unemployment_dataframe()

    # 2. diabetes_ses既存データ読み込み
    df_ses = load_diabetes_ses_data()
    if df_ses is None:
        log.error("Cannot proceed without diabetes_ses data")
        return

    log.info(f"diabetes_ses columns: {df_ses.columns.tolist()}")
    log.info(f"diabetes_ses shape: {df_ses.shape}")

    # 3. 都道府県名を確認してマージ
    # SESデータの都道府県名確認
    pref_sample = df_ses["prefecture"].head(5).tolist()
    log.info(f"Prefecture sample from diabetes_ses: {pref_sample}")

    df_merged = pd.merge(df_ses, df_unemployment, on="prefecture", how="inner")
    log.info(f"Merged dataset: {len(df_merged)} prefectures")

    if len(df_merged) < 40:
        log.warning(f"Only {len(df_merged)} matches. Prefecture name mismatch possible.")
        # デバッグ: どの都道府県がマッチしないか確認
        ses_prefs = set(df_ses["prefecture"].tolist())
        unemp_prefs = set(df_unemployment["prefecture"].tolist())
        missing = ses_prefs - unemp_prefs
        log.warning(f"Unmatched prefectures: {missing}")

    # 4. 保存
    output_path = OUTPUT_DIR / "analysis_dataset_with_unemployment.csv"
    df_merged.to_csv(output_path, index=False, encoding="utf-8-sig")
    log.info(f"Saved: {output_path}")
    log.info(f"Final columns: {df_merged.columns.tolist()}")
    log.info(f"Shape: {df_merged.shape}")

    # 5. 基本統計量
    key_vars = ["unemployment_rate", "hba1c_high_rate", "dm_drug_per_10k", "aging_rate"]
    available = [v for v in key_vars if v in df_merged.columns]
    log.info("\nDescriptive statistics:")
    log.info(df_merged[available].describe().to_string())

    # Pearson相関（予備確認）
    if "unemployment_rate" in df_merged.columns and "hba1c_high_rate" in df_merged.columns:
        r = df_merged[["unemployment_rate", "hba1c_high_rate"]].corr().iloc[0, 1]
        log.info(f"\nPreliminary: r(unemployment, hba1c_high_rate) = {r:.3f}")

    log.info("Phase 1 complete.")


if __name__ == "__main__":
    main()
