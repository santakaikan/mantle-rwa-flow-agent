# Mantle RWA Flow Agent

## Executive Summary
This report evaluates tokenized assets through a `Flow Readiness Score`, a 0-100 framework designed to measure whether an asset can actually circulate, attract liquidity, integrate into markets, and support agent-native finance. In this illustrative sample dataset, **Sports Prediction Liquidity Sample (sPRED)** leads the ranking with a score of **90.96**, while **Onchain SME Credit Pool Sample (oSME)** ranks last at **19.68**. The pattern is consistent: assets with strong routing, active holders, usable market structure, and machine-readable access outperform assets that rely on TVL alone.

## Research Thesis
The future of on-chain finance will be won by assets that can circulate, not merely assets that can be issued. Issuance creates representation; circulation creates utility. The strategic question for Mantle is therefore which tokenized assets can develop liquidity, holder dispersion, market integrations, and agent-native access strong enough to become real on-chain financial primitives.

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
- The top-ranked asset is **Sports Prediction Liquidity Sample (sPRED)**, supported by high liquidity, strong activity, and broad market integrations.
- The weakest asset is **Onchain SME Credit Pool Sample (oSME)**, mainly because circulation is gated by concentration, weak secondary transferability, or missing integrations.
- **Cross-Chain Equity Index Sample (gSPX)** shows why TVL alone can be misleading: it reports large locked value but underperforms on real circulation metrics.
- **Sports Prediction Liquidity Sample (sPRED)** is the strongest candidate for agent-native finance because data access, oracle support, and observable flow are already present.

### Asset Ranking
|   rank | asset_name                           | symbol   | category                   | chain    |   flow_readiness_score |   liquidity_score |   concentration_risk_score |   activity_score |   market_integration_score |   agent_readiness_score |
|--------|--------------------------------------|----------|----------------------------|----------|------------------------|-------------------|----------------------------|------------------|----------------------------|-------------------------|
|      1 | Sports Prediction Liquidity Sample   | sPRED    | prediction market          | Base     |                  90.96 |             95.34 |                      89.50 |            97.29 |                      75.00 |                  100.00 |
|      2 | Dollar Routing Reserve Sample        | dROUTE   | stablecoin liquidity       | Base     |                  90.50 |             78.28 |                      90.90 |            97.12 |                      97.06 |                  100.00 |
|      3 | Mantle Settlement Liquidity Sample   | mUSDL    | stablecoin liquidity       | Mantle   |                  90.33 |             80.25 |                      88.10 |            95.15 |                      98.02 |                  100.00 |
|      4 | Mantle Macro Event Market Sample     | mVOTE    | prediction market          | Mantle   |                  89.61 |             94.35 |                      85.30 |            96.24 |                      75.00 |                  100.00 |
|      5 | Mantle Agent Research Basket Sample  | mAIX     | AI-agent accessible market | Mantle   |                  70.52 |             71.95 |                      71.04 |            52.64 |                      75.00 |                   92.01 |
|      6 | Autonomous Macro Execution Sample    | aMACRO   | AI-agent accessible market | Mantle   |                  66.57 |             57.56 |                      61.02 |            44.61 |                      97.58 |                   86.62 |
|      7 | Mantle Treasury Ladder Sample        | mTBILL   | RWA yield                  | Mantle   |                  66.56 |             49.04 |                      72.70 |            49.46 |                      90.21 |                   93.74 |
|      8 | Cross-Chain Equity Index Sample      | gSPX     | tokenized equity           | Ethereum |                  65.56 |             45.26 |                      69.90 |            54.21 |                      87.74 |                   96.17 |
|      9 | Mantle Tokenized Tech Basket Sample  | mNDX     | tokenized equity           | Mantle   |                  53.11 |             41.22 |                      55.68 |            39.79 |                      64.61 |                   87.26 |
|     10 | Real Estate Income Sleeve Sample     | rRENT    | RWA yield                  | Arbitrum |                  39.71 |             34.16 |                      41.76 |            24.43 |                      63.28 |                   35.71 |
|     11 | Mantle Private Credit Gateway Sample | mCREDIT  | private credit             | Mantle   |                  28.11 |             26.47 |                      29.66 |            14.43 |                      45.71 |                   22.12 |
|     12 | Onchain SME Credit Pool Sample       | oSME     | private credit             | Polygon  |                  19.68 |             25.04 |                      22.42 |            12.06 |                      25.77 |                    1.13 |

## Category Comparison
| category                   |   asset_count |   avg_flow_readiness_score |   avg_liquidity_score |   avg_concentration_risk_score |   avg_activity_score |   avg_market_integration_score |   avg_agent_readiness_score |
|----------------------------|---------------|----------------------------|-----------------------|--------------------------------|----------------------|--------------------------------|-----------------------------|
| stablecoin liquidity       |             2 |                      90.42 |                 79.26 |                          89.50 |                96.14 |                          97.54 |                      100.00 |
| prediction market          |             2 |                      90.28 |                 94.84 |                          87.40 |                96.76 |                          75.00 |                      100.00 |
| AI-agent accessible market |             2 |                      68.54 |                 64.76 |                          66.03 |                48.62 |                          86.29 |                       89.32 |
| tokenized equity           |             2 |                      59.34 |                 43.24 |                          62.79 |                47.00 |                          76.18 |                       91.72 |
| RWA yield                  |             2 |                      53.14 |                 41.60 |                          57.23 |                36.94 |                          76.74 |                       64.72 |
| private credit             |             2 |                      23.90 |                 25.76 |                          26.04 |                13.24 |                          35.74 |                       11.62 |

The category view shows that liquidity-focused and agent-accessible markets can outscore some higher-yield RWA structures when those structures remain operationally closed. Prediction markets also score well because they often have strong participation, frequent transfers, and visible market pricing.

## Why Circulation, Holder Dispersion, Secondary Markets, and Agent Access Matter
- **Circulation** matters because assets that move are more likely to become useful financial primitives rather than passive wrappers.
- **Holder dispersion** matters because concentrated ownership can make an asset brittle even when its TVL looks large.
- **Secondary markets** matter because they turn tokenized claims into tradable and collateral-usable instruments.
- **Agent access** matters because software-driven capital allocation will increasingly favor assets with machine-readable data and executable interfaces.

### Charts
![flow_readiness_ranking](/home/yoshiyuki46/デスクトップ/mantle-rwa-flow-agent/reports/charts/flow_readiness_ranking.png)
![category_comparison](/home/yoshiyuki46/デスクトップ/mantle-rwa-flow-agent/reports/charts/category_comparison.png)
![top5_component_breakdown](/home/yoshiyuki46/デスクトップ/mantle-rwa-flow-agent/reports/charts/top5_component_breakdown.png)

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
