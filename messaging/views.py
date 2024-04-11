from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .forms import SendMessageForm
from .models import Message, MessageUserLink, User


def create_db_message(sender_id, message, subject):
    sender_instance = User.objects.get(pk=sender_id)
    m = Message(
        sender=sender_instance,
        message=message,
        subject=subject,
        creation_datetime=timezone.now(),
    )
    m.save()
    return m


def create_db_message_user_link(receiver_id, message_instance):
    receiver_instance = User.objects.get(pk=receiver_id)
    mul = MessageUserLink(
        message=message_instance, receiver=receiver_instance, is_read=False
    )
    mul.save()
    return mul


@method_decorator(csrf_exempt, name="dispatch")
class MessageCreateView(View):
    def post(self, request: HttpRequest):
        sender_id = request.GET.get("sender_id")
        message = request.GET.get("message")
        subject = request.GET.get("subject")
        receiver_id = request.GET.get("receiver_id")

        form = SendMessageForm(request.GET)
        if form.is_valid():
            message_instance = create_db_message(sender_id, message, subject)
            create_db_message_user_link(
                receiver_id=receiver_id, message_instance=message_instance
            )

            return HttpResponse(f"Message sent to receiver with ID: {receiver_id}")

        else:
            errors = ", ".join(
                [", ".join(error_messages) for error_messages in form.errors.values()]
            )
            return HttpResponse(f"Failed to send message. Errors: {errors}")

    def get(self, request: HttpRequest):
        users = User.objects.all()
        return HttpResponse(users)


# >>> b = Blog(name="Beatles Blog", tagline="All the latest Beatles news.")
# >>> b.save()

# def index(request):
#     return HttpResponse("Hello, world. You're at the zibi index.")

# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)
