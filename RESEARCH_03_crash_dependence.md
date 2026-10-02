# Which "diversifier" actually survives a crash?

Correlation is an average-day number. In a crash what matters is whether your hedge crashes at
the same time as equities. So I measured lower-tail co-exceedance with SPY: the chance a hedge is
in its own worst u% of days given SPY is in its worst u%. Then I pushed u from 10% down to 1% to
look deeper into joint crashes. Under independence that number equals u itself, so at the 1% level
an independent asset would score 1%.

## What I found

The assets most people hold to diversify, international and emerging-market equities, give almost
no protection when it counts. They crash alongside US equities 60 to 70 percent of the time in
the deep tail. Genuinely different assets (Treasuries, the dollar, gold) crash together far less
often, but they are not independent either.

Probability a hedge crashes given SPY crashes, by depth (independence equals the depth u):

| Asset | 10% | 5% | 2.5% | 1% | 1% Wilson CI | avg-day corr |
|---|---|---|---|---|---|---|
| DM ex-US equity | 0.66 | 0.63 | 0.64 | 0.71 | 0.59 to 0.81 | +0.87 |
| EM equity | 0.61 | 0.56 | 0.59 | 0.63 | 0.50 to 0.74 | +0.81 |
| US tech (QQQ) | 0.70 | 0.63 | 0.48 | 0.40 | | +0.85 |
| Gold | 0.18 | 0.12 | 0.12 | 0.11 | 0.05 to 0.22 | +0.07 |
| US dollar | 0.11 | 0.08 | 0.06 | 0.10 | 0.04 to 0.21 | -0.19 |
| Long Treasuries | 0.10 | 0.05 | 0.04 | 0.08 | 0.04 to 0.18 | -0.30 |

Two clear groups (`figures/crash_dependence.png`): the equity "diversifiers" sit up at 0.4 to
0.7, the defensive assets sit near the bottom.

Here is the honest part. The defensive assets are not actually independent. At the 1% level
independence would be 0.01, so Treasuries at 0.08 is eight times the independence rate, and gold
and the dollar are ten to eleven times. They crash with equities far less often than
international equities do, but they still go down together sometimes, which is exactly 2020's
dash for cash and the 2022 stocks-and-bonds-down year. No hedge is unconditional.

Robustness: on a common 2007 to 2026 window for all assets the ranking is the same (DM 0.74, EM
0.64, QQQ 0.70; Treasuries 0.08, gold and dollar 0.10). One warning: the 1% level rests on only
about 50 to 63 joint-tail days, so treat the deep-tail numbers as rough (the Wilson intervals
show how wide).

## Why it matters

For trading: "I'm diversified, I hold US, European and EM equities" is a false comfort. In a
crisis those behave like one position. Real crash protection has to come from a different kind of
asset (duration, the dollar, gold), and even then it is partial and depends on the regime (2022
is the warning). The point is not "buy bonds", it is that a hedge should be judged on its tail
behaviour, not its average-day correlation.

For risk: average-day correlation is the wrong lens for crash risk. It treats +0.87 and -0.30 as
the whole story and cannot see that co-crashing rises into the tail for equity-like assets while
staying low for the defensives. Lower-tail dependence, or a tail copula, captures what a
covariance matrix cannot. I do not fit a full Gaussian-copula portfolio VaR here; that is the
follow-up if you want to put a number on the understatement.

## Method

The statistic is the count of days both SPY and the hedge are below their own u-quantiles,
divided by the count of days SPY is below its u-quantile, for u of 10, 5, 2.5 and 1 percent, with
Wilson 95% intervals. This is finite-threshold co-exceedance, not the limiting tail-dependence
coefficient as u goes to zero. Each pair uses its own overlapping dates, plus a common-window
check from 2007. Pearson correlation is shown as the average-day contrast.

## Caveats

Few observations deep in the tail (about 50 to 63 SPY-tail days at 1%), so the 1% column is
imprecise. The measure is same-day, both-down; it does not give a hedge credit for rising when
equities fall. One ETF per asset class, with different start dates (the dollar ETF starts in
2007); the common-window check handles the overlap concern. A fuller version would add more
hedges and more horizons.
