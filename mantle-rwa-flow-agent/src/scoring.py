from __future__ import annotations

import math
from typing import Any

import pandas as pd


DEFAULT_WEIGHTS = {
    "liquidity": 0.30,
    "concentration_risk": 0.20,
    "activity": 0.20,
    "market_integration": 0.20,
    "agent_readiness": 0.10,
}


def score_assets(data: pd.DataFrame, weights: dict[str, float] | None = None) -> pd.DataFrame:
    """Add component scores and the final Flow Readiness Score.

    The implementation stays intentionally explicit so judges can audit the logic.
    Each component is scored on a 0-100 scale first, then combined with weights.
    """
    weights = weights or DEFAULT_WEIGHTS
    scored = data.copy()

    scored["liquidity_score"] = scored.apply(calculate_liquidity_score, axis=1)
    scored["concentration_risk_score"] = scored.apply(calculate_concentration_score, axis=1)
    scored["activity_score"] = scored.apply(calculate_activity_score, axis=1)
    scored["market_integration_score"] = scored.apply(calculate_market_integration_score, axis=1)
    scored["agent_readiness_score"] = scored.apply(calculate_agent_readiness_score, axis=1)

    scored["flow_readiness_score"] = (
        scored["liquidity_score"] * weights["liquidity"]
        + scored["concentration_risk_score"] * weights["concentration_risk"]
        + scored["activity_score"] * weights["activity"]
        + scored["market_integration_score"] * weights["market_integration"]
        + scored["agent_readiness_score"] * weights["agent_readiness"]
    ).round(2)

    scored = scored.sort_values("flow_readiness_score", ascending=False).reset_index(drop=True)
    scored["rank"] = scored.index + 1
    return scored


def calculate_liquidity_score(row: pd.Series) -> float:
    """Score whether the asset looks tradable rather than merely deposited.

    We reward three things:
    - scale, because a tiny market can be structurally fragile;
    - turnover, because dormant TVL should not score like live liquidity;
    - holder breadth, because more participants usually support better circulation.
    """
    tvl = positive_number(row["tvl_usd"])
    volume = positive_number(row["volume_24h_usd"])
    holders = positive_number(row["holders"])

    # TVL still matters, but only as one input. A large pool with no activity
    # should not dominate the ranking.
    tvl_component = scale_log10(tvl, cap=9.0)

    # Turnover is the core liquidity signal in this model because it tells us
    # whether capital is actually changing hands.
    turnover_ratio = volume / max(tvl, 1.0)
    turnover_component = min(turnover_ratio / 0.20, 1.0) * 100.0

    # A broader holder base usually supports more resilient secondary activity.
    holder_component = min(holders / 10000.0, 1.0) * 100.0

    # Turnover matters more than raw size because dormant TVL does not circulate.
    score = 0.25 * tvl_component + 0.50 * turnover_component + 0.25 * holder_component
    return round(clamp(score), 2)


def calculate_concentration_score(row: pd.Series) -> float:
    """Score how concentrated the asset appears to be.

    Lower top-10 ownership and a larger holder base both improve the score.
    This treats concentration as a risk to credible market circulation.
    """
    top_10_share = positive_number(row["top_10_holder_share"])
    holder_count = positive_number(row["holders"])

    # If the top wallets control too much supply, the market may be fragile even
    # when the headline TVL looks strong.
    decentralization_component = max(0.0, 100.0 - top_10_share)
    holder_component = min(holder_count / 5000.0, 1.0) * 100.0
    score = 0.70 * decentralization_component + 0.30 * holder_component
    return round(clamp(score), 2)


def calculate_activity_score(row: pd.Series) -> float:
    """Score whether the asset is actively used on-chain.

    The model combines address activity, transfer activity, and how much of the
    holder base appears to be engaged rather than passive.
    """
    active_addresses = positive_number(row["active_addresses_30d"])
    transfers = positive_number(row["transfer_count_30d"])
    holders = positive_number(row["holders"])

    # Absolute activity matters because markets need participants to generate
    # price discovery, routing, and behavioral signal.
    active_component = min(active_addresses / 5000.0, 1.0) * 100.0
    transfer_component = min(transfers / 30000.0, 1.0) * 100.0

    # Penetration helps distinguish a broad live market from a large but mostly
    # idle holder set.
    address_penetration = active_addresses / max(holders, 1.0)
    penetration_component = min(address_penetration / 0.80, 1.0) * 100.0

    score = 0.40 * active_component + 0.35 * transfer_component + 0.25 * penetration_component
    return round(clamp(score), 2)


