from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CurrentUserView, UpdateProfileView, ChangePasswordView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", CurrentUserView.as_view(), name="current_user"),
    path("me/profile/", UpdateProfileView.as_view(), name="update_profile"),
    path("me/change-password/", ChangePasswordView.as_view(), name="change_password"),
]
