import datetime as dt

from telegram import Update, ParseMode
from telegram.ext import (
  CallbackContext,
  CommandHandler,
  MessageHandler,
  ConversationHandler,
  Filters
  )

from common import (
  bot_face,
  hhmm_regex,
  h_or_m_regex,
  h_m_regex,
  time_format,
  convo_cancel,
  convo_except
  )

from utils import (
  process_hhmm_time,
  process_h_or_m_time,
  process_hm_time
)

EST_REACH, EST_TRAVEL, EST_READY = range(3)


def est(update: Update, context: CallbackContext) -> int:
  """starts the conversation to estimate the time to start getting ready"""
  update.message.reply_text(
    bot_face + 
    'What time do you need to be there by?\n'
    '(e.g 9:30a or 10:30p)\n\n'
    'send /cancel anytime to cancel'
  )

  return EST_REACH


def est_reach(update: Update, context: CallbackContext) -> int:
  """process the reach time and 
  asks for the time needed to get there for the est command"""
  reach_time = update.message.text

  try: 
    time = process_hhmm_time(reach_time)
    context.user_data['reach_time'] = time
    update.message.reply_text(
      bot_face + 
      "So you have to reach at "
      f"`{context.user_data['reach_time'].strftime(time_format)}`\n\n"
      "How long do you think you will take to get there?\n"
      "\(e\.g\. 1h or 1h 30m or 15m\)",
      parse_mode=ParseMode.MARKDOWN_V2
      )

    return EST_TRAVEL

  except ValueError:
    update.message.reply_text(
      bot_face +
      'Sorry, I could not process what you sent\n'
      'Please send the time in HH:MM period (a or p)'
    )
    return EST_REACH


def est_travel(update: Update, context: CallbackContext) -> int:
  """asks for the time need to get ready or whether to skip """
  travel_time = update.message.text
  try:
    if 'h' in travel_time and 'm' in travel_time:
      delta = process_hm_time(travel_time)
    else:
      delta = process_h_or_m_time(travel_time)

    context.user_data['travel_timedelta'] = delta

    reach_time = context.user_data['reach_time']

    time_to_leave = dt.datetime.combine(
    dt.date.today(), reach_time
    ) + delta

    update.message.reply_text(
      bot_face +
      "You will need to leave the house at "
      f"`{time_to_leave.time().strftime(time_format)}`\n"
      "to reach on time at "
      f"`{reach_time.strftime(time_format)}`\n\n"
      "How long do you think you will need to get ready?\n"
      "\(e\.g\. 1h or 1h 30m or 15m\)\n\n"
      "send /skip if you wish to skip this step",
      parse_mode=ParseMode.MARKDOWN_V2
    )
    
    return EST_READY

  except ValueError:
    update.message.reply_text(
      bot_face +
      f'Sorry, your time was invalid as, please try again'
    )
    return EST_TRAVEL
    

def est_skip_ready(update: Update, context: CallbackContext) -> int:
  """gives the user the time to leave"""
  update.message.reply_text(
      bot_face +
      f'How else might i /help you?'
    )

  return ConversationHandler.END


def est_ready(update: Update, context: CallbackContext) -> int:
  ready_time = update.message.text
  try:
    if 'h' in ready_time and 'm' in ready_time:
      delta = process_hm_time(ready_time)
    else:
      delta = process_h_or_m_time(ready_time)

    reach_time = context.user_data['reach_time']

    time_to_leave = dt.datetime.combine(
      dt.date.today(), reach_time
      ) + context.user_data['travel_timedelta']
    
    time_to_ready = time_to_leave + delta
    
    update.message.reply_text(
      bot_face +
      "You will need to start to get ready by "
      f"`{time_to_ready.time().strftime(time_format)}\n`"
      f"and leave the house at "
      f"`{time_to_leave.time().strftime(time_format)}\n`"
      f"to reach on time at "
      f"`{reach_time.strftime(time_format)}`" 
      ,parse_mode=ParseMode.MARKDOWN_V2
    )

    update.message.reply_text(
      bot_face +
      f'How else might i /help you?'
    )
    
    return ConversationHandler.END

  except ValueError:
    update.message.reply_text(
      bot_face +
      f'Sorry, your time was invalid as, please try again'
    )
    return EST_READY

convo_except_handler = MessageHandler((~Filters.command) & Filters.regex('.*'), convo_except)

est_convo_handler = ConversationHandler(
  entry_points=[CommandHandler('est', est)],
  states={
    EST_REACH: [
      MessageHandler(Filters.regex(hhmm_regex), est_reach),
      convo_except_handler
    ],
    EST_TRAVEL: [
      MessageHandler(Filters.regex(h_or_m_regex) | Filters.regex(h_m_regex), est_travel),
      convo_except_handler
    ],
    EST_READY: [
      MessageHandler(Filters.regex(h_or_m_regex) | Filters.regex(h_m_regex), est_ready),
      convo_except_handler,
      CommandHandler('skip', est_skip_ready)
    ]
  },
  fallbacks=[CommandHandler('cancel', convo_cancel)]
)
  