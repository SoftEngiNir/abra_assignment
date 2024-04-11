from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from django.views.generic import CreateView, DetailView, DeleteView, ListView

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
class SendMessageView(CreateView):
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

def get_user(user_id):
    if not user_id:
        return JsonResponse({'error': 'User ID is required'}, status=400)

    try:
        user_instance = User.objects.get(pk=user_id)
    except (ObjectDoesNotExist, ValueError):
        return JsonResponse({'error': 'User not found'}, status=404)
    return user_instance


class MessagesListView(ListView):

    def get(self, request: HttpRequest):
        user_id = request.GET.get('user_id')

        user_instance = get_user(user_id)
        
        messages = Message.objects.filter(sender=user_instance)
        return JsonResponse(list(messages.values()), safe=False)
    
class UnreadMessagesListView(ListView):

    def get(self, request: HttpRequest):
        user_id = request.GET.get('user_id')

        user_instance = get_user(user_id)
        
        unread_messages = Message.objects.filter(messageuserlink__receiver_id=user_id, messageuserlink__is_read=False)


        return JsonResponse(list(unread_messages.values()), safe=False)




# >>> b = Blog(name="Beatles Blog", tagline="All the latest Beatles news.")
# >>> b.save()

# def index(request):
#     return HttpResponse("Hello, world. You're at the zibi index.")

# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)
