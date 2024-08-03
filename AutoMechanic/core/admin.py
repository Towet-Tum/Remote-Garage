from django.contrib import admin
from .models import CustomUser, MechanicProfile, SelectedService, ServiceRequest, Bid

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(MechanicProfile)
admin.site.register(ServiceRequest)
admin.site.register(SelectedService)
admin.site.register(Bid)
