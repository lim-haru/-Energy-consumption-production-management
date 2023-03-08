from django.urls import path
from . import views
from .views import EnergyDetail, EnergyInfo

urlpatterns = [
    path('api', EnergyDetail.as_view(), name='api'),
    path('api/<int:id>', EnergyInfo.as_view()),
    path('', views.home, name='home'),
]