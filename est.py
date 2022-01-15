import re
import datetime as dt

from multiprocessing.sharedctypes import Value
from common import (
  bot_face,
  hhmm_regex,
  h_or_m_regex,
  h_m_regex,
  time_format,
  convo_cancel
  )
from telegram import Update, ParseMode
from telegram.ext import (
  Updater,
  CallbackContext,
  CommandHandler,
  MessageHandler,
  ConversationHandler,
  Filters
  )

EST_REACH, EST_TRAVEL, EST_READY = range(3)

def process_hhmm_time(txt: str)-> dt.time:
  """process the HH:MM period format to datetime object"""

  raw_hour, minute_period = txt.split(':')
  minute = int(minute_period[:2])
  period = minute_period[-1]

  hour = int(raw_hour)
  if period == 'p' and hour != 12:
    hour += 12

  if hour > 23:
    raise ValueError('hour cannot be more than 23')
  if minute > 59:
    raise ValueError('minutes cannot be more than 59')

  return dt.time(hour=int(hour), minute=minute) 
  
def process_h_or_m_time(txt: str)-> dt.timedelta:
  """process the h or m time format, e.g. 10 m or 1 h"""
  if txt[-1] == 'h':
    # hours
    hours = int(txt[:-1].strip())
    if hours > 23:
      raise ValueError('hours cannot be more than 23')
    return dt.timedelta(hours=-hours)

  else:
    # minutes
    minutes = int(txt[:-1].strip())
    hours = 0
    while minutes > 60:
      hours += 1
      minutes -= 60
    return dt.timedelta(hours=-hours, minutes=-minutes)
    

def process_hm_time(txt: str):
  hours = int(txt.split('h')[0])
  minutes_str = txt.split()[1]
  if 'm' in minutes_str:
    minutes_str = minutes_str[:-1]
  
  minutes = int(minutes_str)

  if minutes > 59:
    raise ValueError('minutes cannot be more than 59')
  return dt.timedelta(hours=-hours, minutes=-minutes)



def est(update: Update, context: CallbackContext) -> int:
  """starts the conversation to estimate the time to start getting ready"""
  update.message.reply_text(
    bot_face + 
    'What time do you need to be there by?\n\n'
    '(e.g 9:30a or 10:30p)\n'
    'send /cancel to cancel'
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
      f"`{context.user_data['reach_time'].strftime(time_format)}`\n"
      "How long do you think you will take to get there?\n"
      "\(e\.g\. 1h or 1h 30m or 15m\)"
      ,parse_mode=ParseMode.MARKDOWN_V2
      )

    return EST_TRAVEL

  except ValueError:
    update.message.reply_text(
      bot_face +
      'Sorry, your time was invalid, please try again'
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
      "send /skip if you wish to skip this step" 
      , parse_mode=ParseMode.MARKDOWN_V2
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
    
    return ConversationHandler.END

  except ValueError:
    update.message.reply_text(
      bot_face +
      f'Sorry, your time was invalid as, please try again'
    )
    return EST_READY


def est_except(update: Update, context: CallbackContext) -> int:
  update.message.reply_text(
    bot_face + 
    "sorry i didn't understand that. \n"
    "please try again!"
    )

est_except_handler = MessageHandler((~Filters.command) & Filters.regex('.*'), est_except)

est_conv_handler = ConversationHandler(
  entry_points=[CommandHandler('est', est)],
  states={
    EST_REACH: [
      MessageHandler(Filters.regex(hhmm_regex), est_reach),
      est_except_handler
    ],
    EST_TRAVEL: [
      MessageHandler(Filters.regex(h_or_m_regex) | Filters.regex(h_m_regex), est_travel),
      est_except_handler
    ],
    EST_READY: [
      MessageHandler(Filters.regex(h_or_m_regex) | Filters.regex(h_m_regex), est_ready),
      est_except_handler,
      CommandHandler('skip', est_skip_ready)
    ]
  },
  fallbacks=[CommandHandler('cancel', convo_cancel)]
)
  