# 🤖 Automated Daily Poster Bot

A Python-based bot that runs continuously on a local machine to automate the creation and submission of content to the RecentHPost API. The bot uses API key authentication and intelligently schedules posts throughout the day.

## 🎯 Core Features

- **Daily Scheduled Post**: Makes one post at exactly 12:00 PM daily
- **5 Random Posts**: Makes 5 additional posts at random intervals throughout the day
- **Multiple Content Sources**: Fetches content from various random internet APIs
- **API Key Authentication**: Uses x-api-key header for authentication
- **MySQL Logging**: Comprehensive logging of all posts with details
- **Intelligent Scheduling**: Distributes remaining posts intelligently if starting late
- **Failure Handling**: Robust error handling and retry logic

## 🗃️ Tech Stack

- **Language**: Python 3.x
- **Database**: MySQL
- **HTTP Requests**: requests
- **Scheduling**: schedule, time, threading
- **Environment Management**: python-dotenv
- **Database Connector**: mysql-connector-python

## 📋 Prerequisites

- Python 3.7 or higher
- MySQL server
- Internet connection for API access

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd autopost
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL database**
   ```bash
   mysql -u root -p < setup_database.sql
   ```

4. **Configure environment variables**
   ```bash
   cp env_example.txt .env
   ```
   
   Edit `.env` file with your configuration:
   ```env
   # Database Configuration
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=autopost_db
   DB_USER=your_username
   DB_PASSWORD=your_password

   # RecentHPost API Configuration
   API_ENDPOINT=http://recenthpost.bakkaz.local/api/posts
   API_KEY=d7J$kLz1p@Gm4xQw9!R6nYb2^T8vEWq0Z*fOj5L&yHgX3rU

   # Post Configuration
   USER_ID=11
   CATEGORY_ID=7
   STATE=lagos
   CITY=ajah
   DEVICE=Python Bot 1.0
   COUNTRIES_ISO=NG,US

   # Bot Configuration
   TIMEZONE=UTC
   LOG_LEVEL=INFO
   ```

## 🎮 Usage

### Basic Usage

**Start the bot:**
```bash
python main.py
```

**Make a test post:**
```bash
python main.py --test
```

**Check bot status:**
```bash
python main.py --status
```

### Running as a Service

**Using systemd (Linux):**
```bash
# Create service file
sudo nano /etc/systemd/system/autopost-bot.service
```

Add the following content:
```ini
[Unit]
Description=Automated Daily Poster Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/autopost
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start the service:**
```bash
sudo systemctl enable autopost-bot
sudo systemctl start autopost-bot
sudo systemctl status autopost-bot
```

## 📊 Content Sources

The bot fetches content from multiple random internet APIs:

1. **Quotes API** - Inspirational quotes with authors
2. **Joke API** - Random jokes with setup and punchline
3. **Advice API** - Random advice
4. **Useless Facts API** - Interesting random facts
5. **Dog Facts API** - Fun facts about dogs

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | MySQL host | localhost |
| `DB_PORT` | MySQL port | 3306 |
| `DB_NAME` | Database name | autopost_db |
| `DB_USER` | Database username | root |
| `DB_PASSWORD` | Database password | (empty) |
| `API_ENDPOINT` | RecentHPost API endpoint | http://recenthpost.bakkaz.local/api/posts |
| `API_KEY` | API authentication key | (required) |
| `USER_ID` | User ID for posts | 11 |
| `CATEGORY_ID` | Category ID for posts | 7 |
| `STATE` | Nigerian state | lagos |
| `CITY` | City name | ajah |
| `DEVICE` | Device info | Python Bot 1.0 |
| `COUNTRIES_ISO` | Country codes | NG,US |
| `TIMEZONE` | Bot timezone | UTC |
| `LOG_LEVEL` | Logging level | INFO |

### Scheduling Configuration

- **Daily Post**: 12:00 PM (configurable in `scheduler.py`)
- **Random Posts**: 5 per day, intelligently distributed
- **Minimum Interval**: 30 minutes between posts
- **Maximum Interval**: 4 hours between posts

## 📈 Monitoring

### Logs

The bot creates detailed logs in `autopost_bot.log`:
```bash
tail -f autopost_bot.log
```

### Database Queries

**Check today's posts:**
```sql
SELECT * FROM posts WHERE DATE(timestamp) = CURDATE() ORDER BY timestamp DESC;
```

**Check post statistics:**
```sql
SELECT 
    post_type,
    COUNT(*) as total,
    SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) as successful,
    SUM(CASE WHEN status = 'FAILURE' THEN 1 ELSE 0 END) as failed
FROM posts 
WHERE DATE(timestamp) = CURDATE()
GROUP BY post_type;
```

## 🛠️ Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Verify MySQL is running
   - Check database credentials in `.env`
   - Ensure database exists: `mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS autopost_db;"`

2. **API Authentication Failed**
   - Verify API endpoint URL
   - Check API key in `.env`
   - Test API endpoint manually

3. **Content Fetching Failed**
   - Check internet connection
   - Verify API endpoints are accessible
   - Bot will use fallback content if APIs fail

4. **Scheduling Issues**
   - Check system time and timezone
   - Verify bot has proper permissions
   - Check logs for scheduling errors

### Debug Mode

Enable debug logging by setting `LOG_LEVEL=DEBUG` in `.env`:
```env
LOG_LEVEL=DEBUG
```

## 🔒 Security Considerations

- Store sensitive credentials in `.env` file (never commit to version control)
- Use strong passwords for database and API accounts
- Consider using environment variables for production deployments
- Regularly rotate API keys

## 📝 API Integration

The bot integrates with the RecentHPost API using the following structure:

**API Endpoint:** `POST http://recenthpost.bakkaz.local/api/posts`

**Authentication:** `x-api-key` header

**Request Format:** `multipart/form-data` with the following fields:
- `title` (string)
- `category_id` (integer)
- `state` (string)
- `device` (string)
- `city` (string)
- `user_id` (integer)
- `countries_iso[]` (array of country codes)
- `hashtags[]` (array of hashtags)
- `media_files_urls[]` (array of media URLs)
- `content` (string)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs
3. Open an issue on GitHub

---

**Happy Posting! 🚀** 