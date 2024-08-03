from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    ServiceRequestForm,
    BidForm,
    LocationForm,
    MechanicProfileForm,
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import ServiceRequest, Bid, CustomUser, SelectedService, MechanicProfile

from django.db.models import Q
from geopy.distance import geodesic


def home_view(request):
    """
    This function will load the home page
    """
    return render(request, "home.html")


def register_view(request):
    """
    This is a registration method that takes in the user input and process it and
    save it to the Customuser table then login the user
    """

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("/")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    """
    This is a login view that take the username and password and authenticate the user

    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_mechanic:
                return redirect("/")
            elif not user.is_mechanic:
                return redirect("car_owner_portal")
            else:
                messages.error(request, "Invalid user type.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")


def logout_view(request):
    """
    This view will logout the user and redirect him to home page
    """
    logout(request)
    return redirect("home")


@login_required
def post_service_request(request):
    """
    This views allow the user to submit the service they want to be solved by mechanic

    """
    if request.method == "POST":
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.owner = request.user
            service_request.save()
            return redirect("service_request_list")
    else:
        form = ServiceRequestForm()
    return render(request, "post_service_request.html", {"form": form})


@login_required
def bid_for_service_request(request, id):
    """
    This views allow the mechanic to bid a particular service request
    """
    service_request = get_object_or_404(ServiceRequest, id=id)
    if not request.user.is_mechanic:
        return redirect("home")  # Or some other appropriate response

    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.mechanic = request.user
            bid.service_request = service_request
            bid.save()
            return redirect("service_request_detail", id=service_request.id)
    else:
        form = BidForm()

    return render(
        request,
        "bid_for_service_request.html",
        {"form": form, "service_request": service_request},
    )


@login_required
def service_request_list(request):
    """
    This view will list all the service requested by car owners or other mechanic
    """
    service_requests = ServiceRequest.objects.all()
    context = {"service_requests": service_requests}
    return render(request, "service_request_list.html", context)


@login_required
def service_request_detail(request, id):
    """
    This view will query  a single service request and display it
    """
    service_request = get_object_or_404(ServiceRequest, id=id)
    context = {"service_request": service_request}
    return render(request, "service_request_detail.html", context)


@login_required
def car_owner_portal(request):
    """
    This view will display the owner of the car info
    """
    service_requests = ServiceRequest.objects.filter(owner=request.user)
    return render(
        request, "car_owner_portal.html", {"service_requests": service_requests}
    )


@login_required
def select_bid(request, request_id):
    """
    This view enable the car owner to select a bid for his/her service posted
    """
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    if request.user != service_request.owner:
        return redirect("home")

    if request.method == "POST":
        bid_id = request.POST.get("bid_id")
        if bid_id:
            try:
                selected_bid = get_object_or_404(Bid, id=bid_id)
                selected_service, created = SelectedService.objects.get_or_create(
                    service_request=service_request,
                    mechanic=selected_bid.mechanic,
                )
                if created:
                    service_request.selected_bid = selected_bid
                    service_request.save()
                    return redirect("car_owner_portal")
                else:
                    # Handle the case where a SelectedService already exists
                    print("Selected service already exists")
            except Exception as e:
                print(f"Error saving selected bid: {e}")
        else:
            print("No bid selected")

    bids = Bid.objects.filter(service_request=service_request)
    return render(
        request, "select_bid.html", {"service_request": service_request, "bids": bids}
    )


#############################################################################

########### This section is yet to completed

"""
def add_mechanic(request):
    if request.method == "POST":
        form = MechanicProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("mechanic_list")
    else:
        form = MechanicProfileForm()
    return render(request, "add_mechanic.html", {"form": form})


def search_mechanics(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            user_latitude = form.cleaned_data["latitude"]
            user_longitude = form.cleaned_data["longitude"]
            mechanics = MechanicProfile.objects.all()
            closest_mechanic = None
            closest_distance = None

            latitudes = []
            longitudes = []

            for mechanic in mechanics:
                latitudes.append(mechanic.latitude)
                longitudes.append(mechanic.longitude)
                mechanic_location = (mechanic.latitude, mechanic.longitude)
                user_location = (user_latitude, user_longitude)
                distance = geodesic(user_location, mechanic_location).km
                if closest_distance is None or distance < closest_distance:
                    closest_distance = distance
                    closest_mechanic = mechanic

            return render(
                request,
                "mechanic_list.html",
                {
                    "mechanics": mechanics,
                    "closest_mechanic": closest_mechanic,
                    "closest_distance": closest_distance,
                    "latitudes": latitudes,
                    "longitudes": longitudes,
                },
            )
    else:
        form = LocationForm()
    return render(request, "search_mechanics.html", {"form": form})


def mechanic_list(request):
    mechanics = MechanicProfile.objects.all()
    latitudes = [mechanic.latitude for mechanic in mechanics]
    longitudes = [mechanic.longitude for mechanic in mechanics]
    return render(
        request,
        "mechanic_list.html",
        {"mechanics": mechanics, "latitudes": latitudes, "longitudes": longitudes},
    )
"""
