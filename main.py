import asyncio
import datetime
import io
import logging
import os

import pytz
from telethon import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest

from funcs import ConfigParser, get_weather, get_image

if not os.path.exists("user.session"):
    raise Exception("You need execute log_in.py file first!")

logging.basicConfig(level=logging.INFO)
client = TelegramClient("user", ConfigParser.getint("Telegram", "api_id"), ConfigParser.get("Telegram", "api_hash"))
client.start()


async def main():
    logging.info("Bot started")
    while True:
        logging.info("Getting weather...")
        temp = get_weather()
        logging.info("Render image...")
        avatar = get_image(
            datetime.datetime.now(tz=pytz.timezone(ConfigParser.get("Data", "locale"))),
            temp
        )

        avatar_file = io.BytesIO()
        avatar.save(avatar_file, "JPEG")
        avatar_file.seek(0)

        logging.info("Clear avatars...")
        await client(DeletePhotosRequest(await client.get_profile_photos('me')))
        logging.info("Sending photo...")
        await client(UploadProfilePhotoRequest(await client.upload_file(avatar_file)))
        logging.info("Picture changed")

        d = datetime.datetime.now(tz=pytz.timezone(ConfigParser.get("Data", "locale")))
        await asyncio.sleep(60 - d.second)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())