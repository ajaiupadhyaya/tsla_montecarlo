"""
Data loading and preprocessing module for the quantitative finance framework.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import yfinance as yf
from datetime import datetime, timedelta

from ..config import Config
from ..utils.logging import get_logger

logger = get_logger(__name__)

class DataLoader:
    """Base class for loading and preprocessing financial data."""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the data loader.
        
        Args:
            config: Optional configuration instance. If None, creates new instance.
        """
        self.config = config or Config()
        self.cache_dir = Path(self.config.get("data_sources.yahoo_finance.cache_dir", "data/cache"))
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def load_stock_data(
        self,
        tickers: Union[str, List[str]],
        start_date: Optional[Union[str, datetime]] = None,
        end_date: Optional[Union[str, datetime]] = None,
        interval: str = "1d",
        use_cache: bool = True
    ) -> pd.DataFrame:
        """
        Load stock data from Yahoo Finance.
        
        Args:
            tickers: Single ticker or list of tickers
            start_date: Start date for data
            end_date: End date for data
            interval: Data interval (1d, 1h, etc.)
            use_cache: Whether to use cached data
            
        Returns:
            pd.DataFrame: Stock data with MultiIndex (ticker, date)
        """
        if isinstance(tickers, str):
            tickers = [tickers]
        
        if end_date is None:
            end_date = datetime.now()
        if start_date is None:
            start_date = end_date - timedelta(days=365)
        
        # Convert dates to datetime
        if isinstance(start_date, str):
            start_date = pd.to_datetime(start_date)
        if isinstance(end_date, str):
            end_date = pd.to_datetime(end_date)
        
        data = {}
        for ticker in tickers:
            cache_file = self.cache_dir / f"{ticker}_{interval}_{start_date.date()}_{end_date.date()}.parquet"
            
            if use_cache and cache_file.exists():
                logger.info(f"Loading cached data for {ticker}")
                ticker_data = pd.read_parquet(cache_file)
            else:
                logger.info(f"Downloading data for {ticker}")
                ticker_data = yf.download(
                    ticker,
                    start=start_date,
                    end=end_date,
                    interval=interval,
                    progress=False
                )
                
                if use_cache:
                    ticker_data.to_parquet(cache_file)
            
            data[ticker] = ticker_data
        
        # Combine all tickers into one DataFrame
        combined_data = pd.concat(
            data,
            axis=0,
            names=["ticker", "date"]
        )
        
        return combined_data
    
    def preprocess_data(
        self,
        data: pd.DataFrame,
        features: Optional[List[str]] = None,
        target: Optional[str] = None,
        fill_method: str = "ffill",
        normalize: bool = True
    ) -> pd.DataFrame:
        """
        Preprocess the data for model training.
        
        Args:
            data: Input DataFrame
            features: List of feature columns to use
            target: Target column for prediction
            fill_method: Method to fill missing values
            normalize: Whether to normalize the data
            
        Returns:
            pd.DataFrame: Preprocessed data
        """
        # Make a copy to avoid modifying original data
        df = data.copy()
        
        # Fill missing values
        df = df.fillna(method=fill_method)
        
        # Select features
        if features is not None:
            df = df[features]
        
        # Normalize data
        if normalize:
            df = (df - df.mean()) / df.std()
        
        return df
    
    def create_technical_indicators(
        self,
        data: pd.DataFrame,
        indicators: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Create technical indicators from price data.
        
        Args:
            data: Price data DataFrame
            indicators: List of indicators to create
            
        Returns:
            pd.DataFrame: Data with technical indicators
        """
        if indicators is None:
            indicators = self.config.get("feature_engineering.technical_indicators.indicators", [])
        
        df = data.copy()
        
        for indicator in indicators:
            name = indicator["name"]
            params = indicator.get("params", {})
            
            if name == "RSI":
                period = params.get("period", 14)
                delta = df["Close"].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
                rs = gain / loss
                df[f"RSI_{period}"] = 100 - (100 / (1 + rs))
            
            elif name == "MACD":
                fast_period = params.get("fast_period", 12)
                slow_period = params.get("slow_period", 26)
                signal_period = params.get("signal_period", 9)
                
                exp1 = df["Close"].ewm(span=fast_period, adjust=False).mean()
                exp2 = df["Close"].ewm(span=slow_period, adjust=False).mean()
                macd = exp1 - exp2
                signal = macd.ewm(span=signal_period, adjust=False).mean()
                
                df[f"MACD_{fast_period}_{slow_period}"] = macd
                df[f"MACD_Signal_{fast_period}_{slow_period}"] = signal
                df[f"MACD_Hist_{fast_period}_{slow_period}"] = macd - signal
            
            elif name == "BollingerBands":
                period = params.get("period", 20)
                std_dev = params.get("std_dev", 2)
                
                df[f"BB_Middle_{period}"] = df["Close"].rolling(window=period).mean()
                std = df["Close"].rolling(window=period).std()
                df[f"BB_Upper_{period}"] = df[f"BB_Middle_{period}"] + (std * std_dev)
                df[f"BB_Lower_{period}"] = df[f"BB_Middle_{period}"] - (std * std_dev)
        
        return df
    
    def create_statistical_features(
        self,
        data: pd.DataFrame,
        features: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Create statistical features from price data.
        
        Args:
            data: Price data DataFrame
            features: List of features to create
            
        Returns:
            pd.DataFrame: Data with statistical features
        """
        if features is None:
            features = self.config.get("feature_engineering.statistical_features.features", [])
        
        df = data.copy()
        
        for feature in features:
            name = feature["name"]
            params = feature.get("params", {})
            
            if name == "returns":
                periods = params.get("periods", [1, 5, 10, 20])
                for period in periods:
                    df[f"Return_{period}d"] = df["Close"].pct_change(periods=period)
            
            elif name == "volatility":
                window = params.get("window", 20)
                df[f"Volatility_{window}d"] = df["Close"].pct_change().rolling(window=window).std()
            
            elif name == "momentum":
                periods = params.get("periods", [5, 10, 20])
                for period in periods:
                    df[f"Momentum_{period}d"] = df["Close"] / df["Close"].shift(period) - 1
        
        return df 