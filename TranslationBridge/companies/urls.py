from django.urls import path
from . import views

app_name = "companies"

urlpatterns = [
    path("list/", views.companies_list_view, name="companies_list_view"),
]