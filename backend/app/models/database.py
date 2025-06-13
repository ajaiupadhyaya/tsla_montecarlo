from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from app.config import DATABASE_URL

Base = declarative_base()

class StockPrice(Base):
    __tablename__ = "stock_prices"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class TechnicalIndicator(Base):
    __tablename__ = "technical_indicators"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    rsi = Column(Float)
    macd = Column(Float)
    macd_signal = Column(Float)
    macd_hist = Column(Float)
    bollinger_upper = Column(Float)
    bollinger_middle = Column(Float)
    bollinger_lower = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class VolatilityMetric(Base):
    __tablename__ = "volatility_metrics"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    historical_volatility = Column(Float)
    parkinson_volatility = Column(Float)
    garman_klass_volatility = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class MarketRegime(Base):
    __tablename__ = "market_regimes"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    regime = Column(String(50))
    probability = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class MLPrediction(Base):
    __tablename__ = "ml_predictions"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    predicted_price = Column(Float)
    confidence = Column(Float)
    model_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db_connection():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)

# Database operations
class DatabaseOperations:
    def __init__(self):
        self.session = get_db_connection()

    def save_stock_data(self, data: dict):
        stock_data = StockPrice(**data)
        self.session.add(stock_data)
        self.session.commit()

    def save_technical_indicators(self, data: dict):
        indicators = TechnicalIndicator(**data)
        self.session.add(indicators)
        self.session.commit()

    def save_volatility_metrics(self, data: dict):
        metrics = VolatilityMetric(**data)
        self.session.add(metrics)
        self.session.commit()

    def save_market_regime(self, data: dict):
        regime = MarketRegime(**data)
        self.session.add(regime)
        self.session.commit()

    def save_ml_prediction(self, data: dict):
        prediction = MLPrediction(**data)
        self.session.add(prediction)
        self.session.commit()

    def get_latest_data(self, model_class, limit: int = 100):
        return self.session.query(model_class).order_by(
            model_class.date.desc()
        ).limit(limit).all()

    def get_data_by_date_range(self, model_class, start_date: datetime, end_date: datetime):
        return self.session.query(model_class).filter(
            model_class.date.between(start_date, end_date)
        ).all() 