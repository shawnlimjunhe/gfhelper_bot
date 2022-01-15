from telegram import Update, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
  CallbackContext,
  CommandHandler,
  )

from common import (
    bot_face
)

def help(update: Update, context: CallbackContext):
  text = (bot_face + 
    "Here are a list of commands to help you\n\n"
    "/sleep: Calculate sleep and wake up times 💤\n"
    "/est: estimate what time you need to leave ⏱️\n"
    "/help: HELP! 🦮\n\n"
    "Use /help <command name> for more information!")
  context.bot.send_message(chat_id=update.effective_chat.id, text=text)

help_handler = CommandHandler('help', help)