"""
04 — Monitor Positions

Polls account balance/equity/PnL and lists every open position on a fixed
interval. Ctrl+C to stop.

Safe to run: read-only.

Usage:
    export TRADEMUX_API_KEY="sb_tmux_..."
    export TRADEMUX_POLL_SECONDS=5
    python 04_monitor_positions.py
"""
import os
import time

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
    poll_seconds = int(os.getenv("TRADEMUX_POLL_SECONDS", "5"))

    try:
        while True:
            account = client.get_account_info()
            positions = client.list_positions().get("positions", [])

            print(
                {
                    "balance": account.get("balance"),
                    "equity": account.get("equity"),
                    "floating_pnl": account.get("floating_pnl"),
                    "open_positions": len(positions),
                }
            )

            for position in positions:
                print(position)

            print("-" * 60)
            time.sleep(poll_seconds)
    except KeyboardInterrupt:
        print("Stopped position monitor.")
