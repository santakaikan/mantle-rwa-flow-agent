from __future__ import annotations

from pathlib import Path

import pandas as pd
from tabulate import tabulate


def generate_markdown_report(
    scored_data: pd.DataFrame,
    category_summary: pd.DataFrame,
    findings: dict,
    chart_paths: list[str],
    report_path: str | Path,
    thesis: str,
) -> str:
    """Build a research-style Markdown report from scored data."""
    report_path = Path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    ranking_table = format_ranking_table(scored_data)
    category_table = format_category_table(category_summary)
    chart_markdown = "\n".join([f"![{Path(path).stem}]({Path(path).as_posix()})" for path in chart_paths])

    highest = findings["highest_ranked"]
    lowest = findings["lowest_ranked"]
    high_tvl_low_flow = findings["high_tvl_low_flow"]
    best_agent_market = findings["best_agent_market"]

    report = f"""# Mantle RWA Flow Agent

## Executive Summary
This report evaluates tokenized assets through a `Flow Readiness Score`, a 0-100 framework designed to measure whether an asset can actually circulate, attract liquidity, integrate into markets, and support agent-native finance. In this illustrative sample dataset, **{highest["asset_name"]} ({highest["symbol"]})** leads the ranking with a score of **{highest["flow_readiness_score"]:.2f}**, while **{lowest["asset_name"]} ({lowest["symbol"]})** ranks last at **{lowest["flow_readiness_score"]:.2f}**. The pattern is consistent: assets with strong routing, active holders, usable market structure, and machine-readable access outperform assets that rely on TVL alone.

## Research Thesis
{thesis}

## Methodology
The Flow Readiness Score combines five components:

1. **Liquidity score**: rewards turnover, tradable depth, and a broader holder base instead of passive TVL alone.
2. **Concentration risk score**: penalizes assets whose supply is dominated by the top 10 wallets.
3. **Activity score**: captures active addresses, transfer count, and holder participation on-chain.
4. **Market integration score**: rewards integration with secondary trading, lending, and oracle infrastructure.
5. **Agent-readiness score**: measures whether an asset is structured for AI-agent analysis, routing, and settlement.

The weighted score uses the following default weights: liquidity 30%, concentration risk 20%, activity 20%, market integration 20%, and agent readiness 10%.

At a high level:

```text
Flow Readiness Score
= 0.30 × Liquidity
+ 0.20 × Concentration Risk
+ 0.20 × Activity
+ 0.20 × Market Integration
+ 0.10 × Agent-Readiness
```

## Why TVL Alone Is Not Enough
TVL is useful as a starting point, but it is not a complete measure of market quality. It tells us how much value is parked inside a structure. It does not tell us whether the asset is actively traded, whether ownership is broad enough to support resilient price discovery, whether secondary liquidity exists, or whether the asset is observable and usable for AI-driven workflows.

In tokenized finance, that distinction matters. A private credit sleeve can report large TVL while remaining operationally closed. A tokenized equity wrapper can appear important while still showing weak transfer activity. By contrast, a prediction market or settlement liquidity layer may have lower TVL but much stronger circulation, integration, and market signal.

## Key Findings
- The top-ranked asset is **{highest["asset_name"]} ({highest["symbol"]})**, supported by high liquidity, strong activity, and broad market integrations.
- The weakest asset is **{lowest["asset_name"]} ({lowest["symbol"]})**, mainly because circulation is gated by concentration, weak secondary transferability, or missing integrations.
- **{high_tvl_low_flow["asset_name"]} ({high_tvl_low_flow["symbol"]})** shows why TVL alone can be misleading: it reports large locked value but underperforms on real circulation metrics.
- **{best_agent_market["asset_name"]} ({best_agent_market["symbol"]})** is the strongest candidate for agent-native finance because data access, oracle support, and observable flow are already present.

### Asset Ranking
{ranking_table}

## Category Comparison
{category_table}

The category view shows that liquidity-focused and agent-accessible markets can outscore some higher-yield RWA structures when those structures remain operationally closed. Prediction markets also score well because they often have strong participation, frequent transfers, and visible market pricing.

## Why Circulation, Holder Dispersion, Secondary Markets, and Agent Access Matter
- **Circulation** matters because assets that move are more likely to become useful financial primitives rather than passive wrappers.
- **Holder dispersion** matters because concentrated ownership can make an asset brittle even when its TVL looks large.
- **Secondary markets** matter because they turn tokenized claims into tradable and collateral-usable instruments.
- **Agent access** matters because software-driven capital allocation will increasingly favor assets with machine-readable data and executable interfaces.

### Charts
{chart_markdown}

## Risks and Limitations
- The sample dataset is synthetic and intended to demonstrate a reproducible workflow, not make live investment claims.
- Raw on-chain signals can miss off-chain market-making agreements or transfer restrictions hidden in legal wrappers.
- Score thresholds and weights are configurable; different research teams may want to tune them for specific asset classes.
- The framework captures circulation readiness, not legal quality, issuer solvency, or regulatory fitness.

## Why This Matters for Mantle
Mantle can differentiate in tokenized finance by becoming the place where assets do not just exist, but move. If Mantle supports secondary routing, oracle coverage, collateral integrations, and agent-native interfaces, it becomes a better execution layer for RWA demand. That matters across several adjacent categories:

- **RWA yield** can supply reserve-bearing collateral and treasury rails.
- **Tokenized equity** can bring globally legible risk assets on-chain.
- **Prediction markets** can generate continuous market intelligence around macro and event risk.
- **AI-agent accessible markets** can make those assets more analyzable, routable, and automatable.

The challenge is therefore less about issuing one more asset and more about building the conditions under which tokenized assets become trusted financial primitives.

## Next Research Steps
- Connect the pipeline to live sources such as RWA.xyz, DeFiLlama, Dune, Flipside, Etherscan, Mantle RPC, and protocol APIs.
- Add time-series analysis to track whether flow readiness is improving or deteriorating over time.
- Distinguish retail flow, professional flow, and agent-executed flow where data allows.
- Add bridge usage, order book depth, slippage, and collateral reuse metrics for a fuller market-structure view.

## How to Extend This Agent
- Connect **Mantle RPC** for transfer activity, holder snapshots, and contract-level observability.
- Add **RWA.xyz** for coverage across tokenized treasury, yield, and credit categories.
- Add **DeFiLlama** for TVL context and protocol-level category data.
- Add **Dune** and **Flipside** for wallet-level flow analysis and time-series research.
- Add **Etherscan-style APIs** for token holders, transfers, and contract metadata.
- Add **protocol-specific APIs** for order books, NAV updates, redemption windows, or collateral settings.
"""

    report_path.write_text(report, encoding="utf-8")
    return report


def format_ranking_table(scored_data: pd.DataFrame) -> str:
    table = scored_data[
        [
            "rank",
            "asset_name",
            "symbol",
            "category",
            "chain",
            "flow_readiness_score",
            "liquidity_score",
            "concentration_risk_score",
            "activity_score",
            "market_integration_score",
            "agent_readiness_score",
        ]
    ].copy()

    return tabulate(table, headers="keys", tablefmt="github", showindex=False, floatfmt=".2f")


def format_category_table(category_summary: pd.DataFrame) -> str:
    table = category_summary[
        [
            "category",
            "asset_count",
            "avg_flow_readiness_score",
            "avg_liquidity_score",
            "avg_concentration_risk_score",
            "avg_activity_score",
            "avg_market_integration_score",
            "avg_agent_readiness_score",
        ]
    ].copy()
    return tabulate(table, headers="keys", tablefmt="github", showindex=False, floatfmt=".2f")
