from django.urls import path
from . import views

urlpatterns = [
    path('', views.getDevelopers, name='developers'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('<str:pk>/', views.getDeveloper, name='developer'),
]