# 🚀 Quick Start Guide - RecentHPost API Integration

This guide will help you get your Automated Poster Bot up and running with the RecentHPost API in just a few minutes!

## 📋 Prerequisites

- Python 3.7 or higher
- MySQL server
- Internet connection

## ⚡ Quick Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Database
```bash
mysql -u root -p < setup_database.sql
```

### 3. Configure Environment
```bash
cp env_example.txt .env
```

Edit `.env` file with your database credentials:
```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=autopost_db
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password

# RecentHPost API Configuration (already configured)
API_ENDPOINT=http://recenthpost.bakkaz.local/api/posts
API_KEY=d7J$kLz1p@Gm4xQw9!R6nYb2^T8vEWq0Z*fOj5L&yHgX3rU

# Post Configuration (customize as needed)
USER_ID=11
CATEGORY_ID=7
STATE=lagos
CITY=ajah
DEVICE=Python Bot 1.0
COUNTRIES_ISO=NG,US
```

### 4. Test API Connection
```bash
python test_api.py
```

You should see:
```
🚀 RecentHPost API Integration Test
==================================================

1️⃣ Testing Configuration...
✅ Configuration is valid

2️⃣ Testing API Connection...
✅ API connection test successful!

3️⃣ Testing Single Post...
✅ Test post successful!

🎉 All tests passed! Your API integration is working correctly.
```

### 5. Start the Bot
```bash
python main.py
```

## 🎯 What the Bot Does

- **12:00 PM Daily**: Makes one scheduled post
- **Random Posts**: Makes 5 additional posts at random intervals
- **Content Sources**: Fetches content from random internet APIs (quotes, jokes, facts, etc.)
- **Logging**: Records all posts in MySQL database

## 🔧 Customization

### Change Post Times
Edit `scheduler.py`:
```python
self.SCHEDULED_POST_TIME = "12:00"  # Change to your preferred time
self.RANDOM_POSTS_PER_DAY = 5       # Change number of random posts
```

### Change Content Sources
Edit `config.py` in the `CONTENT_APIS` section to add/remove content sources.

### Change Post Settings
Edit `.env` file to customize:
- `USER_ID`: Your user ID
- `CATEGORY_ID`: Post category
- `STATE`/`CITY`: Location
- `COUNTRIES_ISO`: Target countries

## 📊 Monitoring

### Check Bot Status
```bash
python main.py --status
```

### View Logs
```bash
tail -f autopost_bot.log
```

### Check Database
```sql
mysql -u root -p autopost_db -e "SELECT * FROM posts WHERE DATE(timestamp) = CURDATE() ORDER BY timestamp DESC;"
```

## 🛠️ Troubleshooting

### API Connection Failed
- Check if the API endpoint is accessible
- Verify the API key is correct
- Test with: `python test_api.py`

### Database Connection Failed
- Ensure MySQL is running
- Check database credentials in `.env`
- Create database: `mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS autopost_db;"`

### Content Fetching Failed
- Check internet connection
- Bot will use fallback content if APIs fail

## 🎉 You're Ready!

Your bot is now configured and ready to automatically post content to RecentHPost! The bot will:

1. Start making posts immediately
2. Schedule the 12 PM daily post
3. Distribute 5 random posts throughout the day
4. Log everything to the database

**Happy Posting! 🚀** 