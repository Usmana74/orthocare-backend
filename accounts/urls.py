from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginView,          # 🔥 YOUR CUSTOM LOGIN VIEW
    CurrentUserView, 
    UpdateProfileView, 
    ChangePasswordView
)

urlpatterns = [
    # 🔥 CUSTOM LOGIN VIEW WITH AllowAny
    path("token/", LoginView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", CurrentUserView.as_view(), name="current_user"),
    path("me/profile/", UpdateProfileView.as_view(), name="update_profile"),
    path("me/change-password/", ChangePasswordView.as_view(), name="change_password"),
]
