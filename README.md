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

### Frontend
- React.js
- Next.js
- Chakra UI (Component library)
- Recharts (Charting library)
- Axios (HTTP client)

## Setup

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

## Deployment

### Backend Deployment (AWS)

1. Create an EC2 instance:
```bash
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t2.micro \
    --key-name your-key-pair \
    --security-group-ids sg-xxxxxxxx
```

2. Install dependencies on EC2:
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-venv nginx
```

3. Set up the application:
```bash
git clone <repository-url>
cd tesla_montecarlo
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

4. Configure Nginx:
```bash
sudo nano /etc/nginx/sites-available/tesla-analysis
```

Add the following configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

5. Enable the site and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/tesla-analysis /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

6. Set up systemd service:
```bash
sudo nano /etc/systemd/system/tesla-analysis.service
```

Add the following configuration:
```ini
[Unit]
Description=Tesla Stock Analysis API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/tesla_montecarlo
Environment="PATH=/home/ubuntu/tesla_montecarlo/venv/bin"
ExecStart=/home/ubuntu/tesla_montecarlo/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

7. Start the service:
```bash
sudo systemctl start tesla-analysis
sudo systemctl enable tesla-analysis
```

### Frontend Deployment (Vercel)

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy to Vercel:
```bash
cd frontend
vercel
```

3. Configure environment variables in Vercel dashboard:
```
NEXT_PUBLIC_API_URL=https://your-backend-domain.com
```

## API Endpoints

- `GET /api/stock/current` - Get current stock price and basic info
- `GET /api/stock/historical` - Get historical stock data
- `GET /api/stock/metrics` - Get calculated financial metrics
- `GET /api/stock/monte-carlo` - Run Monte Carlo simulation
- `GET /api/stock/technical-indicators` - Get technical analysis indicators
- `GET /api/stock/volatility-metrics` - Get volatility metrics
- `GET /api/stock/market-regime` - Get market regime analysis
- `GET /api/stock/historical-analysis` - Get complete historical analysis

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 