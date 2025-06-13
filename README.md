# Tesla Stock Analysis Platform

A comprehensive platform for analyzing Tesla stock data, featuring real-time price updates, Monte Carlo simulations, and advanced financial metrics.

## Features

- Real-time Tesla stock price updates
- Historical price data visualization
- Monte Carlo simulation for price prediction
- Advanced technical analysis:
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands
  - Fibonacci Retracement
- Statistical metrics:
  - Sharpe Ratio
  - Sortino Ratio
  - Value at Risk (VaR)
  - Conditional VaR (CVaR)
  - Maximum Drawdown
  - Calmar Ratio
- Volatility analysis:
  - Historical Volatility
  - Parkinson Volatility
  - Garman-Klass Volatility
- Market regime detection
- Correlation analysis
- Machine Learning price predictions
- SQLite database for historical data storage
- Modern, responsive web interface
- RESTful API for data access

## Tech Stack

### Backend
- FastAPI (Python web framework)
- yfinance (Stock data API)
- Pandas & NumPy (Data analysis)
- SQLAlchemy (Database ORM)
- SciPy (Statistical analysis)
- scikit-learn (Machine learning)
- TensorFlow (Deep learning)

### Frontend
- React.js
- Next.js
- Chakra UI (Component library)
- Recharts (Charting library)
- Axios (HTTP client)

## Local Development Setup

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python -c "from app.models.database import Base, get_db_connection; Base.metadata.create_all(get_db_connection().get_bind())"
```

4. Start the backend server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

The web interface will be available at `http://localhost:3000`

## Free Deployment Guide

### Backend Deployment (Render.com)

1. Create a Render account at https://render.com (free tier)

2. Create a new Web Service:
   - Connect your GitHub repository
   - Select the repository
   - Configure the service:
     - Name: tesla-analysis-backend
     - Environment: Python
     - Build Command: `pip install -r backend/requirements.txt`
     - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
     - Plan: Free

3. Add Environment Variables:
   - `PYTHON_VERSION`: 3.9.0
   - `PORT`: 8000

4. Deploy the service

### Frontend Deployment (Vercel)

1. Create a Vercel account at https://vercel.com (free tier)

2. Install Vercel CLI:
```bash
npm install -g vercel
```

3. Deploy to Vercel:
```bash
cd frontend
vercel
```

4. Configure environment variables in Vercel dashboard:
   - `NEXT_PUBLIC_API_URL`: Your Render.com backend URL

### Database Setup

The project uses SQLite, which is file-based and doesn't require a separate database service. The database file will be automatically created in the backend directory.

## API Endpoints

- `GET /api/stock/current` - Get current stock price and basic info
- `GET /api/stock/historical` - Get historical stock data
- `GET /api/stock/metrics` - Get calculated financial metrics
- `GET /api/stock/monte-carlo` - Run Monte Carlo simulation
- `GET /api/stock/technical-indicators` - Get technical analysis indicators
- `GET /api/stock/volatility-metrics` - Get volatility metrics
- `GET /api/stock/market-regime` - Get market regime analysis
- `GET /api/stock/historical-analysis` - Get complete historical analysis
- `POST /api/stock/ml/train` - Train machine learning models
- `GET /api/stock/ml/predictions` - Get ML price predictions
- `GET /api/stock/analysis/combined` - Get combined analysis

## Free Tier Limitations

### Render.com Free Tier
- 750 hours of runtime per month
- Automatic sleep after 15 minutes of inactivity
- 512 MB RAM
- Shared CPU
- 1 GB disk space

### Vercel Free Tier
- Unlimited static sites
- Serverless functions
- Automatic HTTPS
- Continuous deployment
- Custom domains
- 100 GB bandwidth per month

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 