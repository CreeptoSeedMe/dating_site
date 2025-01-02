from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Подключение маршрутов приложения users
    path('matching/', include('matching.urls')),  # Подключение маршрутов приложения matching
    path('chat/', include('chat.urls')),  # Подключение маршрутов приложения chat
    path('', lambda request: redirect('users:login')),  # Перенаправление на страницу входа
]
