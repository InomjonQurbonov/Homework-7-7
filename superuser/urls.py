from django.urls import path

from .views import send_email, UserView, RegistrationView

urlpatterns = [
    path('superuser/', send_email, name='superuser'),
    path('profile/<int:pk>', UserView.as_view(), name='profile'),
    path('register/', RegistrationView.as_view(), name='registration')
]