from app.infrastructure.message_sender import SMTPMessageSender


def test_create_message(mocker):
    mock_settings = mocker.patch('app.infrastructure.message_sender.settings')
    mock_settings.SMTP_USER = 'user'

    sender = SMTPMessageSender()
    send_to = 'test@example.com'
    text = 'test_text'

    message = sender.create_message(send_to, text)

    assert message['Subject'] == 'Извлеченный текст'
    assert message['From'] == mock_settings.SMTP_USER
    assert message['To'] == send_to
    assert message.get_content() == text + '\n'

def test_send_message(mocker):
    mock_class = mocker.patch('app.infrastructure.message_sender.SMTP_SSL')
    mock_instance = mocker.MagicMock()
    mock_class.return_value.__enter__.return_value = mock_instance

    mock_settings = mocker.patch('app.infrastructure.message_sender.settings')
    mock_settings.SMTP_HOST = 'test_host'
    mock_settings.SMTP_PORT = 1234
    mock_settings.SMTP_USER = 'test_user'
    mock_settings.SMTP_PASS = 'test_pass'

    sender = SMTPMessageSender()
    mock_message = mocker.MagicMock()
    sender.send_message(mock_message)

    mock_class.assert_called_once_with('test_host', 1234)
    mock_instance.login.assert_called_once_with('test_user', 'test_pass')
    mock_instance.send_message.assert_called_once_with(mock_message)



