import os
from dotenv import load_dotenv

load_dotenv()

def get_telegram_bot_token() -> str:
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        raise RuntimeError("Couldn't read TOKEN from the environment")
    
    return TOKEN