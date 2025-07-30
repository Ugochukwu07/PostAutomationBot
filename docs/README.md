# Automated Daily Poster Bot

A sophisticated Python application for automated content posting with intelligent scheduling, multiple content sources, and comprehensive logging.

## 🚀 Features

- **Intelligent Scheduling**: Daily scheduled posts and random posts throughout the day
- **Multiple Content Sources**: Integration with various external APIs for diverse content
- **API Integration**: Seamless posting to RecentHPost API with authentication
- **Database Logging**: Comprehensive MySQL logging of all posts and bot status
- **System Notifications**: Cross-platform notifications for bot events
- **Error Handling**: Robust error handling and fallback mechanisms
- **Configuration Management**: Environment-based configuration with validation

## 📁 Project Structure

```
autopost/
├── autopost/                    # Main package directory
│   ├── __init__.py             # Package initialization
│   ├── __main__.py             # Entry point for package execution
│   ├── core/                   # Core bot functionality
│   │   ├── __init__.py
│   │   └── bot.py              # Main bot class
│   ├── api/                    # API integration
│   │   ├── __init__.py
│   │   └── client.py           # API client for posting
│   ├── content/                # Content management
│   │   ├── __init__.py
│   │   └── fetcher.py          # Content fetching from APIs
│   ├── database/               # Database operations
│   │   ├── __init__.py
│   │   └── manager.py          # Database manager
│   ├── services/               # Service layer
│   │   ├── __init__.py
│   │   └── scheduler.py        # Post scheduling service
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── notifier.py         # Notification utilities
│   │   └── check_status.py     # Status checking utilities
│   ├── config/                 # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py         # Configuration settings
│   └── tests/                  # Test suite
│       ├── __init__.py
│       ├── test_bot.py         # Bot functionality tests
│       ├── test_api.py         # API integration tests
│       ├── test_notifications.py # Notification tests
│       └── demo_notifications.py # Notification demo
├── scripts/                    # Utility scripts
│   ├── setup.sh               # Setup script
│   ├── start_bot.sh           # Bot startup script
│   ├── manage_service.sh      # Service management
│   ├── setup_background_service.sh # Background service setup
│   ├── setup_database.sql     # Database setup
│   └── autopost-bot.service   # Systemd service file
├── docs/                       # Documentation
│   ├── README.md              # This file
│   ├── QUICK_START.md         # Quick start guide
│   ├── BACKGROUND_SERVICE_README.md # Background service guide
│   ├── NOTIFICATION_TEST_REPORT.md # Notification test report
│   └── env_example.txt        # Environment variables example
├── main.py                     # Main entry point
├── setup.py                    # Package setup
├── pyproject.toml             # Modern Python packaging
├── requirements.txt            # Python dependencies
└── .gitignore                 # Git ignore file
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- MySQL database
- RecentHPost API access

### Quick Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/autopost.git
   cd autopost
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package**:
   ```bash
   pip install -e .
   ```

4. **Set up environment variables**:
   ```bash
   cp docs/env_example.txt .env
   # Edit .env with your configuration
   ```

5. **Set up the database**:
   ```bash
   mysql -u your_user -p your_database < scripts/setup_database.sql
   ```

## ⚙️ Configuration

Create a `.env` file in the project root with the following variables:

```env
# Database Configuration
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=autopost_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password

# API Configuration
API_ENDPOINT=https://your-api-endpoint.com/posts
API_KEY=your_api_key
USER_ID=1
CATEGORY_ID=1
STATE=California
CITY=San Francisco
DEVICE=Python Bot 1.0
COUNTRIES_ISO=US

# Bot Configuration
TIMEZONE=UTC
LOG_LEVEL=INFO
```

## 🚀 Usage

### Basic Usage

1. **Test the bot**:
   ```bash
   python -m autopost --test
   ```

2. **Make a single post**:
   ```bash
   python -m autopost --post
   ```

3. **Check bot status**:
   ```bash
   python -m autopost --status
   ```

4. **Start the bot**:
   ```bash
   python -m autopost
   ```

### Alternative Entry Points

You can also use the main.py file directly:

```bash
python main.py --test
python main.py --post
python main.py --status
python main.py
```

### Background Service

To run the bot as a background service:

1. **Set up the systemd service**:
   ```bash
   sudo bash scripts/setup_background_service.sh
   ```

2. **Manage the service**:
   ```bash
   sudo bash scripts/manage_service.sh start
   sudo bash scripts/manage_service.sh stop
   sudo bash scripts/manage_service.sh status
   ```

## 🧪 Testing

### Run all tests:
```bash
python -m pytest autopost/tests/
```

### Run specific tests:
```bash
python -m pytest autopost/tests/test_bot.py
python -m pytest autopost/tests/test_api.py
```

### Run tests with coverage:
```bash
python -m pytest --cov=autopost autopost/tests/
```

## 📊 Monitoring

### Check Bot Status
```bash
python autopost/utils/check_status.py
```

### View Logs
```bash
tail -f autopost_bot.log
```

### Database Queries
```sql
-- Check recent posts
SELECT * FROM posts ORDER BY created_at DESC LIMIT 10;

-- Check bot status
SELECT * FROM bot_status;

-- Check posts by type
SELECT post_type, COUNT(*) FROM posts 
WHERE DATE(created_at) = CURDATE() 
GROUP BY post_type;
```

## 🔧 Development

### Code Quality

The project uses several tools for code quality:

- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pytest**: Testing

### Development Setup

1. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

2. **Format code**:
   ```bash
   black autopost/
   ```

3. **Lint code**:
   ```bash
   flake8 autopost/
   ```

4. **Type check**:
   ```bash
   mypy autopost/
   ```

### Adding New Content APIs

To add a new content API, update the `ContentAPIConfig.SOURCES` in `autopost/config/settings.py`:

```python
{
    'name': 'Your API Name',
    'url': 'https://api.example.com/endpoint',
    'content_key': 'content_field_name',
    'title_key': 'title_field_name',  # Optional
    'author_key': 'author_field_name'  # Optional
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the logs in `autopost_bot.log`
2. Verify your configuration in `.env`
3. Test individual components using the test scripts
4. Open an issue on GitHub with detailed information

## 🔄 Changelog

### Version 1.0.0
- Initial release with complete package structure
- Modular architecture with clear separation of concerns
- Comprehensive testing suite
- Background service support
- Cross-platform notifications
- Multiple content API integrations 