from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path('payment/<int:request_id>/', views.payment_page, name='payment_page'),
    path('issue-invoice/<int:request_pk>/<int:translator_pk>/', views.issue_invoice_and_assign_translator, name='issue_invoice_and_assign'),
    path('invoice/<int:pk>/', views.invoice_detail_view, name='invoice_detail'), 
    path('invoice/<int:invoice_pk>/confirm-transfer/', views.confirm_transfer_to_translator, name='confirm_transfer'),
]