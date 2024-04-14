from django.http import HttpResponse
from django.urls import path

from .views import message_views, user_views


def root(request):
    return HttpResponse("This is the root URL for the abra home assignment")


urlpatterns = [
    # Home
    path("", root, name="index"),
    # Sent messages endpoints
    path(
        "sent/create",
        message_views.SendMessageView.as_view(),
    ),
    path("sent/list", message_views.MessagesListView.as_view()),
    path(
        "sent/update/delete",
        message_views.UpdateDeleteMessageView.as_view(),
    ),
    # Received messages endpoints
    path(
        "received/detail",
        message_views.ReceivedMessageReadView.as_view(),
    ),
    path("received/list", message_views.ReceivedMessagesListView.as_view()),
    path("received/list/unread", message_views.UnreadMessagesListView.as_view()),
    path(
        "received/update/delete",
        message_views.UpdateDeleteMessageRecievedView.as_view(),
    ),
    # Users endpoints
    path("users/detail", user_views.DetailUserView.as_view()),
    path(
        "users/create",
        user_views.CreateUserView.as_view(),
    ),
]
