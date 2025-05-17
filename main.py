
from datetime import datetime, timedelta, timezone
import os
import time
from dotenv import load_dotenv
import pandas as pd

from api.api_client import APIClient
from helper.config_loader import ConfigLoader
from helper.email_sender import EmailSender
from helper.data_fetcher import DataFetcher
from helper.logger_helper import logger
from helper.plot_geneartor import PlotGenerator


def send_email(plot_path:str):
    
    load_dotenv("config/.env")
    email_sender = os.getenv("EMAIL_SENDER")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_receiver = os.getenv("EMAIL_RECEIVER")
    
    if not email_sender or not email_password or not email_receiver:
        raise ValueError("Missing email configuration. Please check your .env file.")

    email_password = email_password.replace(" ", "")
    email_sender = EmailSender(email_sender,email_password,email_receiver)
    

    email_sender.send_email_with_attachment("Bitcoin automation",get_max_bitcoin(),plot_path)


def fetch_and_save(output_file:str):
    config = ConfigLoader().get_api_config()
    base_url = config["base_url"]
    headers = config.get("default_headers", {}) 
    client = APIClient(base_url=base_url,default_headers=headers)
    
    data_featcher = DataFetcher(client=client,output_file=output_file,endpoint="/v2/prices/BTC-USD/spot")
    
    
    data_featcher.fetch_and_save()
    client.close()
    
def clear_file(path: str):
    open(path, "w").close()
    logger.info(f"Cleared file content: {path}")
    
    
def save_plot(output_dir:str,json_path):
    plot_generator = PlotGenerator(output_dir)
    plot_generator.generate_price_plot(json_lines_path=json_path)
    
def get_max_bitcoin(json_lines_path):
       
    try:

        df = pd.read_json(json_lines_path, lines=True)
        if "price" not in df.columns or "timestamp" not in df.columns:
            logger.error("Missing 'price' or 'timestamp' columns.")
            return None

        # המרה לסוגים מתאימים
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

        df = df.dropna(subset=["price", "timestamp"])

        max_row = df.loc[df["price"].idxmax()]

        logger.info(f"Max BTC price: {max_row['price']} at {max_row['timestamp']}")
        return f"Max price: {float(max_row["price"])} at {max_row["timestamp"].isoformat()}"

    except Exception as e:
        logger.error(f"Failed to parse JSON or compute max price: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to catch json {e}")
        
            
if __name__ == "__main__":
    logger.info("Bitcoin automation started")

    last_email_sent = datetime.now(timezone.utc)
    one_hour = timedelta(hours=1)
    result_dir = "result"
    os.makedirs(result_dir, exist_ok=True)
    file_path = f"{result_dir}/data.json"
    
    clear_file(file_path)
    try:
        while True:
            fetch_and_save(file_path)

            # Check if one hour has passed
            if datetime.now(timezone.utc) - last_email_sent >= one_hour:
                save_plot(output_dir=result_dir,json_path=file_path)
                send_email(file_path)
                clear_file(file_path)
                last_email_sent = datetime.now(timezone.utc)

            time.sleep(60)  # wait 1 minute before next fetch
    except KeyboardInterrupt:
        logger.info("Stopped by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    
    
    