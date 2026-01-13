from app.domain.interfaces import InterfaceCache, InterfaceTextExtractor, InterfaceHashGetter

def test_analyze_doc_with_cache(client, mocker, override_dependencies):
    mock_cache = mocker.AsyncMock(spec=InterfaceCache)
    mock_cache.get.return_value = 'test_cache'
    mock_text_extractor = mocker.AsyncMock(spec=InterfaceTextExtractor)
    mock_hash_getter = mocker.AsyncMock(spec=InterfaceHashGetter)

    override_dependencies(cache=mock_cache, text_extractor=mock_text_extractor, hash_getter=mock_hash_getter)

    response = client.post('/analyze_doc', json={'filename': 'test.jpg'})

    assert response.status_code == 200
    assert response.json() == {'text': 'test_cache', 'from_cache': True}

    client.app.dependency_overrides.clear()

def test_analyze_doc_without_cache(client, mocker, override_dependencies):
    mock_cache = mocker.AsyncMock(spec=InterfaceCache)
    mock_cache.get.return_value = None
    mock_text_extractor = mocker.AsyncMock(spec=InterfaceTextExtractor)
    mock_text_extractor.extract_text.return_value = 'test_text_from_image'
    mock_hash_getter = mocker.AsyncMock(spec=InterfaceHashGetter)

    override_dependencies(cache=mock_cache, text_extractor=mock_text_extractor, hash_getter=mock_hash_getter)

    response = client.post('/analyze_doc', json={'filename': 'test.jpg'})

    assert response.status_code == 200
    assert response.json() == {'text': 'test_text_from_image', 'from_cache': False}

    client.app.dependency_overrides.clear()

def test_send_message_to_email(client, mocker):
    mock_task = mocker.patch("app.presentation.routers.send_message_to_email_task.delay")

    response = client.post('/send_message_to_email',
                           json={
                               'email': 'test@example.com',
                               'extracted_text': 'test_text_from_image',
                           })

    assert response.status_code == 200
    assert response.json() == {'publish': 'OK'}
    mock_task.assert_called_once_with('test@example.com', 'test_text_from_image')