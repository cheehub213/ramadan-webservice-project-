"""
Email Service - Send verification and password reset emails
Uses SMTP for sending real emails
"""
from dotenv import load_dotenv
from pathlib import Path

# Load .env file from backend directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

import smtplib
import os
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Optional


# Email Configuration (set these in environment variables for production)
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")  # Your email
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")  # App password for Gmail
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "Ramadan Helper")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", SMTP_USER)

# Debug: Print SMTP config at startup
print(f"[EMAIL SERVICE] SMTP_USER configured: {bool(SMTP_USER)}")
print(f"[EMAIL SERVICE] SMTP_PASSWORD configured: {bool(SMTP_PASSWORD)}")

# Frontend URL for verification links
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8080")

# Token expiry
VERIFICATION_TOKEN_EXPIRE_HOURS = 24
PASSWORD_RESET_TOKEN_EXPIRE_HOURS = 1


def generate_verification_token() -> str:
    """Generate a secure random token for email verification"""
    return secrets.token_urlsafe(32)


def get_verification_link(token: str) -> str:
    """Generate verification link"""
    return f"{FRONTEND_URL}/app.html?verify={token}"


def get_password_reset_link(token: str) -> str:
    """Generate password reset link"""
    return f"{FRONTEND_URL}/app.html?reset={token}"


def send_email(to_email: str, subject: str, html_content: str, text_content: str = "") -> bool:
    """
    Send email using SMTP
    Returns True if successful, False otherwise
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        print(f"[EMAIL] SMTP not configured. Would send to {to_email}: {subject}")
        print(f"[EMAIL] Verification link would be in the email")
        return False  # Return False to indicate email wasn't actually sent
    
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
        msg["To"] = to_email
        
        # Add plain text and HTML versions
        if text_content:
            msg.attach(MIMEText(text_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))
        
        # Connect and send
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_FROM_EMAIL, to_email, msg.as_string())
        
        print(f"[EMAIL] Successfully sent email to {to_email}")
        return True
    except Exception as e:
        print(f"[EMAIL] Failed to send email to {to_email}: {str(e)}")
        return False


def send_verification_email(to_email: str, name: str, token: str) -> dict:
    """
    Send email verification link to new user
    Returns dict with success status and token info
    """
    verification_link = get_verification_link(token)
    
    subject = "🌙 Verify Your Ramadan Helper Account"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #1A1A2E; color: #E5E7EB; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%); border-radius: 16px; padding: 40px; border: 1px solid rgba(212,175,55,0.3); }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .logo {{ font-size: 48px; margin-bottom: 10px; }}
            h1 {{ color: #D4AF37; font-size: 28px; margin: 0; }}
            .subtitle {{ color: #9CA3AF; margin-top: 8px; }}
            .content {{ margin: 30px 0; line-height: 1.6; }}
            .btn {{ display: inline-block; padding: 16px 32px; background: linear-gradient(135deg, #0D5C2E, #166534); color: white; text-decoration: none; border-radius: 10px; font-size: 18px; font-weight: bold; margin: 20px 0; }}
            .btn:hover {{ background: linear-gradient(135deg, #166534, #0D5C2E); }}
            .warning {{ background: rgba(234, 179, 8, 0.2); color: #eab308; padding: 12px; border-radius: 8px; margin: 20px 0; font-size: 14px; }}
            .footer {{ text-align: center; margin-top: 30px; color: #6B7280; font-size: 12px; }}
            .link {{ color: #D4AF37; word-break: break-all; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">☪️</div>
                <h1>Ramadan Helper</h1>
                <p class="subtitle">Your Islamic Companion</p>
            </div>
            
            <div class="content">
                <p>Assalamu Alaikum <strong>{name}</strong>,</p>
                <p>Welcome to Ramadan Helper! 🌙</p>
                <p>Please verify your email address to activate your account and access all features:</p>
                
                <div style="text-align: center;">
                    <a href="{verification_link}" class="btn">✅ Verify My Email</a>
                </div>
                
                <div class="warning">
                    ⏰ This verification link expires in {VERIFICATION_TOKEN_EXPIRE_HOURS} hours.
                </div>
                
                <p>If the button doesn't work, copy and paste this link into your browser:</p>
                <p class="link">{verification_link}</p>
                
                <p>If you didn't create an account with Ramadan Helper, please ignore this email.</p>
            </div>
            
            <div class="footer">
                <p>☪️ Ramadan Mubarak</p>
                <p>© 2026 Ramadan Helper. May Allah accept from us.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Assalamu Alaikum {name},
    
    Welcome to Ramadan Helper!
    
    Please verify your email address to activate your account:
    {verification_link}
    
    This link expires in {VERIFICATION_TOKEN_EXPIRE_HOURS} hours.
    
    If you didn't create this account, please ignore this email.
    
    Ramadan Mubarak!
    """
    
    email_sent = send_email(to_email, subject, html_content, text_content)
    
    return {
        "email_sent": email_sent,
        "token": token,
        "verification_link": verification_link,
        "expires_in_hours": VERIFICATION_TOKEN_EXPIRE_HOURS
    }


