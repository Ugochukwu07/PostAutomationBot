#!/bin/bash

# Automated Daily Poster Bot Startup Script

echo "🤖 Starting Automated Daily Poster Bot..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "✅ Virtual environment found"
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Please create one from env_example.txt"
    echo "   cp env_example.txt .env"
    echo "   Then edit .env with your configuration"
    exit 1
fi

# Run the bot
echo "🚀 Launching bot..."
python main.py 