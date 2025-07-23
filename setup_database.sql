-- Automated Daily Poster Bot Database Setup
-- Run this script to create the database and tables

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS autopost_db;
USE autopost_db;

-- Create posts table
CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_type ENUM('SCHEDULED', 'RANDOM', 'TEST') NOT NULL,
    timestamp DATETIME NOT NULL,
    status ENUM('SUCCESS', 'FAILURE') NOT NULL,
    api_used VARCHAR(255),
    content TEXT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_timestamp (timestamp),
    INDEX idx_post_type (post_type),
    INDEX idx_status (status)
);

-- Create bot_stats table for additional statistics
CREATE TABLE IF NOT EXISTS bot_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    total_posts INT DEFAULT 0,
    successful_posts INT DEFAULT 0,
    failed_posts INT DEFAULT 0,
    scheduled_posts INT DEFAULT 0,
    random_posts INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_date (date)
);

-- Insert sample data for testing (optional)
-- INSERT INTO posts (post_type, timestamp, status, api_used, content) VALUES
-- ('TEST', NOW(), 'SUCCESS', 'Quotes API', 'This is a test post from the Automated Poster Bot');

-- Show tables
SHOW TABLES;

-- Show table structure
DESCRIBE posts;
DESCRIBE bot_stats; 