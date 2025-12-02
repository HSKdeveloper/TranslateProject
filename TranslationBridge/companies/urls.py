from django.urls import path
from . import views

app_name = "companies"

urlpatterns = [
    path("create/", views.companies_create_view, name="companies_create_view"),
    path("list/", views.companies_list_view, name="companies_list_view"),
    path("detail/<int:company_id>/", views.company_detail_view, name="company_detail_view"),
]