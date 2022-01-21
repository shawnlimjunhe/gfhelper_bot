import pytest
from commands import help


@pytest.mark.parametrize(
    "context_args, expected",
    [
        (None, help.help_default_txt),
        (['est'], help.command_mapping['est']),
        (['sleep'], help.command_mapping['sleep']),
        # failure cases
        ([''], help.invalid_command_txt),
        (['est', 'random'], help.command_mapping['est']),
        ([], help.help_default_txt)
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

    help.help(mocked_update, mocked_context)

    mocked_context.bot.send_message.assert_called()
    mocked_context.bot.send_message.assert_called_with(
        chat_id=0, text=expected)
