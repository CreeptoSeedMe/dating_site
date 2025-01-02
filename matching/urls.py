from django.urls import path
from . import views

urlpatterns = [
    path('browse/', views.browse_profiles, name='browse_profiles'),
    path('like/<int:profile_id>/', views.like_profile, name='like_profile'),
    path('matches/', views.matches, name='matches'),
]