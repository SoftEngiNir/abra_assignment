from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length=50)
    body = models.CharField(max_length=500)
    creation_datetime = models.DateTimeField()
    deleted = models.BooleanField(default=False)


class MessageReceived(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    message = models.ForeignKey(Message, on_delete=models.DO_NOTHING)
    is_read = models.BooleanField(default=False)
    creation_datetime = models.DateTimeField()
    deleted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipient", "message"], name="unique_recipient_message"
            )
        ]
