from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('signup/', views.sign_up, name="sign_up"),
    path('signin/', views.sign_in, name="sign_in"),
    path('logout/', views.logout, name="logout"),
    path('profile/', views.profile_view, name="profile_view"),
    path('update_profile/', views.update_profile_view, name="update_profile_view"),
]