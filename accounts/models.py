# accounts/models.py
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to="doctors/",
        blank=True,
        null=True,
        help_text="Doctor profile picture"
    )

    def __str__(self):
        return f"{self.user.username} Profile"
