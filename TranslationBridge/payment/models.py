from django.db import models
from django.contrib.auth.models import User
# تأكد من أن هذا الاستيراد صحيح
from translation_request.models import TranslationRequest 
from translators.models import Translator # 🎯 نحتاج لربط الفاتورة بالمترجم

class Invoice(models.Model):
    
    # حالات الفاتورة/الدفع
    class InvoiceStatus(models.TextChoices):
        ISSUED = 'issued', 'Issued'        # تم إصدارها (في انتظار الدفع)
        PAID = 'paid', 'Paid'              # تم دفعها للشركة (للدلالة على تحويل الشركة للمال)
        TRANSFERRED = 'transferred', 'Transferred to Translator' # تم تحويل المبلغ للمترجم (التأكيد النهائي)
    
    # ربط الفاتورة بطلب الترجمة (علاقة واحد لواحد)
    request = models.OneToOneField(TranslationRequest, on_delete=models.CASCADE, related_name="invoice")
    
    # 🎯 الشركة (التي تدفع) - مربوطة بـ TranslationRequest.company
    
    # 🎯 المترجم (الذي يستلم) - يجب ربطه بالمترجم المعيّن
    translator = models.ForeignKey(Translator, on_delete=models.SET_NULL, null=True, related_name="invoices_received")

    # المبلغ المتفق عليه
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # تاريخ إصدار الفاتورة
    issue_date = models.DateTimeField(auto_now_add=True)
    
    # حالة الفاتورة
    status = models.CharField(max_length=50, choices=InvoiceStatus.choices, default=InvoiceStatus.ISSUED)
    
    # سجل الدفع (إذا تم استخدام بوابة دفع خارجية)
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    # 🎯 تاريخ تأكيد الدفع من الشركة (هذا هو الزر الذي ستضغط عليه الشركة)
    company_payment_date = models.DateTimeField(null=True, blank=True)
    
    # 🎯 تاريخ تأكيد التحويل للمترجم (إذا كنت تريد تتبع هذه المرحلة)
    transfer_confirmation_date = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"Invoice #{self.pk} for Request {self.request.pk}"