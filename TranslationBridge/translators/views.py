from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

#import models
from .models import Country, City, Translator, Review, Language

#import form
from .forms import TranslatorForm

#for pagination
from django.core.paginator import Paginator

#for messages notifications
from django.contrib import messages

#for email messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

#for aggregation
from django.db.models import Count, Avg, Sum, Max, Min, Q, F



# Create your views here.


#Create new translator info
def create_translator_view(request:HttpRequest):

    #Form calling
    translator_form = TranslatorForm()

    city = City.objects.all()
    languages = Language.objects.all()

    if request.method == "POST":

        translator_form = TranslatorForm(request.POST)
        if translator_form.is_valid():
            translator_form.save()

            messages.success(request, "Add Translator information successfully!", "alert-success")
            return redirect('main:home_view')
        else:
            print("not valid form", translator_form.errors)
    

    return render(request, "translators/translators_create.html", {"translator_form":translator_form, "RatingChoices":Translator.RatingChoices.choices, "cities":city, "languages":languages } )