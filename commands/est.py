import common
import utils
import datetime as dt

from telegram import Update, ParseMode
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    Filters
)

EST_REACH, EST_TRAVEL, EST_READY = range(3)

est_text_map = {
    'est_entry': (
        common.hedgehog +
        'What time do you need to be there by?\n'
        '(e.g 930a or 1030p)\n\n'
        'send /cancel anytime to cancel'
    ),
    'est_reach_failure':
    (
        common.hedgehog +
        'Sorry, I could not process what you sent\n'
        'Please send the time in HH:MM period (a or p)'
    ),
    'est_travel_failure':
    (
        common.hedgehog +
        'Sorry, your time was invalid, please try again'
    )
}


def est(update: Update, context: CallbackContext) -> int:
    """starts the conversation to estimate the time to start getting ready"""

    update.message.reply_text(
        est_text_map['est_entry']
    )

    return EST_REACH


def est_reach(update: Update, context: CallbackContext) -> int:
    """process the reach time and
    asks for the time needed to get there for the est command"""
    reach_time = update.message.text

    try:
        time = utils.process_hhmm_time(reach_time)
        sgt_time = utils.convert_utc_to_sgt(time)
        context.user_data['reach_time'] = time
        update.message.reply_text(
            common.hedgehog +
            "So you have to reach at "
            f"{sgt_time.strftime(common.time_format)}\n\n"
            "How long do you think you will take to get there?\n"
            "\(e\.g\. 1h or 1h 30m or 15m\)",
            parse_mode=ParseMode.MARKDOWN_V2
        )

        return EST_TRAVEL

    except ValueError as err:
        update.message.reply_text(est_text_map['est_reach_failure'])
        return EST_REACH


def est_travel(update: Update, context: CallbackContext) -> int:
    """asks for the time need to get ready or whether to skip """
    travel_time = update.message.text
    try:
        if 'h' in travel_time and 'm' in travel_time:
            delta = utils.process_hm_time(travel_time)
        else:
            delta = utils.process_h_or_m_time(travel_time)

        context.user_data['travel_timedelta'] = delta

        reach_time = context.user_data['reach_time']

        time_to_leave = reach_time + delta

        sgt_reach_time = utils.convert_utc_to_sgt(reach_time)
        sgt_time_to_leave = utils.convert_utc_to_sgt(time_to_leave)

        update.message.reply_text(
            common.hedgehog +
            "You will need to leave the house at "
            + utils.underline_str(f"{sgt_time_to_leave.strftime(common.time_format)}\n") +
            "to reach on time at "
            f"{sgt_reach_time.strftime(common.time_format)}\n\n"
            "How long do you think you will need to get ready?\n"
            "\(e\.g\. 1h or 1h 30m or 15m\)\n\n"
            "send /skip if you wish to skip this step",
            parse_mode=ParseMode.MARKDOWN_V2
        )

        return EST_READY

    except ValueError as err:
        print(err.args[0])
        update.message.reply_text(
            est_text_map['est_travel_failure']
        )
        return EST_TRAVEL


def est_skip_ready(update: Update, context: CallbackContext) -> int:
    """gives the user the time to leave"""
    update.message.reply_text(
        common.hedgehog +
        'How else might i /help you?'
    )

    return ConversationHandler.END


def est_ready(update: Update, context: CallbackContext) -> int:
    ready_time = update.message.text
    try:
        if 'h' in ready_time and 'm' in ready_time:
            delta = utils.process_hm_time(ready_time)
        else:
            delta = utils.process_h_or_m_time(ready_time)

        reach_time = context.user_data['reach_time']
        time_to_leave = reach_time + context.user_data['travel_timedelta']
        time_to_ready = time_to_leave + delta

        sgt_reach_time = utils.convert_utc_to_sgt(reach_time)
        sgt_time_to_leave = utils.convert_utc_to_sgt(time_to_leave)
        sgt_time_to_ready = utils.convert_utc_to_sgt(time_to_ready)

        update.message.reply_text(
            common.hedgehog +
            "You will need to start to get ready by "
            + utils.underline_str(f"{sgt_time_to_ready.time().strftime(common.time_format)}\n") +
            f"and leave the house at "
            + utils.underline_str(f"{sgt_time_to_leave.time().strftime(common.time_format)}\n") +
            f"to reach on time at "
            f"{sgt_reach_time.strftime(common.time_format)}", parse_mode=ParseMode.MARKDOWN_V2
        )

        update.message.reply_text(
            common.hedgehog +
            f'How else might i /help you?'
        )

        return ConversationHandler.END

    except ValueError:
        update.message.reply_text(
            common.hedgehog +
            f'Sorry, your time was invalid as, please try again'
        )
        return EST_READY


convo_except_handler = MessageHandler(
    (~Filters.command) & Filters.regex('.*'), common.convo_except)

est_convo_handler = ConversationHandler(
    entry_points=[CommandHandler('est', est)],
    states={
        EST_REACH: [
            MessageHandler(Filters.regex(common.hhmm_regex), est_reach),
            convo_except_handler
        ],
        EST_TRAVEL: [
            MessageHandler(Filters.regex(common.h_or_m_regex) |
                           Filters.regex(common.h_m_regex), est_travel),
            convo_except_handler
        ],
        EST_READY: [
            MessageHandler(Filters.regex(common.h_or_m_regex) |
                           Filters.regex(common.h_m_regex), est_ready),
            convo_except_handler,
            CommandHandler('skip', est_skip_ready)
        ]
    },
    fallbacks=[CommandHandler('cancel', common.convo_cancel)]
)
