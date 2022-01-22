import common
import utils
import datetime as dt

from telegram import Update, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    Filters
)


SLEEP_CHOICE, SLEEP_WAKE = range(2)
fall_asleep_time_minutes = 10
sleep_cycle_length = 90
fall_asleep_timedelta = dt.timedelta(minutes=fall_asleep_time_minutes)
sleep_cycle_timedelta = dt.timedelta(minutes=sleep_cycle_length)


def sleep_time_arr_to_str(utc_datetimes: list[dt.datetime]) -> str:
    strs = []
    for utc_datetime in utc_datetimes:
        sgt_datetime = utils.convert_utc_to_sgt(utc_datetime)
        strs.append(utils.underline_str(
            f"{sgt_datetime.strftime(common.time_format)}"))

    return " or\n".join(strs)


def get_sleeptimes_from_wake(wake_datetime: dt.datetime) -> list[dt.datetime]:
    """
    Converts waketime to datetime object to use timedelta
    To calculate sleep times
    """
    now = utils.get_datetime_utc_now()

    time_difference = wake_datetime - now
    if time_difference.seconds < (10 * 60):
        # shouldn't sleep if less than 10 minutes
        return []

    sleep_times = []
    nap_time_minutes = min(20, time_difference.seconds // 60)
    nap = wake_datetime - dt.timedelta(minutes=nap_time_minutes)
    sleep_times.append(nap)

    curr = wake_datetime - fall_asleep_timedelta - sleep_cycle_timedelta
    i = 0
    while curr > now and i < 6:
        new_dt = curr.replace()
        sleep_times.append(new_dt)
        curr -= sleep_cycle_timedelta
        i += 1

    return sleep_times


def process_sleep_times_text(sleep_times: list[dt.datetime], wake_time: dt.datetime) -> str:
    sgt_wake_time = utils.convert_utc_to_sgt(wake_time)

    if not sleep_times:
        return (
            common.hedgehog +
            "Hmm, it seems like you don\'t have a lot of time\n"
            "before you have to wake up at "
            f"{sgt_wake_time.strftime(common.time_format)}\.\.\.\n"
            "maybe a cup of coffee will help ☕"
        )

    if len(sleep_times) == 1:
        sgt_sleep_time = utils.convert_utc_to_sgt(sleep_times[0])
        return (
            common.hedgehog +
            "It seem's you have a bit to time to nap\!\n"
            "before you have to wake up at "
            f"{sgt_wake_time.strftime(common.time_format)}\n"
            "Sleep at "
            + utils.underline_str(f"{sgt_sleep_time.strftime(common.time_format)}") +
            " for a power nap\! 💪"
        )

    text = sleep_time_arr_to_str(sleep_times[::-1])
    return (
        common.hedgehog +
        "You can sleep at the following times to feel rested\!\n"
        + text
    )


def sleep(update: Update, context: CallbackContext) -> int:
    """starts the conversation to determine sleep or wakeup time"""
    sleep_reply_keyboard = [['Sleep Now', 'Wake Time']]

    update.message.reply_text(
        common.hedgehog +
        f"Hi {update.message.from_user.first_name}!\n\n"
        "Choose:\n"
        "'*Sleep Now*' to see what time you should wake up\n"
        "if you sleep now\n"
        "or\n"
        "'*Wake Time*' to see what time you should sleep to\n"
        "wake up at a certain time\n\n"
        "type /cancel anytime to cancel",
        reply_markup=ReplyKeyboardMarkup(
            sleep_reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder='Sleep now or Wake time?'
        )
    )

    return SLEEP_CHOICE


def sleep_now(update: Update, context: CallbackContext) -> int:
    curr = utils.get_datetime_utc_now()
    time_to_sleep = utils.convert_utc_to_sgt(curr)

    wake_times = [(curr + dt.timedelta(minutes=20))]

    curr += fall_asleep_timedelta
    for i in range(6):
        curr += sleep_cycle_timedelta
        new_datetime = curr.replace()
        wake_times.append(new_datetime)

    wake_time_str = sleep_time_arr_to_str(wake_times)

    update.message.reply_text(
        common.hedgehog +
        "If you sleep now at "
        + utils.underline_str(f"{time_to_sleep.strftime(common.time_format)}\n") +
        "you should wake up at:\n" +
        wake_time_str,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.MARKDOWN_V2
    )

    return ConversationHandler.END


def sleep_wake(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        common.hedgehog +
        "What time do you want to wake up by?\n"
        "(e.g 930a or 1030p)"
    )

    return SLEEP_WAKE


def sleep_wake_time(update: Update, context: CallbackContext) -> int:
    wake_time_raw = update.message.text
    try:
        wake_time = utils.process_hhmm_time(wake_time_raw)
        sleep_times = get_sleeptimes_from_wake(wake_time)
        text = process_sleep_times_text(sleep_times, wake_time)

        update.message.reply_text(
            text,
            parse_mode=ParseMode.MARKDOWN_V2
        )

        return ConversationHandler.END

    except ValueError:
        update.message.reply_text(
            common.hedgehog +
            'Sorry, I could not process what you sent\n'
            'Please send the time in HH:MM period (a or p)'
        )

        return SLEEP_WAKE


convo_except_handler = MessageHandler(
    (~Filters.command) & Filters.regex('.*'), common.convo_except)

sleep_convo_handler = ConversationHandler(
    entry_points=[CommandHandler('sleep', sleep)],
    states={
        SLEEP_CHOICE: [
            MessageHandler(Filters.regex('^(Sleep Now)$'), sleep_now),
            MessageHandler(Filters.regex('^(Wake Time)$'), sleep_wake),
            convo_except_handler
        ],
        SLEEP_WAKE: [
            MessageHandler(Filters.regex(common.hhmm_regex), sleep_wake_time),
            convo_except_handler
        ]
    },
    fallbacks=[CommandHandler('cancel', common.convo_cancel)]
)
