from django.contrib import admin 
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('comment/', views.comment, name="comment"),
    path('comment_submit/', views.comment_submit, name="comment_submit"),
    path('search/', views.search, name="search"),
]