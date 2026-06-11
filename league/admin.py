from django.contrib import admin
from .models import Team, Match

# This tells Django to show these tables in the admin dashboard
admin.site.register(Team)
admin.site.register(Match)
