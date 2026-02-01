from rest_framework import viewsets, permissions, filters
from .models import Patient
from .serializers import PatientSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["full_name", "cnic", "phone"]
    ordering_fields = ["full_name", "created_at","age"]
    ordering = ["full_name"]
