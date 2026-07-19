from chartink import ChartinkClient
from email_sender import EmailSender
from state_manager import StateManager
from config import SCREENER_NAME

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