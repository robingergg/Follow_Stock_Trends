import uvicorn
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from service_modules.data_processor import StockDataProcessor


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Stock Data API"}

@app.get("/stock/{symbol}")
async def get_stock_data(symbol: str, time_series: str, use_mock: bool = True) -> Dict[str, Any]:
    """
    This endpoint is used to get the stock data for a given symbol and time series.
    Example call: 'http://localhost:8000/stock/IBM?time_series=monthly&use_mock=true'
    """
    try:
        # Collect data
        processor = StockDataProcessor()

        # TODO: create a look-up table for retrieving time_series vlaue dynamically
        if time_series == "monthly":
            data = processor.get_monthly_returns(symbol, use_mock=use_mock)
            return data

    # TODO: create more detaled error(s)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    # get_stock_data("IBM", "monthly", use_mock=True)
