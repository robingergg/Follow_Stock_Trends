"""
This module is responsible for collecting data from the Alpha Vantage API.
"""


import os
import json
import pprint
import requests
from enum import Enum
from typing import Union
from ast import literal_eval
from dotenv import load_dotenv
from requests.exceptions import JSONDecodeError


load_dotenv()


class CollectorBase:
    """
    This class is responsible for containing the base class for all collectors.

    NOTE: This is made for future development opstions for multiper API support.
    """
    def __init__(self, api_key: str, base_url: str, collector_type: str):
        self.api_key = None
        self.base_url = None
        self.collector_type = None

    def _my_type(self) -> str:
        """
        This method is responsible for returning the collector type.
        """
        return self.collector_type
    
    def make_request(self, endpoint: str, method: str, mock: str = None) -> dict:
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
                print("DEBUG: Mock data used.")
                response = self._mock_data(mock)
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
        
    

class DataCollector(CollectorBase):
    """
    This class is responsible for containing different types of data collector classes.
    """
    def __init__(self, collector_type: str):
        """
        collector_type: str - The type of collector to get. It can be "stock", "crypto", or "commodity".
        """
        self.data_collector = self._get_collector(collector_type)

    def what_collector(self) -> str:
        """
        This method is responsible for returning the collector type.
        Help identify the type of collector. This migth be useful in case of many collector types.
        """
        return self.data_collector._my_type()

    def _get_collector(self, collector_type: str) -> Union['DataCollector.StockDataCollector', \
                                                           'DataCollector.CryptoDataCollector', \
                                                            'DataCollector.CommodityDataCollector']:
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


    class StockDataCollector(CollectorBase):
        """
        This class is responsible for collecting data from the Alpha Vantage API for stocks.
        """
        def __init__(self):
            self.api_key = os.getenv("ALPHAVANTAGE_API_KEY")
            self.base_url = "https://www.alphavantage.co/query"
            self.collector_type = DataCollector.DataCollectionType.STOCK
            self.daily_endpoint = "{base}?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={key}".format(base=self.base_url, symbol="{}", key=self.api_key)
            self.weekly_endpoint = "{base}?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={key}".format(base=self.base_url, symbol="{}", key=self.api_key)
            self.monthly_endpoint = "{base}?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={key}".format(base=self.base_url, symbol="{}", key=self.api_key)

        def _mock_data(self, mock: str) -> dict:
            """
            mock: str - The mock data to use. It is the path to the mock data file, eg: "Monthly_data.txt"
            """
            exmp_req_data = None
            with open(f"{mock}", "r") as f:
                exmp_req_data = f.read()
                proper_string = literal_eval(f"'{exmp_req_data}'")
            proper_string = json.loads(proper_string.encode("utf-8"))
            return proper_string

        def get_daily_data(self, symbol: str, method: str = "GET", mock: str = None) -> dict:
            """
            This method is responsible for getting the daily data for a given symbol.

            Params:
                symbol: str - The symbol of the stock to get the data for.

            Returns:
                dict - The daily data for the given symbol.
            """
            endpoint = self.daily_endpoint.format(symbol)
            return self.make_request(endpoint, method, mock)
        
        def get_weekly_data(self, symbol: str, method: str = "GET", mock: str = None) -> dict:
            """
            This method is responsible for getting the weekly data for a given symbol.
            """
            endpoint = self.weekly_endpoint.format(symbol)
            return self.make_request(endpoint, method, mock)
        
        def get_monthly_data(self, symbol: str, method: str = "GET", mock: str = None) -> dict:
            """
            This method is responsible for getting the monthly data for a given symbol.
            """
            endpoint = self.monthly_endpoint.format(symbol)
            return self.make_request(endpoint, method, mock)


if __name__ == "__main__":
    import itertools
    # pprint.pprint(DataCollector("stock").data_collector.get_daily_data("IBM"))
    data = DataCollector("stock").data_collector.get_daily_data("IBM")
    first_n = dict(itertools.islice(data['Monthly Time Series'].items(), 10))
    pprint.pprint(first_n)
