from django.urls import path
from . import views

app_name = "translators"

urlpatterns = [
    path("create-new/", views.create_translator_view, name= "create_translator_view"),
    path("all-list/", views.translator_list_view, name="translator_list_view"),
    path("detail/<translators_id>", views.translator_detail_view, name="translator_detail_view"),
    path("review/<int:translator_id>/", views.review_view, name="review_view"),
    path("update/<translators_id>/", views.translator_update_view, name="translator_update_view"),
    path("delete/<translator_id>/", views.translator_delete_view, name="translator_delete_view"),
]