
from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.index, name="index"),
    path('main/', views.main, name='main'),
    path('about/', views.about, name="about"),
    path('comment/', views.comment, name="comment"),
    path('comment_submit/', views.comment_submit, name="comment_submit"),
    path('creator/<int:id>/', views.creator_page, name="creator"),
    path('show/<int:id>/', views.show_page, name="show"),
]