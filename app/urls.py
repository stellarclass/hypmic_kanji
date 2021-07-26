from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('lesson/', views.lesson_page, name='lesson_page'),
    path('review/', views.review_page, name='review_page'),
]