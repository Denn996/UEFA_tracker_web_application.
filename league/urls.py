from django.urls import path
from . import views

urlpatterns = [
    path('', views.standings, name='standings'),
    path('matches/', views.match_results, name='matches'),
    path('home/', views.home, name='home'),

    #Authentication urls
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), 
]