from email.message import EmailMessage
from config import settings
import aiosmtplib

async def send_verification_letter(recipient_email: str, otp_code: str):
    message = EmailMessage()
    message['From'] = settings.smtp_user
    message["To"] = recipient_email
    message["Subject"] = "Verify Your Email Address"
    message.set_content(
        f"""
        Verify your email address.

        Your verification code is: {otp_code}

        This code expires in 10 minutes.

        If you didn't create an account, you can safely ignore this email.
        
        Smart Courier Assistant Team
        """
    )
    await aiosmtplib.send(message, hostname=settings.smtp_host, use_tls=True, port=settings.smtp_port, username=settings.smtp_user, password=settings.smtp_password)