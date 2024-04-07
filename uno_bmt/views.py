from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from rest_framework import permissions
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import WorldNews, Members
from .serializers import (
    MembersSerializer, WorldNewsSerializer, NewsDetailsSerializer,
    UpdateNewsSerializer, DeleteNewsSerializer, MembersDetailSerializer,
    UpdateMembersSerializer, DeleteMemberSerializer, CreateMembersSerializer
)


def index(request):
    news = WorldNews.objects.all()
    return render(request, 'index.html', {'news': news})


class MemberListView(ListView):
    model = Members
    template_name = 'about_us.html'
    context_object_name = 'members'


class NewPageView(ListView):
    model = WorldNews
    template_name = 'news/news_list.html'
    context_object_name = 'news'


class NewsDetailView(DetailView):
    model = WorldNews
    template_name = 'news/about_news.html'
    context_object_name = 'news'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        WorldNews.objects.filter(pk=self.object.pk).update(add_views_count=F('add_views_count') + 1)
        return response


class NewsAddView(LoginRequiredMixin, CreateView):
    model = WorldNews
    template_name = 'news/add_news.html'
    fields = ['news_title', 'news_content', 'news_image', 'news_description', 'news_areas']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.news_author = self.request.user
        return super().form_valid(form)


class NewsListView(ListView):
    model = WorldNews
    template_name = 'news/news_list.html'
    context_object_name = 'news'

    def get_queryset(self):
        if 'areas' in self.request.GET:
            try:
                return WorldNews.objects.filter(news_areas=self.request.GET['areas'])
            except:
                return redirect('news')
        if 'keyword' in self.request.GET:
            try:
                return (WorldNews.objects.filter(
                    news_title__icontains=self.request.GET['keyword']) |
                        WorldNews.objects.filter(news_description__icontains=self.request.GET['keyword']) |
                        WorldNews.objects.filter(news_content__icontains=self.request.GET['keyword']))
            except:
                return WorldNews.objects.none()
        return WorldNews.objects.all()


class UpdateNewsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'news/edit_news.html'
    model = WorldNews
    fields = ['news_title', 'news_description', 'news_image', 'news_content', 'news_areas']
    success_url = reverse_lazy('list_news')

    def test_func(self):
        news = WorldNews.objects.get(pk=self.kwargs['pk'])
        return self.request.user == news.news_author

    def form_valid(self, form):
        form.instance.news_author = self.request.user
        return super().form_valid(form)


class DeleteNewsView(LoginRequiredMixin, DeleteView):
    model = WorldNews
    success_url = reverse_lazy('list_news')
    template_name = 'news/confirm_delete.html'

    def get_queryset(self):
        return super().get_queryset().filter(news_author=self.request.user)


class MemberListAPIView(ListAPIView):
    queryset = Members.objects.all()
    serializer_class = MembersSerializer

    def get_queryset(self):
        if 'members' in self.request.GET:
            try:
                return (Members.objects.filter(member_name__icontains=self.request.GET['keyword']))
            except:
                return Members.objects.none()
        return Members.objects.all()


class MembersDetailAPIView(RetrieveAPIView):
    queryset = Members.objects.all()
    serializer_class = MembersDetailSerializer


class MembersCreateAPIView(CreateAPIView):
    queryset = Members.objects.all()
    serializer_class = CreateMembersSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]


class IsVacationOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return view.get_object().members_user == request.user


class MembersUpdateAPIView(IsVacationOwner, RetrieveUpdateAPIView):
    queryset = Members.objects.all()
    serializer_class = UpdateMembersSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]


class MembersDeleteAPIView(DestroyAPIView):
    queryset = Members.objects.all()
    serializer_class = DeleteMemberSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]


class NewsListAPIView(ListAPIView):
    queryset = WorldNews.objects.all()
    serializer_class = WorldNewsSerializer

    def get_queryset(self):
        if 'news' in self.request.GET:
            try:
                return (WorldNews.objects.filter(
                    news_title__icontains=self.request.GET['keyword']) |
                        WorldNews.objects.filter(news_description__icontains=self.request.GET['keyword']) |
                        WorldNews.objects.filter(news_content__icontains=self.request.GET['keyword']))
            except:
                return WorldNews.objects.none()
        return WorldNews.objects.all()


class NewsDetailAPIView(RetrieveAPIView):
    queryset = WorldNews.objects.all()
    serializer_class = NewsDetailsSerializer


class NewsCreateAPIView(CreateAPIView):
    queryset = WorldNews.objects.all()
    serializer_class = WorldNewsSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]


class NewsUpdateAPIView(UpdateAPIView):
    queryset = WorldNews.objects.all()
    serializer_class = UpdateNewsSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]


class NewsDeleteAPIView(DestroyAPIView):
    queryset = WorldNews.objects.all()
    serializer_class = DeleteNewsSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]
