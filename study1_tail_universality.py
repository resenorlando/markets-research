"""STUDY 1 - Are extreme returns universal?

Hypothesis: much of the apparent difference in cross-asset tail RISK is really a
difference in volatility LEVEL, not tail SHAPE. If so, after we divide each
asset's returns by an ex-ante (causal) volatility estimate, the standardised
tails should look far more alike -- except where a market has genuinely fatter
tails (crypto, oil?).

Method (all causal, no look-ahead):
  raw:     losses = -logreturn;      fit GPD shape xi over the 95th pct
  scaled:  z = r / EWMA_vol(t-1);    fit GPD shape xi to standardised losses
We compare xi (tail shape; higher = fatter) raw vs scaled, with stationary-
bootstrap CIs, and plot left-tail survival curves before/after scaling.

Outputs: results/tail_universality.md, figures/tail_universality.png,
         figures/xi_raw_vs_scaled.png
"""
from __future__ import annotations
import sys, pathlib
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "lib"))
import evt

DATA, FIG, RES = HERE / "data", HERE / "figures", HERE / "results"
FIG.mkdir(exist_ok=True); RES.mkdir(exist_ok=True)

UNIVERSE = {  # symbol file : (label, asset class, colour)
    "SPY": ("US large cap", "equity", "#1f4e79"),
    "QQQ": ("US tech", "equity", "#2e75b6"),
    "IWM": ("US small cap", "equity", "#5b9bd5"),
    "EFA": ("DM ex-US eq", "equity", "#8faadc"),
    "EEM": ("EM equity", "equity", "#00b0f0"),
    "TLT": ("US Treasuries 20y+", "bonds", "#548235"),
    "GLD": ("Gold", "commodity", "#bf9000"),
    "USO": ("Crude oil", "commodity", "#c55a11"),
    "UUP": ("US dollar", "fx", "#7030a0"),
    "BTC_USD": ("Bitcoin", "crypto", "#c00000"),
    "ETH_USD": ("Ethereum", "crypto", "#ff0000"),
}
POT_Q = 0.95


def xi_of_losses(losses):
    u = np.quantile(losses, POT_Q)
    return evt.pot_fit(losses, u)["xi"]


def analyse(sym):
    df = pd.read_csv(DATA / f"{sym}.csv")
    r = evt.log_returns(df["AdjClose"].astype(float).values)
    r = r[np.isfinite(r)]
    losses_raw = evt.losses_from_returns(r)
    sigma = evt.ewma_vol(r, lam=0.94)
    z = r / sigma
    losses_scaled = evt.losses_from_returns(z)
    xi_raw = xi_of_losses(losses_raw)
    xi_scaled = xi_of_losses(losses_scaled)
    lo_r, hi_r, *_ = evt.bootstrap_ci(losses_raw, xi_of_losses, n_boot=200, seed=1)
    lo_s, hi_s, *_ = evt.bootstrap_ci(losses_scaled, xi_of_losses, n_boot=200, seed=1)
    return {
        "n": len(r), "xi_raw": xi_raw, "xi_scaled": xi_scaled,
        "xi_raw_ci": (lo_r, hi_r), "xi_scaled_ci": (lo_s, hi_s),
        "losses_raw": losses_raw, "losses_scaled": losses_scaled,
        "ann_vol": np.std(r) * np.sqrt(252) * 100,
    }


def survival(losses):
    x = np.sort(losses[losses > 0])[::-1]
    surv = np.arange(1, len(x) + 1) / len(x)
    return x, surv


