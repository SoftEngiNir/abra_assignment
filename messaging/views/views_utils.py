from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.utils import timezone

from ..models import Message


def get_user(user_id: int) -> JsonResponse:
    try:
        user_instance = User.objects.get(pk=user_id)
    except (ObjectDoesNotExist, ValueError):
        return None
    return user_instance


def create_db_message(
    sender_id: int, receiver_id: int, message: str, subject: str, **kwargs
) -> Message:
    sender_instance = User.objects.get(pk=sender_id)
    receiver_instance = User.objects.get(pk=receiver_id)
    m = Message(
        sender=sender_instance,
        receiver=receiver_instance,
        message=message,
        subject=subject,
        creation_datetime=timezone.now(),
        **kwargs
    )
    m.save()
    return m


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
