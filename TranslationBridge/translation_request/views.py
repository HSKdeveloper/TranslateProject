from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .models import TranslationRequest


# Create your views here.

def Request_create_view(request: HttpRequest):
   
   
   



   return render(request, "translation_request/request_create.html")