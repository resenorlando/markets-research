"""STUDY 3 - Which 'diversifier' actually survives a crash?

Correlation is an average-day statistic; in a crash what matters is whether your
hedge crashes WITH equities. We measure finite-threshold lower-tail co-exceedance:

  chi(u) = P( hedge in its worst u% | SPY in its worst u% )

Under INDEPENDENCE chi(u) = u itself (so the benchmark line is the diagonal, not
a flat 0.1). As u shrinks (10% -> 1%) we look deeper into joint crashes. A genuine
crash hedge keeps chi far below the equity assets; but note even "hedges" sit at
several times the independence level in the deep tail. This is finite-threshold
co-exceedance, NOT the asymptotic tail-dependence coefficient lim_{u->0} chi(u).

Outputs: results/crash_dependence.md, figures/crash_dependence.png
"""
from __future__ import annotations
import sys, pathlib
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "lib")); import evt
DATA, FIG, RES = HERE / "data", HERE / "figures", HERE / "results"

BASE = "SPY"
HEDGES = {
    "TLT": ("Long Treasuries", "#548235"),
    "GLD": ("Gold", "#bf9000"),
    "UUP": ("US dollar", "#7030a0"),
    "EFA": ("DM ex-US equity", "#8faadc"),
    "EEM": ("EM equity", "#00b0f0"),
    "QQQ": ("US tech", "#2e75b6"),
}
LEVELS = [0.10, 0.05, 0.025, 0.01]


def load(sym):
    df = pd.read_csv(DATA / f"{sym}.csv")[["Date", "AdjClose"]]
    df["r"] = np.log(df["AdjClose"].astype(float)).diff()
    return df[["Date", "r"]].dropna()


def lower_tail_dep(rb, rh, u):
    qb, qh = np.quantile(rb, u), np.quantile(rh, u)
    base_bad = rb <= qb
    both = base_bad & (rh <= qh)
    return both.sum() / base_bad.sum(), int(base_bad.sum()), int(both.sum())


def wilson(k, n, z=1.96):
    """Wilson 95% CI for a binomial proportion k/n."""
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0, centre - half), min(1, centre + half))


def main():
    base = load(BASE).rename(columns={"r": "rb"})
    rows, curves = [], {}
    for sym, (lab, col) in HEDGES.items():
        h = load(sym).rename(columns={"r": "rh"})
        m = base.merge(h, on="Date")
        rb, rh = m["rb"].values, m["rh"].values
        corr = np.corrcoef(rb, rh)[0, 1]
        chis = []
        for u in LEVELS:
            chi, nb, nboth = lower_tail_dep(rb, rh, u)
            lo, hi = wilson(nboth, nb)
            chis.append(chi)
            rows.append((lab, f"{u*100:.1f}%", chi, lo, hi, nboth, nb, corr, m["Date"].min()))
        curves[sym] = chis

    # ---- common-window robustness: intersect ALL assets' dates ----
    common = base.copy()
    for sym in HEDGES:
        common = common.merge(load(sym).rename(columns={"r": sym}), on="Date")
    cw = {}
    rb = common["rb"].values
    for sym in HEDGES:
        chi, nb, nboth = lower_tail_dep(rb, common[sym].values, 0.01)
        cw[sym] = (chi, nboth, nb)
    cw_span = (common["Date"].min(), common["Date"].max())

    # ---- figure ----
    fig, ax = plt.subplots(figsize=(9, 5))
    xs = [f"{u*100:.1f}%" for u in LEVELS]
    for sym, (lab, col) in HEDGES.items():
        ax.plot(xs, curves[sym], "o-", color=col, lw=1.8, label=lab)
    ax.plot(xs, LEVELS, "k--", lw=1.1, label="independence (chi = u)")
    ax.set_xlabel("Joint-crash depth: both assets in their worst X% of days (1% = deepest)")
    ax.set_ylabel("P( hedge crashes | SPY crashes )")
    ax.set_title("Which 'diversifier' survives a crash?  Lower-tail co-exceedance with SPY")
    ax.invert_xaxis()
    ax.legend(fontsize=8, ncol=2); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(FIG / "crash_dependence.png", dpi=140); plt.close(fig)

    # ---- results ----
    L = ["# Study 3 - Which diversifier survives a crash?\n",
         "Finite-threshold lower-tail co-exceedance chi(u) = P(hedge in worst u% | "
         "SPY in worst u%), with Wilson 95% CIs. **Under independence chi(u)=u** "
         "(so the deep-tail benchmark is 1%, not 10%). Pearson corr = average-day "
         "contrast. Pairwise overlap sample (each pair uses its own common dates).\n",
         "| Hedge | u | chi | 95% CI (Wilson) | joint / SPY-bad days | corr | since |",
         "|---|---|---|---|---|---|---|"]
    for lab, u, chi, lo, hi, nboth, nb, corr, since in rows:
        L.append(f"| {lab} | {u} | {chi:.2f} | [{lo:.2f},{hi:.2f}] | {nboth}/{nb} | {corr:+.2f} | {since} |")
    L.append(f"\n## Common-window robustness (all assets, {cw_span[0]}..{cw_span[1]}), 1% level\n")
    L.append("| Hedge | chi (1%) | joint / SPY-bad |")
    L.append("|---|---|---|")
    for sym in HEDGES:
        chi, nboth, nb = cw[sym]
        L.append(f"| {HEDGES[sym][0]} | {chi:.2f} | {nboth}/{nb} |")
    (RES / "crash_dependence.md").write_text("\n".join(L), encoding="utf-8")

    print("=== P(hedge crashes | SPY crashes), by depth (independence = u) ===")
    print(f"{'hedge':18s} " + "  ".join(f"{u*100:>5.1f}%" for u in LEVELS) + "   corr")
    for sym, (lab, col) in HEDGES.items():
        c = curves[sym]
        corr = [r[7] for r in rows if r[0] == lab][0]
        print(f"{lab:18s} " + "  ".join(f"{v:5.2f}" for v in c) + f"   {corr:+.2f}")
    print(f"\nCommon window {cw_span[0]}..{cw_span[1]} (1% level):")
    for sym in HEDGES:
        print(f"  {HEDGES[sym][0]:18s} chi={cw[sym][0]:.2f}  ({cw[sym][1]}/{cw[sym][2]})")


if __name__ == "__main__":
    main()
