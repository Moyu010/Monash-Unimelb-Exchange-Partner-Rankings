from abc import abstractmethod, ABC
import requests
from bs4 import BeautifulSoup


class SupportedUniversity(ABC):
    def __init__(self, url=""):
        self.url = url
        self._soup = self._get_soup()

    def _get_soup(self):
        web_page = requests.get(self.url).text
        return BeautifulSoup(web_page, 'lxml')

    @abstractmethod
    def get_exchange_info(self):
        pass
