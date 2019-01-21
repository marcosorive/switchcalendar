from django.db import models
from django import forms
class ContactForm(forms.Form):
	name=forms.CharField(label='Your name',required=True)
	from_email=forms.EmailField(label='Your email',required=True)
	subject=forms.CharField(required=True)
	message=forms.CharField(widget=forms.Textarea,required=True)
