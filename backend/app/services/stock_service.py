import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from ..models.database import DatabaseOperations
from .technical_analysis import TechnicalAnalysis
from .ml_service import MLService

class StockService:
    def __init__(self):
        self.ticker = "TSLA"
        self.stock = yf.Ticker(self.ticker)
        self.db = DatabaseOperations()
        self.technical_analysis = TechnicalAnalysis()
        self.ml_service = MLService()

    async def get_current_price(self) -> Dict:
        """Get current stock price and basic info"""
        info = self.stock.info
        return {
            "price": info.get("currentPrice"),
            "change": info.get("regularMarketChangePercent"),
            "volume": info.get("regularMarketVolume"),
            "market_cap": info.get("marketCap"),
            "timestamp": datetime.now().isoformat()
        }

    async def get_historical_data(
        self,
        period: str = "1y",
        interval: str = "1d"
    ) -> pd.DataFrame:
        """Get historical stock data"""
        hist = self.stock.history(period=period, interval=interval)
        hist = hist.reset_index()
        
        # Save to database
        for _, row in hist.iterrows():
            self.db.save_stock_data({
                'date': row['Date'],
                'open': row['Open'],
                'high': row['High'],
                'low': row['Low'],
                'close': row['Close'],
                'volume': row['Volume']
            })
        
        return hist

    async def calculate_metrics(self, data: pd.DataFrame) -> Dict:
        """Calculate various financial metrics"""
        returns = data['Close'].pct_change()
        
        # Calculate technical indicators
        rsi = self.technical_analysis.calculate_rsi(data['Close'])
        macd, signal, hist = self.technical_analysis.calculate_macd(data['Close'])
        bb_upper, bb_middle, bb_lower = self.technical_analysis.calculate_bollinger_bands(data['Close'])
        
        # Calculate statistical metrics
        stats_metrics = self.technical_analysis.calculate_statistical_metrics(data['Close'])
        
        # Calculate volatility metrics
        vol_metrics = self.technical_analysis.calculate_volatility_metrics(data['Close'])
        
        # Calculate market regime
        regime = self.technical_analysis.calculate_market_regime(data['Close'])
        
        # Save all metrics to database
        for date, row in data.iterrows():
            self.db.save_technical_indicators({
                'date': date,
                'rsi': rsi[date],
                'macd': macd[date],
                'macd_signal': signal[date],
                'macd_histogram': hist[date],
                'bb_upper': bb_upper[date],
                'bb_middle': bb_middle[date],
                'bb_lower': bb_lower[date]
            })
            
            self.db.save_statistical_metrics({
                'date': date,
                **stats_metrics
            })
            
            self.db.save_volatility_metrics({
                'date': date,
                **vol_metrics
            })
            
            self.db.save_market_regime({
                'date': date,
                'regime': regime[date],
                'z_score': (returns[date] - returns.mean()) / returns.std()
            })
        
        return {
            'technical_indicators': {
                'rsi': rsi.to_dict(),
                'macd': macd.to_dict(),
                'macd_signal': signal.to_dict(),
                'macd_histogram': hist.to_dict(),
                'bollinger_bands': {
                    'upper': bb_upper.to_dict(),
                    'middle': bb_middle.to_dict(),
                    'lower': bb_lower.to_dict()
                }
            },
            'statistical_metrics': stats_metrics,
            'volatility_metrics': vol_metrics,
            'market_regime': regime.to_dict()
        }

    async def run_monte_carlo(
        self,
        days: int = 252,
        simulations: int = 1000
    ) -> Dict:
        """Run Monte Carlo simulation"""
        hist_data = await self.get_historical_data(period="1y")
        returns = hist_data['Close'].pct_change().dropna()
        
        mu = returns.mean()
        sigma = returns.std()
        last_price = hist_data['Close'].iloc[-1]
        
        # Generate simulations
        dt = 1/days
        simulation_matrix = np.zeros((days, simulations))
        simulation_matrix[0] = last_price
        
        for t in range(1, days):
            random_shocks = np.random.normal(0, 1, simulations)
            simulation_matrix[t] = simulation_matrix[t-1] * np.exp(
                (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * random_shocks
            )
        
        result = {
            "simulations": simulation_matrix.tolist(),
            "mean_path": simulation_matrix.mean(axis=1).tolist(),
            "confidence_interval_95": {
                "upper": np.percentile(simulation_matrix, 97.5, axis=1).tolist(),
                "lower": np.percentile(simulation_matrix, 2.5, axis=1).tolist()
            }
        }
        
        # Save simulation results to database
        self.db.save_monte_carlo_simulation({
            'date': datetime.now(),
            'simulation_date': datetime.now() + timedelta(days=days),
            'mean_path': result['mean_path'],
            'upper_bound': result['confidence_interval_95']['upper'],
            'lower_bound': result['confidence_interval_95']['lower'],
            'confidence_interval': 0.95
        })
        
        return result

    async def get_historical_analysis(self, start_date: datetime, end_date: datetime) -> Dict:
        """Get historical analysis data from database"""
        return {
            'technical_indicators': self.db.get_data_by_date_range(
                self.db.TechnicalIndicators, start_date, end_date
            ),
            'statistical_metrics': self.db.get_data_by_date_range(
                self.db.StatisticalMetrics, start_date, end_date
            ),
            'volatility_metrics': self.db.get_data_by_date_range(
                self.db.VolatilityMetrics, start_date, end_date
            ),
            'market_regime': self.db.get_data_by_date_range(
                self.db.MarketRegime, start_date, end_date
            )
        }

    async def train_ml_models(self, period: str = "2y") -> Dict:
        """Train machine learning models"""
        try:
            data = await self.get_historical_data(period=period)
            results = self.ml_service.train_models(data)
            return results
        except Exception as e:
            raise Exception(f"Error training ML models: {str(e)}")

    async def get_ml_predictions(self) -> Dict:
        """Get next day price predictions from ML models"""
        try:
            data = await self.get_historical_data(period="1y")
            predictions = self.ml_service.predict_next_day(data)
            return predictions
        except Exception as e:
            raise Exception(f"Error getting ML predictions: {str(e)}")

    async def get_combined_analysis(self) -> Dict:
        """Get combined analysis including ML predictions"""
        try:
            current_price = await self.get_current_price()
            historical_data = await self.get_historical_data(period="1y")
            metrics = await self.calculate_metrics(historical_data)
            ml_predictions = await self.get_ml_predictions()
            monte_carlo = await self.run_monte_carlo()

            return {
                "current_price": current_price,
                "technical_analysis": metrics['technical_indicators'],
                "statistical_metrics": metrics['statistical_metrics'],
                "volatility_metrics": metrics['volatility_metrics'],
                "market_regime": metrics['market_regime'],
                "ml_predictions": ml_predictions,
                "monte_carlo": monte_carlo
            }
        except Exception as e:
            raise Exception(f"Error getting combined analysis: {str(e)}") 