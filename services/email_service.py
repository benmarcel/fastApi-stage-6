from fastapi_mail import FastMail, MessageSchema, MessageType
from config.config import conf
from pydantic import NameEmail
FRONTEND_RESET_URL = "http://localhost:3000/reset-password"  # swap for your real frontend route

async def send_reset_email(to_email: str, reset_token: str) -> None:
    reset_link = f"{FRONTEND_RESET_URL}?token={reset_token}"
    html = f"""
    <p>You requested a password reset.</p>
    <p><a href="{reset_link}">Click here to reset your password</a></p>
    <p>This link expires in 15 minutes. If you didn't request this, ignore this email.</p>
    """

    message = MessageSchema(
        subject="Reset Your Password",
        recipients=[NameEmail(name="", email=to_email)],
        body=html,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)