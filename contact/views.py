from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.template.loader import render_to_string, get_template
from django.shortcuts import render, redirect
import sendgrid
from sendgrid.helpers.mail import *
from .forms import ContactForm

def contactView(request):
	if request.method == 'GET':
		form=ContactForm()
	else:
		form=ContactForm(request.POST)
		if form.is_valid():
			name=form.cleaned_data['name']
			user_email=form.cleaned_data['from_email']
			subject=form.cleaned_data['subject']
			message=form.cleaned_data['message']
			sg = sendgrid.SendGridAPIClient(apikey="")
			from_email = Email("noreply@switchcalendar.com")
			to_email = Email("switch@orive.me")
			subject = 'Nuevo mensaje en switchcalendar'
			content = Content("text/plain", render_to_string('contact/contact_template.txt', {
				'name':name,
				'from_email':user_email,
				'subject':subject,
				'message':message,
			}))

			try:
				mail = Mail(from_email, subject, to_email, content)
				response = sg.client.mail.send.post(request_body=mail.get())			
			except BadHeaderError:
				return redirect('failure')
			return redirect('success')
	return render(request,"contact/contact.html",{'form':form})

def successView(request):
	return render(request,'contact/success.html',{})

def failureView(request):
	return render(request,'contact/failure.html',{})
