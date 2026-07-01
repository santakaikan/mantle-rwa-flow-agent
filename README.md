# Mantle RWA Flow Agent

**Mantle RWA Flow Agent** is a reproducible research workflow built for **Mantle Research Challenge, Track 2: Research Agent**. It is designed to test a specific claim:

> **The future of on-chain finance will be won by assets that can circulate, not merely assets that can be issued.**

This project argues that the strategic question for RWA, tokenized equities, prediction markets, and AI-agent finance is not just whether an asset exists on-chain, but whether it can actually move through markets with enough liquidity, holder diversity, integration, and machine-readable access to become a useful financial primitive.

The agent reads structured asset data from CSV, computes a `Flow Readiness Score`, generates charts, and produces a research-style Markdown memo that shows why **circulation quality** is a stronger lens than headline TVL alone.

## What this submission is trying to prove
This tool is built to demonstrate that:

- token issuance is only the first milestone in on-chain finance;
- TVL alone can hide weak liquidity, narrow ownership, and poor downstream usability;
- the next winners in tokenized finance will be assets that are easy to trade, collateralize, observe, and automate;
- Mantle can compete by becoming the chain where tokenized assets are not only issued, but actively circulated and agent-accessible.

## What this tool does
- Loads tokenized asset data from a CSV file.
- Scores each asset from 0 to 100 using circulation-focused metrics.
- Produces an asset ranking table and category-level comparison.
- Exports PNG charts for visual analysis.
- Generates a Markdown report with a research thesis, methodology, findings, and Mantle-specific implications.

## Why TVL alone is not enough
TVL tells you how much value is parked inside a protocol or wrapper. It does **not** tell you whether the asset is actually moving, whether holders are diversified, whether secondary liquidity exists, whether the asset can be used as collateral, or whether AI agents can observe and transact on it. In tokenized finance, issuance is only step one. The harder problem is circulation.

This project is built around that idea:

> The future of on-chain finance will be won by assets that can circulate, not merely assets that can be issued.

In practical terms, this means a tokenized asset should be evaluated not only by how much capital is parked inside it, but by whether it can:

- trade with meaningful depth;
- attract a broad enough holder base to avoid brittle ownership;
- plug into secondary markets, lending venues, and oracle systems;
- expose data and interfaces that AI agents can analyze, route, and settle against.

## Flow Readiness Score
Each asset receives a `Flow Readiness Score` from 0 to 100.

### Score components
- `liquidity score`
  Rewards turnover, tradable depth, and a broader holder base. A large TVL with weak volume is penalized.
- `concentration risk score`
  Penalizes assets where the top 10 holders control too much of supply.
- `activity score`
  Measures whether holders are actually active on-chain through addresses and transfers.
- `market integration score`
  Rewards connection to secondary markets, lending markets, and oracle infrastructure.
- `agent-readiness score`
  Measures whether the asset is observable and usable by AI agents.

### Default weights
- Liquidity: `30%`
- Concentration risk: `20%`
- Activity: `20%`
- Market integration: `20%`
- Agent readiness: `10%`

### Formula
The score is intentionally simple and auditable:

```text
Flow Readiness Score
= 0.30 × Liquidity Score
+ 0.20 × Concentration Risk Score
+ 0.20 × Activity Score
+ 0.20 × Market Integration Score
+ 0.10 × Agent-Readiness Score
```

Each component is normalized to a `0-100` range before weighting.

### How the components work
```text
Liquidity Score
= f(TVL size, 24h volume / TVL turnover, holder breadth)

Concentration Risk Score
= f(100 - top_10_holder_share, holder count)

Activity Score
= f(active_addresses_30d, transfer_count_30d, active_addresses / holders)

Market Integration Score
= f(secondary market, lending market, oracle support, turnover bonus)

Agent-Readiness Score
= f(agent access, oracle support, secondary market access, observability)
```

Interpretation:
- High TVL with weak turnover should not score like a healthy market.
- High yield with concentrated ownership should not score like a durable financial primitive.
- Assets that are tradable, collateral-usable, and machine-readable should score higher because they are more likely to support real on-chain circulation.

The weights are configurable in `config.yaml` or `config.example.yaml`.

## Project structure
```text
mantle-rwa-flow-agent/
├── README.md
├── requirements.txt
├── config.example.yaml
├── data/
│   └── sample_assets.csv
├── src/
│   ├── main.py
│   ├── data_loader.py
│   ├── scoring.py
│   ├── report_generator.py
│   └── charts.py
└── reports/
    └── sample_report.md
```

When you run the script, it also creates:
- `reports/generated_report.md`
- `reports/charts/flow_readiness_ranking.png`
- `reports/charts/category_comparison.png`
- `reports/charts/top5_component_breakdown.png`

## Sample dataset
The included sample data covers the categories requested for Mantle-oriented research:
- `tokenized equity`
- `RWA yield`
- `private credit`
- `prediction market`
- `stablecoin liquidity`
- `AI-agent accessible market`

The CSV schema includes:
- `asset_name`
- `symbol`
- `category`
- `chain`
- `protocol`
- `tvl_usd`
- `volume_24h_usd`
- `holders`
- `active_addresses_30d`
- `transfer_count_30d`
- `top_10_holder_share`
- `has_secondary_market`
- `has_lending_market`
- `has_oracle`
- `has_agent_access`
- `notes`

