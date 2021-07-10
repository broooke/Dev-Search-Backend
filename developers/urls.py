from django.urls import path
from . import views

urlpatterns = [
    path('', views.getDevelopers, name='developers'),
    path('<str:pk>/', views.getDeveloper, name='developer'),
]