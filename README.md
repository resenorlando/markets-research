# Markets research

Short, reproducible research notes on tail risk, liquidity and market structure. Each note
starts with a question, uses free daily data, ships the code and data so anyone can rerun it,
and ends with what it means for a risk desk and for a trader.

Author: Resen Orlando. The tail-risk code is shared with my other repo,
[extreme-value-risk](https://github.com/resenorlando/extreme-value-risk).

## Notes

**01. Are extreme returns universal?** ([read](RESEARCH_01_tail_universality.md))
An EVT test across 11 markets. Once you divide each asset's returns by its own (causal)
volatility, the tails of equities, bonds, gold and FX mostly line up on one shape, so a lot of
what looks like "fat tails" is really just volatility clustering. Bitcoin is the exception: its
tail stays the fattest even after scaling. Its worst day was about 15 times its own volatility
forecast.
Figures: `figures/tail_universality.png`, `figures/xi_raw_vs_scaled.png`

**02. Almost all of the equity ETF return is earned overnight.** ([read](RESEARCH_02_overnight_drift.md))
Splitting 33 years of SPY/QQQ/IWM into the overnight gap and the trading session. Almost the
whole price return shows up overnight, while the market is shut ($1 in SPY held overnight only
grew to about $14; the intraday-only version stayed flat). For tech and small caps the intraday
session actually lost money. The worst single days, though, are mostly intraday.
Figures: `figures/overnight_intraday_SPY.png`, `figures/overnight_intraday_tails.png`

**03. Which "diversifier" actually survives a crash?** ([read](RESEARCH_03_crash_dependence.md))
Lower-tail co-exceedance with SPY. International and emerging-market equities crash alongside US
stocks 60 to 70 percent of the time in the deep tail, so they offer little protection when it
matters. Treasuries, the dollar and gold hold up far better, though none of them is fully
independent (2020 and 2022 both show up). Ordinary correlation misses most of this.
Figure: `figures/crash_dependence.png`

## Running it

```bash
pip install numpy pandas scipy matplotlib
python fetch_multi.py # pull full daily history into data/
python study1_tail_universality.py # note 01
python study2_overnight_intraday.py # note 02
python study3_crash_dependence.py # note 03
```

## Approach

I fix the question, the universe and the thresholds before I look at the result. Everything is
strictly causal (volatility forecasts only use past data). Each note gives one main chart, some
uncertainty where it matters, the exact sample period, and the caveats. A boring or null result
is fine; a forced one is not.
