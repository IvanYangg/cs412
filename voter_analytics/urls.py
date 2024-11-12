# Name: Ivan Yang
# BU Email: yangi@bu.edu
# Description: This file defines all the custom urls/url-mapping that are used in this project

from django.urls import path
from . import views

urlpatterns = [
    path('', views.VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>/', views.VoterDetailView.as_view(), name='voter'),
]