## Setup
Recommended:
```bash
python -m venv .venv
source .venv/bin/activate
```

Then install dependencies:
```bash
pip install -r requirements.txt
```

Optional:
```bash
cp config.example.yaml config.yaml
```

Configuration behavior:
- If `config.yaml` exists, the script uses it.
- If `config.yaml` does not exist, the script falls back to `config.example.yaml`.
- Missing keys are filled from internal defaults in `src/main.py`.

## Run
```bash
python src/main.py
```

## Output example
After running, the workflow prints a short summary in the terminal and writes:
- A ranked asset table in Markdown
- A category comparison table in Markdown
- PNG charts under `reports/charts/`
- A research memo under `reports/generated_report.md`

Example interpretation:
- A stablecoin liquidity layer may rank above a larger private credit vault if it has stronger volume, more holders, better oracle coverage, and live market integrations.
- A tokenized equity wrapper with strong TVL can still score poorly if transfers are rare and the supply is concentrated.

## 1-minute demo flow
For a judge or reviewer, the demo is simple:

1. Load a CSV of tokenized assets across categories such as RWA yield, tokenized equity, prediction markets, and AI-agent accessible markets.
2. Score each asset with the `Flow Readiness Score`, which weighs liquidity, holder dispersion, activity, integrations, and agent access.
3. Output a ranked table and research-ready PNG charts.
4. Generate a Markdown report that explains the thesis, method, and findings.
5. Show that two assets with similar or even very different TVL can have very different market quality once circulation is measured directly.

In one minute, the reviewer can see the full pipeline from raw structured inputs to a defensible research conclusion: **TVL alone does not capture the quality of on-chain finance.**

## Mantle Research Challenge relevance
This project is designed as a compact but credible submission candidate for **Mantle Research Challenge, Track 2: Research Agent**.

Why it fits:
- It is reproducible and API-key free.
- It expresses a clear, arguable research thesis.
- It moves beyond descriptive TVL dashboards toward a more decision-useful framework.
- It is directly relevant to Mantle's RWA, tokenized finance, prediction market, and agent-finance positioning.

## Future live data integrations
This version intentionally runs with no API keys and no external dependencies beyond simple Python libraries. The architecture is ready to connect to real data sources later, including:
- `RWA.xyz`
- `DeFiLlama`
- `Dune`
- `Flipside`
- `Etherscan`
- `Mantle RPC`
- protocol-specific APIs

The intended future path is to replace or enrich `data/sample_assets.csv` with real-time or scheduled data collection while keeping the same scoring and reporting pipeline.

## Notes for readers and judges
- This repository is a transparent workflow, not a black-box dashboard.
- Every score can be traced back to CSV inputs and readable Python functions.
- The code is intentionally simple and beginner-friendly so the research logic is inspectable.

## Short submission blurb
Mantle RWA Flow Agent is a reproducible research agent that evaluates tokenized assets beyond TVL by scoring whether they can actually circulate. It compares liquidity, holder concentration, on-chain activity, market integrations, and AI-agent access to show which assets are most likely to become usable financial primitives inside the Mantle ecosystem.

## Submission Checklist
- [x] The script runs without API keys
- [x] The sample report is generated
- [x] Charts are generated
- [x] The methodology is explained
- [x] The project is linked in the X post
- [ ] The Mantle submission form is completed

## Submission Assets
Application form blurb:
Mantle RWA Flow Agent is a reproducible research agent for evaluating tokenized assets beyond headline TVL. It scores whether assets can actually circulate by comparing liquidity, holder concentration, on-chain activity, market integration, and AI-agent access. The goal is to help Mantle identify which on-chain asset categories are most likely to become usable financial primitives rather than static token wrappers.

X / Twitter post:
I built Mantle RWA Flow Agent for Mantle Research Challenge Track 2: a reproducible research workflow for evaluating tokenized assets beyond headline TVL. Core idea: the future of on-chain finance will be won by assets that can circulate, not merely assets that can be issued. It scores liquidity, holder dispersion, activity, integrations, and agent-native access. #Mantle #RWA #OnchainFinance #AIAgents

GitHub repository description:
Reproducible research agent for scoring tokenized assets beyond TVL across liquidity, concentration, activity, market integration, and AI-agent readiness.

1-minute demo script:
1. This repo loads a simple CSV of tokenized assets across categories like RWA yield, tokenized equity, prediction markets, stablecoin liquidity, private credit, and AI-agent accessible markets.
2. It scores each asset with a Flow Readiness Score instead of relying on TVL alone.
3. The score combines liquidity, holder concentration, on-chain activity, market integration, and agent-readiness into one transparent framework.
4. Then it outputs a ranking table, category comparison, and PNG charts that are easy to inspect quickly.
5. Finally, it generates a Markdown research memo explaining why some assets are more circulation-ready than others.
6. The main takeaway is that Mantle's opportunity is not just hosting issuance, but enabling tokenized assets to become liquid, trusted, and automatable financial primitives.

## X / Twitter post
I built Mantle RWA Flow Agent, a reproducible research workflow for evaluating tokenized assets beyond headline TVL. The core idea: tokenization is only the first step. The real challenge is distribution, liquidity, trust, and agent-native access. #Mantle #RWA #OnchainFinance #AIAgents
