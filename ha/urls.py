from django.urls import path
from .views import ha_config

urlpatterns = [
    path('', ha_config, name='ha_config'),
]
