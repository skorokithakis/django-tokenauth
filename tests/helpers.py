from django.contrib.messages import get_messages


def messages(response):
    return list(get_messages(response.wsgi_request))


def message_texts(response):
    return [message.message for message in messages(response)]
