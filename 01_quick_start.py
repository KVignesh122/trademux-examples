"""
01 — Quick Start

Connects to TradeMux, prints server status, your MT account state, and a
live quote for one symbol. Safe to run: read-only, no orders placed.

Usage:
    export TRADEMUX_API_KEY="sb_tmux_..."
    python 01_quick_start.py
"""
import os

from trademux import MTClient


def build_client() -> MTClient:
    api_key = os.getenv("TRADEMUX_API_KEY")
    if not api_key:
        raise SystemExit("Set TRADEMUX_API_KEY first.")
    server_url = os.getenv("TRADEMUX_SERVER_URL", "https://mux.skybluefin.tech")
    timeout = int(os.getenv("TRADEMUX_TIMEOUT", "20"))
    return MTClient(api_key=api_key, server_url=server_url, timeout=timeout)


if __name__ == "__main__":
    client = build_client()
    symbol = os.getenv("TRADEMUX_SYMBOL", "EURUSD")

    print("== Server ==")
    print(client.get_server_status())

    print("\n== Account ==")
    print(client.get_account_info())

    print(f"\n== Live Quote: {symbol} ==")
    print(client.get_price(symbol))
