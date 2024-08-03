from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, MechanicProfile


@receiver(post_save, sender=CustomUser)
def create_mechanic_profile(sender, instance, created, **kwargs):
    if created and instance.is_mechanic:
        MechanicProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_mechanic_profile(sender, instance, **kwargs):
    if instance.is_mechanic:
        instance.mechanic_profile.save()
