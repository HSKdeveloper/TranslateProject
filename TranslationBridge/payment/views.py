from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

# Create your views here.

def payment_view(request: HttpRequest):

    return render(request, "payment/payment_create.html")

def payment_success_view(request: HttpRequest):

    return render(request, "payment/payment_detail.html")


def payment_cancel_view(request: HttpRequest):

    return render(request, "main/home.html")