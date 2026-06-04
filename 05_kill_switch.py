"""
05 — Kill Switch

Closes every open position and cancels every pending order on the account.
Guarded against accidental execution — refuses to run unless
TRADEMUX_CONFIRM_KILL_SWITCH=YES.

Usage:
    export TRADEMUX_API_KEY="sb_tmux_..."
    export TRADEMUX_CONFIRM_KILL_SWITCH=YES
    python 05_kill_switch.py
"""
import os

from trademux import MTClient


def build_client() -> MTClient:
    api_key = os.getenv("TRADEMUX_API_KEY")
    if not api_key:
        raise SystemExit("Set TRADEMUX_API_KEY first.")
    server_url = os.getenv("TRADEMUX_SERVER_URL", "https://mux.skybluefin.tech")
    timeout = int(os.getenv("TRADEMUX_TIMEOUT", "60"))
    return MTClient(api_key=api_key, server_url=server_url, timeout=timeout)


if __name__ == "__main__":
    if os.getenv("TRADEMUX_CONFIRM_KILL_SWITCH") != "YES":
        raise SystemExit(
            "Refusing to trigger kill switch. Set TRADEMUX_CONFIRM_KILL_SWITCH=YES when you really mean it."
        )

    client = build_client()
    timeout = int(os.getenv("TRADEMUX_KILL_SWITCH_TIMEOUT", "60"))
    print(client.kill_switch(timeout=timeout))
