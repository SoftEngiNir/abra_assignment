from django.urls import path

from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    # path("messages/", views.SenderView.as_view()),
    path("create/", views.SendMessageView.as_view()),
    path("", views.MessagesListView.as_view()),
    # path("/messages/<str:message>/<str:subject>/<int:receiver_id>/", views.SenderView.as_view())
]
