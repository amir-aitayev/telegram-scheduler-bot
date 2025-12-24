import os
import asyncio
from zoneinfo import ZoneInfo
from aiogram import Bot
from aiogram.types import FSInputFile, Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiohttp import ClientError

# ====== CONFIG ======
TOKEN = os.getenv("BOT_TOKEN")  # place the bot token here
CHAT_ID = os.getenv("CHAT_ID")  # place the chat id here
TZ = ZoneInfo("Europe/Rome")

VIDEO_FILE = ""  # your video file
HOURLY_CAPTION = (
"""

"""
)
GOODNIGHT_TEXT = "Good night! 🌙✨"
# =====================

bot = Bot(token=TOKEN)
last_message_id: int | None = None


async def delete_previous_if_any():
    global last_message_id
    if last_message_id is None:
        return
    try:
        await bot.delete_message(CHAT_ID, last_message_id)
        print(f"[OK] Deleted previous message: {last_message_id}")
    except Exception as e:
        print(f"[WARN] Delete previous failed: {e}")
    finally:
        last_message_id = None


async def send_with_retry(coro_fn, *, tries=3, base_delay=2.0):
    attempt = 0
    while True:
        try:
            return await coro_fn()
        except (TimeoutError, ClientError) as e:
            attempt += 1
            if attempt >= tries:
                print(f"[ERROR] Send failed after {tries} tries: {e}")
                raise
            delay = base_delay * (2 ** (attempt - 1))
            print(f"[WARN] Network issue ({e}). Retry in {delay:.1f}s...")
            await asyncio.sleep(delay)


async def send_hourly():
    global last_message_id
    await delete_previous_if_any()
    try:
        async def _send():
            return await bot.send_message(
                CHAT_ID,
                HOURLY_CAPTION
            )

        msg: Message = await send_with_retry(_send)
        last_message_id = msg.message_id
        print(f"[OK] Hourly message sent, id={last_message_id}")
    except Exception as e:
        print(f"[ERROR] Hourly send failed: {e}")



async def send_goodnight():
    global last_message_id
    await delete_previous_if_any()
    try:
        async def _send():
            return await bot.send_message(CHAT_ID, GOODNIGHT_TEXT)

        msg: Message = await send_with_retry(_send)
        last_message_id = msg.message_id
        print(f"[OK] Goodnight sent, id={last_message_id}")
    except Exception as e:
        print(f"[ERROR] Goodnight send failed: {e}")


async def main():
    scheduler = AsyncIOScheduler(
        timezone=TZ,
        job_defaults={
            "coalesce": True,
            "max_instances": 1,
            "misfire_grace_time": 3600,
        },
    )
    # Hourly at :00 from 08:00–23:00
    scheduler.add_job(send_hourly, "cron", minute=0, hour="8-23")
    # Goodnight at 00:00
    scheduler.add_job(send_goodnight, "cron", minute=0, hour=0)

    scheduler.start()
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())


