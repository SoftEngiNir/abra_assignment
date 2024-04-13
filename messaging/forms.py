from django import forms

from .models import User


class SendMessageForm(forms.Form):
    creator_id = forms.ModelChoiceField(
        queryset=User.objects.values_list("id", flat=True), label="Creator ID"
    )
    recipient_id = forms.ModelChoiceField(
        queryset=User.objects.all(), label="Recipient ID"
    )
    body = forms.CharField(label="Body", max_length=500)
    subject = forms.CharField(label="Subject", max_length=50)
