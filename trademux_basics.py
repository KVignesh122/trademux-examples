"""Small MetaTrader examples. Uncomment one section at a time and run this file.
To view all available methods, see documentation at https://docs.trademux.io/mt/"""

import time

from trademux import MTClient

# Put your own TradeMux key here. Use a demo account while learning.
TRADEMUX_API_KEY = "starter_tmux_..."
SYMBOL = "EURUSD"  # Use the exact symbol shown in your MT5 Market Watch.

client = MTClient(api_key=TRADEMUX_API_KEY)


# -----------------------------------------------------------------------------
# 01 — Connection and account: safe, read-only.
# Balance is realized funds; equity also includes open trade profit/loss.
# -----------------------------------------------------------------------------
# print("Server:", client.get_server_status())
# print("Account:", client.get_account_info())
# print("Balance:", client.get_balance())
# print("Equity:", client.get_equity())
# print("Unrealized profit/loss:", client.get_floating_pnl())


# -----------------------------------------------------------------------------
# 02 — Prices, instruments, and candles: safe, read-only.
# Uncomment the lines you want to try. as_df=True returns a pandas DataFrame.
# Its time index is UTC and sorted from oldest to newest.
# -----------------------------------------------------------------------------
# print("Quote:", client.get_price(SYMBOL))  # Bid, ask, and mid.
# print("Spread:", client.get_spread(SYMBOL))  # Ask minus bid.
# print("Symbol rules:", client.get_symbol_specs(SYMBOL))  # Lot limits, digits, etc.
# print("Available symbols:", client.list_tradeable_instruments())
# candles = client.get_ohlc(SYMBOL, timeframe="1h", count=200, as_df=True)
# print("Recent candles:\n", candles.tail(10))

# For a date range, use start_date and end_date instead of count (max 5000 bars).
# history_candles = client.get_ohlc(
#     SYMBOL, timeframe="1h",
#     start_date="2025-01-01", end_date="2025-01-31", as_df=True,
# )
# print("Historical candles:\n", history_candles.tail(10))


# -----------------------------------------------------------------------------
# 03 — Market orders: these lines send REAL trades if uncommented.
# Edit lots and replace None with your SL/TP prices if you want them.
# Check the result status: a rejected order has an error instead of a ticket.
# -----------------------------------------------------------------------------
# result = client.buy_market(SYMBOL, lots=0.01, sl=None, tp=None)
# print("Market buy result:", result)
# result = client.sell_market(SYMBOL, lots=0.01, sl=None, tp=None)
# print("Market sell result:", result)


# -----------------------------------------------------------------------------
# 04 — Advanced order types: pending limit and stop orders.
# These wait for the market to reach the entry price. The numbers below are
# examples: change each price for the CURRENT quote before uncommenting it.
# Buy limit < ask; sell limit > bid; buy stop > ask; sell stop < bid.
# -----------------------------------------------------------------------------
# result = client.buy_limit(SYMBOL, lots=0.01, price=1.0800, sl=None, tp=None)
# print("Buy limit result:", result)
# result = client.sell_limit(SYMBOL, lots=0.01, price=1.1000, sl=None, tp=None)
# print("Sell limit result:", result)
# result = client.buy_stop(SYMBOL, lots=0.01, price=1.1000, sl=None, tp=None)
# print("Buy stop result:", result)
# result = client.sell_stop(SYMBOL, lots=0.01, price=1.0800, sl=None, tp=None)
# print("Sell stop result:", result)


# -----------------------------------------------------------------------------
# 05 — Inspect and manage positions and pending orders.
# list_positions() includes BOTH: position_type is "position" or "order".
# The inspection lines are read-only; modify/close lines change your account.
# -----------------------------------------------------------------------------
# items = client.list_positions().get("positions", [])
# for item in items:
#     print(item["position_type"], item["ticket"], item["symbol"], item["type"])
# Replace 123456789 with a ticket from list_positions().
# print("Ticket details:", client.get_order_details(123456789))

# Choose valid new prices for that trade.
# Change the stop loss or take profit of an open trade:
# print("Modify trade:", client.modify_order(
#     123456789, sl=1.0800, tp=1.1000,
# ))
# Change a pending order's entry price instead:
# print("Modify pending order:", client.modify_order(123456789, price=1.0800))
# Close one open position, or cancel one pending order, using its ticket:
# print("Close or cancel:", client.close_ticket(123456789))
# Close all positions and pending orders for one symbol:
# print("Close symbol:", client.close_symbol(SYMBOL))
# Close positions and pending orders tagged with one strategy's magic number:
# print("Close magic number 122:", client.close_magic(122))

# Monitor account and positions repeatedly. Uncomment this whole block;
# press Ctrl+C to stop it before running other sections below.
# try:
#     while True:
#         account = client.get_account_info()
#         print("Balance:", account.get("balance"), "Equity:", account.get("equity"))
#         for item in client.list_positions().get("positions", []):
#             print(item)
#         time.sleep(5)  # Check again after 5 seconds.
# except KeyboardInterrupt:
#     print("Monitor stopped.")


# -----------------------------------------------------------------------------
# 06 — Account history and emergency stop.
# History is read-only. The kill switch closes ALL open positions and cancels
# ALL pending orders across the account; uncomment it only when intended.
# -----------------------------------------------------------------------------
# trades = client.get_history(start_date="2025-01-01", as_df=True)
# print("Trade history:\n", trades.tail(10))
# print("Kill switch:", client.kill_switch(timeout=60))
