from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from config.settings import EMAIL_HOST_USER
from superuser.forms import RegistrationForm

from rest_framework.response import Response
from .serializer import UserSerializer


def send_email_view(request):
    if request.method == 'POST':
        email_subject = request.POST['subject']
        email_message = request.POST['message']
        email_from = EMAIL_HOST_USER
        email_to = [user.email for user in User.objects.all()]

        try:
            send_mail(email_subject, email_message, email_from, email_to)
            return HttpResponse('<h1>Email sent!</h1>')
        except Exception as e:
            return HttpResponse(f'<h1>Something went wrong</h1><p>{e}</p>', status=500)
    return render(request, 'superuser/email_message.html')


class UserDetailView(DetailView):
    model = User
    template_name = 'superuser/user.html'


class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        login(self.request, user)
        return redirect(self.success_url)


class RegisterAPIView(CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()
