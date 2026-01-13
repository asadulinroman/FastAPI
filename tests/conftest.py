import pytest
from starlette.testclient import TestClient
from app.main import create_app
from app.presentation.dependencies import get_cache, get_text_extractor, get_message_sender, get_hash_getter


@pytest.fixture()
def client():
    app = create_app()
    with TestClient(app) as client:
        yield client

@pytest.fixture()
def conf_mock(mocker):
    mock_cache = mocker.AsyncMock()
    mock_text_extractor = mocker.AsyncMock()
    mock_hash_getter = mocker.AsyncMock()

    mock_hash_getter.get_hash.return_value = 'test_hash'

    return mock_cache, mock_text_extractor, mock_hash_getter

@pytest.fixture
def override_dependencies(client):
    def override(cache=None, text_extractor=None, message_sender=None, hash_getter=None):
        app = client.app
        if cache is not None:
            app.dependency_overrides[get_cache] = lambda: cache
        if text_extractor is not None:
            app.dependency_overrides[get_text_extractor] = lambda: text_extractor
        if message_sender is not None:
            app.dependency_overrides[get_message_sender] = lambda: message_sender
        if hash_getter is not None:
            app.dependency_overrides[get_hash_getter] = lambda: hash_getter
    return override