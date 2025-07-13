import os
import json
from telethon import TelegramClient
from dotenv import load_dotenv
from scripts.utils.logger import setup_logger

logger = setup_logger(__name__)

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_NAME = "session_name"

RAW_DATA_DIR = "data/raw/telegram_messages"
IMAGES_DIR = "data/images"
MAX_IMAGES = 100

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def download_images_from_file(json_filepath):
    logger.info(f"Processing {json_filepath}")
    with open(json_filepath, "r", encoding="utf-8") as f:
        messages = json.load(f)

    if not messages:
        logger.warning("No messages found in file.")
        return

    channel_name = os.path.splitext(os.path.basename(json_filepath))[0]
    save_folder = os.path.join(IMAGES_DIR, channel_name)
    os.makedirs(save_folder, exist_ok=True)

    downloaded_count = 0
    for msg in messages:
        if downloaded_count >= MAX_IMAGES:
            logger.info(f"Reached limit of {MAX_IMAGES} images for {channel_name}")
            break

        msg_id = msg.get("id")
        try:
            message = await client.get_messages(channel_name, ids=msg_id)
            if message and message.media and message.photo:
                filename = os.path.join(save_folder, f"{msg_id}.jpg")
                if os.path.exists(filename):
                    logger.info(f"Image {msg_id} already exists, skipping.")
                    continue
                await message.download_media(file=filename)
                logger.info(f"Downloaded image {msg_id} to {filename}")
                downloaded_count += 1
        except Exception as e:
            logger.error(f"Error downloading image {msg_id}: {e}")

    logger.info(f"Finished {channel_name}: Downloaded {downloaded_count} images")

async def main():
    await client.start()
    logger.info("Telegram client started")

    for root, _, files in os.walk(RAW_DATA_DIR):
        for file in files:
            if file.endswith(".json"):
                filepath = os.path.join(root, file)
                await download_images_from_file(filepath)

    await client.disconnect()
    logger.info("Telegram client disconnected")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())