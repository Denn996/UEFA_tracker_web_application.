from django.contrib import admin
from django.urls import path, include

from league import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # This points the traffic to your league app
    path('', include('league.urls')),

    
]
