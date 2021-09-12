from django.urls import path

from profiles import views

urlpatterns = [
    path('profile', views.my_profile, name='profile'),
    path('change_password', views.change_password, name='change_password'),
]

