from dagster import op
import subprocess

@op
def scrape_telegram_channels():
    """
    Scrapes all channels and downloads images using subprocess.
    Assumes scripts are already working and use channel_list.txt.
    """
    print("🔁 Starting Telegram scraping and image download...")

    try:
        # Scrape Telegram messages
        subprocess.run(["python", "scripts/scraping/scrape_all_channels.py"], check=True)

        # Download images
        subprocess.run(["python", "scripts/scraping/download_images.py"], check=True)

        print("✅ Scraping and image download complete.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Scraping step failed: {e}")
        raise
