from telegram import Update, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    CallbackContext,
    CommandHandler,
)

from common import (
    bot_face
)


def help(update: Update, context: CallbackContext):
    default_text = (bot_face +
                    "Here's how i can help you!\n\n"
                    "/sleep: Calculate sleep and wake up times 💤\n"
                    "/est: estimate what time you need to leave ⏱️\n"
                    "/help: HELP! 🦮\n\n"
                    "Use /help <command name> for more information!")
    command_map = {
        "est": (
            "Estimates the time to start getting ready\n"
            "and the time to leave your house to\n"
            "reach your destination on time"
        ),
        "sleep": (
            "Calculates what time you should wake up at\n"
            "or sleep by using the 90 minute rule\n"
            "to help you feel less groggy when you wake up!"
        )
    }

    if not (context.args):
        text = default_text
    else:
        help_text = (context.args)[0]
        if help_text not in command_map:
            text = (bot_face +
                    "Sorry, that command does not exist :("
                    )
        else:
            text = bot_face + command_map[help_text]
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


help_handler = CommandHandler('help', help)
