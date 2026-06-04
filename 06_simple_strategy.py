"""
06 — Simple Strategy

Minimal end-to-end loop: fetch 3 bars → compare last close to previous bar's
high/low → emit BUY / SELL / no-signal. If a signal exists and no position
is open on the symbol, prints the intended order; executes it live only when
TRADEMUX_ALLOW_LIVE_TRADES=1 is set.

This is a deliberately tiny strategy meant as a wiring template, not a
profitable system.

Usage:
    export TRADEMUX_API_KEY="sb_tmux_..."
    python 06_simple_strategy.py                          # signal-only (safe)
    export TRADEMUX_ALLOW_LIVE_TRADES=1                   # then will execute
    python 06_simple_strategy.py
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


def latest_signal(client: MTClient, symbol: str, timeframe: str):
    frame = client.get_ohlc(symbol, timeframe=timeframe, count=3, as_df=True)
    if len(frame) < 3:
        raise RuntimeError("Need at least 3 bars to compute the signal.")

    previous = frame.iloc[-2]
    current = frame.iloc[-1]

    if float(current["close"]) > float(previous["high"]):
        return "BUY", frame
    if float(current["close"]) < float(previous["low"]):
        return "SELL", frame
    return None, frame


if __name__ == "__main__":
    client = build_client()
    symbol = os.getenv("TRADEMUX_SYMBOL", "EURUSD")
    timeframe = os.getenv("TRADEMUX_TIMEFRAME", "1h")
    lots = float(os.getenv("TRADEMUX_LOTS", "0.01"))

    signal, frame = latest_signal(client, symbol, timeframe)
    positions = client.list_positions().get("positions", [])
    symbol_positions = [p for p in positions if str(p.get("symbol", "")).upper() == symbol.upper()]

    print({
        "symbol": symbol,
        "timeframe": timeframe,
        "signal": signal,
        "open_positions_on_symbol": len(symbol_positions),
        "last_close": float(frame["close"].iloc[-1]),
    })

    if signal is None:
        print("No trade signal.")
    elif symbol_positions:
        print("Signal exists, but a position on this symbol is already open.")
    elif os.getenv("TRADEMUX_ALLOW_LIVE_TRADES") == "1":
        if signal == "BUY":
            print(client.buy_market(symbol, lots, comment="trademux_examples_simple_strategy"))
        else:
            print(client.sell_market(symbol, lots, comment="trademux_examples_simple_strategy"))
    else:
        print("Signal detected. Set TRADEMUX_ALLOW_LIVE_TRADES=1 to execute.")
