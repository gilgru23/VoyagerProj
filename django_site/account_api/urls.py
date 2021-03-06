from django.urls import path
from . import views

urlpatterns = [
    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register'),
    path('create_consumer_profile', views.create_consumer_profile, name='create consumer profile'),
    path('db_check', views.check_db, name='check db')
]