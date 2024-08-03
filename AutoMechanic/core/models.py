from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class CustomUser(AbstractUser):
    is_mechanic = models.BooleanField(default=False)


class MechanicProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, related_name="mechanic_profile", on_delete=models.CASCADE
    )
    address = models.CharField(max_length=100)
    speciality = models.CharField(max_length=250)
    bio = models.CharField(max_length=250)
    tell = models.CharField(max_length=15)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.user.username


class ServiceRequest(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    car_model = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Service Request by {self.owner.username} - {self.description[:20]}"


class Bid(models.Model):
    mechanic = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bid by {self.mechanic.username} for {self.service_request.title}"


class SelectedService(models.Model):
    service_request = models.OneToOneField(
        ServiceRequest, related_name="selected_service", on_delete=models.CASCADE
    )
    mechanic = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="selected_services",
        on_delete=models.CASCADE,
    )
    selected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Selected Service - {self.service_request.description[:20]} by {self.mechanic.username}"
