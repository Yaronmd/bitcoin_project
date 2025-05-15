from playwright.sync_api import sync_playwright,APIResponse

from helper.logger_helper import logger
class APIClient:
    
    def __init__(self,base_url:str,default_headers:str):
        self.base_url = base_url
        self.default_headers = default_headers
        self.playwright = sync_playwright().start()
        self.request_context = self.playwright.request.new_context(base_url=self.base_url,extra_http_headers=self.default_headers)
        
    def get(self, endpoint: str, params: dict = None, headers: dict = None):
        
        if params is not None and not isinstance(params, dict):
            error_message = "Expected 'params' to be a dictionary or None."
            logger.error(error_message)
            raise TypeError(error_message)
        if headers is not None and not isinstance(headers, dict):
            error_message = "Expected 'headers' to be a dictionary or None."
            logger.error(error_message)
            raise TypeError(error_message)
        
        url = f"{self.base_url}{endpoint}"
        logger.debug(f"url: {url}")
        response = self.request_context.get(url, params=params, headers=headers)
        logger.debug(f"response: {response}")
        return response

    def close(self):
        logger.debug("request and api client closed")
        self.request_context.dispose()
        self.playwright.stop()
        
    
        