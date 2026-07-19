# config.py

SCREENER_NAME = "RSI Overbought"

SCREENER_URL = "https://chartink.com/screener/rsi-overbought-2549"

SCAN_CLAUSE = """
({33489}(
[0] 15 minute rsi(30) > 70 and
[-1] 15 minute rsi(30) > 70 and
[-2] 15 minute rsi(30) > 70 and
[-3] 15 minute rsi(30) > 70
))
"""

PROCESS_URL = "https://chartink.com/screener/process"