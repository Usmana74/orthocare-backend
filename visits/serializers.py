from rest_framework import serializers
from django.db import transaction
import json
from .models import Visit, Vitals, Prescription, Attachment
from patients.models import Patient

# ---------------------- Patient Mini ----------------------
class PatientMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "full_name","phone", "age", "gender"]


# ------------------------- Vitals -------------------------
class VitalsSerializer(serializers.ModelSerializer):
    bmi = serializers.ReadOnlyField()

    class Meta:
        model = Vitals
        fields = [
            "bp_systolic",
            "bp_diastolic",
            "pulse_rate",
            "temperature_f",
            "weight_kg",
            "height_cm",
            "blood_sugar",
            "bmi",
        ]


# ---------------------- Prescription ----------------------
class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = [
            "id",
            "drug_name",
            "dose",
            "frequency",
            "duration_days",
            "instructions",
        ]


# ---------------------- Attachment ------------------------
class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ["id", "kind", "image", "region_note", "uploaded_at"]
        read_only_fields = ["uploaded_at"]


# ---------------------- Visit List ------------------------
class VisitListSerializer(serializers.ModelSerializer):
    patient = PatientMiniSerializer(read_only=True)

    class Meta:
        model = Visit
        fields = "__all__"


# ---------------------- Visit Write ----------------------
class VisitWriteSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    
    # ✅ Use JSONField instead of ListField/DictField - more permissive
    prescriptions = serializers.JSONField(required=False, allow_null=True, write_only=True)
    vitals = serializers.JSONField(required=False, allow_null=True, write_only=True)

    class Meta:
        model = Visit
        fields = "__all__"
        read_only_fields = ["doctor", "created_at", "updated_at"]

    def to_internal_value(self, data):
     """Don't parse - let JSONField handle it"""
     print("\n🔍 to_internal_value - RAW DATA RECEIVED:")
     print(f"  vitals raw: {data.get('vitals')} (type: {type(data.get('vitals'))})")
     print(f"  prescriptions raw: {data.get('prescriptions')} (type: {type(data.get('prescriptions'))})")
    
     if hasattr(data, '_mutable'):
        data._mutable = True
    
    # ✅ DON'T PARSE - Just pass strings to JSONField
    # JSONField will handle the parsing
    
     try:
        result = super().to_internal_value(data)
        
        print(f"\n🔍 to_internal_value - AFTER super():")
        print(f"  'vitals' in result: {'vitals' in result}")
        print(f"  vitals value: {result.get('vitals')}")
        print(f"  vitals type: {type(result.get('vitals'))}")
        
        return result
     except Exception as e:
        print(f"\n❌ ERROR in super().to_internal_value:")
        print(f"  Type: {type(e)}")
        print(f"  Message: {str(e)}")
        raise



    def to_representation(self, instance):
        """Use detail serializer for output"""
        return VisitDetailSerializer(instance, context=self.context).data

    def create(self, validated_data):
        print("\n" + "="*80)
        print("🔍 SERIALIZER CREATE CALLED")
        
        # Extract nested data
        vitals_data = validated_data.pop("vitals", None)
        prescriptions_data = validated_data.pop("prescriptions", None)

        print(f"\n🔍 VITALS DATA: {vitals_data}")
        print(f"🔍 PRESCRIPTIONS DATA: {prescriptions_data}")

        # Unwrap double-nested prescriptions
        if prescriptions_data and isinstance(prescriptions_data, list) and len(prescriptions_data) > 0:
            if isinstance(prescriptions_data[0], list):
                prescriptions_data = prescriptions_data[0]

        # Set doctor
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["doctor"] = request.user

        with transaction.atomic():
            visit = Visit.objects.create(**validated_data)
            print(f"✅ Visit created: {visit.id}")

            # Create vitals (don't filter - save everything)
            if vitals_data:
                Vitals.objects.create(visit=visit, **vitals_data)
                print(f"✅ Vitals created")

            # Create prescriptions
            if prescriptions_data:
                for presc in prescriptions_data:
                    if isinstance(presc, dict) and presc.get("drug_name"):
                        Prescription.objects.create(visit=visit, **presc)
                        print(f"✅ Created prescription: {presc.get('drug_name')}")

        visit.refresh_from_db()
        print("="*80 + "\n")
        return visit

    def update(self, instance, validated_data):
        print("\n" + "="*80)
        print("🔍 SERIALIZER UPDATE CALLED")
        
        # Extract nested data
        vitals_data = validated_data.pop("vitals", None)
        prescriptions_data = validated_data.pop("prescriptions", None)
        
        print(f"\n🔍 VITALS DATA: {vitals_data}")
        print(f"🔍 PRESCRIPTIONS DATA: {prescriptions_data}")

        # Unwrap double-nested prescriptions
        if prescriptions_data and isinstance(prescriptions_data, list) and len(prescriptions_data) > 0:
            if isinstance(prescriptions_data[0], list):
                prescriptions_data = prescriptions_data[0]

        with transaction.atomic():
            # Update basic fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            print("✅ Basic fields updated")

            # Update vitals (don't filter - save everything)
            if vitals_data:
                Vitals.objects.update_or_create(
                    visit=instance,
                    defaults=vitals_data
                )
                print("✅ Vitals updated")

            # Update prescriptions
            if prescriptions_data is not None:
                instance.prescriptions.all().delete()
                for presc in prescriptions_data:
                    if isinstance(presc, dict) and presc.get("drug_name"):
                        Prescription.objects.create(visit=instance, **presc)
                        print(f"✅ Created prescription: {presc.get('drug_name')}")

        instance.refresh_from_db()
        print(f"✅ FINAL: Prescriptions={instance.prescriptions.count()}, Vitals={'Yes' if hasattr(instance, 'vitals') else 'No'}")
        print("="*80 + "\n")
        
        return instance




# ---------------------- Visit Detail ----------------------
class VisitDetailSerializer(serializers.ModelSerializer):
    patient = PatientMiniSerializer(read_only=True)
    vitals = VitalsSerializer(read_only=True)
    prescriptions = PrescriptionSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Visit
        fields = "__all__"