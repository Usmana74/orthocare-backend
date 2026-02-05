from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.core.exceptions import PermissionDenied

from .models import Visit, Attachment, Prescription
from .serializers import (
    VisitListSerializer,
    VisitDetailSerializer,
    VisitWriteSerializer,
    AttachmentSerializer,
)


class VisitViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "chief_complaint",
        "final_diagnosis",
        "patient__full_name",
        "patient__cnic",
    ]
    ordering_fields = ["visit_datetime", "follow_up_date"]
    ordering = ["-visit_datetime"]

    def get_queryset(self):
        """🔒 IDOR FIX: Only return visits for doctor's own patients"""
        qs = (
            Visit.objects
            .filter(doctor=self.request.user)  # 🔒 CRITICAL LINE
            .select_related("patient", "doctor", "vitals")
            .prefetch_related("prescriptions", "attachments")
        )

        patient_id = self.request.query_params.get("patient")
        if patient_id:
            qs = qs.filter(patient_id=patient_id)

        return qs.order_by("-visit_datetime")

    def get_serializer_class(self):
        if self.action == "list":
            return VisitListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return VisitWriteSerializer
        return VisitDetailSerializer

    def perform_create(self, serializer):
        """Handle attachment uploads during create + assign doctor"""
        print("\n🔍 PERFORM_CREATE called")
        
        # 🔒 Auto-assign current doctor
        visit = serializer.save(doctor=self.request.user)
        
        # Handle new attachments
        attachments = self.request.FILES.getlist('attachments')
        print(f"  Found {len(attachments)} attachments to upload")
        
        for file in attachments:
            att = Attachment.objects.create(
                visit=visit,
                image=file,
                kind=Attachment.Kind.OTHER,
            )
            print(f"  ✅ Created attachment: {att.id}")
        
        return visit

    def perform_update(self, serializer):
        """Handle attachment deletions and uploads during update"""
        print("\n🔍 PERFORM_UPDATE called")
        
        # 🔒 Verify ownership before update
        if serializer.instance.doctor != self.request.user:
            raise PermissionDenied("You can only update your own visits")
        
        # 1. Delete marked attachments
        deleted_ids = self.request.data.get('deleted_attachment_ids')
        if deleted_ids:
            print(f"  Deleted attachment IDs received: {deleted_ids}")
            try:
                import json
                ids = json.loads(deleted_ids) if isinstance(deleted_ids, str) else deleted_ids
                print(f"  Parsed IDs: {ids}")
                
                for att_id in ids:
                    try:
                        att = Attachment.objects.get(id=att_id, visit=serializer.instance)
                        print(f"  Deleting attachment {att_id}: {att.image.name}")
                        
                        # Delete file from storage
                        if att.image:
                            att.image.delete(save=False)
                        
                        # Delete database record
                        att.delete()
                        print(f"  ✅ Deleted attachment {att_id}")
                    except Attachment.DoesNotExist:
                        print(f"  ⚠️ Attachment {att_id} not found")
                        pass
            except (json.JSONDecodeError, ValueError) as e:
                print(f"  ❌ Error parsing deleted_attachment_ids: {e}")
                pass
        
        # 2. Save the visit
        visit = serializer.save()
        print(f"  ✅ Visit {visit.id} updated")
        
        # 3. Handle new attachments
        attachments = self.request.FILES.getlist('attachments')
        print(f"  Found {len(attachments)} new attachments to upload")
        
        for file in attachments:
            att = Attachment.objects.create(
                visit=visit,
                image=file,
                kind=Attachment.Kind.OTHER,
            )
            print(f"  ✅ Created attachment: {att.id}")
        
        return visit

    @action(detail=True, methods=["post"])
    def attachments(self, request, pk=None):
        """Legacy endpoint for adding attachments"""
        visit = self.get_object()  # 🔒 Uses get_queryset filter
        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "No file provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Attachment.objects.create(
            visit=visit,
            image=file,
            kind=request.data.get("kind", Attachment.Kind.OTHER),
            region_note=request.data.get("region_note", ""),
        )

        return Response(
            {"status": "uploaded"},
            status=status.HTTP_201_CREATED,
        )


class AttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "delete"]
    
    def get_queryset(self):
        """🔒 IDOR FIX: Only return attachments from doctor's visits"""
        return Attachment.objects.filter(visit__doctor=self.request.user)
    
    def perform_destroy(self, instance):
        """Delete file from storage when deleting attachment"""
        print(f"\n🔍 DELETING ATTACHMENT {instance.id}")
        
        # 🔒 Verify ownership
        if instance.visit.doctor != self.request.user:
            raise PermissionDenied("You can only delete your own attachments")
        
        print(f"  File: {instance.image.name}")
        
        # Delete the actual file from storage
        if instance.image:
            try:
                instance.image.delete(save=False)
                print(f"  ✅ File deleted from storage")
            except Exception as e:
                print(f"  ⚠️ Error deleting file: {e}")
        
        # Delete database record
        instance.delete()
        print(f"  ✅ Database record deleted")
