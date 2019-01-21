from django.shortcuts import render,redirect
import sendgrid
import os
from sendgrid.helpers.mail import *
#from django.http import HttpResponse
#from django.template import Context, loader
from django.template.loader import render_to_string, get_template
#from django.contrib.auth.forms import UserCreationForm
#from django.utils import timezone,translation
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from . import tokens
from .models import SignUpForm

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			sg = sendgrid.SendGridAPIClient(apikey="")
			from_email = Email("noreply@switchcalendar.com")
			to_email = Email(user.email)
			subject = 'Activate Your Nintendo Switch calendar Account'
			current_site = 'switchcalendar.pythonanywhere.com'
			content = Content("text/plain", render_to_string('accounts/account_activation_email.html', {
				'user': user,
				'domain': current_site,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
				'token': tokens.account_activation_token.make_token(user),
			}))
			mail = Mail(from_email, subject, to_email, content)
			response = sg.client.mail.send.post(request_body=mail.get())
			#user.email_user(subject, message,'noreply@switchcalendar.com')
			return redirect('account_activation_sent')
	else:
		form = SignUpForm()
	return render(request, 'accounts/signup.html', {'form': form})

def profile_view(request):
	return render(request,'accounts/profile.html',{})

def account_activation_sent(request):
	return render(request,'accounts/account_activation_sent.html',{})

def account_activation_sent_error(request):
	return render(request,'accounts/account_activation_sent_error.html',{})

def account_activation_successful(request):
	return render(request,'accounts/account_activation_successful.html',{})

def activate(request, uidb64, token):
	try:
		uid = urlsafe_base64_decode(uidb64).decode()
		user = User.objects.get(pk=uid)
	except Exception as e:
		print(e)
		user = None

	if user is not None and tokens.account_activation_token.check_token(user, token):
		user.is_active = True
		user.profile.email_confirmed = True
		user.save()
		login(request, user)
		return redirect('account_activation_successful')
	else:
		return render(request, 'accounts/account_activation_invalid.html')
