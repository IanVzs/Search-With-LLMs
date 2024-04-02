import requests
from loguru import logger


class SearchBase:

    def __init__(self):
        self.alive = self.ping()

    def ping(self):
        try:
            requests.get(self.endpoint, headers=self.headers)
            logger.info(f"{self.__class__.__name__} [√]")
            return True
        except Exception as err:
            logger.warning(f"{self.__class__.__name__} [x]")
            return False

