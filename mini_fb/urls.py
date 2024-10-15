# Name: Ivan Yang
# BU Email: yangi@bu.edu
# Description: This file maps all views to URLs

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
]
