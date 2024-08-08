from django.urls import path
from . import views

app_name = "seller"

urlpatterns = [
    path("profile-setup/", views.SellerProfileCreateView.as_view(), name="profile_setup_form"),
]