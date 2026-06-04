<p align="center">
  <img src="assets/banner.svg" alt="TradeMux — Unified API for forex trading" width="100%" />
</p>

<h1 align="center">TradeMux Examples</h1>

<p align="center">
  <b>Trade MT4 / MT5 from Python. No strategy logic in MQL. No custom bridge to maintain.</b>
</p>

<p align="center">
  <a href="https://pypi.org/project/trademux/"><img src="https://img.shields.io/pypi/v/trademux.svg?color=0AE9EB&label=pypi" alt="PyPI"></a>
  <a href="https://pypi.org/project/trademux/"><img src="https://img.shields.io/pypi/pyversions/trademux.svg?color=0925F9" alt="Python versions"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-555.svg" alt="License"></a>
  <a href="https://docs.trademux.io"><img src="https://img.shields.io/badge/docs-trademux.io-0925F9" alt="Docs"></a>
</p>

---

Six runnable scripts that show what a real Python workflow looks like on top of [TradeMux](https://www.trademux.io) — from a one-line account check to a momentum strategy that fires live orders.

```python
from trademux import MTClient

client = MTClient(api_key="sb_tmux_...")

print(client.get_account_info())
print(client.get_ohlc("EURUSD", timeframe="1h", count=200, as_df=True).tail())
print(client.buy_market("EURUSD", lots=0.01, sl=1.0900, tp=1.1000))
```

That's it. Same code works for MT4 and MT5.

---

## How it fits together

```
┌──────────────┐        ┌──────────────┐        ┌─────────────────┐
│  Your Python │  HTTPS │   TradeMux   │   EA   │  MT4 / MT5      │
│   strategy   │ ─────▶ │   Gateway    │ ─────▶ │  Terminal       │
└──────────────┘        └──────────────┘        └─────────────────┘
   (this repo)            (mux.skybluefin.tech)    (your broker)
```

Your code talks to TradeMux over HTTPS while a lightweight EA in MT4/MT5 handles terminal execution and posts results back.

---

## Install

```bash
pip install trademux
```

Grab a free starter key from [console.trademux.io](https://console.trademux.io) and map it to an MT account.

## Configure

```bash
export TRADEMUX_API_KEY="sb_tmux_..."
export TRADEMUX_SERVER_URL="https://mux.skybluefin.tech"   # optional
export TRADEMUX_TIMEOUT="20"                               # optional
```

## Run

```bash
python 01_quick_start.py
```

---

## The Examples

| # | File | What it shows |
|---|---|---|
| 01 | `01_quick_start.py` | Connect, check server, print account state and a live quote |
| 02 | `02_fetch_ohlc.py` | Recent bars or a bounded historical window straight into a DataFrame |
| 03 | `03_place_order.py` | Market BUY / SELL with optional SL/TP — guarded against accidents |
| 04 | `04_monitor_positions.py` | Poll account + open positions in a clean loop |
| 05 | `05_kill_switch.py` | Flatten everything fast, with explicit confirmation guard |
| 06 | `06_simple_strategy.py` | End-to-end: OHLC → signal → position check → optional execution |

### What you'll see

`01_quick_start.py`:

```
== Server ==
{'status': 'ok'}

== Account ==
{'balance': 10000.0, 'equity': 10042.5, 'floating_pnl': 42.5, 'open_positions': 1, ...}

== Live Quote: EURUSD ==
{'symbol': 'EURUSD', 'bid': 1.0852, 'ask': 1.0853, 'mid': 1.08525, ...}
```

`02_fetch_ohlc.py` returns a pandas DataFrame indexed by UTC time, sorted oldest-first — drop straight into your research notebook.

---

## Safety Rails

The two scripts that can move money are intentionally locked behind explicit opt-ins:

| Script | Required env var |
|---|---|
| `03_place_order.py` | `TRADEMUX_ALLOW_LIVE_TRADES=1` |
| `05_kill_switch.py` | `TRADEMUX_CONFIRM_KILL_SWITCH=YES` |
| `06_simple_strategy.py` (execution path) | `TRADEMUX_ALLOW_LIVE_TRADES=1` |

Without the flags, they print what they would do and exit. Test on a demo account first.

---

## Common Patterns

**Backfill bounded historical OHLC** (capped at 5000 bars per request):

```python
chunk = client.get_ohlc(
    "EURUSD",
    timeframe="1h",
    start_date="2025-01-01",
    end_date="2025-06-01",
    as_df=True,
)
```

**Close every position with one magic number** (useful when one strategy needs to bail out):

```python
client.close_magic(122)
```

**Emergency stop everything across all symbols / orders**:

```python
client.kill_switch(timeout=60)
```

---

## Links

- 🌐 [trademux.io](https://www.trademux.io)
- 📚 [docs.trademux.io](https://docs.trademux.io) — full SDK reference
- 🐍 [pypi.org/project/trademux](https://pypi.org/project/trademux/)
- 💬 Issues & feature requests welcome here

If these snippets save you time, a ⭐ on the repo helps other quants find it.

---

## About SkyBlue Fintech

TradeMux is built and operated by **SkyBlue Fintech Solutions LLP**, a Singapore-based trading technology company focused on clean APIs, cross-platform execution infrastructure, and developer-first tooling for systematic traders.

Thanks for checking out the repo.

<p>
  <img src="assets/banner.svg" alt="TradeMux by SkyBlue Fintech" width="220" />
</p>
