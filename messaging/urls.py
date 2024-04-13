from django.urls import path

from .views import message_views, user_views

urlpatterns = [
    path("", message_views.index, name="index"),
    # Sent messages endpoints
    path(
        "sent/create/<int:recipient_id>/<str:body>/<str:subject>",
        message_views.SendMessageView.as_view(),
    ),
    path(
        "sent/detail/<int:message_id>",
        message_views.ReadMessageView.as_view(),
    ),
    path("sent/list", message_views.MessagesListView.as_view()),
    path(
        "sent/update/delete/<int:message_id>",
        message_views.UpdateDeleteMessageView.as_view(),
    ),
    # Received messages endpoints
    path("received/list", message_views.ReceivedMessagesListView.as_view()),
    path("received/list/unread", message_views.UnreadMessagesListView.as_view()),
    path(
        "received/update/delete/<int:message_id>",
        message_views.UpdateDeleteMessageRecievedView.as_view(),
    ),
    # Users endpoints
    path("users/detail/<int:user_id>", user_views.DetailUserView.as_view()),
    path(
        "users/create/<str:password>/<str:username>/<str:first_name>/<str:last_name>/<str:email>",
        user_views.CreateUserView.as_view(),
    ),
]
