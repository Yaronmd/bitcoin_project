import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DataFetcher:
    def __init__(self, client, endpoint: str, output_file: str):
        self.client = client
        self.endpoint = endpoint
        self.output_file = output_file

    def fetch_and_save(self):
        response = self.client.get(self.endpoint)
        if response.status == 200:
            data = response.json()
            record = {
                "timestamp": datetime.utcnow().isoformat(),
                "data": data
            }
            self._save_to_file(record)
            logger.info(f"Fetched and saved at {record['timestamp']}")
        else:
            logger.warning(f"Failed to fetch: {response.status}")

    def _save_to_file(self, record):
        try:
            with open(self.output_file, "r") as f:
                existing = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing = []

        existing.append(record)
        with open(self.output_file, "w") as f:
            json.dump(existing, f, indent=2)