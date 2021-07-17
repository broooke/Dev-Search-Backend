from django.urls import path
from . import views

urlpatterns = [
    path('', views.getDevelopers, name='developers'),
    path('add/skill/', views.addSkill, name='add_skill'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('update/', views.updateUser, name='update'),
    path('register/', views.registerUser, name='register'),
    path('<str:pk>/', views.getDeveloper, name='developer'),
]