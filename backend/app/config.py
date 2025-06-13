import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/tesla_stock.db")

# API configuration
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")  # Use demo key if not provided
API_BASE_URL = "https://www.alphavantage.co/query"

# Stock configuration
STOCK_SYMBOL = "TSLA"
MARKET = "NASDAQ"

# Analysis configuration
MONTE_CARLO_SIMULATIONS = 1000
PREDICTION_DAYS = 30
TRAINING_DAYS = 365

# Technical analysis parameters
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BOLLINGER_PERIOD = 20
BOLLINGER_STD = 2

# Volatility parameters
VOLATILITY_WINDOW = 252  # Trading days in a year
PARKINSON_WINDOW = 20
GK_WINDOW = 20

# Machine learning parameters
ML_TRAINING_SPLIT = 0.8
ML_FEATURES = [
    "close",
    "volume",
    "rsi",
    "macd",
    "bollinger_upper",
    "bollinger_lower",
    "volatility"
]

# CORS configuration
CORS_ORIGINS = [
    "http://localhost:3000",
    "https://tesla-analysis.vercel.app",
    os.getenv("FRONTEND_URL", "")
]

# Cache configuration
CACHE_EXPIRY = 3600  # 1 hour in seconds 