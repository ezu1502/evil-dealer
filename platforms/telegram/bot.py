from __future__ import annotations

from platforms.config import get_telegram_bot_token
from engine import Game

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import CallbackQueryHandler

from engine.core import Message
from engine.enums import Actions, TurnState as TS


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

    query: CallbackQuery = update.callback_query
    await query.answer()

    if query.data is None:
        return

    action = Actions(query.data)

    if action == Actions.PLAY_AGAIN:
        game = Game().prepare_game()
        context.user_data["game"] = game
        await flush_messages(game = game, update = update)

        return

    _game = context.user_data.get("game")
    if _game is None:
        return
    game: Game = _game


        

    if not game.check_state(TS.FINISHED):
        game.player_action(action)

        await flush_messages(game = game, update = update)

        if game.check_state(TS.DEALER_TURN):
            game.dealer_turn()

            await flush_messages(game = game, update = update)


            if game.check_state(TS.FINISHED):
                winner = game.determine_winner()

                if winner is None:
                    if game.player.score != game.dealer.score:
                        raise RuntimeError("Winner was None while their scores were different")
                    
                    await send_message(
                        f"No winners this round! Both you and the Evil Dealer got {game.player.score}",
                        update = update
                    )
                else:
                    winner_str: str = "YOU" if winner is game.player else "The Evil Dealer"

                    await send_message(
                        f"The winner is... {winner_str}!\n"
                        f"With {winner.score} points",
                        update = update
                    )

                await send_message(
                    Message(
                        "Do you want to play again?",
                        options = (("Yes", Actions.PLAY_AGAIN), ("No", Actions.END))
                    ),
                    update = update
                )
            return



            
    else:
        if action == Actions.END:
            del context.user_data["game"]
            del game

            await send_message(
                Message(
                    "Thank you for wasting your time (and chips).\n"
                    "If you wanna play again, tap the button below or type the command /play",

                    options = (("PLAY again", Actions.PLAY_AGAIN),)
                ),
                update = update
            )

        else:
            raise RuntimeError("Invalid Action given at current TurnState")


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
