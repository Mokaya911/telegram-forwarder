import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from telethon import TelegramClient, events
from telethon.sessions import StringSession

# -------------------------------
# CONFIG
# -------------------------------
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# -------------------------------
# EMAIL SENDER
# -------------------------------
def send_email(subject, body, attachments=None):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    if attachments:
        for file_path in attachments:
            with open(file_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file_path)}")
            msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

# -------------------------------
# TELEGRAM CLIENT
# -------------------------------
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    sender = await event.get_sender()
    chat = await event.get_chat()

    sender_name = getattr(sender, "first_name", "Unknown")
    if getattr(sender, "last_name", None):
        sender_name += f" {sender.last_name}"
    if getattr(sender, "username", None):
        sender_name += f" (@{sender.username})"

    chat_type = "Private Chat"
    chat_name = ""
    if getattr(chat, "title", None):  # groups/channels have titles
        chat_type = "Group/Channel"
        chat_name = chat.title

    message_text = event.message.message or "[Media Only]"

    # save media if exists
    attachments = []
    if event.message.media:
        file_path = await event.message.download_media()
        attachments.append(file_path)

    # SUBJECT LINE now clearly shows source
    if chat_type == "Private Chat":
        subject = f"📩 Private | {sender_name}"
    else:
        subject = f"👥 {chat_name} | {sender_name}"

    # BODY
    body = f"""
Source: {chat_type}
Chat: {chat_name if chat_name else 'Direct Message'}
Sender: {sender_name}

Message:
{message_text}
"""

    send_email(subject, body.strip(), attachments)

def run_worker():
    print("📡 Listening for Telegram messages...")
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    run_worker()
