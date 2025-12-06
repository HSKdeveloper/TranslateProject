from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest

#for sending email message
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .forms import TranslationRequestForm
from companies.models import Language, City 
from translators.models import specialty, Translator, City, Language
from django.contrib import messages
from .models import TranslationRequest


# Create your views here.

def request_create_view(request: HttpRequest):
    
    languages = Language.objects.all()
    if request.method == "POST":
        form = TranslationRequestForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.company = request.user
            obj.status = "pending"  # تعيين الحالة تلقائياً
            obj.save()
            messages.success(request, "Request added successfully!", "alert-success")
            return redirect('translation_request:request_matched_view', request_id=obj.id)
        else:
            print("Form not valid", form.errors)
    else:
        form = TranslationRequestForm()
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
    translation_request = TranslationRequest.objects.get(pk=pk)

    if request.method == "POST":
        form = TranslationRequestForm(request.POST, request.FILES, instance=translation_request)
        if form.is_valid():
            form.save()
            messages.success(request, "Request updated successfully!", "alert-success")
            return redirect('translation_request:request_detail_view', pk=pk)
        else:
            messages.error(request, "Please correct the errors below.", "alert-danger")
    else:
        form = TranslationRequestForm(instance=translation_request)
    return render(request, "translation_request/request_update.html", {"form": form, "translation_request": translation_request})


def request_delete_view(request: HttpRequest, pk: int):
    translation_request = TranslationRequest.objects.get(pk=pk)
    translation_request.delete()
    messages.success(request, "Request deleted successfully!", "alert-success")
    return redirect('translation_request:request_list_view')

def request_matched_view(request: HttpRequest, request_id: int):

    translation_request = TranslationRequest.objects.get(pk=request_id)

    # البحث عن المدينة
    city_obj = None
    if translation_request.city:
        city_obj = City.objects.filter(name__iexact=translation_request.city).first()

    # البحث عن اللغة
    language_obj = None
    if translation_request.language:
        if isinstance(translation_request.language, Language):
            language_obj = translation_request.language
        else:
            language_obj = Language.objects.filter(name__iexact=str(translation_request.language)).first()

    # البحث عن التخصص
    specialty_obj = None
    if translation_request.specialty:
        specialty_obj = specialty.objects.filter(name__iexact=translation_request.specialty).first()

    # فلترة المترجمين
    matched_translators = Translator.objects.all()
    # فلترة فقط إذا كانت القيم كائنات نموذج صحيحة
    if city_obj is not None and isinstance(city_obj, City):
        matched_translators = matched_translators.filter(city=city_obj)
    if language_obj is not None and isinstance(language_obj, Language):
        matched_translators = matched_translators.filter(languages=language_obj)
    if specialty_obj is not None and isinstance(specialty_obj, specialty):
        matched_translators = matched_translators.filter(specialties=specialty_obj)

    matched_translators = matched_translators.distinct()

    return render(request, "translation_request/request_matched.html", {
        "translation_request": translation_request,
        "matched_translators": matched_translators
    })

def assign_translator(request, request_id, translator_id):

    translation_request = get_object_or_404(TranslationRequest, id=request_id)
    translator = get_object_or_404(Translator, id=translator_id)

    # تعيين المترجم للطلب وتغيير الحالة
    translation_request.translator = translator
    translation_request.status = TranslationRequest.StatusChoices.ASSIGNED
    translation_request.save()
    messages.success(request, "Translator assigned successfully!", "alert-success")
    return redirect('translation_request:request_list_view')
