# Study 3 - Which diversifier survives a crash?

Finite-threshold lower-tail co-exceedance chi(u) = P(hedge in worst u% | SPY in worst u%), with Wilson 95% CIs. **Under independence chi(u)=u** (so the deep-tail benchmark is 1%, not 10%). Pearson corr = average-day contrast. Pairwise overlap sample (each pair uses its own common dates).

| Hedge | u | chi | 95% CI (Wilson) | joint / SPY-bad days | corr | since |
|---|---|---|---|---|---|---|
| Long Treasuries | 10.0% | 0.10 | [0.07,0.12] | 58/607 | -0.30 | 2002-07-31 |
| Long Treasuries | 5.0% | 0.05 | [0.03,0.08] | 15/304 | -0.30 | 2002-07-31 |
| Long Treasuries | 2.5% | 0.04 | [0.02,0.08] | 6/152 | -0.30 | 2002-07-31 |
| Long Treasuries | 1.0% | 0.08 | [0.04,0.18] | 5/61 | -0.30 | 2002-07-31 |
| Gold | 10.0% | 0.18 | [0.15,0.22] | 101/549 | +0.07 | 2004-11-19 |
| Gold | 5.0% | 0.12 | [0.09,0.17] | 34/275 | +0.07 | 2004-11-19 |
| Gold | 2.5% | 0.12 | [0.08,0.19] | 17/138 | +0.07 | 2004-11-19 |
| Gold | 1.0% | 0.11 | [0.05,0.22] | 6/55 | +0.07 | 2004-11-19 |
| US dollar | 10.0% | 0.11 | [0.09,0.14] | 55/491 | -0.19 | 2007-03-02 |
| US dollar | 5.0% | 0.08 | [0.05,0.12] | 20/246 | -0.19 | 2007-03-02 |
| US dollar | 2.5% | 0.06 | [0.03,0.11] | 7/123 | -0.19 | 2007-03-02 |
| US dollar | 1.0% | 0.10 | [0.04,0.21] | 5/50 | -0.19 | 2007-03-02 |
| DM ex-US equity | 10.0% | 0.66 | [0.62,0.70] | 416/630 | +0.87 | 2001-08-28 |
| DM ex-US equity | 5.0% | 0.63 | [0.57,0.68] | 198/315 | +0.87 | 2001-08-28 |
| DM ex-US equity | 2.5% | 0.64 | [0.56,0.71] | 101/158 | +0.87 | 2001-08-28 |
| DM ex-US equity | 1.0% | 0.71 | [0.59,0.81] | 45/63 | +0.87 | 2001-08-28 |
| EM equity | 10.0% | 0.61 | [0.57,0.65] | 359/589 | +0.81 | 2003-04-15 |
| EM equity | 5.0% | 0.56 | [0.50,0.61] | 164/295 | +0.81 | 2003-04-15 |
| EM equity | 2.5% | 0.59 | [0.51,0.66] | 87/148 | +0.81 | 2003-04-15 |
| EM equity | 1.0% | 0.63 | [0.50,0.74] | 37/59 | +0.81 | 2003-04-15 |
| US tech | 10.0% | 0.70 | [0.66,0.73] | 483/692 | +0.85 | 1999-03-11 |
| US tech | 5.0% | 0.63 | [0.58,0.68] | 218/346 | +0.85 | 1999-03-11 |
| US tech | 2.5% | 0.48 | [0.41,0.55] | 83/173 | +0.85 | 1999-03-11 |
| US tech | 1.0% | 0.40 | [0.29,0.52] | 28/70 | +0.85 | 1999-03-11 |

## Common-window robustness (all assets, 2007-03-02..2026-09-04), 1% level

| Hedge | chi (1%) | joint / SPY-bad |
|---|---|---|
| Long Treasuries | 0.08 | 4/50 |
| Gold | 0.10 | 5/50 |
| US dollar | 0.10 | 5/50 |
| DM ex-US equity | 0.74 | 37/50 |
| EM equity | 0.64 | 32/50 |
| US tech | 0.70 | 35/50 |