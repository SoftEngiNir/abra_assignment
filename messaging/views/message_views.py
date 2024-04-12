from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from ..forms import SendMessageForm
from ..models import Message
from .views_utils import create_db_message, get_user


@method_decorator(csrf_exempt, name="dispatch")
class SendMessageView(CreateView):
    def post(self, request: HttpRequest, sender_id, receiver_id, message, subject):
        data = {
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "message": message,
            "subject": subject,
        }
        form = SendMessageForm(data)
        if form.is_valid():
            create_db_message(sender_id, receiver_id, message, subject)

            return HttpResponse(f"Message sent to receiver with ID: {receiver_id}")

        else:
            errors = ", ".join(
                [", ".join(error_messages) for error_messages in form.errors.values()]
            )
            return HttpResponse(f"Failed to send message. Errors: {errors}")


class ReadMessageView(DetailView):
    def get(self, request, message_id):
        try:
            message = Message.objects.get(pk=message_id)
            message.is_read = True
            message.save()
            return JsonResponse(
                model_to_dict(
                    message, fields=["id", "sender", "receiver", "subject", "message"]
                )
            )
        except Message.DoesNotExist:
            return JsonResponse({"error": "Message does not exist"}, status=404)


class MessagesListView(ListView):
    def get(self, request: HttpRequest, user_id):
        user_instance = get_user(user_id)
        if not user_instance:
            return JsonResponse(
                {"error": f"User with ID {user_id} does not exist..."}, status=404
            )

        messages = Message.objects.filter(sender=user_instance)
        return JsonResponse(list(messages.values()), safe=False)


class UnreadMessagesListView(ListView):
    def get(self, request: HttpRequest, user_id):
        user_instance = get_user(user_id)
        if not user_instance:
            return JsonResponse(
                {"error": f"User with ID {user_id} does not exist..."}, status=404
            )
        unread_messages = Message.objects.filter(receiver=user_instance, is_read=False)
        return JsonResponse(list(unread_messages.values()), safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class DeleteMessageView(UpdateView):
    def patch(self, request: HttpRequest, message_id):
        return HttpResponse(request.user)


def index(request):
    return HttpResponse("Hey bro")
