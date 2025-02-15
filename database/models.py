from datetime import date
from pydantic import BaseModel
from database.database import Base
from sqlalchemy import Column, Integer, String, Numeric, Date

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), index=True)
    date = Column(Date)
    time_series = Column(String(10))
    open = Column(Numeric)
    high = Column(Numeric)
    low = Column(Numeric)
    close = Column(Numeric)
    volume = Column(Integer)

class StockSchema(BaseModel):
    id: int
    symbol: str
    date: date
    time_series: str
    open: float
    high: float
    low: float
    close: float
    volume: int

    class Config:
        from_attributes = True  # Allows conversion from ORM models