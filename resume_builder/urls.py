from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from builder import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('builder.urls')),
]