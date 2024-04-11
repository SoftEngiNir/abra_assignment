from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    # def __str__(self):
    #     return self.first_name + ' ' + self.last_name


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    message = models.CharField(max_length=500)
    subject = models.CharField()
    creation_datetime = models.DateTimeField()


class MessageUserLink(models.Model):
    message = models.ForeignKey(Message, on_delete=models.DO_NOTHING)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
