# modules/telegram_utils.py
from typing import Dict, Any

from telegram import Bot, InputMediaPhoto
from telegram.constants import ParseMode

from modules.weather import weather_codes


async def send_telegram_message(bot_token: str, chat_id: str, message: str, photo_path: str = None,
                                sat_image_path: str = None) -> None:
    """
    Send a message to a Telegram channel or chat.

    Parameters:
    - bot_token (str): The Telegram Bot API token.
    - chat_id (str): The ID of the Telegram channel or chat.
    - message (str): The message to send.
    - photo_path (str, optional): The path to the photo to send.
    """
    bot = Bot(token=bot_token)

    sky_image = InputMediaPhoto(open(photo_path, 'rb'))
    sat_image = InputMediaPhoto(media=sat_image_path)
    print(sat_image)

    if photo_path:
        await bot.send_media_group(chat_id=chat_id, media=[sky_image, sat_image], caption=message,
                                   parse_mode=ParseMode.HTML)
    else:
        await bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)


async def send_internet_metrics_to_telegram(
        bot_token: str, chat_id: str, internet_metrics: Dict[str, float], image_path: str, STARLINK_NAME: str,
        weather_forecast: Dict[str, Any], game_pings: Dict[str, Any], sat_image: str
) -> None:
    """
    Send internet metrics and an image to a Telegram channel or chat.

    Parameters:
    - bot_token (str): The Telegram Bot API token.
    - chat_id (str): The ID of the Telegram channel or chat.
    - internet_metrics (Dict[str, float]): Dictionary containing 'download_speed',
                                            'upload_speed', 'ping' and 'fast_download_speed'
    - image_path (str): The path to the image to send.
    - STARLINK_NAME (str): The location of Starlink for customization
    - game_pings (Dict[str, Any]): Dictionary containing game pings
    - weather_forecast (Dict[str, Any]): Dictionary containing game pings
    - sat_image (str): Satellite image
    """
    message = (
        f'<b><u>Starlink Stats for {STARLINK_NAME}</u></b>\n\n'
        f'<b>Speedtest by Ookla</b>\n'
        f'🌐 ISP: {internet_metrics["isp"]}\n'
        f'⬇️ Download Speed: {internet_metrics["download_speed"]:.2f} Mbps\n'
        f'⬆️ Upload Speed: {internet_metrics["upload_speed"]:.2f} Mbps\n'
        f'🏓 Latency: {internet_metrics["ping"]:.2f} ms\n\n'
        f'<b>Speedtest by Fast</b>\n'
        f'⬇️ Download Speed: {internet_metrics["fast_download_speed"]:.2f} Mbps\n\n'
        f'🔫 CS2 Singapore Ping: {game_pings["cs2_sgp"]}\n'
        f'🔫 CS2 Bombay Ping: {game_pings["cs2_bom"]}\n'
        f'🔫 Valorant SEA Ping: {game_pings["valo_sea"]}\n\n'
        f"💧 Relative Humidity: {weather_forecast['relative_humidity_2m']}%\n"
        f"🌧️ Precipitation: {weather_forecast['precipitation']} mm\n"
        f"🌧️ Rain: {weather_forecast['rain']} mm\n"
        f"🌧️ Showers: {weather_forecast['showers']} mm\n"
        f"🌥️ Weather: {weather_codes.get(weather_forecast['weather_code'], 'Unknown')}\n"
        f"☁️ Cloud Cover: {weather_forecast['cloud_cover']}%\n"
        f"🌬️ Wind Speed: {weather_forecast['wind_speed_10m']:.2f} km/h\n"
        f"🧭 Wind Direction: {weather_forecast['wind_direction_10m']:.2f}°\n"
        f"💨 Wind Gusts: {weather_forecast['wind_gusts_10m']:.2f} km/h"
    )
    print(sat_image)
    await send_telegram_message(bot_token, chat_id, message, photo_path=image_path, sat_image_path=sat_image)
