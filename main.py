import asyncio
import logging
import os
import sys

import nest_asyncio
from dotenv import load_dotenv

from modules.camera import capture_image
from modules.game_pings import get_game_pings
from modules.internet_metrics import get_internet_metrics
from modules.telegram_utils import send_internet_metrics_to_telegram
from modules.weather import get_weather

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Define your environment variables
RTSP_URL = os.getenv("RTSP_URL")
OUTPUT_PATH = os.getenv("OUTPUT_PATH")
TG_BOT_API_KEY = os.getenv("TG_BOT_API_KEY")
TG_CHANNEL_ID = os.getenv("TG_CHANNEL_ID")
STARLINK_NAME = os.getenv("STARLINK_NAME")
RUN_EVERY_X_MIN = int(os.getenv("RUN_EVERY_X_MIN", 15))  # Every 15 minutes
LATITUDE = float(os.getenv("LATITUDE"))
LONGITUDE = float(os.getenv("LONGITUDE"))

nest_asyncio.apply()


async def job():
    try:
        logger.info("Starting job...")

        # Capture an image
        image_path = capture_image(RTSP_URL, OUTPUT_PATH)
        logger.info(f"Image captured: {image_path}")

        if image_path:
            # Get internet metrics
            internet_metrics = get_internet_metrics()
            logger.info(f"Internet metrics: {internet_metrics}")

            game_pings = get_game_pings()
            weather_data = get_weather(LATITUDE, LONGITUDE)

            # Send internet metrics and image to Telegram
            await send_internet_metrics_to_telegram(TG_BOT_API_KEY, TG_CHANNEL_ID, internet_metrics, image_path,
                                                    STARLINK_NAME, weather_data, game_pings)
            logger.info("Metrics sent to Telegram")
        else:
            logger.warning("No image")
        logger.info("Job completed.")
    except Exception as e:
        logger.error(f"An error occurred in the job: {e}")


async def main():
    try:
        while True:
            await job()
            await asyncio.sleep(RUN_EVERY_X_MIN * 60)  # Convert minutes to seconds
    except KeyboardInterrupt:
        logger.info("Received KeyboardInterrupt. Exiting...")
        sys.exit(0)


if __name__ == '__main__':
    asyncio.run(main())
