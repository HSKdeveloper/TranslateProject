from django.urls import path
from . import views

app_name = "translation_request"

urlpatterns = [
    path("create/", views.Request_create_view, name="Request_create_view"),
    
]