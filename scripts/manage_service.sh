#!/bin/bash

# Simple management script for the autopost bot service

SERVICE_NAME="autopost-bot"

case "$1" in
    start)
        echo "🚀 Starting $SERVICE_NAME service..."
        sudo systemctl start $SERVICE_NAME
        ;;
    stop)
        echo "🛑 Stopping $SERVICE_NAME service..."
        sudo systemctl stop $SERVICE_NAME
        ;;
    restart)
        echo "🔄 Restarting $SERVICE_NAME service..."
        sudo systemctl restart $SERVICE_NAME
        ;;
    status)
        echo "📊 Status of $SERVICE_NAME service:"
        sudo systemctl status $SERVICE_NAME --no-pager -l
        ;;
    logs)
        echo "📋 Recent logs for $SERVICE_NAME service:"
        sudo journalctl -u $SERVICE_NAME -n 50 --no-pager
        ;;
    follow-logs)
        echo "📋 Following logs for $SERVICE_NAME service (Ctrl+C to exit):"
        sudo journalctl -u $SERVICE_NAME -f
        ;;
    enable)
        echo "✅ Enabling $SERVICE_NAME service to start on boot..."
        sudo systemctl enable $SERVICE_NAME
        ;;
    disable)
        echo "❌ Disabling $SERVICE_NAME service from starting on boot..."
        sudo systemctl disable $SERVICE_NAME
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|follow-logs|enable|disable}"
        echo ""
        echo "Commands:"
        echo "  start        - Start the service"
        echo "  stop         - Stop the service"
        echo "  restart      - Restart the service"
        echo "  status       - Show service status"
        echo "  logs         - Show recent logs"
        echo "  follow-logs  - Follow logs in real-time"
        echo "  enable       - Enable service to start on boot"
        echo "  disable      - Disable service from starting on boot"
        exit 1
        ;;
esac 