from django.db import models

class Patient(models.Model):
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    full_name = models.CharField(max_length=128)  # required
    age = models.PositiveIntegerField()           # required (years)

    gender = models.CharField(max_length=1, choices=Gender.choices)  # required
    cnic = models.CharField(max_length=20, blank=True, null=True)  # optional
    phone = models.CharField(max_length=20)       # required

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name
