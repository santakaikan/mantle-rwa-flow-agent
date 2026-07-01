from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def generate_charts(scored_data: pd.DataFrame, category_summary: pd.DataFrame, chart_dir: str | Path, chart_style: dict | None = None) -> list[str]:
    """Create PNG charts that are easy to embed into the report."""
    chart_dir = Path(chart_dir)
    chart_dir.mkdir(parents=True, exist_ok=True)
    chart_style = chart_style or {}

    figure_width = chart_style.get("figure_width", 12)
    figure_height = chart_style.get("figure_height", 7)
    color_primary = chart_style.get("color_primary", "#0F766E")
    color_secondary = chart_style.get("color_secondary", "#D97706")
    color_accent = chart_style.get("color_accent", "#1D4ED8")

    chart_paths = []
    chart_paths.append(
        create_asset_ranking_chart(
            scored_data,
            chart_dir / "flow_readiness_ranking.png",
            figure_width,
            figure_height,
            color_primary,
        )
    )
    chart_paths.append(
        create_category_comparison_chart(
            category_summary,
            chart_dir / "category_comparison.png",
            figure_width,
            figure_height,
            color_secondary,
        )
    )
    chart_paths.append(
        create_component_breakdown_chart(
            scored_data.head(5),
            chart_dir / "top5_component_breakdown.png",
            figure_width,
            figure_height,
            color_accent,
        )
    )
    return [str(path) for path in chart_paths]


def create_asset_ranking_chart(scored_data: pd.DataFrame, output_path: Path, width: int, height: int, color: str) -> Path:
    top_assets = scored_data.head(10).sort_values("flow_readiness_score")
    plt.figure(figsize=(width, height))
    plt.barh(top_assets["symbol"], top_assets["flow_readiness_score"], color=color)
    plt.xlabel("Flow Readiness Score (0-100, higher means stronger circulation readiness)")
    plt.ylabel("Tokenized Asset")
    plt.title("Figure 1. Top Tokenized Assets Ranked by Flow Readiness")
    plt.xlim(0, 100)
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()
    return output_path


def create_category_comparison_chart(category_summary: pd.DataFrame, output_path: Path, width: int, height: int, color: str) -> Path:
    comparison = category_summary.sort_values("avg_flow_readiness_score", ascending=False)
    plt.figure(figsize=(width, height))
    plt.bar(comparison["category"], comparison["avg_flow_readiness_score"], color=color)
    plt.ylabel("Average Flow Readiness Score (category mean)")
    plt.xlabel("Tokenized Asset Category")
    plt.title("Figure 2. Category Comparison by Average Flow Readiness")
    plt.xticks(rotation=25, ha="right")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()
    return output_path


def create_component_breakdown_chart(scored_data: pd.DataFrame, output_path: Path, width: int, height: int, accent_color: str) -> Path:
    components = scored_data.set_index("symbol")[
        [
            "liquidity_score",
            "concentration_risk_score",
            "activity_score",
            "market_integration_score",
            "agent_readiness_score",
        ]
    ]

    ax = components.plot(kind="bar", figsize=(width, height), color=["#0F766E", "#1D4ED8", "#D97706", "#7C3AED", accent_color])
    ax.set_title("Figure 3. Component Breakdown for the Top 5 Ranked Assets")
    ax.set_xlabel("Tokenized Asset")
    ax.set_ylabel("Component Score (0-100)")
    ax.set_ylim(0, 100)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()
    return output_path
