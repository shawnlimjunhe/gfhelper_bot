import pytest
from unittest import mock


@pytest.fixture
def mocked_update():
    mocked_update = mock.Mock()
    mocked_update.effective_chat.id = 0
    return mocked_update


@pytest.fixture
def mocked_context():
    return mock.Mock()
