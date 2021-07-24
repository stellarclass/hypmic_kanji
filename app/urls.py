from django.urls import path
from . import views

urlpatterns = [
    path('', views.lesson_page, name='lesson_page'),
]