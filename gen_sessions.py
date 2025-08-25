from telethon.sync import TelegramClient
from telethon.sessions import StringSession

API_ID = int(input("Enter API_ID: ").strip())
API_HASH = input("Enter API_HASH: ").strip()

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print("\n==== COPY YOUR SESSION STRING BELOW ====\n")
    print(client.session.save())
    print("\n==== KEEP THIS SECRET ====\n")
