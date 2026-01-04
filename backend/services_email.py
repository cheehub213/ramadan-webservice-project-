import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailService:
    '''Email service for sending verification codes'''
    
    # Gmail SMTP Configuration
    # To use this, you need to:
    # 1. Create a Gmail App Password at: https://myaccount.google.com/apppasswords
    # 2. Set environment variables or update these values
    
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "cheehub.business111@gmail.com")  # Your Gmail address
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "pbnxsipzmrgulaxx")  # Gmail App Password (not regular password)
    
    @classmethod
    def send_verification_email(cls, to_email: str, verification_code: str, user_name: str = "User") -> bool:
        '''Send verification code to user's email'''
        
        if not cls.EMAIL_ADDRESS or not cls.EMAIL_PASSWORD:
            print(f"[EMAIL SERVICE] Email not configured. Code for {to_email}: {verification_code}")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = ' Ramadan Helper - Verify Your Email'
            msg['From'] = f'Ramadan Helper <{cls.EMAIL_ADDRESS}>'
            msg['To'] = to_email
            
            # Plain text version
            text = f'''
Assalamu Alaikum {user_name}!

Welcome to Ramadan Helper! 

Your verification code is: {verification_code}

Enter this 6-digit code in the app to verify your email.

If you didn't create this account, please ignore this email.

May Allah bless you,
Ramadan Helper Team
'''
            
            # HTML version
            html = f'''
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f3f4f6; margin: 0; padding: 20px; }}
        .container {{ max-width: 500px; margin: 0 auto; background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #047857, #059669); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 24px; }}
        .content {{ padding: 30px; text-align: center; }}
        .code-box {{ background: #f0fdf4; border: 2px dashed #10b981; border-radius: 12px; padding: 20px; margin: 20px 0; }}
        .code {{ font-size: 36px; font-weight: bold; color: #047857; letter-spacing: 8px; }}
        .footer {{ background: #f9fafb; padding: 20px; text-align: center; color: #6b7280; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1> Ramadan Helper</h1>
            <p>Email Verification</p>
        </div>
        <div class="content">
            <h2>Assalamu Alaikum {user_name}!</h2>
            <p>Welcome to Ramadan Helper! Please verify your email to get started.</p>
            <div class="code-box">
                <p style="margin: 0 0 10px 0; color: #6b7280;">Your verification code:</p>
                <div class="code">{verification_code}</div>
            </div>
            <p style="color: #6b7280;">Enter this code in the app to complete your registration.</p>
        </div>
        <div class="footer">
            <p>If you didn't create this account, please ignore this email.</p>
            <p> 2026 Ramadan Helper. May Allah accept from us.</p>
        </div>
    </div>
</body>
</html>
'''
            
            msg.attach(MIMEText(text, 'plain'))
            msg.attach(MIMEText(html, 'html'))
            
            # Send email
            with smtplib.SMTP(cls.SMTP_SERVER, cls.SMTP_PORT) as server:
                server.starttls()
                server.login(cls.EMAIL_ADDRESS, cls.EMAIL_PASSWORD)
                server.sendmail(cls.EMAIL_ADDRESS, to_email, msg.as_string())
            
            print(f"[EMAIL SERVICE] Verification email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"[EMAIL SERVICE] Failed to send email: {e}")
            return False
    
    @classmethod
    def is_configured(cls) -> bool:
        '''Check if email service is properly configured'''
        return bool(cls.EMAIL_ADDRESS and cls.EMAIL_PASSWORD)

    @classmethod
    def send_password_reset_email(cls, to_email: str, reset_code: str, user_name: str = "User") -> bool:
        '''Send password reset code to user's email'''

        if not cls.EMAIL_ADDRESS or not cls.EMAIL_PASSWORD:
            print(f"[EMAIL SERVICE] Email not configured. Reset code for {to_email}: {reset_code}")
            return False

        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = ' Ramadan Helper - Password Reset'
            msg['From'] = f'Ramadan Helper <{cls.EMAIL_ADDRESS}>'
            msg['To'] = to_email

            text = f'''
Assalamu Alaikum {user_name}!

You requested to reset your password for Ramadan Helper.

Your password reset code is: {reset_code}

Enter this 6-digit code in the app to reset your password.

If you didn't request this, please ignore this email - your password will remain unchanged.

May Allah bless you,
Ramadan Helper Team
'''

            html = f'''
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f3f4f6; margin: 0; padding: 20px; }}
        .container {{ max-width: 500px; margin: 0 auto; background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #dc2626, #b91c1c); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 24px; }}
        .content {{ padding: 30px; text-align: center; }}
        .code-box {{ background: #fef2f2; border: 2px dashed #ef4444; border-radius: 12px; padding: 20px; margin: 20px 0; }}
        .code {{ font-size: 36px; font-weight: bold; color: #dc2626; letter-spacing: 8px; }}
        .footer {{ background: #f9fafb; padding: 20px; text-align: center; color: #6b7280; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1> Password Reset</h1>
            <p>Ramadan Helper</p>
        </div>
        <div class="content">
            <h2>Assalamu Alaikum {user_name}!</h2>
            <p>You requested to reset your password. Use the code below:</p>
            <div class="code-box">
                <p style="margin: 0 0 10px 0; color: #6b7280;">Your reset code:</p>
                <div class="code">{reset_code}</div>
            </div>
            <p style="color: #6b7280;">This code expires in 15 minutes.</p>
        </div>
        <div class="footer">
            <p>If you didn't request this, please ignore this email.</p>
            <p> 2026 Ramadan Helper</p>
        </div>
    </div>
</body>
</html>
'''

            msg.attach(MIMEText(text, 'plain'))
            msg.attach(MIMEText(html, 'html'))

            with smtplib.SMTP(cls.SMTP_SERVER, cls.SMTP_PORT) as server:
                server.starttls()
                server.login(cls.EMAIL_ADDRESS, cls.EMAIL_PASSWORD)
                server.sendmail(cls.EMAIL_ADDRESS, to_email, msg.as_string())

            print(f"[EMAIL SERVICE] Password reset email sent to {to_email}")
            return True

        except Exception as e:
            print(f"[EMAIL SERVICE] Failed to send password reset email: {e}")
            return False

    @classmethod
    def send_password_reset_email(cls, to_email: str, reset_code: str, user_name: str = "User") -> bool:
        '''Send password reset code to user's email'''

        if not cls.EMAIL_ADDRESS or not cls.EMAIL_PASSWORD:
            print(f"[EMAIL SERVICE] Email not configured. Reset code for {to_email}: {reset_code}")
            return False

        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = ' Ramadan Helper - Password Reset'
            msg['From'] = f'Ramadan Helper <{cls.EMAIL_ADDRESS}>'
            msg['To'] = to_email

            text = f'''
Assalamu Alaikum {user_name}!

You requested to reset your password for Ramadan Helper.

Your password reset code is: {reset_code}

Enter this 6-digit code in the app to reset your password.

If you didn't request this, please ignore this email - your password will remain unchanged.

May Allah bless you,
Ramadan Helper Team
'''

            html = f'''
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f3f4f6; margin: 0; padding: 20px; }}
        .container {{ max-width: 500px; margin: 0 auto; background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #dc2626, #b91c1c); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 24px; }}
        .content {{ padding: 30px; text-align: center; }}
        .code-box {{ background: #fef2f2; border: 2px dashed #ef4444; border-radius: 12px; padding: 20px; margin: 20px 0; }}
        .code {{ font-size: 36px; font-weight: bold; color: #dc2626; letter-spacing: 8px; }}
        .footer {{ background: #f9fafb; padding: 20px; text-align: center; color: #6b7280; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1> Password Reset</h1>
            <p>Ramadan Helper</p>
        </div>
        <div class="content">
            <h2>Assalamu Alaikum {user_name}!</h2>
            <p>You requested to reset your password. Use the code below:</p>
            <div class="code-box">
                <p style="margin: 0 0 10px 0; color: #6b7280;">Your reset code:</p>
                <div class="code">{reset_code}</div>
            </div>
            <p style="color: #6b7280;">This code expires in 15 minutes.</p>
        </div>
        <div class="footer">
            <p>If you didn't request this, please ignore this email.</p>
            <p> 2026 Ramadan Helper</p>
        </div>
    </div>
</body>
</html>
'''

            msg.attach(MIMEText(text, 'plain'))
            msg.attach(MIMEText(html, 'html'))

            with smtplib.SMTP(cls.SMTP_SERVER, cls.SMTP_PORT) as server:
                server.starttls()
                server.login(cls.EMAIL_ADDRESS, cls.EMAIL_PASSWORD)
                server.sendmail(cls.EMAIL_ADDRESS, to_email, msg.as_string())

            print(f"[EMAIL SERVICE] Password reset email sent to {to_email}")
            return True

        except Exception as e:
            print(f"[EMAIL SERVICE] Failed to send password reset email: {e}")
            return False
