from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from typing import Dict, Optional
from datetime import datetime, timedelta
from ..services.stock_service import StockService

router = APIRouter(prefix="/api/stock", tags=["stock"])
stock_service = StockService()

@router.get("/current")
async def get_current_price():
    """Get current Tesla stock price and basic info"""
    try:
        return await stock_service.get_current_price()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/historical")
async def get_historical_data(
    period: str = "1y",
    interval: str = "1d"
):
    """Get historical Tesla stock data"""
    try:
        data = await stock_service.get_historical_data(period, interval)
        return data.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics")
async def get_stock_metrics(period: str = "1y"):
    """Get calculated financial metrics"""
    try:
        data = await stock_service.get_historical_data(period)
        metrics = await stock_service.calculate_metrics(data)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/monte-carlo")
async def run_monte_carlo(
    days: int = 252,
    simulations: int = 1000
):
    """Run Monte Carlo simulation"""
    try:
        return await stock_service.run_monte_carlo(days, simulations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/technical-indicators")
async def get_technical_indicators(
    start_date: datetime = Query(default=None),
    end_date: datetime = Query(default=None)
):
    """Get technical indicators for the specified date range"""
    try:
        if not start_date:
            start_date = datetime.now() - timedelta(days=365)
        if not end_date:
            end_date = datetime.now()
        
        data = await stock_service.get_historical_data(
            period=f"{(end_date - start_date).days}d",
            interval="1d"
        )
        metrics = await stock_service.calculate_metrics(data)
        return metrics['technical_indicators']
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/volatility-metrics")
async def get_volatility_metrics(
    start_date: datetime = Query(default=None),
    end_date: datetime = Query(default=None)
):
    """Get volatility metrics for the specified date range"""
    try:
        if not start_date:
            start_date = datetime.now() - timedelta(days=365)
        if not end_date:
            end_date = datetime.now()
        
        data = await stock_service.get_historical_data(
            period=f"{(end_date - start_date).days}d",
            interval="1d"
        )
        metrics = await stock_service.calculate_metrics(data)
        return metrics['volatility_metrics']
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market-regime")
async def get_market_regime(
    start_date: datetime = Query(default=None),
    end_date: datetime = Query(default=None)
):
    """Get market regime analysis for the specified date range"""
    try:
        if not start_date:
            start_date = datetime.now() - timedelta(days=365)
        if not end_date:
            end_date = datetime.now()
        
        data = await stock_service.get_historical_data(
            period=f"{(end_date - start_date).days}d",
            interval="1d"
        )
        metrics = await stock_service.calculate_metrics(data)
        return metrics['market_regime']
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/historical-analysis")
async def get_historical_analysis(
    start_date: datetime = Query(default=None),
    end_date: datetime = Query(default=None)
):
    """Get complete historical analysis for the specified date range"""
    try:
        if not start_date:
            start_date = datetime.now() - timedelta(days=365)
        if not end_date:
            end_date = datetime.now()
        
        return await stock_service.get_historical_analysis(start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ml/train")
async def train_ml_models(
    background_tasks: BackgroundTasks,
    period: str = "2y"
):
    """Train machine learning models"""
    try:
        # Run training in background
        background_tasks.add_task(stock_service.train_ml_models, period)
        return {"message": "ML model training started in background"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ml/predictions")
async def get_ml_predictions():
    """Get next day price predictions from ML models"""
    try:
        return await stock_service.get_ml_predictions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analysis/combined")
async def get_combined_analysis():
    """Get combined analysis including ML predictions"""
    try:
        return await stock_service.get_combined_analysis()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 