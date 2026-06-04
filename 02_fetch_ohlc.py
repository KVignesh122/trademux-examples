"""
02 — Fetch OHLC

Pulls candles into a pandas DataFrame. Two modes:
- latest N bars (default 200, set TRADEMUX_COUNT)
- bounded historical window (set TRADEMUX_START_DATE and optionally
  TRADEMUX_END_DATE, max 5000 bars per call)

Safe to run: read-only.

Usage:
    export TRADEMUX_API_KEY="sb_tmux_..."
    python 02_fetch_ohlc.py
"""
import os
from trademux import MTClient


def build_client() -> MTClient:
    api_key = os.getenv("TRADEMUX_API_KEY")
    if not api_key:
        raise SystemExit("Set TRADEMUX_API_KEY first.")
    server_url = os.getenv("TRADEMUX_SERVER_URL", "https://mux.skybluefin.tech")
    timeout = int(os.getenv("TRADEMUX_TIMEOUT", "30"))
    return MTClient(api_key=api_key, server_url=server_url, timeout=timeout)


if __name__ == "__main__":
    client = build_client()
    symbol = os.getenv("TRADEMUX_SYMBOL", "EURUSD")
    timeframe = os.getenv("TRADEMUX_TIMEFRAME", "1h")
    start_date = os.getenv("TRADEMUX_START_DATE")
    end_date = os.getenv("TRADEMUX_END_DATE")

    if start_date:
        frame = client.get_ohlc(
            symbol,
            timeframe=timeframe,
            start_date=start_date,
            end_date=end_date,
            as_df=True,
        )
        print(f"Fetched bounded history for {symbol} {timeframe}")
    else:
        count = int(os.getenv("TRADEMUX_COUNT", "200"))
        frame = client.get_ohlc(symbol, timeframe=timeframe, count=count, as_df=True)
        print(f"Fetched latest {count} bars for {symbol} {timeframe}")

    print(frame.tail(10))
    if not frame.empty:
        print("\nRange:")
        print({
            "from": frame.index.min().isoformat(),
            "to": frame.index.max().isoformat(),
            "rows": len(frame),
            "close": float(frame["close"].iloc[-1]),
        })
