from datetime import datetime
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.template import Context, loader
from django.template.loader import render_to_string, get_template
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone,translation
from django.core import serializers
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from .models import Game
from accounts.models import Profile
import json


def calendar_view(request):
	if request.get_full_path()=="/myCalendar":
		context=get_calendar(request.user)
		return render(request,'games/calendar.html',context)
	else:
		context=get_calendar(None)
		return render(request,'games/calendar.html',context)


def month_detail_view(request):
	categories=[(0,"First party"),(1,"Third Party"),(2,"Indie"),(3,"Other")]
	month=request.GET.get("month")
	year=request.GET.get("year")
	is_user=request.GET.get("user")
	print("Mes",month,"año",year)
	if request.user==None:
		all_games=Game.objects.all()
	elif request.user!=None and is_user=="1":
		all_games=Game.objects.all()
	elif request.user!=None and is_user=="0":
		print("entra")
		all_games=Profile.objects.get(user=request.user).games
	if month=="0" and year=="0":
		try:
			games=all_games.filter(release_date=None).filter(year_release=None).order_by("release_date")
		except:
			games=[]
	elif month=="0" and year!="0":
		try: 
			games=all_games.filter(release_date=None,year_release=year).order_by("release_date")
		except: 
			games=[]
	else:
		try:
			games=all_games.filter(release_date__year=year).filter(release_date__month=month).order_by("release_date")
		except:
			games=[]
	context={
		'categories':categories,
		'games':games
	}
	return render(request,'games/monthDetail.html',context)

@login_required 
def add_games_view(request):
	context={'games':Game.objects.all()}
	return render(request,'games/addGames.html',context)
@login_required
def search_games_view(request):
	user_games=Profile.objects.get(user=request.user.id).games.all()
	search_query=request.GET.get("q")
	games=Game.objects.filter(name__icontains=search_query)
	json_list=[]
	for i in games:
		game_dict=dict()
		game_dict["id"]=i.id
		game_dict["name"]=i.name
		if i in user_games:
			game_dict["added"]=1
		else:
			game_dict["added"]=0
		json_list.append(game_dict)
	return JsonResponse(json_list,safe=False)
@login_required
def add_game_to_profile_view(request):
	profile=request.user.profile
	game_id=request.GET.get("id")
	try:
		profile.games.add(Game.objects.get(id=game_id))
		data={"status":"Added!"}
	except Exception as e:
		data={"status":"Something went wrong"}
	return JsonResponse(data)
@login_required
def remove_game_from_profile_view(request):
	profile=request.user.profile
	game_id=request.GET.get("id")
	try:
		profile.games.remove(Game.objects.get(id=game_id))
		data={"status":"Removed!"}
	except:
		data={"status":"Something went wrong"}
	return JsonResponse(data)
@login_required
def add_new_game_view(request):
	try:
		gname=request.POST.get("game_name")
		gtype=request.POST.get("game_type")
		radio=request.POST.get("radio_date")
		if radio=="TBA":
			game=Game(name=gname,category=gtype,added_by=request.user.username)
			game.save()
		elif radio=="year":
			game=Game(name=gname,category=gtype,year_release=request.POST.get("game_year"),added_by=request.user.username)
			game.save()
		else:
			gdate=datetime.strptime(request.POST.get("game_date"), '%Y-%m-%d')
			game=Game(name=gname,category=gtype,release_date=gdate,added_by=request.user.username)
			game.save()
		data={
			'status':'success'
		}
		return JsonResponse(data)
	except Exception as e :
		data={
			'status':'failure'
		}
		return JsonResponse(data)


def about_view(request):
	return render(request,'games/about.html',{})


def get_calendar(user):
	months=["January","February","March","April","May","June","July","August","September","October","November","December"]
	monthly_2018=list()
	monthly_2019=list()
	context={}
	if user==None:
		games=Game.objects.all()
		context["is_user"]="1"
	else:
		games=Profile.objects.get(user=user).games
		context["is_user"]="0"
	for i in range(12):
		try:
			if user==None:
				monthly_2018.append((months[i],i+1,games.filter(release_date__year=2018).filter(release_date__month=i+1).filter(front_page=True).order_by("release_date")))
				monthly_2019.append((months[i],i+1,games.filter(release_date__year=2019).filter(release_date__month=i+1).filter(front_page=True).order_by("release_date")))
			else:
				monthly_2018.append((months[i],i+1,games.filter(release_date__year=2018).filter(release_date__month=i+1).order_by("release_date")))
				monthly_2019.append((months[i],i+1,games.filter(release_date__year=2019).filter(release_date__month=i+1).order_by("release_date")))
		except:
			monthly_2018.append((months[i],i+1,None))
			monthly_2019.append((months[i],i+1,None))
	try: 
		twoeighteen=Game.objects.filter(release_date=None,year_release=2018)
	except: 
		twoeighteen=[]
	twonineteen=[]
	try:
		twonineteen=Game.objects.filter(release_date=None,year_release=2019)
	except: 
		twonineteen=[]
	tba=[]
	try:
		tba = Game.objects.filter(release_date=None).filter(year_release=None)
	except:
		tba=[]
	context['monthly_2018']=monthly_2018
	context['monthly_2019']=monthly_2019
	context['twoeighteen']=twoeighteen
	context['twonineteen']=twonineteen
	context['tba']=tba
	return context