from telegram import Update
from telegram.ext import (
  CallbackContext,
  ConversationHandler,
  )

bot_face = '🤖: \n'
hhmm_regex = '^\d{1,}:\d{2}\s?[ap]$'
h_or_m_regex = '^\d{1,3}[hm]$' 
h_m_regex = '^\d+h\s\d{1,2}m$'
time_format = "%I:%M %p"

def convo_cancel(update: Update, context: CallbackContext) -> int:
  """Cancels and ends the conversation"""
  update.message.reply_text(
    '🤖: \nCancelled! Anything else i can /help you with?'
  )

  return ConversationHandler.END