def main():
    res = {s: analyse(s) for s in UNIVERSE}

    # ---- hero figure: raw vs scaled left-tail survival curves ----
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 5.2))
    for sym, (label, cls, col) in UNIVERSE.items():
        r = res[sym]
        x, s = survival(r["losses_raw"])
        m = x > np.quantile(r["losses_raw"], 0.90)
        axL.semilogy(x[m] * 100, s[m], color=col, lw=1.4, label=label)
        xz, sz = survival(r["losses_scaled"])
        mz = xz > np.quantile(r["losses_scaled"], 0.90)
        axR.semilogy(xz[mz], sz[mz], color=col, lw=1.4, label=label)
    axL.set_title("Raw daily losses: tails fan out by volatility level")
    axL.set_xlabel("Daily loss (%)"); axL.set_ylabel("P(loss > x | loss>0)  [log]")
    axL.set_xlim(0, 20); axL.grid(alpha=0.3, which="both")
    axR.set_title("Volatility-scaled losses: do they collapse?")
    axR.set_xlabel("Daily loss (in std deviations of that day's vol forecast)")
    axR.set_ylabel("P(loss > x | loss>0)  [log]")
    axR.set_xlim(0, 10); axR.grid(alpha=0.3, which="both")
    axR.legend(fontsize=7, ncol=2, loc="upper right")
    fig.suptitle("Are extreme returns universal?  Cross-asset tails before vs after volatility scaling",
                 fontsize=13, weight="bold")
    fig.tight_layout(); fig.savefig(FIG / "tail_universality.png", dpi=140); plt.close(fig)

    # ---- xi raw vs scaled bar chart ----
    syms = list(UNIVERSE)
    xr = [res[s]["xi_raw"] for s in syms]; xs = [res[s]["xi_scaled"] for s in syms]
    xpos = np.arange(len(syms)); w = 0.4
    fig, ax = plt.subplots(figsize=(11, 4.6))
    ax.bar(xpos - w/2, xr, w, label="raw", color="#999")
    ax.bar(xpos + w/2, xs, w, label="volatility-scaled",
           color=[UNIVERSE[s][2] for s in syms])
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xticks(xpos); ax.set_xticklabels([UNIVERSE[s][0] for s in syms], rotation=40, ha="right", fontsize=8)
    ax.set_ylabel("GPD tail-shape  ξ   (higher = fatter tail)")
    ax.set_title("Tail-shape ξ before vs after volatility scaling")
    ax.legend(); ax.grid(alpha=0.3, axis="y")
    fig.tight_layout(); fig.savefig(FIG / "xi_raw_vs_scaled.png", dpi=140); plt.close(fig)

    # ---- results markdown ----
    L = ["# Study 1 - Are extreme returns universal?\n",
         "GPD tail-shape ξ (95th-pct threshold) before/after causal EWMA(0.94) "
         "volatility scaling. Higher xi = fatter tail; xi near 0 is a Gaussian-like tail. "
         "CIs are stationary-bootstrap (200 resamples).\n",
         "| Asset | Class | N | ann.vol % | ξ raw | ξ raw 95% CI | ξ scaled | ξ scaled 95% CI |",
         "|---|---|---|---|---|---|---|---|"]
    for s in syms:
        r = res[s]; lab, cls, _ = UNIVERSE[s]
        L.append(f"| {lab} | {cls} | {r['n']} | {r['ann_vol']:.0f} | {r['xi_raw']:.3f} | "
                 f"[{r['xi_raw_ci'][0]:.2f},{r['xi_raw_ci'][1]:.2f}] | {r['xi_scaled']:.3f} | "
                 f"[{r['xi_scaled_ci'][0]:.2f},{r['xi_scaled_ci'][1]:.2f}] |")
    # simple summary stats
    eq = [s for s in syms if UNIVERSE[s][1] == "equity"]
    cr = [s for s in syms if UNIVERSE[s][1] == "crypto"]
    L.append(f"\n**Equity ξ (scaled):** mean {np.mean([res[s]['xi_scaled'] for s in eq]):.3f}, "
             f"range [{min(res[s]['xi_scaled'] for s in eq):.3f}, {max(res[s]['xi_scaled'] for s in eq):.3f}]")
    L.append(f"**Crypto ξ (scaled):** {', '.join(f'{UNIVERSE[s][0]} {res[s]['xi_scaled']:.3f}' for s in cr)}")
    (RES / "tail_universality.md").write_text("\n".join(L), encoding="utf-8")

    print("=== xi raw -> scaled ===")
    for s in syms:
        r = res[s]
        print(f" {UNIVERSE[s][0]:20s} {r['xi_raw']:+.3f} -> {r['xi_scaled']:+.3f}")
    print("\nWrote figures + results/tail_universality.md")


if __name__ == "__main__":
    main()
