from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class StockData(Base):
    __tablename__ = 'stock_data'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class TechnicalIndicators(Base):
    __tablename__ = 'technical_indicators'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    rsi = Column(Float)
    macd = Column(Float)
    macd_signal = Column(Float)
    macd_histogram = Column(Float)
    bb_upper = Column(Float)
    bb_middle = Column(Float)
    bb_lower = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class StatisticalMetrics(Base):
    __tablename__ = 'statistical_metrics'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    mean = Column(Float)
    std = Column(Float)
    skewness = Column(Float)
    kurtosis = Column(Float)
    sharpe_ratio = Column(Float)
    sortino_ratio = Column(Float)
    var_95 = Column(Float)
    cvar_95 = Column(Float)
    max_drawdown = Column(Float)
    calmar_ratio = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class VolatilityMetrics(Base):
    __tablename__ = 'volatility_metrics'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    historical_volatility = Column(Float)
    parkinson_volatility = Column(Float)
    garman_klass_volatility = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class MarketRegime(Base):
    __tablename__ = 'market_regime'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    regime = Column(String)
    z_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class MonteCarloSimulation(Base):
    __tablename__ = 'monte_carlo_simulation'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    simulation_date = Column(DateTime, nullable=False)
    mean_path = Column(JSON)
    upper_bound = Column(JSON)
    lower_bound = Column(JSON)
    confidence_interval = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database connection
def get_db_connection():
    engine = create_engine('sqlite:///tesla_analysis.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

# Database operations
class DatabaseOperations:
    def __init__(self):
        self.session = get_db_connection()

    def save_stock_data(self, data: dict):
        stock_data = StockData(**data)
        self.session.add(stock_data)
        self.session.commit()

    def save_technical_indicators(self, data: dict):
        indicators = TechnicalIndicators(**data)
        self.session.add(indicators)
        self.session.commit()

    def save_statistical_metrics(self, data: dict):
        metrics = StatisticalMetrics(**data)
        self.session.add(metrics)
        self.session.commit()

    def save_volatility_metrics(self, data: dict):
        metrics = VolatilityMetrics(**data)
        self.session.add(metrics)
        self.session.commit()

    def save_market_regime(self, data: dict):
        regime = MarketRegime(**data)
        self.session.add(regime)
        self.session.commit()

    def save_monte_carlo_simulation(self, data: dict):
        simulation = MonteCarloSimulation(**data)
        self.session.add(simulation)
        self.session.commit()

    def get_latest_data(self, model_class, limit: int = 100):
        return self.session.query(model_class).order_by(
            model_class.date.desc()
        ).limit(limit).all()

    def get_data_by_date_range(self, model_class, start_date: datetime, end_date: datetime):
        return self.session.query(model_class).filter(
            model_class.date.between(start_date, end_date)
        ).all() 