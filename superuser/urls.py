from django.urls import path

from .views import (
    send_email_view, UserDetailView, RegistrationView,
    RegisterAPIView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('superuser/', send_email_view, name='superuser'),
    path('profile/<int:pk>', UserDetailView.as_view(), name='profile'),
    path('register/', RegistrationView.as_view(), name='registration'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterAPIView.as_view()),
]
