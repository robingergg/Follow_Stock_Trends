import pandas as pd
from enum import Enum

# Add paths to PYTHONPATH here temporarly
# When using Docker, it will be added automatically
import sys
sys.path.append("service_modules")

from data_collector import DataCollector


class DataProcessorBase:
    def __init__(self):
        self.data_processor = None

    def calc_returns(self):
        pass


class StockDataProcessor(DataProcessorBase):

    class TimeSeries(Enum):
        DAILY = "daily"
        WEEKLY = "weekly"
        MONTHLY = "monthly"

    def __init__(self):
        self.data = None
        self.collector = DataCollector("stock")
        self.data_processor_type = self.collector.what_collector()
        # TODO: Figure out how to make this dynamic
        self.monthly_series = "Monthly Time Series"
        self.weekly_series = "Weekly Time Series"
        self.daily_series = "Time Series (Daily)"

    def _get_time_series_data(self, time_series: str, symbol: str, mock: str = None):
        if time_series == StockDataProcessor.TimeSeries.DAILY:
            self.data = self.collector.data_collector.get_daily_data(symbol)
        elif time_series == StockDataProcessor.TimeSeries.WEEKLY:
            self.data = self.collector.data_collector.get_weekly_data(symbol)
        elif time_series == StockDataProcessor.TimeSeries.MONTHLY:
            self.data = self.collector.data_collector.get_monthly_data(symbol, mock=mock)
        else:
            raise ValueError(f"Invalid time series: {time_series}")
        
        return self.data
    
    def get_monthly_returns(self, symbol: str, use_mock: bool = False, display_cli: bool = False) -> dict:
        mock = None
        if use_mock:
            mock = "mock_data/Monthly_data.txt"
        self.data = self._get_time_series_data(StockDataProcessor.TimeSeries.MONTHLY, symbol, mock)

        df = pd.DataFrame(self.data[self.monthly_series]).T.astype(float)
        df = df.sort_index()
        df["Monthly Return (%)"] = df["4. close"].pct_change() * 100
        if display_cli:
            print(df)
        return self.data
    
    # TODO: add weekly and daily returns
            

if __name__ == "__main__":
    stock_data_processor = StockDataProcessor()
    stock_data_processor.get_monthly_returns("IBM", use_mock=True)