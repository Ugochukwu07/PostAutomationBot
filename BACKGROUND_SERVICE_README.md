# Background Service Setup for Automated Daily Poster Bot

This guide explains how to set up the Automated Daily Poster Bot to run as a background service on your local machine using the `.env.production` configuration file.

## Prerequisites

- Linux system with systemd (Ubuntu, Debian, CentOS, etc.)
- Python 3.7+ installed
- MySQL database running
- `.env.production` file configured with your production settings

## Quick Setup

1. **Run the setup script with sudo:**
   ```bash
   sudo ./setup_background_service.sh
   ```

   This script will:
   - Check for virtual environment and create one if needed
   - Verify `.env.production` file exists
   - Install the bot as a systemd service
   - Enable the service to start on boot
   - Start the service immediately

## Service Management

Use the management script for easy control:

```bash
# Start the service
./manage_service.sh start

# Stop the service
./manage_service.sh stop

# Restart the service
./manage_service.sh restart

# Check service status
./manage_service.sh status

# View recent logs
./manage_service.sh logs

# Follow logs in real-time
./manage_service.sh follow-logs

# Enable service to start on boot
./manage_service.sh enable

# Disable service from starting on boot
./manage_service.sh disable
```

## Manual Systemd Commands

You can also use systemd commands directly:

```bash
# Start service
sudo systemctl start autopost-bot

# Stop service
sudo systemctl stop autopost-bot

# Restart service
sudo systemctl restart autopost-bot

# Check status
sudo systemctl status autopost-bot

# View logs
sudo journalctl -u autopost-bot -f

# Enable on boot
sudo systemctl enable autopost-bot

# Disable on boot
sudo systemctl disable autopost-bot
```

## Configuration

The service uses the `.env.production` file for configuration. Make sure this file contains:

- Database connection details
- API endpoint and key
- User and category IDs
- Other required settings

## Logs

Service logs are available through systemd journal:

```bash
# View all logs
sudo journalctl -u autopost-bot

# View recent logs (last 50 lines)
sudo journalctl -u autopost-bot -n 50

# Follow logs in real-time
sudo journalctl -u autopost-bot -f

# View logs from today
sudo journalctl -u autopost-bot --since today
```

## Troubleshooting

### Service won't start
1. Check the logs: `sudo journalctl -u autopost-bot -n 50`
2. Verify `.env.production` file exists and is properly configured
3. Ensure MySQL is running and accessible
4. Check that the virtual environment exists and has all dependencies

### Service stops unexpectedly
1. Check logs for error messages
2. Verify database connectivity
3. Check API endpoint accessibility
4. Ensure all required environment variables are set

### Permission issues
1. Make sure the service file has correct user/group settings
2. Verify file permissions on the bot directory
3. Check that the user has access to the virtual environment

## Service Details

- **Service Name**: `autopost-bot`
- **Configuration File**: `/etc/systemd/system/autopost-bot.service`
- **Working Directory**: Your bot directory
- **User**: Your username
- **Environment File**: `.env.production`
- **Restart Policy**: Always restart on failure (10-second delay)

## Uninstalling

To remove the service:

```bash
# Stop and disable the service
sudo systemctl stop autopost-bot
sudo systemctl disable autopost-bot

# Remove the service file
sudo rm /etc/systemd/system/autopost-bot.service

# Reload systemd
sudo systemctl daemon-reload
```

## Security Notes

- The service runs as your user account
- Environment variables are loaded from `.env.production`
- Logs are stored in systemd journal
- The service automatically restarts on failure
- Consider using a dedicated user account for production deployments 