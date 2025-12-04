from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

#import models
from .models import Country, City, Translator, Review, Language, specialty

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
            return redirect('translators:translator_list_view') 
        else:
            print("not valid form", translator_form.errors)
             
    return render(request, "translators/translators_create.html", {"translator_form":translator_form , "RatingChoices":Translator.RatingChoices.choices, "cities":city, "languages":languages } )


#All translator list
def translator_list_view(request:HttpRequest):

    translators = Translator.objects.all()
    languages = Language.objects.all()
    cities = City.objects.all()

    page_number = request.GET.get("page",1)
    paginator = Paginator(translators, 6)
    translators_page =paginator.get_page(page_number)

    context = { "translators": translators_page, "languages": languages, "cities":cities }

    return render(request, "translators/translators_list.html", context)


#Translator detail
def translator_detail_view(request:HttpRequest, translators_id:int):

    translator = Translator.objects.get(pk=translators_id)

    return render(request, 'translators/translators_detail.html',{ "translator" : translator })


#Translator update information
def translator_update_view(request:HttpRequest, translators_id):

    translator = Translator.objects.get( pk=translators_id)
    languages = Language.objects.all()
    specialties = specialty.objects.all()
    all_cities = City.objects.all()

    if request.method == "POST":
        #using TranslatorForm for update
        translator_form = TranslatorForm( instance=translator, data= request.POST, files=request.FILES)
        if translator_form.is_valid():
            translator_form.save()
            messages.success(request, "Translator information updated successfuly", "alert-success")
        else:
            print(translator_form.errors)
        
        return redirect("translators:translator_detail_view", translators_id=translator.id)
    
    return render(request, "translators/translators_update.html", {"translator": translator, "cities": all_cities, "languages":languages, "specialties":specialties})
           



#Translator delete information
def translator_delete_view(request:HttpRequest, translator_id:int):

    try:
        translator = Translator.objects.get(pk = translator_id)
        translator.delete()
        messages.success(request, "Translator information deleted successfuly", "alert-success")
    
    except Exception as e:
        messages.error(request, "Couldn't delete translator information", "alert-danger")

    return redirect("translators:translator_list_view")
