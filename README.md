<p align="center">
  <img src="assets/banner.svg" alt="TradeMux — Unified API for forex trading" width="100%" />
</p>

<h1 align="center">TradeMux Examples</h1>

Two beginner-friendly Python files for an MT4 or MT5 account connected to TradeMux:

| File | What it shows |
| --- | --- |
| [`trademux_basics.py`](trademux_basics.py) | Account details, quotes, candles, orders, positions, trade history, and account controls. |
| [`simple_strategy.py`](simple_strategy.py) | A one-minute breakout loop with stop loss, take profit, and optional market orders. |

## Get started

1. Install the packages: `pip install -r requirements.txt`
2. Get a key from [TradeMux Console](https://console.trademux.io) and connect your MT4/MT5 account and TradeMux EA. See the [MetaTrader setup guide](https://docs.trademux.io/mt/setup).
3. Put your key in `TRADEMUX_API_KEY` at the top of the file you want to run. Set `SYMBOL` to the exact name in your terminal's Market Watch. No `.env` file is needed.
4. Run `python trademux_basics.py` or `python simple_strategy.py`.

`trademux_basics.py` has numbered sections with commented code. Edit values directly in the example calls, uncomment the lines you want to try, and run the file. It prints nothing until you enable a section. Order, modification, close, and kill-switch calls act on the connected account when uncommented. Try those on a demo account first. Keep your real API key out of commits.

`simple_strategy.py` fetches three one-minute candles shortly after each minute starts. It compares the most recently closed candle with the one before it: a close above the previous high is a buy signal, and a close below the previous low is a sell signal. It places the stop loss beyond those two completed candles and uses `RISK_REWARD` to set the take profit. Adjust `FETCH_DELAY` if the new candle takes longer to appear. `PLACE_TRADES = False` prints signals without placing orders; set it to `True` to trade. Set `ONLY_ONE_POSITION = True` if you want to skip signals while a position is already open on `SYMBOL`. Stop the loop with Ctrl+C.

These are learning examples, not a tested profitable strategy. See the [TradeMux MetaTrader SDK reference](https://docs.trademux.io/mt/) for all available methods and their parameters.

---

## About SkyBlue Fintech

TradeMux is built and operated by **SkyBlue Fintech Solutions LLP** ([corporate site](https://skybluefin.tech)), a Singapore-based Data Analytics and Processing Company and a member of the Singapore FinTech Association.

<p>
  <img src="assets/skyblue-logo-dark.svg" alt="SkyBlue Fintech logo" width="220" />
</p>
