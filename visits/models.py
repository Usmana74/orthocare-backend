from django.db import models
from django.conf import settings
from patients.models import Patient

# -----------------------------
# Visit Model
# -----------------------------
class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="visits")
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="visits",
    )
    visit_datetime = models.DateTimeField(auto_now_add=True)

    chief_complaint = models.TextField()
    history_of_illness = models.TextField(blank=True)
    physical_exam = models.TextField(blank=True)
    final_diagnosis = models.TextField()
    treatment_plan = models.TextField(blank=True)

    # New field: tests prescribed by doctor
    tests = models.JSONField(blank=True, null=True, default=list)

    follow_up_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-visit_datetime"]

    def __str__(self):
        return f"Visit {self.pk} - {self.patient}"


# -----------------------------
# Vitals Model
# -----------------------------
class Vitals(models.Model):
    visit = models.OneToOneField(Visit, on_delete=models.CASCADE, related_name="vitals")
    bp_systolic = models.PositiveIntegerField(null=True, blank=True)
    bp_diastolic = models.PositiveIntegerField(null=True, blank=True)
    pulse_rate = models.PositiveIntegerField(null=True, blank=True)
    temperature_f = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)  # now in °F
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    blood_sugar = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Vitals for {self.visit}"

    @property
    def bmi(self):
        if self.weight_kg and self.height_cm and self.height_cm > 0:
            h_m = float(self.height_cm) / 100
            if h_m > 0:
                return round(float(self.weight_kg) / (h_m ** 2), 2)
        return None


# -----------------------------
# Prescription Model
# -----------------------------
class Prescription(models.Model):
    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        related_name="prescriptions",
        blank=True,
        null=True  # optional: a visit may not have any prescriptions
    )
    drug_name = models.CharField(max_length=128)
    dose = models.CharField(max_length=64, blank=True)
    frequency = models.CharField(max_length=64, blank=True)
    duration_days = models.CharField(max_length=32, blank=True)
    instructions = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.drug_name} ({self.dose})"


# -----------------------------
# Attachments Model
# -----------------------------
class Attachment(models.Model):
    class Kind(models.TextChoices):
        XRAY = "XRAY", "X-ray imaging"
        MRI = "MRI", "MRI"
        CT = "CT", "CT scan"
        LAB = "LAB", "Lab report"
        OTHER = "OTHER", "Other"

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name="attachments")
    kind = models.CharField(max_length=10, choices=Kind.choices, default=Kind.XRAY)
    image = models.ImageField(upload_to="attachments/%Y/%m/%d/")
    region_note = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.kind} - {self.visit}"
