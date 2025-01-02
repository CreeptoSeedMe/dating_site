from django.urls import path
from . import views

urlpatterns = [
    path('conversations/', views.conversations, name='conversations'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
]