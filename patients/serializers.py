from rest_framework import serializers
from .models import Patient
from visits.models import Visit
from visits.serializers import VisitListSerializer



class PatientSerializer(serializers.ModelSerializer):
    visits = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            "id",
            "full_name",
            "age",
            "gender",
            "cnic",
            "phone",
            "created_at",
            "updated_at",
            "visits",
        ]

    def get_visits(self, obj):
        # Fetch visits related to this patient
        visits = obj.visits.all().order_by("-visit_datetime")  # use visit_datetime
        from visits.serializers import VisitListSerializer  # import here to avoid circular imports
        return VisitListSerializer(visits, many=True).data
