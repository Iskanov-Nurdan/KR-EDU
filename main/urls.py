from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
]
