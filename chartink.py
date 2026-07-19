import requests
from bs4 import BeautifulSoup
from config import SCREENER_URL, PROCESS_URL, SCAN_CLAUSE


class ChartinkClient:

    def __init__(self):
        self.session = requests.Session()

        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    def get_csrf_token(self):

        response = self.session.get(
            SCREENER_URL,
            headers=self.headers
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        csrf = soup.find(
            "meta",
            {"name": "csrf-token"}
        )["content"]

        return csrf

    def run_scan(self):

        csrf = self.get_csrf_token()

        self.headers.update({
            "X-CSRF-TOKEN": csrf,
            "X-Requested-With": "XMLHttpRequest"
        })

        payload = {
            "scan_clause": SCAN_CLAUSE
        }

        response = self.session.post(
            PROCESS_URL,
            headers=self.headers,
            data=payload
        )

        response.raise_for_status()

        data = response.json()

        stocks = []

        for item in data.get("data", []):

            stocks.append({
                "symbol": item["nsecode"],
                "close": item.get("close"),
                "volume": item.get("volume")
            })

        return stocks