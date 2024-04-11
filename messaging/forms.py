from django import forms

from .models import User


class SendMessageForm(forms.Form):
    sender_id = forms.ModelChoiceField(
        queryset=User.objects.values_list("id", flat=True), label="Sender ID"
    )
    message = forms.CharField(label="Message", max_length=500)
    subject = forms.CharField(label="Subject", max_length=50)
    receiver_id = forms.ModelChoiceField(
        queryset=User.objects.all(), label="Reciever ID"
    )
