from app.infrastructure.celery.tasks import send_message_to_email_task

def test_send_message_to_email_task(mocker):
    mock_sender = mocker.MagicMock()
    mock_get_sender = mocker.patch(
        "app.infrastructure.celery.tasks.get_message_sender",
        return_value=mock_sender
    )

    created_message = mock_sender.create_message.return_value
    send_message_to_email_task('test@example.com', 'test_text')

    mock_sender.create_message.assert_called_once_with('test@example.com', 'test_text')
    mock_sender.send_message.assert_called_once_with(created_message)