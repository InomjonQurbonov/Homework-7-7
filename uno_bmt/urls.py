from django.urls import path
from .views import (
    index, NewPageView, NewsDetailView,
    NewsAddView, UpdateNewsView, DeleteNewsView,
    MemberListView, MemberListAPIView, NewsListAPIView,
    NewsCreateAPIView, NewsDetailAPIView,NewsUpdateAPIView,
    NewsDeleteAPIView
)

urlpatterns = [
    path('', index, name='home'),
    path('news/', NewPageView.as_view(), name='news'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='about_news'),
    path('add_news', NewsAddView.as_view(), name='add_news'),
    path('update/<int:pk>/', UpdateNewsView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteNewsView.as_view(), name='delete'),
    path('members/', MemberListView.as_view(), name='about_us'),
    path('members_api/', MemberListAPIView.as_view()),
    path('worldnews/', NewsListAPIView.as_view()),
    path('worldnews/<int:pk>/', NewsDetailAPIView.as_view()),
    path('worldnews/create/', NewsCreateAPIView.as_view()),
    path('worldnews/update/<int:pk>/', NewsUpdateAPIView.as_view()),
    path('worldnews/delete/<int:pk>/', NewsDeleteAPIView.as_view())
]