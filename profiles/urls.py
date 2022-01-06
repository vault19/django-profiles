from django.urls import path

from profiles.views import base, ajax

urlpatterns = [
    path('profile/', base.full_profile, name='profile'),
    path('profile/edit/', ajax.edit_profile, name='edit_profile'),
    path('profile/edit/address', ajax.edit_address, name='edit_address'),
    path('profile/<str:username>/', base.public_profile, name='public_profile'),
    path('search/school/', ajax.search_school, name='search_school'),
]
