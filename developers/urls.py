from django.urls import path
from . import views

urlpatterns = [
    path('', views.getDevelopers, name='developers'),
    path('add/skill/', views.addSkill, name='add_skill'),
    path('edit/skill/', views.editSkill, name='edit_skill'),
    path('delete/skill/', views.deleteSkill, name='delete_skill'),
    path('add/project/', views.addProject, name='add_project'),
    path('delete/project/', views.deleteProject, name='delete_project'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('update/', views.updateUser, name='update'),
    path('register/', views.registerUser, name='register'),
    path('<str:pk>/', views.getDeveloper, name='developer'),
]