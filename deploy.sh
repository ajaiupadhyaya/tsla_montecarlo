#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Starting deployment process...${NC}"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}AWS CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo -e "${RED}Vercel CLI is not installed. Installing...${NC}"
    npm install -g vercel
fi

# Deploy Backend
echo -e "${GREEN}Deploying backend to AWS EC2...${NC}"

# Create EC2 instance
echo "Creating EC2 instance..."
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t2.micro \
    --key-name your-key-pair \
    --security-group-ids sg-xxxxxxxx \
    --user-data file://backend_setup.sh \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "Waiting for instance to be running..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

# Get instance public IP
INSTANCE_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo "Backend will be available at: http://$INSTANCE_IP"

# Deploy Frontend
echo -e "${GREEN}Deploying frontend to Vercel...${NC}"

cd frontend

# Create .env.production file
echo "NEXT_PUBLIC_API_URL=http://$INSTANCE_IP" > .env.production

# Deploy to Vercel
vercel --prod

echo -e "${GREEN}Deployment completed!${NC}"
echo "Backend URL: http://$INSTANCE_IP"
echo "Frontend URL: Check Vercel dashboard for the deployment URL" 