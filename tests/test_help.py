from distutils import command
import pytest
from unittest import mock
from commands.help import help, help_default_txt, command_mapping, invalid_command_txt
# test 1 replys with expected help message when no context args


@pytest.fixture
def mocked_update():
    mocked_update = mock.Mock()
    mocked_update.effective_chat.id = 0
    return mocked_update


@pytest.fixture
def mocked_context():
    return mock.Mock()


@pytest.mark.parametrize(
    "context_args, expected",
    [
        (None, help_default_txt),
        (['est'], command_mapping['est']),
        (['sleep'], command_mapping['sleep']),
        # failure cases
        ([''], invalid_command_txt),
        (['est', 'random'], command_mapping['est']),
        ([], help_default_txt)
    ],
    ids=[
        'help command default behavior',
        'help est',
        'help sleep',
        'help invalid call',
        'help called with vaild command but extra words',
        'help with context.args as empty list'
    ]
)
def test_help(mocked_update, mocked_context, context_args, expected):
    mocked_update.message.text = "test message"
    mocked_context.args = context_args

    help(mocked_update, mocked_context)

    mocked_context.bot.send_message.assert_called()
    mocked_context.bot.send_message.assert_called_with(
        chat_id=0, text=expected)
