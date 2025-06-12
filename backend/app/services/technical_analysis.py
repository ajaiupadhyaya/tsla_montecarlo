import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

class TechnicalAnalysis:
    @staticmethod
    def calculate_rsi(data: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    @staticmethod
    def calculate_macd(data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        exp1 = data.ewm(span=fast, adjust=False).mean()
        exp2 = data.ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        return macd, signal_line, histogram

    @staticmethod
    def calculate_bollinger_bands(data: pd.Series, period: int = 20, std_dev: float = 2.0) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate Bollinger Bands"""
        middle_band = data.rolling(window=period).mean()
        std = data.rolling(window=period).std()
        upper_band = middle_band + (std * std_dev)
        lower_band = middle_band - (std * std_dev)
        return upper_band, middle_band, lower_band

    @staticmethod
    def calculate_fibonacci_retracement(high: float, low: float) -> Dict[str, float]:
        """Calculate Fibonacci Retracement Levels"""
        diff = high - low
        return {
            '0.0': low,
            '0.236': low + 0.236 * diff,
            '0.382': low + 0.382 * diff,
            '0.5': low + 0.5 * diff,
            '0.618': low + 0.618 * diff,
            '0.786': low + 0.786 * diff,
            '1.0': high
        }

    @staticmethod
    def calculate_statistical_metrics(data: pd.Series) -> Dict:
        """Calculate advanced statistical metrics"""
        returns = data.pct_change().dropna()
        
        metrics = {
            'mean': returns.mean(),
            'std': returns.std(),
            'skewness': stats.skew(returns),
            'kurtosis': stats.kurtosis(returns),
            'jarque_bera': stats.jarque_bera(returns),
            'sharpe_ratio': (returns.mean() * 252) / (returns.std() * np.sqrt(252)),
            'sortino_ratio': (returns.mean() * 252) / (returns[returns < 0].std() * np.sqrt(252)),
            'var_95': np.percentile(returns, 5),
            'cvar_95': returns[returns <= np.percentile(returns, 5)].mean(),
            'max_drawdown': (data / data.cummax() - 1).min(),
            'calmar_ratio': (returns.mean() * 252) / abs((data / data.cummax() - 1).min())
        }
        return metrics

    @staticmethod
    def calculate_volatility_metrics(data: pd.Series, window: int = 20) -> Dict:
        """Calculate various volatility metrics"""
        returns = data.pct_change().dropna()
        
        # Historical Volatility
        hist_vol = returns.rolling(window=window).std() * np.sqrt(252)
        
        # Parkinson Volatility (High-Low Range)
        high_low_range = np.log(data / data.shift(1))
        park_vol = np.sqrt(1 / (4 * window * np.log(2)) * 
                          (high_low_range ** 2).rolling(window=window).sum()) * np.sqrt(252)
        
        # Garman-Klass Volatility
        log_hl = np.log(data / data.shift(1))
        log_co = np.log(data / data.shift(1))
        gk_vol = np.sqrt(0.5 * log_hl**2 - (2*np.log(2)-1) * log_co**2)
        gk_vol = gk_vol.rolling(window=window).mean() * np.sqrt(252)
        
        return {
            'historical_volatility': hist_vol,
            'parkinson_volatility': park_vol,
            'garman_klass_volatility': gk_vol
        }

    @staticmethod
    def calculate_market_regime(data: pd.Series, window: int = 20) -> pd.Series:
        """Detect market regime using rolling statistics"""
        returns = data.pct_change().dropna()
        
        # Calculate rolling mean and std
        rolling_mean = returns.rolling(window=window).mean()
        rolling_std = returns.rolling(window=window).std()
        
        # Define regimes based on z-score
        z_score = (returns - rolling_mean) / rolling_std
        
        regime = pd.Series(index=returns.index)
        regime[z_score > 2] = 'high_volatility_bull'
        regime[z_score < -2] = 'high_volatility_bear'
        regime[(z_score >= -0.5) & (z_score <= 0.5)] = 'low_volatility'
        regime[(z_score > 0.5) & (z_score <= 2)] = 'bull'
        regime[(z_score < -0.5) & (z_score >= -2)] = 'bear'
        
        return regime

    @staticmethod
    def calculate_correlation_analysis(data: pd.DataFrame, other_assets: pd.DataFrame) -> Dict:
        """Calculate correlation analysis with other assets"""
        returns = data.pct_change().dropna()
        other_returns = other_assets.pct_change().dropna()
        
        # Calculate correlation matrix
        corr_matrix = returns.corrwith(other_returns)
        
        # Calculate rolling correlation
        rolling_corr = returns.rolling(window=20).corr(other_returns)
        
        return {
            'correlation_matrix': corr_matrix.to_dict(),
            'rolling_correlation': rolling_corr.to_dict()
        } 