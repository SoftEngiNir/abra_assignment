import json
from typing import Dict

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from django.utils import timezone

from ..models import Message, MessageReceived


def get_user(user_id: int) -> User:
    try:
        user_instance = User.objects.get(pk=user_id)
    except (ObjectDoesNotExist, ValueError):
        return None
    return user_instance


def get_message(message_id: int, **kwargs) -> Message:
    try:
        message_instance = Message.objects.get(pk=message_id, **kwargs)
    except (ObjectDoesNotExist, ValueError):
        return None
    return message_instance


def get_message_received(recipient: int, message: int, **kwargs) -> MessageReceived:
    try:
        message_instance = MessageReceived.objects.get(
            recipient=recipient, message=message, **kwargs
        )
    except (ObjectDoesNotExist, ValueError):
        return None
    return message_instance


def get_all_messages(creator: User, **kwargs) -> QuerySet:
    return Message.objects.filter(creator=creator, **kwargs)


def get_all_messages_received(recipient: User, **kwargs) -> QuerySet:
    return MessageReceived.objects.filter(recipient=recipient, **kwargs)


def create_db_message(creator: int, body: str, subject: str, **kwargs) -> Message:
    m = Message(
        creator=creator,
        body=body,
        subject=subject,
        creation_datetime=timezone.now(),
        **kwargs
    )
    m.save()
    return m


def create_db_message_sent(
    recipient: int, message: Message, **kwargs
) -> MessageReceived:
    ms = MessageReceived(
        recipient=recipient,
        message=message,
        is_read=False,
        creation_datetime=timezone.now(),
        **kwargs
    )
    ms.save()
    return ms


def create_db_user(
    username: str, password: str, first_name: str, last_name: str, **kwargs
) -> User:
    u = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        date_joined=timezone.now(),
        **kwargs
    )
    u.save()
    return u


def decode_bytes(raw_bytes: bytes, encoding: str = "utf-8") -> Dict:
    body_unicode = raw_bytes.decode(encoding)
    return json.loads(body_unicode)
