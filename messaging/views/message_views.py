from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from ..forms import SendMessageForm
from .views_utils import (
    create_db_message,
    create_db_message_sent,
    decode_bytes,
    get_all_messages,
    get_all_messages_received,
    get_message,
    get_message_received,
    get_user,
)


@method_decorator(csrf_exempt, name="dispatch")
class SendMessageView(CreateView, LoginRequiredMixin):
    def post(self, request: HttpRequest):
        creator_id = request.user.id

        recipient_id = request.GET.get("recipient_id")
        body_json = decode_bytes(request.body)
        body = body_json.get("body")
        subject = body_json.get("subject")
        data = {
            "creator_id": creator_id,
            "recipient_id": recipient_id,
            "body": body,
            "subject": subject,
        }
        form = SendMessageForm(data)
        if form.is_valid():
            creator_instance = get_user(creator_id)
            recipient_instance = get_user(recipient_id)

            message_instance = create_db_message(creator_instance, body, subject)
            create_db_message_sent(recipient_instance, message_instance)
            return HttpResponse(f"Message sent to recipient with ID: {recipient_id}")

        else:
            errors = ", ".join(
                [", ".join(error_messages) for error_messages in form.errors.values()]
            )
            return HttpResponse(f"Failed to send message. Errors: {errors}")


class MessagesListView(ListView, LoginRequiredMixin):
    def get(self, request: HttpRequest):
        user_instance = get_user(request.user.id)
        if not user_instance:
            return JsonResponse(
                {"error": f"User with ID {request.user.id} does not exist..."},
                status=404,
            )

        messages = get_all_messages(creator=user_instance, deleted=False)
        return JsonResponse(
            list(
                messages.values(
                    "id", "creator_id", "subject", "body", "creation_datetime"
                )
            ),
            safe=False,
        )


class ReceivedMessageReadView(DetailView, LoginRequiredMixin):
    def get(self, request: HttpRequest):
        recipient_instance = get_user(request.user.id)
        message_id = request.GET.get("message_id")
        message_instance = get_message(message_id)
        message_received = get_message_received(
            recipient=recipient_instance, message=message_instance, deleted=False
        )
        if message_received:
            message_received.is_read = True
            message_received.save()

            return JsonResponse(model_to_dict(message_received.message))

        return HttpResponse(f"Could not find message with id {message_id}")


class ReceivedMessagesListView(ListView, LoginRequiredMixin):
    def get(self, request: HttpRequest):
        user_instance = get_user(request.user.id)
        if not user_instance:
            return JsonResponse(
                {"error": f"User with ID {request.user.id} does not exist..."},
                status=404,
            )
        messages_received = get_all_messages_received(recipient=user_instance, deleted=False)
        return JsonResponse(list(messages_received.values()), safe=False)


class UnreadMessagesListView(ListView, LoginRequiredMixin):
    def get(self, request: HttpRequest):
        user_instance = get_user(request.user.id)
        if not user_instance:
            return JsonResponse(
                {"error": f"User with ID {request.user.id} does not exist..."},
                status=404,
            )
        unread_messages = get_all_messages_received(
            recipient=user_instance, is_read=False
        )
        return JsonResponse(list(unread_messages.values()), safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class UpdateDeleteMessageView(UpdateView, LoginRequiredMixin):
    def patch(self, request: HttpRequest):
        user_instance = get_user(request.user.id)
        message_id = request.GET.get("message_id")
        message_instance = get_message(message_id, creator=user_instance)
        if message_instance:
            message_instance.deleted = True
            message_instance.save()
            return HttpResponse(
                f"Deleted message {message_instance.subject} with id {message_id}"
            )

        return HttpResponse(f"Could not find message with id {message_id}")


@method_decorator(csrf_exempt, name="dispatch")
class UpdateDeleteMessageRecievedView(UpdateView, LoginRequiredMixin):
    def patch(self, request: HttpRequest):
        recipient = get_user(request.user.id)
        message_id = request.GET.get("message_id")
        message = get_message(message_id)
        message_received_instance = get_message_received(recipient, message)
        if message_received_instance:
            message_received_instance.deleted = True
            message_received_instance.save()
            return HttpResponse(
                f"Deleted message {message_received_instance.message.subject} with id {message_id}"
            )

        return HttpResponse(f"Could not find message with id {message_id}")


def index(request):
    return HttpResponse("Hey bro")
