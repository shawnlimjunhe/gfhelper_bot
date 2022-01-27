from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
)

hedgehog = '🦔: \n'
hhmm_regex = '^\d{1,}\d{2}\s?[ap]$'
h_or_m_regex = '^\d{1,3}[hm]$'
h_m_regex = '^\d{1,2}h\s\d{1,2}m$'
time_format = "%I:%M %p"


def convo_cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation"""

    update.message.reply_text(
        hedgehog +
        'Cancelled! Anything else i can /help you with?', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def convo_except(update: Update, context: CallbackContext) -> int:
    """Generic message to send the user when there is an error"""
    update.message.reply_text(
        hedgehog +
        "sorry i didn't understand that. \n"
        "please try again!"
    )
