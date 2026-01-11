"""
Services module for backend functionality
"""
from .email_service import (
    send_verification_email,
    send_password_reset_email,
    send_welcome_email,
    generate_verification_token
)
