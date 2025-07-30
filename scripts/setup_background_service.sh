#!/bin/bash

# Setup script for running autopost bot as a background service
# This script will install the bot as a systemd service using .env.production

echo "🤖 Setting up Automated Daily Poster Bot as a background service..."

# Check if running as root (needed for systemd service installation)
if [ "$EUID" -ne 0 ]; then
    echo "❌ This script needs to be run with sudo to install the systemd service"
    echo "   Please run: sudo ./setup_background_service.sh"
    exit 1
fi

# Get the current user (who invoked sudo)
ACTUAL_USER=${SUDO_USER:-$USER}
CURRENT_DIR=$(pwd)

echo "📁 Current directory: $CURRENT_DIR"
echo "👤 User: $ACTUAL_USER"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "✅ Virtual environment found"
fi

# Check if .env.production exists
if [ ! -f ".env.production" ]; then
    echo "❌ .env.production file not found!"
    echo "   Please create .env.production with your production configuration"
    exit 1
fi

echo "✅ .env.production file found"

# Update the service file with correct paths and user
sed -i "s|User=hp|User=$ACTUAL_USER|g" autopost-bot.service
sed -i "s|Group=hp|Group=$ACTUAL_USER|g" autopost-bot.service
sed -i "s|WorkingDirectory=/home/hp/Desktop/CODE/Personal/autopost|WorkingDirectory=$CURRENT_DIR|g" autopost-bot.service
sed -i "s|Environment=PATH=/home/hp/Desktop/CODE/Personal/autopost/venv/bin|Environment=PATH=$CURRENT_DIR/venv/bin|g" autopost-bot.service
sed -i "s|ExecStart=/home/hp/Desktop/CODE/Personal/autopost/venv/bin/python /home/hp/Desktop/CODE/Personal/autopost/main.py|ExecStart=$CURRENT_DIR/venv/bin/python $CURRENT_DIR/main.py|g" autopost-bot.service
sed -i "s|EnvironmentFile=/home/hp/Desktop/CODE/Personal/autopost/.env.production|EnvironmentFile=$CURRENT_DIR/.env.production|g" autopost-bot.service

echo "📝 Service file updated with correct paths"

# Copy service file to systemd directory
cp autopost-bot.service /etc/systemd/system/

# Reload systemd daemon
systemctl daemon-reload

# Enable the service (start on boot)
systemctl enable autopost-bot.service

echo "✅ Service installed and enabled"
echo ""
echo "🎯 Service Management Commands:"
echo "   Start service:   sudo systemctl start autopost-bot"
echo "   Stop service:    sudo systemctl stop autopost-bot"
echo "   Restart service: sudo systemctl restart autopost-bot"
echo "   Check status:    sudo systemctl status autopost-bot"
echo "   View logs:       sudo journalctl -u autopost-bot -f"
echo "   Disable service: sudo systemctl disable autopost-bot"
echo ""
echo "🚀 Starting the service now..."
systemctl start autopost-bot.service

# Check if service started successfully
sleep 2
if systemctl is-active --quiet autopost-bot.service; then
    echo "✅ Service started successfully!"
    echo "📊 Current status:"
    systemctl status autopost-bot.service --no-pager -l
else
    echo "❌ Service failed to start. Check logs with:"
    echo "   sudo journalctl -u autopost-bot -n 50"
fi 