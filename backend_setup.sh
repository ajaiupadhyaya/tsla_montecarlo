#!/bin/bash

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y python3-pip python3-venv nginx

# Create application directory
sudo mkdir -p /var/www/tesla-analysis
sudo chown ubuntu:ubuntu /var/www/tesla-analysis

# Clone repository (replace with your repository URL)
git clone https://github.com/yourusername/tesla_montecarlo.git /var/www/tesla-analysis

# Set up Python virtual environment
cd /var/www/tesla-analysis
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# Create models directory
mkdir -p /var/www/tesla-analysis/backend/models

# Configure Nginx
sudo tee /etc/nginx/sites-available/tesla-analysis << EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/tesla-analysis /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Create systemd service
sudo tee /etc/systemd/system/tesla-analysis.service << EOF
[Unit]
Description=Tesla Stock Analysis API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/var/www/tesla-analysis/backend
Environment="PATH=/var/www/tesla-analysis/venv/bin"
ExecStart=/var/www/tesla-analysis/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
EOF

# Start service
sudo systemctl start tesla-analysis
sudo systemctl enable tesla-analysis

# Train initial ML models
cd /var/www/tesla-analysis/backend
source ../venv/bin/activate
python3 -c "from app.services.stock_service import StockService; import asyncio; asyncio.run(StockService().train_ml_models())" 