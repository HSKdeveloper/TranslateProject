
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .forms import TranslationRequestForm
from companies.models import Language
from django.contrib import messages
from .models import TranslationRequest


# Create your views here.

def request_create_view(request: HttpRequest):
    
   languages = Language.objects.all()
   if request.method == "POST":
        form = TranslationRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Add Translator information successfully!", "alert-success")
            return redirect('translation_request:request_list_view')  #
        else:
            print("Form not valid", form.errors)
   else:
        form = TranslationRequestForm() #hessa
   return render(request, "translation_request/request_create.html", {"form": form, "languages": languages})

      
def request_list_view(request: HttpRequest):

    requests = TranslationRequest.objects.all()

    selected_type = request.GET.get("type")
    if selected_type:
        requests = requests.filter(request_type=selected_type)

    if not request.user.is_authenticated:
      messages.error(request, "You must be logged in to view this list", "alert-danger")
      return redirect("accounts:sign_in")

    return render(request, "translation_request/request_list.html", {"requests": requests})
   

def request_detail_view(request: HttpRequest, pk: int):

    translation_request = TranslationRequest.objects.get(pk=pk)
    related_requests = TranslationRequest.objects.filter(
        location=translation_request.location
    ).exclude(pk=pk)[:3]

    return render(request, "translation_request/request_detail.html", {
        "translation_request": translation_request,
        "related_requests": related_requests
    })

def request_update_view(request: HttpRequest, pk: int):
    pass
def request_delete_view(request: HttpRequest, pk: int):
    pass