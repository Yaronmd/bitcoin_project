from api.api_client import APIClient
from helper.config_loader import ConfigLoader
from helper.logger_helper import logger

def test_api_data():
    config = ConfigLoader().get_api_config()
    base_url = config["base_url"]
    headers = config.get("default_headers", {})
    get_bitcoin_price_usd = config.get("get_bitcoin_price_usd")
    client = APIClient(base_url=base_url,default_headers=headers)

    response = client.get(endpoint=get_bitcoin_price_usd)
    assert response.status == 200

    data = response.json()
    logger.info(f"data: {data['data']}")
    
    # validate strcture
    assert "data" in data
    price_data = data["data"]
    assert all(k in price_data for k in ["amount", "base", "currency"])
    
    # validate values
    assert float(price_data['amount']) >= 0
    assert price_data["base"] == "BTC"
    assert price_data["currency"] == "USD"
    

    client.close()