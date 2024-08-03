from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, ServiceRequest, Bid, MechanicProfile


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "is_mechanic",
            "password",
        )


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "password")


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ["title", "description", "car_model", "service_type"]


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["amount", "message"]


class MechanicProfileForm(forms.ModelForm):
    class Meta:
        model = MechanicProfile
        fields = "__all__"


class LocationForm(forms.Form):
    latitude = forms.FloatField()
    longitude = forms.FloatField()
