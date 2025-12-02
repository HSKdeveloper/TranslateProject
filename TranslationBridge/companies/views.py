from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .models import Company
from django.contrib import messages


# Create your views here.

def companies_list_view(request:HttpRequest):

    companies = Company.objects.all()

    return render(request, "companies/companies_list.html", {"companies": companies})






