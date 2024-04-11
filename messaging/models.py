from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Message(models.Model):
    sender_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='sender_id')
    receiver_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='receiver_id')
    message = models.CharField(max_length=500)
    subject = models.CharField()
    creation_datetime = models.DateTimeField()
    is_read = models.BooleanField(default=False)
