from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	path('signup/', views.signup, name='signup'),
    path('log_in', auth_views.login,{'template_name': 'accounts/login.html'}, name='login'),
    path('logout', auth_views.logout, {'next_page': '/'},name='logout'),
    path('account_activation_successful',views.account_activation_successful,name='account_activation_successful'),
    path('account_activation_sent', views.account_activation_sent, name='account_activation_sent'),
    path('account_activation_sent_error',views.account_activation_sent_error,name='account_activation_sent_error'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('profile',views.profile_view,name="profile"),
]