def send_password_reset_email(to_email: str, name: str, token: str) -> dict:
    """
    Send password reset link to user
    """
    reset_link = get_password_reset_link(token)
    
    subject = "🔑 Reset Your Ramadan Helper Password"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #1A1A2E; color: #E5E7EB; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%); border-radius: 16px; padding: 40px; border: 1px solid rgba(212,175,55,0.3); }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .logo {{ font-size: 48px; margin-bottom: 10px; }}
            h1 {{ color: #D4AF37; font-size: 28px; margin: 0; }}
            .subtitle {{ color: #9CA3AF; margin-top: 8px; }}
            .content {{ margin: 30px 0; line-height: 1.6; }}
            .btn {{ display: inline-block; padding: 16px 32px; background: linear-gradient(135deg, #D4AF37, #B8860B); color: #1A1A2E; text-decoration: none; border-radius: 10px; font-size: 18px; font-weight: bold; margin: 20px 0; }}
            .warning {{ background: rgba(220, 38, 38, 0.2); color: #f87171; padding: 12px; border-radius: 8px; margin: 20px 0; font-size: 14px; }}
            .footer {{ text-align: center; margin-top: 30px; color: #6B7280; font-size: 12px; }}
            .link {{ color: #D4AF37; word-break: break-all; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🔑</div>
                <h1>Password Reset</h1>
                <p class="subtitle">Ramadan Helper</p>
            </div>
            
            <div class="content">
                <p>Assalamu Alaikum <strong>{name}</strong>,</p>
                <p>We received a request to reset your password. Click the button below to create a new password:</p>
                
                <div style="text-align: center;">
                    <a href="{reset_link}" class="btn">🔑 Reset Password</a>
                </div>
                
                <div class="warning">
                    ⏰ This reset link expires in {PASSWORD_RESET_TOKEN_EXPIRE_HOURS} hour(s).
                </div>
                
                <p>If the button doesn't work, copy and paste this link into your browser:</p>
                <p class="link">{reset_link}</p>
                
                <p><strong>Didn't request this?</strong> If you didn't request a password reset, you can safely ignore this email. Your password will remain unchanged.</p>
            </div>
            
            <div class="footer">
                <p>☪️ Ramadan Mubarak</p>
                <p>© 2026 Ramadan Helper. May Allah accept from us.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Assalamu Alaikum {name},
    
    We received a request to reset your password.
    
    Click this link to reset your password:
    {reset_link}
    
    This link expires in {PASSWORD_RESET_TOKEN_EXPIRE_HOURS} hour(s).
    
    If you didn't request this, please ignore this email.
    
    Ramadan Mubarak!
    """
    
    email_sent = send_email(to_email, subject, html_content, text_content)
    
    return {
        "email_sent": email_sent,
        "token": token,
        "reset_link": reset_link,
        "expires_in_hours": PASSWORD_RESET_TOKEN_EXPIRE_HOURS
    }


def send_welcome_email(to_email: str, name: str) -> bool:
    """
    Send welcome email after successful verification
    """
    subject = "🌙 Welcome to Ramadan Helper!"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #1A1A2E; color: #E5E7EB; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%); border-radius: 16px; padding: 40px; border: 1px solid rgba(212,175,55,0.3); }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .logo {{ font-size: 48px; margin-bottom: 10px; }}
            h1 {{ color: #D4AF37; font-size: 28px; margin: 0; }}
            .subtitle {{ color: #9CA3AF; margin-top: 8px; }}
            .content {{ margin: 30px 0; line-height: 1.6; }}
            .feature {{ background: rgba(13, 92, 46, 0.2); padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #0D5C2E; }}
            .footer {{ text-align: center; margin-top: 30px; color: #6B7280; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">☪️</div>
                <h1>Welcome to Ramadan Helper!</h1>
                <p class="subtitle">Your account is now verified ✅</p>
            </div>
            
            <div class="content">
                <p>Assalamu Alaikum <strong>{name}</strong>,</p>
                <p>Alhamdulillah! Your email has been verified and your account is now active.</p>
                <p>Here's what you can do with Ramadan Helper:</p>
                
                <div class="feature">📿 <strong>Dua Generator</strong> - Get personalized duas for any situation</div>
                <div class="feature">🔍 <strong>AI Analyzer</strong> - Find relevant Quran verses and Hadith</div>
                <div class="feature">💬 <strong>Chat with Imams</strong> - Get guidance from qualified scholars</div>
                <div class="feature">📺 <strong>Islamic Videos</strong> - Watch educational content</div>
                <div class="feature">📅 <strong>Events</strong> - Find Islamic events in your area</div>
                
                <p>May Allah bless your journey of faith! 🌙</p>
            </div>
            
            <div class="footer">
                <p>☪️ Ramadan Mubarak</p>
                <p>© 2026 Ramadan Helper. May Allah accept from us.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Assalamu Alaikum {name},
    
    Alhamdulillah! Your email has been verified and your account is now active.
    
    You can now use all features of Ramadan Helper:
    - Dua Generator
    - AI Analyzer
    - Chat with Imams
    - Islamic Videos
    - Events
    
    May Allah bless your journey of faith!
    
    Ramadan Mubarak!
    """
    
    return send_email(to_email, subject, html_content, text_content)
