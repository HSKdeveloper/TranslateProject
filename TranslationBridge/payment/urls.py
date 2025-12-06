from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("create/", views.payment_view, name="payment_view"),
    path("success/", views.payment_success_view, name="payment_success_view"),
    path("cancel/", views.payment_cancel_view, name="payment_cancel_view"),
]