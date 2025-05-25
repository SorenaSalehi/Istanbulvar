from .views import (
    httpContact,
    httpIndex,
    httpAbout,
    httpMSS,
    httpGP,
    httpOrderAndRefound,
    httpOrders,
    customer_contact_view,
    retailer_contact_view,
)
from django.urls import path

app_name = "website"

urlpatterns = [
    path("", httpIndex, name="index"),
    path("about/", httpAbout, name="about"),
    path("mss/", httpMSS, name="mss"),
    path("gp/", httpGP, name="gp"),
    path("order-refound/", httpOrderAndRefound, name="orderAndRefound"),
    path("orders/", httpOrders, name="orders"),
    path("contact/", httpContact, name="contact"),
    path("customer_contact/", customer_contact_view, name="customer_contact"),
    path("retailer_contact/", retailer_contact_view, name="retailer_contact"),
]
