from django.urls import path 
from .views import *

app_name = "account"

urlpatterns = [
    path("signup/", register, name="register"),
    path("signout/", log_out, name="logout")
]