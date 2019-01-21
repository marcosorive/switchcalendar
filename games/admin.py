from django.contrib import admin
from .models import Game

class GameAdmin(admin.ModelAdmin):
	list_display=('name', 'release_date', 'category', 'front_page')
	list_filter = ('release_date','category', 'front_page')
	ordering = ['-release_date']
	search_fields = ('name',)
	readonly_fields = ['added_by']

admin.site.register(Game,GameAdmin)