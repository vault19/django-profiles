from django.urls import path

from profiles import views

urlpatterns = [
    path('profile', views.my_profile, name='profile'),
    path('search/school', views.search_school, name='search_school'),
]

