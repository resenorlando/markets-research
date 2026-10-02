# Study 2 - Overnight vs intraday: return and tail

overnight=ln(O_t/C_{t-1}), intraday=ln(C_t/O_t) on RAW OHLC; the `adj_*` rows use a dividend-consistent adjusted open (AdjOpen=Open*AdjClose/Close). 'ann.Sharpe' is a **zero-rate log-return Sharpe proxy** (mean/std of daily log returns * sqrt(252), no risk-free rate). GPD xi is the loss-tail shape (fit to the worst ~2.2-2.4% of ALL days, i.e. the 95th pct of loss-only days). Samples: SPY from 1993, QQQ 1999, IWM 2000.

| Asset | leg | ann.ret % | ann.Sharpe(proxy) | GPD xi (loss tail) |
|---|---|---|---|---|
| US large cap | overnight | 8.1 | 0.73 | 0.322 |
| US large cap | intraday | 0.8 | 0.05 | 0.293 |
| US large cap | c2c | 8.9 | 0.46 | 0.318 |
| US large cap | adj_overnight | 10.0 | 0.90 | 0.324 |
| US large cap | adj_intraday | 0.8 | 0.05 | 0.292 |
| US tech | overnight | 13.2 | 0.87 | 0.287 |
| US tech | intraday | -2.7 | -0.12 | -0.012 |
| US tech | c2c | 10.1 | 0.36 | 0.009 |
| US tech | adj_overnight | 13.9 | 0.91 | 0.295 |
| US tech | adj_intraday | -2.7 | -0.12 | -0.012 |
| US small cap | overnight | 12.0 | 0.85 | 0.225 |
| US small cap | intraday | -4.1 | -0.21 | 0.234 |
| US small cap | c2c | 7.4 | 0.30 | 0.368 |
| US small cap | adj_overnight | 13.4 | 0.95 | 0.222 |
| US small cap | adj_intraday | -4.1 | -0.21 | 0.234 |

**SPY 100 worst close-to-close days:** overnight contributed -184% cumulative log-loss, intraday -270% (overnight = 40% of the damage).