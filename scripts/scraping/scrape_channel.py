import os
import json
import asyncio
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

DATA_DIR = "data/raw/telegram_messages"

async def scrape_channel(channel_username, limit=100):
    os.makedirs(DATA_DIR, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{DATA_DIR}/{today}_{channel_username.replace('@', '')}.json"

    async with TelegramClient('anon', api_id, api_hash) as client:
        messages = []
        async for message in client.iter_messages(channel_username, limit=limit):
            msg = {
                "id": message.id,
                "date": message.date.strftime("%Y-%m-%d %H:%M:%S"),
                "sender_id": getattr(message.sender_id, 'user_id', None),
                "text": message.text,
                "has_photo": isinstance(message.media, MessageMediaPhoto)
            }
            messages.append(msg)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)

        print(f"✅ Saved {len(messages)} messages to {filename}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("❌ Usage: python scrape_channel.py <channel_username>")
        exit(1)

    channel = sys.argv[1]
    asyncio.run(scrape_channel(channel))
