from django.urls import path
from . import views

urlpatterns = [
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('settings', views.settings, name='settings'),
]