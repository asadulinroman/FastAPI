import pytest

from app.infrastructure.text_extractor import TesseractTextExtractor


@pytest.mark.anyio
async def test_extract_text(mocker):
    mock_image = mocker.MagicMock()
    mock_open = mocker.patch('app.infrastructure.text_extractor.Image.open', return_value=mock_image)
    mock_text_extractor = mocker.patch('app.infrastructure.text_extractor.image_to_string', return_value='test_text')
    mock_open.return_value.__enter__.return_value = mock_image

    extractor = TesseractTextExtractor()
    result = await extractor.extract_text('test_path', 'rus+eng')

    assert result == 'test_text'
    mock_open.assert_called_once_with('test_path')
    mock_text_extractor.assert_called_once_with(mock_image, 'rus+eng')


