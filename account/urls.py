from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from account.views import RegisterAPIView, ActivateAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('activate/', ActivateAPIView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]