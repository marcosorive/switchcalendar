from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import UserCreationForm
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string


class Game(models.Model):
	CATEGORY_OPTIONS=(
		(0,"First Party"),
		(1,"Third Party"),
		(2,"Indie"),
		(3,"Other"),
	)
	id=models.AutoField(primary_key=True)
	name=models.CharField(max_length=50)
	release_date=models.DateField(auto_now=False, auto_now_add=False,null=True,default=None,blank=True)
	year_release=models.IntegerField(null=True,default=None,blank=True)
	category=models.IntegerField(null=True,blank=True,choices=CATEGORY_OPTIONS)
	front_page=models.BooleanField(default=False)
	switch_exclusive=models.NullBooleanField(null=True,blank=True)
	link=models.CharField(max_length=200,null=True,default=None,blank=True)
	added_by=models.CharField(max_length=50,null=True,default=None,blank=True)

	def __str__(self):
		return self.name