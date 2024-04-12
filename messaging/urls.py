from django.urls import path

from .views import message_views, user_views

urlpatterns = [
    path("", message_views.index, name="index"),
    # path("messages/", views.SenderView.as_view()),
    path(
        "create/<int:sender_id>/<int:receiver_id>/<str:message>/<str:subject>",
        message_views.SendMessageView.as_view(),
    ),
    path("detail/<int:message_id>", message_views.ReadMessageView.as_view()),
    path("list/<int:user_id>", message_views.MessagesListView.as_view()),
    path("list/unread/<int:user_id>", message_views.UnreadMessagesListView.as_view()),
    path("update/<int:message_id>", message_views.DeleteMessageView.as_view()),
    path("users/detail/<int:user_id>", user_views.DetailUserView.as_view()),
    path(
        "users/create/<str:password>/<str:username>/<str:first_name>/<str:last_name>/<str:email>",
        user_views.CreateUserView.as_view(),
    ),
]
