from unittest import mock
import pytest
from commands import est
import common
import datetime
from telegram import ParseMode


def test_est(mocked_update, mocked_context):
    # test
    resp = est.est(mocked_update, mocked_context)

    # assertions
    mocked_update.message.reply_text.assert_called()
    mocked_update.message.reply_text.assert_called_with(
        common.hedgehog +
        'What time do you need to be there by?\n'
        '(e.g 930a or 1030p)\n\n'
        'send /cancel anytime to cancel'
    )

    assert resp == est.EST_REACH


def test_est_reach_success(mocked_update, mocked_context):
    # set up
    mocked_update.message.text = "930a"
    time = datetime.time(hour=9, minute=30)
    expected_text = (
        common.hedgehog +
        "So you have to reach at "
        f"{time.strftime(common.time_format)}\n\n"
        "How long do you think you will take to get there?\n"
        "\(e\.g\. 1h or 1h 30m or 15m\)"
    )

    # test
    resp = est.est_reach(mocked_update, mocked_context)

    # assertions
    mocked_update.message.reply_text.assert_called()
    mocked_update.message.reply_text.assert_called_with(
        expected_text, parse_mode=ParseMode.MARKDOWN_V2
    )
    assert resp == est.EST_TRAVEL


@pytest.mark.skip(reason="yet to implement")
def test_est_reach_failure():
    pass


@pytest.mark.skip(reason="yet to implement")
def test_est_travel():
    pass


@pytest.mark.skip(reason="yet to implement")
def test_est_skip_ready():
    pass


@pytest.mark.skip(reason="yet to implement")
def test_est_ready():
    pass
