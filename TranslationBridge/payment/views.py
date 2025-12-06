from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone  # Used for confirmation timestamps
from translation_request.models import TranslationRequest
from translators.models import Translator
from .models import Invoice  # Assumes you modified the model to 'Invoice'
from django.contrib.auth.models import User
from django.contrib import messages


# -------------------------------------------------------------
# 1. Payment Page (Initial View)
# -------------------------------------------------------------

def payment_page(request: HttpRequest, request_id: int):
    # Fetch the linked request
    translation_request = get_object_or_404(TranslationRequest, id=request_id)
    # Fetch the assigned translator
    translator = translation_request.translator if translation_request.translator else None
    # Fetch the user who made the request (The Company)
    user = translation_request.company
    
    # Check if an invoice already exists for this request
    try:
        invoice = translation_request.invoice
        # If the invoice exists, redirect directly to the invoice detail page
        return redirect('payment:invoice_detail', pk=invoice.pk)
    except Invoice.DoesNotExist:
        pass # If no invoice, continue to display the original page
    
    return render(request, "payment/payment_create.html", {
        "translation_request": translation_request,
        "translator": translator,
        "user": user,
    })


# -------------------------------------------------------------
# 2. Issue Invoice and Assign Translator (Triggered by Company Acceptance)
# -------------------------------------------------------------

def issue_invoice_and_assign_translator(request: HttpRequest, request_pk: int, translator_pk: int):
    # 1. Fetch objects
    req = get_object_or_404(TranslationRequest, pk=request_pk)
    translator_obj = get_object_or_404(Translator, pk=translator_pk)

    # 2. Authorization Check: Only the request owner (Company) can assign
    if request.user != req.company:
        messages.error(request, "Access denied. You are not authorized to assign a translator.", "alert-danger")
        return redirect('translation_request:request_detail_view', pk=request_pk)

    # 3. Update Request Status and Assign Translator
    req.translator = translator_obj
    req.status = TranslationRequest.StatusChoices.ASSIGNED
    req.save()

    # 4. Create the Invoice
    try:
        # Use req.cost as the invoice amount, default to 0 if None
        amount_to_charge = req.cost if req.cost is not None else 0 
        
        invoice = Invoice.objects.create(
            request=req,
            translator=translator_obj,
            amount=amount_to_charge,
            status=Invoice.InvoiceStatus.ISSUED # Status: Issued
        )
        
        # 🎯 Success Message
        messages.success(request, f"Translator assigned and Invoice #{invoice.pk} issued successfully.", "alert-success")
        
        # 5. Send Email Notification to the Translator (Invoice Issued)
        send_mail(
            f"New Invoice Issued for Request #{req.pk}",
            f"Dear {translator_obj.user.username},\n\nA new invoice (ID: {invoice.pk}) has been issued for the request '{req.company_name}'. Please check the platform for details and payment confirmation.\n\nThank you.",
            settings.DEFAULT_FROM_EMAIL,
            [translator_obj.user.email]
        )

    except Exception as e:
        # 🎯 Error Message
        messages.error(request, f"An error occurred while issuing the invoice or sending the email: {e}", "alert-danger")

    # 6. Redirect to the Invoice Details Page
    return redirect('payment:invoice_detail', pk=invoice.pk)


# -------------------------------------------------------------
# 3. Invoice Detail View (Visible to both Company and Translator)
# -------------------------------------------------------------

def invoice_detail_view(request: HttpRequest, pk: int):
    # 1. Fetch the invoice
    invoice = get_object_or_404(Invoice, pk=pk)
    
    # 2. Authorization Check: Must be the Company owner or the assigned Translator
    is_owner = request.user == invoice.request.company
    is_translator = request.user == invoice.translator.user
    
    if not request.user.is_authenticated or (not is_owner and not is_translator):
        messages.error(request, "Access denied. You are not authorized to view this invoice.", "alert-danger")
        return redirect('homepage') 

    # 3. Render Invoice Details
    return render(request, "payment/invoice_detail.html", {
        "invoice": invoice,
    })


# -------------------------------------------------------------
# 4. Confirm Payment Transfer to Translator (Triggered by Company Button Press)
# -------------------------------------------------------------

def confirm_transfer_to_translator(request: HttpRequest, invoice_pk: int):
    invoice = get_object_or_404(Invoice, pk=invoice_pk)
    
    # 1. Authorization Check: Only the Request Company can confirm transfer
    if request.user != invoice.request.company:
        # 🎯 Error Message
        messages.error(request, "Access denied. You are not authorized to confirm this payment.", "alert-danger")
        return redirect('payment:invoice_detail', pk=invoice_pk)

    # 2. Update Invoice Status and Confirmation Dates
    invoice.status = Invoice.InvoiceStatus.TRANSFERRED # Status: Transferred to Translator
    invoice.company_payment_date = timezone.now()
    invoice.transfer_confirmation_date = timezone.now()
    invoice.save()

    # 3. Send Final Email Notification to the Translator (Payment Confirmed)
    translator_email = invoice.translator.user.email
    
    subject = f"✅ Payment Transfer Confirmed for Request #{invoice.request.pk}"
    # 🎯 Email Content in English
    message = (
        f"Dear {invoice.translator.user.username},\n\n"
        f"The company {invoice.request.company.username} confirms that the payment of {invoice.amount} has been transferred for translation request #{invoice.request.pk}.\n"
        "Please check your bank account to verify the funds.\n\n"
        "Thank you for using the platform."
    )

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [translator_email])
        # 🎯 Success Message
        messages.success(request, "Payment transfer confirmed and email successfully sent to the translator.", "alert-success")
    except Exception as e:
        # 🎯 Error Message
        messages.error(request, "Payment confirmed, but failed to send notification email to the translator.", "alert-danger")

    return redirect('payment:invoice_detail', pk=invoice_pk)