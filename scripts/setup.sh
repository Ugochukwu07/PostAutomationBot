#!/bin/bash

# Automated Daily Poster Bot Setup Script

echo "🚀 Setting up Automated Daily Poster Bot..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo "⚠️  MySQL not found. Please install MySQL server:"
    echo "   sudo apt install mysql-server"
    echo "   or"
    echo "   sudo yum install mysql-server"
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment and install dependencies
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp env_example.txt .env
    echo "✅ .env file created. Please edit it with your configuration:"
    echo "   nano .env"
else
    echo "✅ .env file already exists"
fi

# Make scripts executable
chmod +x main.py
chmod +x start_bot.sh

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your API endpoints and database credentials"
echo "2. Set up MySQL database: mysql -u root -p < setup_database.sql"
echo "3. Test the bot: ./start_bot.sh --test"
echo "4. Start the bot: ./start_bot.sh"
echo ""
echo "📚 For more information, see README.md" 