
from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.index, name="index"),
    path('main/', views.main, name='main'),
    path('about/', views.about, name="about"),
    path('comment/', views.comment, name="comment"),
    path('comment_submit/', views.comment_submit, name="comment_submit"),
]