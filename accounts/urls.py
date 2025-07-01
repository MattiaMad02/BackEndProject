from .views import RegisterUser
from django.urls import path, include
urlpatterns = [
    path("register/", RegisterUser.as_view(), name="register"),
]
