
from django.urls import path
from . import views
#from script_app.views import APIindexPaginationView


urlpatterns = [
    path('', views.index.as_view(), name="index"),
    path('main/', views.main.as_view(), name='main'),
    path('about/', views.about.as_view(), name="about"),
    path('comment/', views.comment.as_view(), name="comment"),
    path('comment_submit/', views.comment_submit.as_view(), name="comment_submit"),
    path('creator/<int:id>/', views.creator_page.as_view(), name="creator"),
    path('show/<int:id>/', views.show_page.as_view(), name="show"),
]