import os
import time
import json
import datetime
import base64
from telethon import TelegramClient
from dotenv import load_dotenv
from scripts.utils.logger import setup_logger

# Setup logger
logger = setup_logger(__name__)

# Load env vars
load_dotenv()
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_NAME = "session_name"

RAW_DATA_DIR = "data/raw/telegram_messages"
CHANNEL_LIST_FILE = "scripts/scraping/channel_list.txt"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Custom JSON encoder for datetime and bytes serialization
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, bytes):
            return base64.b64encode(obj).decode('utf-8')
        return super().default(obj)

async def scrape_channel(channel):
    logger.info(f"Scraping channel: {channel}")
    messages = []
    try:
        async for msg in client.iter_messages(channel, limit=1000):
            messages.append(msg.to_dict())
    except Exception as e:
        logger.error(f"Error scraping {channel}: {e}")
        return

    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    filename = os.path.join(RAW_DATA_DIR, f"{channel.replace('@', '')}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2, cls=DateTimeEncoder)

    logger.info(f"Saved {len(messages)} messages from {channel} to {filename}")

async def main():
    await client.start()
    logger.info("Telegram client started")

    with open(CHANNEL_LIST_FILE, "r") as f:
        channels = [line.strip() for line in f if line.strip()]

    for channel in channels:
        await scrape_channel(channel)
        time.sleep(1)  # Avoid rate limits

    await client.disconnect()
    logger.info("Telegram client disconnected")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())