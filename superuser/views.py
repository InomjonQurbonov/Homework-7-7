from django.contrib.auth import login
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView

from config.settings import EMAIL_HOST_USER
from superuser.forms import RegistrationForm


def send_email(request):
    if request.method == 'POST':
        try:
            recipient_list = [user.email for user in User.objects.all()]

            send_mail(
                subject=request.POST['subject'],
                message=request.POST['message'],
                from_email=EMAIL_HOST_USER,
                recipient_list=recipient_list
            )
            return HttpResponse('<h1>Email sent!</h1>')
        except Exception as e:
            return HttpResponse(f'<h1>Something went wrong</h1><p>{e}</p>', status=500)
    return render(request, 'superuser/email_message.html')


class UserView(DetailView):
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
