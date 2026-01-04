-- PostgreSQL Setup Script for Ramadan Helper
-- Run this in PostgreSQL to create the database and user

-- Create user (if not exists)
-- Note: Change password to something secure
CREATE USER ramadan_user WITH PASSWORD 'secure_password_123' CREATEDB;

-- Create database
CREATE DATABASE ramadan_db OWNER ramadan_user;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE ramadan_db TO ramadan_user;

-- Connect to the new database and set privileges
\c ramadan_db

GRANT ALL ON SCHEMA public TO ramadan_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ramadan_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ramadan_user;
