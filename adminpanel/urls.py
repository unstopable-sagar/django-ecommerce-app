from django.urls import path
from .views import *

urlpatterns=[
    path('dashboard/',show_dashboard),
]