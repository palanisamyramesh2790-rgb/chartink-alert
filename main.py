from chartink import ChartinkClient
from email_sender import EmailSender
from state_manager import StateManager
from config import SCREENER_NAME
from datetime import datetime
from zoneinfo import ZoneInfo
import sys

#from chartink import ChartinkClient
#from email_sender import EmailSender
#from state_manager import StateManager
#from config import SCREENER_NAME

# Market hours check
now = datetime.now(ZoneInfo("Asia/Kolkata"))

if now.weekday() >= 5:
    print("Weekend. Exiting.")
    sys.exit(0)

market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)

if not (market_open <= now <= market_close):
    print("Outside NSE market hours. Exiting.")
    sys.exit(0)

client = ChartinkClient()
mailer = EmailSender()
state = StateManager()

current = client.run_scan()

current_symbols = sorted([
    stock["symbol"]
    for stock in current
])

previous_symbols = state.load()

new_symbols = sorted(
    list(
        set(current_symbols) -
        set(previous_symbols)
    )
)

if new_symbols:

    print("New Stocks Found")

    print(new_symbols)

    new_stock_details = [
        stock
        for stock in current
        if stock["symbol"] in new_symbols
    ]

    mailer.send(
        SCREENER_NAME,
        new_stock_details
    )

else:

    print("No New Stocks")

state.save(current_symbols)