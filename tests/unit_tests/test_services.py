import pytest

from app.application.services import AnalyzeDocService, SendMessageToEmailService

@pytest.mark.anyio
async def test_analyze_doc_service_with_cache(conf_mock):
    mock_cache, mock_text_extractor, mock_hash_getter = conf_mock
    mock_cache.get.return_value = 'test_text_from_image'

    service = AnalyzeDocService(mock_cache, mock_text_extractor, mock_hash_getter)

    result = await service.analyze_doc('test_path')

    assert result['text'] == 'test_text_from_image'
    assert result['from_cache'] == True
    mock_hash_getter.get_hash.assert_awaited_once_with("test_path")
    mock_cache.get.assert_awaited_once_with('test_hash')
    mock_text_extractor.extract_text.assert_not_awaited()
    mock_cache.set.assert_not_awaited()

@pytest.mark.anyio
async def test_analyze_doc_service_without_cache(conf_mock):
    mock_cache, mock_text_extractor, mock_hash_getter = conf_mock
    mock_cache.get.return_value = None
    mock_text_extractor.extract_text.return_value = 'test_text_from_image'

    service = AnalyzeDocService(mock_cache, mock_text_extractor, mock_hash_getter)

    result = await service.analyze_doc('test_path')

    assert result['text'] == 'test_text_from_image'
    assert result['from_cache'] == False
    mock_hash_getter.get_hash.assert_awaited_once_with("test_path")
    mock_cache.get.assert_awaited_once_with('test_hash')
    mock_text_extractor.extract_text.assert_awaited_once_with('test_path', "rus+eng")
    mock_cache.set.assert_awaited_once_with('test_hash', 3600, 'test_text_from_image')

def test_send_message_to_email_service(mocker):
    mock_email_sender = mocker.MagicMock()
    mock_message = mocker.MagicMock()
    mock_email_sender.create_message.return_value = mock_message

    service = SendMessageToEmailService(mock_email_sender)

    email = 'test@example.com'
    extracted_text = 'test_text_from_image'

    service.send_email(email, extracted_text)

    mock_email_sender.create_message.assert_called_once_with(email, extracted_text)
    mock_email_sender.send_message.assert_called_once_with(mock_message)






