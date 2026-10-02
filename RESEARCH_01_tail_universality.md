# Are extreme returns universal? An EVT test across 11 markets

Different assets look like they have very different crash risk. I wanted to know how much of that
is genuinely fatter tails and how much is just higher volatility. So I compared the tail shape of
11 markets (equities, bonds, gold, oil, the dollar, crypto) before and after taking out each
asset's own volatility, using Extreme Value Theory.

## What I found

Most of what looks like different crash risk across ordinary assets is really different
volatility, not a different tail shape. When you divide each day's return by a causal estimate of
that day's volatility, the tails of equities, bonds, gold and FX mostly line up on one shape. A
big part of the raw tail heaviness was volatility clustering. Bitcoin is the clear exception: it
keeps the fattest tail of the whole group even after scaling.

Some detail:

* Raw tails fan out a long way. A bad day is about 1% for the dollar and 15 to 20% for Bitcoin.
* After dividing by a causal EWMA volatility forecast (lambda 0.94, using only past data), the
 scaled tails collapse onto each other out to roughly 4 or 5 standard deviations.
* Measured by the GPD shape parameter (higher means fatter), scaling lowers it for 9 of the 11
 assets and pulls the equities into a tight band, 0.07 to 0.15. Two assets go the other way: QQQ
 a little (0.02 to 0.09) and Bitcoin a lot (0.16 to 0.31, the largest of all).

Why Bitcoin's scaled tail is so fat. These are real events, not bad data:

| Date | What happened | Log return | Price fall | vs its own vol forecast |
|---|---|---|---|---|
| 2020-03-12 | Covid "Black Thursday" | -46.5% | -37.2% | about 15x |
| 2015-08-18 | 2015 bear market | -20.1% | -18.2% | about 10x |
| 2018-11-14 | November 2018 crash | -10.3% | -9.8% | about 9.5x |

A day worth about 15 times its own volatility forecast is astronomically unlikely if the
day-to-day moves were Gaussian around that forecast. So Bitcoin still carries a lot of tail risk
after you account for its volatility.

## Notes on interpretation

* The "-46.5%" is a log return. The actual price fall that day was about 37%. Both are in the
 table so the difference is clear.
* The rise in Bitcoin's shape is not precise. The raw and scaled confidence intervals overlap,
 and a paired bootstrap of the change is not significant at 95%. The fair claim is that Bitcoin
 keeps the fattest scaled tail, not that scaling provably fattens it.
* This is not proof of a jump process. Daily close data cannot tell a true discontinuous jump
 from an unusually large continuous 24-hour move. "Residual heavy-tail, jump-like risk under
 this filter" is as far as the data goes.
* It is a Bitcoin result, not a blanket crypto one. Ethereum's scaled shape (0.13) sits inside
 the equity range. Only Bitcoin stands out here.

## Why it matters

For risk: volatility scaling, which is the core of most modern risk models, does most of the work
in explaining fat tails for equities and bonds, so a GARCH-EVT model will look good there. But
Bitcoin (and to a lesser extent oil) keeps a fat tail after scaling, so a model that treats
scaled returns as roughly Gaussian will under-reserve for exactly the days that matter. Vol
targeting alone is not enough for those markets.

For trading: "Bitcoin is risky" is usually a comment about its volatility. The sharper point is
that even after adjusting for how much it moves day to day, Bitcoin has an unusually high chance
of an extreme move, which matters for how you size it, how wide you quote it, and why plain vol
targeting still leaves you exposed to weekend and holiday gaps. One idea worth testing (not done
here): crypto downside options may stay underpriced by any model that assumes returns are
Gaussian after vol scaling.

## Method

Universe: SPY, QQQ, IWM, EFA, EEM (equities), TLT (bonds), GLD, USO (commodities), UUP (dollar),
BTC and ETH (crypto). Full daily history per asset from Yahoo Finance (SPY back to 1993, BTC to
2014), frozen in `data/`. Raw tail: losses are minus the log return, fit a GPD (POT, 95th
percentile threshold) for the shape. Scaled tail: standardise each return by a causal EWMA
volatility forecast (today's forecast uses only returns up to yesterday), then fit the same GPD
to the standardised losses. Confidence intervals are a stationary block bootstrap
(`results/tail_universality.md`).

## Caveats

Different sample periods per asset (BTC from 2014, SPY from 1993), so this is a distributional
statement, not a matched-period one; a common window is the natural next step. EWMA is one
volatility filter; a GARCH filter with a leverage term might scale things a little differently,
though the ordering (Bitcoin fattest) should hold. The shape estimates move with the threshold.
The assets are correlated and the crises overlap, so this is consistent evidence, not 11
independent tests.
