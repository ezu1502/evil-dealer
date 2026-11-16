from __future__ import annotations

from platforms.config import get_telegram_bot_token
from engine import Game

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import CallbackQueryHandler

from engine.core import Message
from engine.enums import Actions


TOKEN: str = get_telegram_bot_token()

async def flush_messages(*, game: Game, update: Update) -> None:
    while (message := game.get_message()) is not None:
        await send_message(message, update = update)

async def send_message(message: str | Message, *, update: Update) -> None:
    """
        Converts a Message object into a Telegram message, then sends it.
    """
    target = update.effective_message

    if not message or target is None:
        return

    if isinstance(message, str):
        await target.reply_text(message)
        return

    if not message.options:
        await target.reply_text(message.text)
        return


    keyboard = [[
        InlineKeyboardButton(option_text, callback_data = option_action.value)
        for option_text, option_action in message.options
    ]]

    markup = InlineKeyboardMarkup(keyboard)

    await target.reply_text(
        message.text,
        reply_markup = markup
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    
    await send_message(
        "The Evil Dealer rests on his chair, while counting all the chips he's taken from miserable players like you.\n"
        "Are you willing to challenge him?\n\n"

        "To start a game, type /play",

        update = update
    )

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    if context.user_data is None:
        return

    game = Game().prepare_game()

    context.user_data["game"] = game

    await flush_messages(game = game, update = update)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query is None:
        return
    if context.user_data is None:
        return

    _game = context.user_data.get("game")
    
    if _game is None:
        return

    game: Game = _game

    query: CallbackQuery = update.callback_query
    await query.answer()

    if query.data is None:
        return

    action = Actions(query.data)

    game.player_action(action)

    await flush_messages(game = game, update = update)

    
    
    
    




    



def main() -> None:
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))

    app.add_handler(CallbackQueryHandler(handle_callback))

    print("Evil Dealer is online!")

    app.run_polling()


if __name__ == "__main__":
    main()

# TODO continuar aqui!!!!! Ligar a Engine ao bot
