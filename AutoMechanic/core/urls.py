from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    home_view,
    post_service_request,
    bid_for_service_request,
    select_bid,
    service_request_list,
    service_request_detail,
    car_owner_portal,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    # Other URL patterns
    path("post_service_request/", post_service_request, name="post_service_request"),
    path("service_request/<int:request_id>/select_bid/", select_bid, name="select_bid"),
    path("service_requests/", service_request_list, name="service_request_list"),
    path(
        "service_requests/<int:id>/",
        service_request_detail,
        name="service_request_detail",
    ),
    path(
        "service_request/<int:id>/bid/",
        bid_for_service_request,
        name="bid_for_service_request",
    ),
    path("car_owner_portal/", car_owner_portal, name="car_owner_portal"),
    # Mechanics urls
    # path("add_mechanic/", add_mechanic, name="add_mechanic"),
    # path("search_mechanics/", search_mechanics, name="search_mechanics"),
    # path("mechanic_list/", mechanic_list, name="mechanic_list"),
]
