import json
import os
from datetime import datetime

class FlightLogger:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        ts = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
        self.path = f"logs/flight_{ts}.jsonl"
        self.errors = []

    def add_error(self, text):
        self.errors.append(text)
        if len(self.errors) > 20:
            self.errors.pop(0)

    def write(self, data):
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            **data,
            "errors": list(self.errors)
        }
        with open(self.path, "a") as f:
            f.write(json.dumps(entry) + "\n")
