import os
import html
import traceback
import json
import telegram

from setuptools import Command
from telegram import Update, ReplyKeyboardMarkup, ParseMode
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters
)
import logging
from dotenv import load_dotenv

from common import bot_face
from commands import (
    est,
    sleep,
    help
)

load_dotenv('./.env')
API_KEY = os.environ["API_KEY"]
DEVELOPER_CHAT_ID = os.environ["DEVELOPER_CHAT_ID"]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    text = bot_face + \
        f'beep boop\nHello there {update.message.from_user.first_name}!\Anything i can /help you with?'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text)


def caps(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="🤖: Sorry, I didn't understand that command.")


def error_handler(update: object, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:",
                 exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    # Finally, send the message
    context.bot.send_message(chat_id=DEVELOPER_CHAT_ID,
                             text=message, parse_mode=ParseMode.HTML)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="🤖: Sorry, an error has occurred, please contact shawn")


def main() -> None:
    """Run bot."""

    updater = Updater(API_KEY, use_context=True)

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)

    #echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    #caps_handler = CommandHandler('caps', caps)
    unknown_handler = MessageHandler(Filters.command, unknown)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help.help_handler)
    # dispatcher.add_handler(caps_handler)
    dispatcher.add_handler(est.est_convo_handler)
    dispatcher.add_handler(sleep.sleep_convo_handler)
    # dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(unknown_handler)

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
