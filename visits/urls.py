from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VisitViewSet, AttachmentViewSet

router = DefaultRouter()
router.register("", VisitViewSet, basename="visit")
router.register("attachments", AttachmentViewSet, basename="attachment")

urlpatterns = [
    path("", include(router.urls)),
]
