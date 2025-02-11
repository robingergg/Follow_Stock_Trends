"""
This module is responsible for collecting data from the Alpha Vantage API.
"""


import os
import json
import pprint
import requests
from enum import Enum
from ast import literal_eval
from dotenv import load_dotenv
from requests.exceptions import JSONDecodeError


load_dotenv()


class DataCollector:
    """
    This class is responsible for containing different types of data collector classes.
    """
    def __init__(self, collector_type: str):
        """
        collector_type: str - The type of collector to get. It can be "stock", "crypto", or "commodity".
        """
        self.data_collector = self._get_collector(collector_type)

    def _get_collector(self, collector_type: str):
        """
        This method is responsible for getting the collector type.
        NOTE: This is made for future development opstions.

        Params:
            collector_type: str - The type of collector to get.

        Returns:
            DataCollector - The collector type.
        """
        collector_type = DataCollector.DataCollectionType(collector_type)
        if collector_type == DataCollector.DataCollectionType.STOCK:
            return self.StockDataCollector()
        elif collector_type == DataCollector.DataCollectionType.CRYPTO:
            raise NotImplementedError("Crypto collector not implemented")
        elif collector_type == DataCollector.DataCollectionType.COMMODITY:
            raise NotImplementedError("Commodity collector not implemented")
        else:
            raise ValueError(f"Unsupported collector type: {collector_type}")


    class DataCollectionType(Enum):
        """
        NOTE: This is made for future development opstions.
        """
        STOCK = "stock"
        CRYPTO = "crypto"
        COMMODITY = "commodity"


    class StockDataCollector:
        """
        This class is responsible for collecting data from the Alpha Vantage API for stocks.
        """
        def __init__(self):
            self.api_key = os.getenv("ALPHAVANTAGE_API_KEY")
            self.base_url = "https://www.alphavantage.co/query"
            self.daily_endpoint = "{base}?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={key}".format(base=self.base_url, symbol="{}", key=self.api_key)
            self.daily_endpoint = "{base}?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={key}".format(base=self.base_url, symbol="{}", key=self.api_key)
            self.daily_endpoint = "{base}?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={key}".format(base=self.base_url, symbol="{}", key=self.api_key)

        def _mock_data(self) -> dict:
            exmp_req_data = None
            with open("exmp_binary_data.txt", "r") as f:
                exmp_req_data = f.read()
                proper_string = literal_eval(f"'{exmp_req_data}'")
            proper_string = json.loads(proper_string.encode("utf-8"))
            return proper_string

        def make_request(self, endpoint: str, method: str, mock: bool = True) -> dict:
            """
            This method is responsible for making a request to the Alpha Vantage API.

            Params:
                endpoint: str - The endpoint to make the request to.
                method: str - The method to make the request with. NOTE: This is made for future development opstions.
                mock: bool - Whether to use the mock data.

            Returns:
                dict - The response from the request.
            """
            response = None

            try:
                if mock:
                    response = self._mock_data()
                    return response
                else:
                    response = requests.request(method, endpoint)
                    # response = requests.get(endpoint)
                    return response.json()
            except JSONDecodeError as e:
                raise JSONDecodeError(e)
            except requests.RequestException as e:
                raise requests.RequestException(e)
            except Exception as e:
                raise Exception(f"Unexpected error: {e}")

        def get_daily_data(self, symbol: str, method: str = "GET") -> dict:
            """
            This method is responsible for getting the daily data for a given symbol.

            Params:
                symbol: str - The symbol of the stock to get the data for.

            Returns:
                dict - The daily data for the given symbol.
            """
            endpoint = self.daily_endpoint.format(symbol)
            return self.make_request(endpoint, method)


pprint.pprint(DataCollector("stock").data_collector.get_daily_data("IBM"))
