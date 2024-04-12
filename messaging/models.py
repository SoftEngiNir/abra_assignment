from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="receiver"
    )
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=500)
    creation_datetime = models.DateTimeField()
    is_read = models.BooleanField(default=False)
    deleted_by_sender = models.BooleanField(default=False)
    deleted_by_receiver = models.BooleanField(default=False)
