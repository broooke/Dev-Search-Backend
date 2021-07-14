from django.urls import path
from . import views

urlpatterns = [
    path('', views.getProjects, name='projects'),
    path('<str:name>/', views.getProject, name='project'),
    path('review/add/', views.addReview, name='add_review')
]