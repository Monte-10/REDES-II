from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.lista_dispositivos, name='lista_dispositivos'),
    path('nuevo/', views.nuevo_dispositivo, name='nuevo_dispositivo'),
    path('editar/<int:pk>/', views.editar_dispositivo, name='editar_dispositivo'),
]
