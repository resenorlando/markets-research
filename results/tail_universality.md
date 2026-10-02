# Study 1 - Are extreme returns universal?

GPD tail-shape ξ (95th-pct threshold) before/after causal EWMA(0.94) volatility scaling. Higher xi = fatter tail; xi near 0 is a Gaussian-like tail. CIs are stationary-bootstrap (200 resamples).

| Asset | Class | N | ann.vol % | ξ raw | ξ raw 95% CI | ξ scaled | ξ scaled 95% CI |
|---|---|---|---|---|---|---|---|
| US large cap | equity | 8457 | 19 | 0.215 | [0.06,0.34] | 0.149 | [0.03,0.26] |
| US tech | equity | 6915 | 27 | 0.021 | [-0.12,0.15] | 0.086 | [-0.04,0.17] |
| US small cap | equity | 6607 | 24 | 0.255 | [0.05,0.39] | 0.066 | [-0.06,0.17] |
| DM ex-US eq | equity | 6292 | 21 | 0.266 | [0.05,0.37] | 0.114 | [0.01,0.22] |
| EM equity | equity | 5886 | 27 | 0.256 | [0.03,0.37] | 0.093 | [-0.05,0.19] |
| US Treasuries 20y+ | bonds | 6064 | 14 | 0.136 | [-0.14,0.29] | 0.072 | [-0.09,0.17] |
| Gold | commodity | 5482 | 18 | 0.190 | [0.06,0.31] | 0.138 | [0.01,0.24] |
| Crude oil | commodity | 5133 | 38 | 0.271 | [-0.01,0.45] | 0.159 | [0.00,0.31] |
| US dollar | fx | 4910 | 8 | 0.198 | [0.07,0.31] | 0.160 | [-0.10,0.33] |
| Bitcoin | crypto | 4370 | 55 | 0.162 | [-0.02,0.32] | 0.313 | [0.12,0.48] |
| Ethereum | crypto | 3221 | 71 | 0.201 | [-0.13,0.39] | 0.129 | [-0.10,0.25] |

**Equity ξ (scaled):** mean 0.102, range [0.066, 0.149]
**Crypto ξ (scaled):** Bitcoin 0.313, Ethereum 0.129