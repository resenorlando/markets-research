"""STUDY 2 - Where does the equity return (and the equity TAIL) happen:
overnight or intraday?

Decompose each day's close-to-close move into:
  overnight = ln(Open_t / Close_{t-1})     # the gap while the market is shut
  intraday  = ln(Close_t / Open_t)         # the cash session
  c2c       = overnight + intraday

Two questions:
  (1) RETURN: which piece earns the long-run equity return?  (the "overnight drift")
  (2) TAIL:   which piece delivers the worst days, and which has the fatter GPD tail?

Data: RAW (unadjusted) Yahoo OHLC for SPY/QQQ/IWM -- we deliberately use raw open
AND raw close together so the decomposition is internally consistent (never mix
adjusted close with unadjusted open). Dividends make the raw c2c slightly understate
total return; that does not affect the overnight-vs-intraday SPLIT, which is the point.

Outputs: results/overnight_intraday.md, figures/overnight_intraday_SPY.png,
         figures/overnight_intraday_tails.png
"""
from __future__ import annotations
import sys, pathlib
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "lib")); import evt
DATA, FIG, RES = HERE / "data", HERE / "figures", HERE / "results"
ASSETS = {"SPY": "US large cap", "QQQ": "US tech", "IWM": "US small cap"}
ANN = 252


def decompose(sym):
    df = pd.read_csv(DATA / f"{sym}.csv")
    o = df["Open"].astype(float).values
    c = df["Close"].astype(float).values
    a = df["AdjClose"].astype(float).values
    d = df["Date"].values
    overnight = np.log(o[1:] / c[:-1])
    intraday = np.log(c[1:] / o[1:])
    c2c = overnight + intraday
    # Dividend/split-consistent version: reconstruct an adjusted open so the
    # overnight leg is not artificially penalised on ex-dividend days.
    adj_open = o * (a / c)
    adj_overnight = np.log(adj_open[1:] / a[:-1])
    adj_intraday = np.log(a[1:] / adj_open[1:])
    return {"date": d[1:], "overnight": overnight, "intraday": intraday, "c2c": c2c,
            "adj_overnight": adj_overnight, "adj_intraday": adj_intraday}


def stats(x):
    mu, sd = np.mean(x), np.std(x)
    return {"ann_ret": (np.exp(np.sum(x)) ** (ANN / len(x)) - 1) * 100,
            "ann_sharpe": (mu / sd) * np.sqrt(ANN) if sd > 0 else np.nan,
            "total_growth": np.exp(np.sum(x))}


def gpd_xi(losses):
    losses = losses[losses > 0]
    return evt.pot_fit(losses, np.quantile(losses, 0.95))["xi"]


def main():
    allres = {s: decompose(s) for s in ASSETS}

    # ---- hero figure: cumulative overnight vs intraday for SPY ----
    r = allres["SPY"]
    x = np.arange(len(r["c2c"]))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, np.exp(np.cumsum(r["overnight"])), color="#1f4e79", lw=1.8,
            label="Overnight only (close->open)")
    ax.plot(x, np.exp(np.cumsum(r["intraday"])), color="#c0392b", lw=1.8,
            label="Intraday only (open->close)")
    ax.plot(x, np.exp(np.cumsum(r["c2c"])), color="#888", lw=1.2, ls="--",
            label="Buy & hold (close->close, ex-div)")
    yrs = pd.to_datetime(r["date"])
    ticks = np.linspace(0, len(x) - 1, 7).astype(int)
    ax.set_xticks(ticks); ax.set_xticklabels([str(yrs[t])[:4] for t in ticks])
    ax.set_yscale("log"); ax.set_ylabel("Growth of $1 (log scale)")
    ax.set_title("SPY: where the return happens - overnight vs intraday (1993-2026)")
    ax.legend(); ax.grid(alpha=0.3, which="both")
    fig.tight_layout(); fig.savefig(FIG / "overnight_intraday_SPY.png", dpi=140); plt.close(fig)

    # ---- worst-day tail attribution (SPY) ----
    order = np.argsort(r["c2c"])[:100]  # 100 worst close-to-close days
    on_contrib = r["overnight"][order].sum()
    id_contrib = r["intraday"][order].sum()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.6))
    a1.scatter(r["overnight"][order] * 100, r["intraday"][order] * 100, s=18,
               c="#c0392b", alpha=0.7)
    a1.axhline(0, color="k", lw=0.5); a1.axvline(0, color="k", lw=0.5)
    a1.set_xlabel("Overnight part (%)"); a1.set_ylabel("Intraday part (%)")
    a1.set_title("SPY 100 worst days: overnight vs intraday split")
    a1.grid(alpha=0.3)
    a2.bar(["Overnight", "Intraday"], [on_contrib * 100, id_contrib * 100],
           color=["#1f4e79", "#c0392b"])
    a2.set_ylabel("Summed log-loss on the 100 worst days (%)")
    a2.set_title("Which part drives the worst days?")
    a2.grid(alpha=0.3, axis="y")
    fig.tight_layout(); fig.savefig(FIG / "overnight_intraday_tails.png", dpi=140); plt.close(fig)

    # ---- results table ----
    L = ["# Study 2 - Overnight vs intraday: return and tail\n",
         "overnight=ln(O_t/C_{t-1}), intraday=ln(C_t/O_t) on RAW OHLC; the `adj_*` "
         "rows use a dividend-consistent adjusted open (AdjOpen=Open*AdjClose/Close). "
         "'ann.Sharpe' is a **zero-rate log-return Sharpe proxy** (mean/std of daily "
         "log returns * sqrt(252), no risk-free rate). GPD xi is the loss-tail shape "
         "(fit to the worst ~2.2-2.4% of ALL days, i.e. the 95th pct of loss-only days). "
         "Samples: SPY from 1993, QQQ 1999, IWM 2000.\n",
         "| Asset | leg | ann.ret % | ann.Sharpe(proxy) | GPD xi (loss tail) |",
         "|---|---|---|---|---|"]
    for s, lab in ASSETS.items():
        rr = allres[s]
        for leg in ["overnight", "intraday", "c2c", "adj_overnight", "adj_intraday"]:
            st = stats(rr[leg]); xi = gpd_xi(evt.losses_from_returns(rr[leg]))
            L.append(f"| {lab} | {leg} | {st['ann_ret']:.1f} | {st['ann_sharpe']:.2f} | {xi:.3f} |")
    # SPY worst-day attribution summary
    tot = on_contrib + id_contrib
    L.append(f"\n**SPY 100 worst close-to-close days:** overnight contributed "
             f"{100*on_contrib:.0f}% cumulative log-loss, intraday {100*id_contrib:.0f}% "
             f"(overnight = {100*on_contrib/tot:.0f}% of the damage).")
    (RES / "overnight_intraday.md").write_text("\n".join(L), encoding="utf-8")

    print("=== annualised return: overnight vs intraday ===")
    for s, lab in ASSETS.items():
        rr = allres[s]
        so, si = stats(rr["overnight"]), stats(rr["intraday"])
        print(f" {lab:14s} overnight {so['ann_ret']:+6.1f}%/yr (Sharpe {so['ann_sharpe']:+.2f})   "
              f"intraday {si['ann_ret']:+6.1f}%/yr (Sharpe {si['ann_sharpe']:+.2f})")
    print(f"\nSPY worst-100-days: overnight {100*on_contrib:.0f}% vs intraday {100*id_contrib:.0f}% of log-loss")
    print("Wrote figures + results/overnight_intraday.md")


if __name__ == "__main__":
    main()
