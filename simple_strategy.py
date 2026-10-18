"""Trade a simple 1-minute breakout. Once a minute, fetch the latest 3 candles and
check whether the candle that just closed broke the high or low of the one before."""

import time
from trademux import MTClient

# Edit these settings, then run this file on a demo account first.
TRADEMUX_API_KEY = "starter_tmux_..."
SYMBOL = "EURUSD"
LOTS = 0.01
RISK_REWARD = 2  # Take profit is this many times as far from entry as the stop loss.
FETCH_DELAY = 1  # Seconds past each minute to fetch candles, so the new one can appear.
PLACE_TRADES = False  # Set True to send real orders; False only prints signals.
ONLY_ONE_POSITION = (
    False  # If True, skip signals if there's already an open position on this symbol.
)

client = MTClient(api_key=TRADEMUX_API_KEY)
digits = client.get_symbol_specs(SYMBOL)["digits"]  # Decimal places for SL/TP prices.

print(f"Watching {SYMBOL} on 1-minute candles. Press Ctrl+C to stop.")

try:
    while True:
        # Sleep until the computer clock reaches FETCH_DELAY seconds past the minute.
        time.sleep(60 - time.time() % 60 + FETCH_DELAY)

        try:
            bars = client.get_ohlc(SYMBOL, timeframe="1min", count=3, as_df=True)
            print("\n", bars)

            # [-1] is the new, forming candle. [-2] and [-3] are completed candles.
            previous_bar = bars.iloc[-3]
            last_closed_bar = bars.iloc[-2]
            price = last_closed_bar["close"]  # Roughly where a market order will fill.

            # The stop loss goes just beyond the two completed candles.
            signal = None
            if price > previous_bar["high"]:
                signal = "BUY"
                sl = min(previous_bar["low"], last_closed_bar["low"])
                tp = price + RISK_REWARD * (price - sl)
            elif price < previous_bar["low"]:
                signal = "SELL"
                sl = max(previous_bar["high"], last_closed_bar["high"])
                tp = price - RISK_REWARD * (sl - price)

            print(f"Candle {bars.index[-2]} closed at {price}. Signal: {signal}")

            if signal is None:
                continue
            sl, tp = round(sl, digits), round(tp, digits)

            open_on_symbol = []
            if ONLY_ONE_POSITION:
                # TradeMux returns pending orders here too; only open positions count.
                positions = client.list_positions().get("positions", [])
                open_on_symbol = [
                    item
                    for item in positions
                    if item.get("symbol", "").upper() == SYMBOL.upper()
                    and item.get("position_type") == "position"
                ]

            if ONLY_ONE_POSITION and open_on_symbol:
                print(f"Already have an open {SYMBOL} position; skipping this signal.")
            elif not PLACE_TRADES:
                print(f"Would send a {signal} for {LOTS} lots (SL {sl}, TP {tp}).")
            elif signal == "BUY":
                result = client.buy_market(SYMBOL, lots=LOTS, sl=sl, tp=tp)
                print("Buy result:", result)
            else:
                result = client.sell_market(SYMBOL, lots=LOTS, sl=sl, tp=tp)
                print("Sell result:", result)
        except Exception as error:
            print("Error; will try again next minute:", error)
except KeyboardInterrupt:
    print("Strategy stopped.")
