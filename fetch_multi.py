"""Fetch full-history daily OHLC + adjusted close for a multi-asset universe
from the Yahoo Finance chart API. Saves one CSV per symbol (Date, Open, Close,
AdjClose) into ./data. Used by both research studies.
"""
import json, time, urllib.request, urllib.parse, pathlib, datetime as dt, sys

DATA = pathlib.Path(__file__).resolve().parent / "data"
DATA.mkdir(exist_ok=True)

# Cross-asset universe: US large/mid/small, DM & EM ex-US, bonds, gold, oil,
# the dollar, and crypto. Labelled by asset class for the tail study.
UNIVERSE = {
    "SPY": "US large cap", "QQQ": "US tech", "IWM": "US small cap",
    "EFA": "DM ex-US eq", "EEM": "EM equity", "TLT": "US 20y+ Treasuries",
    "GLD": "Gold", "USO": "Crude oil", "UUP": "US dollar",
    "BTC-USD": "Bitcoin", "ETH-USD": "Ethereum",
}
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def fetch(symbol, rng="max", interval="1d", retries=3):
    # Use explicit period1/period2 (unix secs) to force DAILY granularity over
    # full history; range=max silently downgrades to monthly bars.
    p2 = int(time.time())
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/"
           f"{urllib.parse.quote(symbol)}?period1=0&period2={p2}&interval={interval}")
    for a in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode())
        except Exception as e:  # noqa: BLE001
            print(f"  retry {a+1} {symbol}: {e}", file=sys.stderr); time.sleep(2)
    return None


def parse(js):
    res = js["chart"]["result"][0]
    ts = res["timestamp"]
    q = res["indicators"]["quote"][0]
    adj = res["indicators"].get("adjclose", [{}])[0].get("adjclose", q["close"])
    rows = []
    for i, t in enumerate(ts):
        o, c, a = q["open"][i], q["close"][i], adj[i]
        if c is None or o is None:
            continue
        d = dt.datetime.utcfromtimestamp(t).strftime("%Y-%m-%d")
        rows.append((d, o, c, a if a is not None else c))
    return rows


def main():
    import pandas as pd
    for sym, label in UNIVERSE.items():
        print(f"Fetching {sym} ({label}) ...")
        js = fetch(sym)
        if js is None:
            print(f"  SKIP {sym}"); continue
        rows = parse(js)
        df = pd.DataFrame(rows, columns=["Date", "Open", "Close", "AdjClose"]).drop_duplicates("Date")
        name = sym.replace("-", "_")
        df.to_csv(DATA / f"{name}.csv", index=False)
        print(f"  {name}: {len(df)} rows, {df.Date.min()} -> {df.Date.max()}")
        time.sleep(1)


if __name__ == "__main__":
    main()