def calculate_market_integration_score(row: pd.Series) -> float:
    """Score whether the asset plugs into usable market rails.

    Secondary trading, lending support, and oracle coverage each matter because
    they make the asset more reusable across the broader on-chain economy.
    """
    score = 0.0
    if row["has_secondary_market"]:
        score += 40.0
    if row["has_lending_market"]:
        score += 25.0
    if row["has_oracle"]:
        score += 20.0

    # Small bonus when turnover indicates the integrations are actually used,
    # not just nominally available.
    turnover_bonus = min((positive_number(row["volume_24h_usd"]) / max(positive_number(row["tvl_usd"]), 1.0)) / 0.15, 1.0) * 15.0
    score += turnover_bonus
    return round(clamp(score), 2)


def calculate_agent_readiness_score(row: pd.Series) -> float:
    """Score whether the asset is legible and usable for AI-agent workflows.

    This is intentionally pragmatic: observable markets, oracle support, and
    explicit agent access matter more than abstract claims about automation.
    """
    active_addresses = positive_number(row["active_addresses_30d"])
    transfer_count = positive_number(row["transfer_count_30d"])

    score = 0.0
    # Direct agent access is the strongest signal because it removes manual
    # integration friction for research and execution systems.
    if row["has_agent_access"]:
        score += 45.0
    if row["has_oracle"]:
        score += 20.0
    if row["has_secondary_market"]:
        score += 10.0

    # Observable on-chain usage gives agents enough signal to analyze and route.
    observability_component = min(active_addresses / 3000.0, 1.0) * 15.0
    transfer_component = min(transfer_count / 20000.0, 1.0) * 10.0
    score += observability_component + transfer_component
    return round(clamp(score), 2)


def summarize_by_category(scored_data: pd.DataFrame) -> pd.DataFrame:
    """Aggregate average category performance for the report and charts."""
    summary = (
        scored_data.groupby("category", as_index=False)
        .agg(
            asset_count=("asset_name", "count"),
            avg_flow_readiness_score=("flow_readiness_score", "mean"),
            avg_liquidity_score=("liquidity_score", "mean"),
            avg_concentration_risk_score=("concentration_risk_score", "mean"),
            avg_activity_score=("activity_score", "mean"),
            avg_market_integration_score=("market_integration_score", "mean"),
            avg_agent_readiness_score=("agent_readiness_score", "mean"),
            total_tvl_usd=("tvl_usd", "sum"),
            total_volume_24h_usd=("volume_24h_usd", "sum"),
        )
        .sort_values("avg_flow_readiness_score", ascending=False)
        .reset_index(drop=True)
    )

    score_columns = [column for column in summary.columns if column.startswith("avg_")]
    summary[score_columns] = summary[score_columns].round(2)
    return summary


def identify_key_findings(scored_data: pd.DataFrame) -> dict[str, Any]:
    """Extract a few narrative anchors for the generated report."""
    highest = scored_data.iloc[0]
    lowest = scored_data.iloc[-1]
    high_tvl_low_flow = scored_data.sort_values(["tvl_usd", "flow_readiness_score"], ascending=[False, True]).iloc[0]
    best_agent_market = scored_data.sort_values("agent_readiness_score", ascending=False).iloc[0]

    return {
        "highest_ranked": highest.to_dict(),
        "lowest_ranked": lowest.to_dict(),
        "high_tvl_low_flow": high_tvl_low_flow.to_dict(),
        "best_agent_market": best_agent_market.to_dict(),
    }


def positive_number(value: Any) -> float:
    """Coerce a value into a non-negative float."""
    try:
        return max(float(value), 0.0)
    except (TypeError, ValueError):
        return 0.0


def scale_log10(value: float, cap: float) -> float:
    """Compress wide value ranges into a stable 0-100 score."""
    if value <= 0:
        return 0.0
    return min(math.log10(value) / cap, 1.0) * 100.0


def clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    """Keep any score inside the expected 0-100 range."""
    return max(minimum, min(value, maximum))
