from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from translation_request.models import TranslationRequest
from translators.models import Translator
from .models import Payment
from django.contrib.auth.models import User
from django.contrib import messages

def payment_page(request, request_id):
    # جلب الطلب المرتبط
    translation_request = get_object_or_404(TranslationRequest, id=request_id)
    # جلب المترجم إذا كان الطلب يحتوي مترجم
    translator = translation_request.translator if hasattr(translation_request, 'translator') else None
    # جلب المستخدم صاحب الطلب
    user = translation_request.company
    return render(request, "payment/payment_create.html", {
        "translation_request": translation_request,
        "translator": translator,
        "user": user,
    })