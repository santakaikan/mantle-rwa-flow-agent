from __future__ import annotations

import os
from pathlib import Path

import yaml

DEFAULT_CONFIG = {
    "data_path": "data/sample_assets.csv",
    "report_path": "reports/generated_report.md",
    "chart_dir": "reports/charts",
    "weights": {
        "liquidity": 0.30,
        "concentration_risk": 0.20,
        "activity": 0.20,
        "market_integration": 0.20,
        "agent_readiness": 0.10,
    },
    "chart_style": {
        "figure_width": 12,
        "figure_height": 7,
        "color_primary": "#0F766E",
        "color_secondary": "#D97706",
        "color_accent": "#1D4ED8",
    },
}

THESIS = (
    "The future of on-chain finance will be won by assets that can circulate, not merely assets that can be issued. "
    "Issuance creates representation; circulation creates utility. The strategic question for Mantle is therefore "
    "which tokenized assets can develop liquidity, holder dispersion, market integrations, and agent-native access "
    "strong enough to become real on-chain financial primitives."
)


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    matplotlib_config_dir = project_root / ".mplconfig"
    matplotlib_config_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(matplotlib_config_dir))

    from charts import generate_charts
    from data_loader import load_asset_data
    from report_generator import generate_markdown_report
    from scoring import identify_key_findings, score_assets, summarize_by_category

    config = load_config(project_root / "config.yaml", project_root / "config.example.yaml")

    data_path = project_root / config["data_path"]
    report_path = project_root / config["report_path"]
    chart_dir = project_root / config["chart_dir"]

    asset_data = load_asset_data(data_path)
    scored_data = score_assets(asset_data, config["weights"])
    category_summary = summarize_by_category(scored_data)
    findings = identify_key_findings(scored_data)
    chart_paths = generate_charts(scored_data, category_summary, chart_dir, config.get("chart_style"))

    generate_markdown_report(
        scored_data=scored_data,
        category_summary=category_summary,
        findings=findings,
        chart_paths=chart_paths,
        report_path=report_path,
        thesis=THESIS,
    )

    print("Mantle RWA Flow Agent completed successfully.")
    print(f"Loaded assets: {len(asset_data)}")
    print(f"Top asset: {scored_data.iloc[0]['asset_name']} ({scored_data.iloc[0]['flow_readiness_score']:.2f})")
    print(f"Report written to: {report_path}")
    print(f"Charts written to: {chart_dir}")


def load_config(primary_path: Path, fallback_path: Path) -> dict:
    """Use config.yaml when present; otherwise fall back to the example config."""
    config_path = primary_path if primary_path.exists() else fallback_path
    with config_path.open("r", encoding="utf-8") as file:
        loaded_config = yaml.safe_load(file) or {}
    return merge_config(DEFAULT_CONFIG, loaded_config)


def merge_config(defaults: dict, overrides: dict) -> dict:
    merged = defaults.copy()
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_config(merged[key], value)
        else:
            merged[key] = value
    return merged


if __name__ == "__main__":
    main()
