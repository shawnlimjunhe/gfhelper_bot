import common
from telegram import Update, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    CallbackContext,
    CommandHandler,
)

help_default_txt = (
    common.hedgehog +
    "Here's how i can help you!\n\n"
    "/sleep: Calculate sleep and wake up times 💤\n"
    "/est: estimate what time you need to leave ⏱️\n"
    "/help: HELP! 🦮\n\n"
    "Use /help <command name> for more information!"
)

command_mapping = {
    "est": (
        common.hedgehog +
        "Estimates the time to start getting ready\n"
        "and the time to leave your house to\n"
        "reach your destination on time"
    ),
    "sleep": (
        common.hedgehog +
        "Calculates what time you should wake up at\n"
        "or sleep by using the 90 minute rule\n"
        "to help you feel less groggy when you wake up!"
    )
}

invalid_command_txt = (
    common.hedgehog +
    "Sorry, I did not understand that command :("
)


def help(update: Update, context: CallbackContext):
    if not (context.args):
        text = help_default_txt
    else:
        help_text = (context.args)[0]
        if help_text not in command_mapping:
            text = invalid_command_txt
        else:
            text = command_mapping[help_text]
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


help_handler = CommandHandler('help', help)
