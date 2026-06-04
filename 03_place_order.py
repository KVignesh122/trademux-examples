"""
03 — Place a Market Order

Sends a BUY or SELL market order with optional SL/TP. Guarded against
accidental execution — refuses to run unless TRADEMUX_ALLOW_LIVE_TRADES=1.

Test on a demo account first.

Usage:
    export TRADEMUX_API_KEY="sb_tmux_..."
    export TRADEMUX_ALLOW_LIVE_TRADES=1
    export TRADEMUX_SIDE=BUY            # or SELL
    export TRADEMUX_LOTS=0.01
    python 03_place_order.py
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
    if os.getenv("TRADEMUX_ALLOW_LIVE_TRADES") != "1":
        raise SystemExit(
            "Refusing to place a live order. Set TRADEMUX_ALLOW_LIVE_TRADES=1 when you really mean it."
        )

    client = build_client()
    symbol = os.getenv("TRADEMUX_SYMBOL", "EURUSD")
    side = os.getenv("TRADEMUX_SIDE", "BUY").upper()
    lots = float(os.getenv("TRADEMUX_LOTS", "0.01"))
    sl = os.getenv("TRADEMUX_SL")
    tp = os.getenv("TRADEMUX_TP")
    comment = os.getenv("TRADEMUX_COMMENT", "trademux_examples_market_order")

    kwargs = {
        "sl": float(sl) if sl else None,
        "tp": float(tp) if tp else None,
        "comment": comment,
    }

    if side == "BUY":
        result = client.buy_market(symbol, lots, **kwargs)
    elif side == "SELL":
        result = client.sell_market(symbol, lots, **kwargs)
    else:
        raise SystemExit("TRADEMUX_SIDE must be BUY or SELL.")

    print(result)
