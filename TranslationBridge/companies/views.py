from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .models import Company, Language
from django.contrib import messages


# Create your views here.


def companies_create_view(request:HttpRequest):


    return render(request, "companies/company_create.html")




def companies_list_view(request:HttpRequest):

    companies = Company.objects.all()

    return render(request, "companies/companies_list.html", {"companies": companies})




def company_detail_view(request:HttpRequest, company_id:int):

  
    

    return render(request, "companies/company_detail.html")




