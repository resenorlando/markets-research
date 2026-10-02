# Almost all of the equity ETF return is earned overnight

The US market is only open about six and a half hours a day. So which part of the day actually
pays you: the overnight gap (close to open, while the market is shut) or the trading session
(open to close)? I split the daily return of three US equity ETFs into those two pieces and held
each on its own.

## What I found

Almost the entire long-run price return of these ETFs is earned overnight, while the market is
closed. The trading session, where nearly all the volume happens, has paid close to nothing, and
for tech and small caps it has actually lost money.

Annualised return of holding only the overnight leg versus only the intraday leg:

| Asset (sample) | Overnight (raw) | Overnight (div-adjusted) | Intraday |
|---|---|---|---|
| SPY, US large cap (from 1993) | 8.1%/yr | 10.0%/yr | 0.8%/yr |
| QQQ, US tech (from 1999) | 13.2%/yr | 13.9%/yr | -2.7%/yr |
| IWM, US small cap (from 2000) | 12.0%/yr | 13.4%/yr | -4.1%/yr |

A dollar held only overnight in SPY grew to about $14 since 1993. A dollar held only during the
trading day stayed roughly flat around $1 (`figures/overnight_intraday_SPY.png`). This is the
overnight drift, or night effect, and it is large.

The dividend check makes it stronger, not weaker. Raw open and close prices book every
ex-dividend drop into the overnight leg, which understates it. If you rebuild a dividend-
consistent adjusted open (open times adjclose over close), SPY's overnight return goes from 8.1%
to 10.0% a year while intraday stays at 0.8%, so the gap gets wider.

The tail behaves differently from the return, though. On SPY's 100 worst close-to-close days,
the trading session delivered about 60% of the total decline and the overnight gap about 40%
(intraday was the more negative leg on 66 of those 100 days), see
`figures/overnight_intraday_tails.png`. So the return builds up overnight, but most of the worst
single-day damage happens while the market is open.

## Why it matters

For trading: the price gains show up almost entirely as overnight gaps, on positions carried
through the close when you cannot trade. Intraday, liquidity providers and day traders fight over
a pie that is roughly flat in aggregate. It reframes a lot of "day-trading edge", and it helps
explain overnight-tilted products and why the closing auction is where the real risk transfer
happens.

For risk: return and risk live in different sessions. The gains are overnight, but a majority of
the worst single-day shocks are intraday. A risk model or an execution schedule that treats a day
as one uniform block gets both wrong.

## Method

Raw (unadjusted) Yahoo OHLC for SPY, QQQ, IWM. Overnight is the log of open over the previous
close; intraday is the log of close over open; the two add up to the close-to-close return. Raw
open and raw close are used together so the split is consistent; the adjusted version rebuilds a
dividend-consistent open. Where I say "Sharpe" it is a zero-rate log-return Sharpe (mean over
standard deviation of daily log returns, times the square root of 252, no risk-free rate). Full
table in `results/overnight_intraday.md`.

## Caveats

This is a return decomposition, not a tradeable strategy or the equity risk premium. It leaves
out dividends (in the raw version), the risk-free rate, and, most importantly, costs. An
overnight-only position means crossing the spread around every close and open, and whether the
effect survives those costs is the real next question. Sample lengths differ (only SPY goes back
to 1993). US large, mid and small only; whether the night effect holds in Europe and Asia is an
obvious follow-up.
