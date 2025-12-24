# Telegram Scheduled Message Bot

A simple asynchronous Telegram bot that sends:
- **Hourly messages** at a fixed schedule
- A **daily “Good night” message** at midnight

Built with **aiogram**, **asyncio**, and **APScheduler**.  
Designed to be easy to configure using environment variables.

---

## ✨ Features
- Hourly scheduled messages (08:00–23:00)
- Daily goodnight message at 00:00
- Automatic deletion of the previous message to avoid chat clutter
- Retry mechanism with exponential backoff for network errors
- Timezone-aware scheduling

---

## 🛠️ Technologies Used
- Python 3.9+
- aiogram
- APScheduler
- asyncio
- aiohttp

---

## ⚙️ Configuration (Environment Variables)

Before running the bot, set the following environment variables:

```bash
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_chat_or_user_id
TZ=your_location
How to get these values
BOT_TOKEN: Create a bot via @BotFather
CHAT_ID:
For private chat: use @userinfobot
For group/channel: add the bot and get the chat ID
▶️ How to Run
1. Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate
2. Install dependencies
pip install aiogram APScheduler aiohttp
3. Run the bot
python bot.py
⏰ Scheduling Logic
Hourly message: every hour from 08:00 to 23:00
Goodnight message: once per day at 00:00
All times follow the configured timezone
⚠️ Notes
The bot must be started in Telegram (/start) before it can send messages
For channels or groups, the bot must have permission to post and delete messages
📌 License
This project is for educational and personal use.
