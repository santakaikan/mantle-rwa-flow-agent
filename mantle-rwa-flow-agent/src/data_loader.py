from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


REQUIRED_COLUMNS = [
    "asset_name",
    "symbol",
    "category",
    "chain",
    "protocol",
    "tvl_usd",
    "volume_24h_usd",
    "holders",
    "active_addresses_30d",
    "transfer_count_30d",
    "top_10_holder_share",
    "has_secondary_market",
    "has_lending_market",
    "has_oracle",
    "has_agent_access",
    "notes",
]

BOOLEAN_COLUMNS = [
    "has_secondary_market",
    "has_lending_market",
    "has_oracle",
    "has_agent_access",
]

NUMERIC_COLUMNS = [
    "tvl_usd",
    "volume_24h_usd",
    "holders",
    "active_addresses_30d",
    "transfer_count_30d",
    "top_10_holder_share",
]


def load_asset_data(csv_path: str | Path) -> pd.DataFrame:
    """Load asset data from CSV and enforce a predictable schema."""
    csv_path = Path(csv_path)
    data = pd.read_csv(csv_path)
    validate_columns(data.columns)
    data = normalize_types(data)
    return data


def validate_columns(columns: Iterable[str]) -> None:
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in columns]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"CSV is missing required columns: {missing}")


def normalize_types(data: pd.DataFrame) -> pd.DataFrame:
    normalized = data.copy()

    for column in NUMERIC_COLUMNS:
        normalized[column] = pd.to_numeric(normalized[column], errors="coerce").fillna(0.0)

    for column in BOOLEAN_COLUMNS:
        normalized[column] = normalized[column].apply(parse_bool)

    normalized["asset_name"] = normalized["asset_name"].fillna("").astype(str)
    normalized["symbol"] = normalized["symbol"].fillna("").astype(str)
    normalized["category"] = normalized["category"].fillna("").astype(str)
    normalized["chain"] = normalized["chain"].fillna("").astype(str)
    normalized["protocol"] = normalized["protocol"].fillna("").astype(str)
    normalized["notes"] = normalized["notes"].fillna("").astype(str)
    return normalized


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    normalized = str(value).strip().lower()
    return normalized in {"1", "true", "yes", "y"}
