from rest_framework import viewsets, permissions, filters
from django.core.exceptions import PermissionDenied
from .models import Patient
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["full_name", "cnic", "phone"]
    ordering_fields = ["full_name", "created_at", "age"]
    ordering = ["full_name"]
    
    def get_queryset(self):
        """🔒 IDOR FIX: Only return doctor's own patients"""
        return Patient.objects.filter(doctor=self.request.user)
    
    def perform_create(self, serializer):
        """Auto-assign current doctor to new patients"""
        serializer.save(doctor=self.request.user)
