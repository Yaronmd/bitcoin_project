import json
import os
from dotenv import load_dotenv

load_dotenv()

class ConfigLoader:
    def __init__(self, path=None):
        
        self.path = path or os.getenv("CONFIG_PATH", "api_config/api_config.json")
        with open(self.path, "r") as f:
            self.config = json.load(f)

    def get_api_config(self):
        return self.config.get("api", {})
    
    
    