from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path('payment/<int:request_id>/', views.payment_page, name='payment_page'),
]