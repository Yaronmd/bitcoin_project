import pandas as pd
import matplotlib.pyplot as plt
import os
from helper.logger_helper import logger

class PlotGenerator:
    def __init__(self, output_dir="result"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_price_plot(self, json_lines_path: str, output_filename="btc_price_plot.png"):
        try:

            df = pd.read_json(json_lines_path, lines=True)

            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df["price"] = pd.to_numeric(df["price"])

            df = df.sort_values("timestamp")

            plt.figure(figsize=(10, 5))
            plt.plot(df["timestamp"], df["price"], marker="o", linestyle="-", color="blue")

            plt.title("BTC Price Over Time")
            plt.xlabel("Time")
            plt.ylabel("Price (USD)")
            plt.grid(True)
            plt.tight_layout()

            output_path = os.path.join(self.output_dir, output_filename)
            plt.savefig(output_path)
            plt.close()
            logger.info(f"Plot saved to {output_path}")

        except Exception as e:
            logger.error(f"Failed to generate plot: {e}")
