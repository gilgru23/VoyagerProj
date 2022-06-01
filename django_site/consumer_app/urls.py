#created by tzuri (not autogenerated)
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('register_dispenser', views.register_dispenser, name='register dispenser'),
    path('register_pod', views.register_pod, name='register_pod'),
    path('dose', views.dose, name='dose'),
    path('get_recomendation', views.get_recomendation, name='get_recomendation'),
    path('set_dosing_reminder', views.set_dosing_reminder, name='set_dosing_reminder'),
    path('set_regimen', views.set_regimen, name='set_regimen'),
    path('get_regimen', views.get_regimen, name='get_regimen'),
    path('get_dosing_history', views.get_dosing_history, name='get_dosing_history'),
    path('get_pods_of_consumer', views.get_pods_of_consumer, name='get_pods_of_consumer'),
    path('get_dispensers_of_consumer', views.get_dispensers_of_consumer, name='get_dispensers_of_consumer'),
    path('provide_feedback', views.provide_feedback, name='provide_feedback'),
    path('get_feedback_for_dosing', views.get_feedback_for_dosing, name='get_feedback_for_dosing')
]