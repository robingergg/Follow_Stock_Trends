import uvicorn
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Response
import json
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
async def get_stock_data(symbol: str, time_series: str, use_mock: bool = True) -> Dict[str, str]:
    """
    This endpoint is used to get the stock data for a given symbol and time series.
    Example call: 'http://localhost:8000/stock/IBM?time_series=monthly&use_mock=true'
    """

    time_series_callback = None
    data = None
    try:
        # Collect data
        processor = StockDataProcessor()

        # TODO: create a look-up table for retrieving time_series value dynamically
        if time_series == "monthly":
            time_series_callback = processor.get_monthly_returns
        elif time_series == "weekly":
            time_series_callback = processor.get_weekly_returns
        elif time_series == "daily":
            time_series_callback = processor.get_daily_returns
        else:
            raise ValueError(f"Invalid time series: {time_series}")

        if time_series_callback:
            data = time_series_callback(symbol, use_mock=use_mock)
        else:
            raise ValueError(f"Invalid time series: {time_series}")

        if not data:
            raise ValueError("Unexpected error: No data returned")

        response = Response(content=json.dumps(data), media_type="application/json")
        # NOTE: adding headers for CORS as it seems that add_middle doesnt properly allows all origin
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    # TODO: create more detaled error(s)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    # get_stock_data("IBM", "monthly", use_mock=True)
