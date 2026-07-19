import json
import os


class StateManager:

    def __init__(self, filename="previous_results.json"):
        self.filename = filename

    def load(self):

        if not os.path.exists(self.filename):
            return []

        with open(self.filename, "r") as f:
            return json.load(f)

    def save(self, stocks):

        with open(self.filename, "w") as f:
            json.dump(stocks, f, indent=4)