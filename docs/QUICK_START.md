# Quick Start Guide

This guide will help you get the Automated Daily Poster Bot up and running quickly.

## 🚀 Prerequisites

- Python 3.8 or higher
- MySQL database
- RecentHPost API access

## ⚡ Quick Setup

### 1. Clone and Install

```bash
# Clone the repository
git clone https://github.com/yourusername/autopost.git
cd autopost

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

### 2. Configure Environment

```bash
# Copy environment template
cp docs/env_example.txt .env

# Edit the .env file with your settings
nano .env
```

Required environment variables:
```env
# Database
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=autopost_db
DB_USER=your_username
DB_PASSWORD=your_password

# API
API_ENDPOINT=https://your-api-endpoint.com/posts
API_KEY=your_api_key
USER_ID=1
CATEGORY_ID=1
```

### 3. Set Up Database

```bash
# Create database and tables
mysql -u your_username -p your_database < scripts/setup_database.sql
```

### 4. Test the Bot

```bash
# Test the bot functionality
python -m autopost --test

# Make a single post
python -m autopost --post

# Check bot status
python -m autopost --status
```

### 5. Start the Bot

```bash
# Start the bot (runs continuously)
python -m autopost
```

## 🛠️ Alternative Installation Methods

### Using pip (if published to PyPI)

```bash
pip install autopost
autopost --test
```

### Using Docker (if Dockerfile is available)

```bash
docker build -t autopost .
docker run -d --name autopost-bot autopost
```

## 📋 Common Commands

| Command | Description |
|---------|-------------|
| `python -m autopost --test` | Test bot functionality |
| `python -m autopost --post` | Make a single post |
| `python -m autopost --status` | Check bot status |
| `python -m autopost` | Start the bot |
| `make test` | Run all tests |
| `make format` | Format code |
| `make lint` | Run linting |

## 🔧 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check MySQL is running
   sudo systemctl status mysql
   
   # Test connection
   mysql -u your_username -p your_database
   ```

2. **API Connection Failed**
   ```bash
   # Test API endpoint
   curl -H "x-api-key: your_key" https://your-api-endpoint.com/posts
   ```

3. **Import Errors**
   ```bash
   # Reinstall package
   pip install -e . --force-reinstall
   ```

### Getting Help

- Check logs: `tail -f autopost_bot.log`
- Run tests: `make test`
- Check status: `python -m autopost --status`

## 🎯 Next Steps

1. **Customize Content Sources**: Edit `autopost/config/settings.py` to add new APIs
2. **Adjust Scheduling**: Modify schedule settings in the scheduler
3. **Set Up Monitoring**: Configure system notifications
4. **Deploy as Service**: Use the provided systemd service scripts

## 📚 Additional Resources

- [Full Documentation](README.md)
- [Configuration Guide](README.md#configuration)
- [API Integration](README.md#api-integration)
- [Troubleshooting](README.md#troubleshooting) 