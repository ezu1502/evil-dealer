from ..config import get_telegram_bot_token
from engine import Game

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


TOKEN: str = get_telegram_bot_token()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    
    await update.message.reply_text(
        "The Evil Dealer rests on his chair, while counting all the chips he's taken from miserable players like you.\n"
        "Are you willing to challenge him?"
    )

def main() -> None:
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Evil Dealer is online!")

    app.run_polling()


if __name__ == "__main__":
    main()

# TODO continuar aqui!!!!! Ligar a Engine ao bot
