from django.db import models
from companies.models import Language
from django.contrib.auth.models import User
from translators.models import Translator
# Create your models here.

class TranslationRequest(models.Model):

    # -------- Choices بطريقة TextChoice --------
    class RequestTypeChoices(models.TextChoices):
        INSTANT = "instant", "Instant Translation"   # ترجمة فورية
        HIRE = "hire", "Hire a Translator"           # طلب مترجم

    class CompnyTypeChoices(models.TextChoices):
        GOVERNMENT = 'government', 'Government'
        PRIVATE = 'private', 'Private'    

    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        ASSIGNED = "assigned", "Assigned"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"    
    # -------- الشركة (User) --------
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name="company_requests", null=True, blank=True)
    # -------- الحقول المشتركة --------
    company_name = models.CharField(max_length=200)
    company_type = models.CharField(max_length=20, choices=CompnyTypeChoices.choices)
    request_type = models.CharField(max_length=20, choices=RequestTypeChoices.choices)
    specialty = models.CharField(max_length=100, null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.PROTECT, null=True, blank=True)

    # -------- معلومات عامة --------
    description = models.TextField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # -------- الترجمة الفورية --------
    file = models.FileField(upload_to="pdf/", null=True, blank=True)
    duration_days = models.CharField(max_length=50, null=True, blank=True)

    # -------- طلب مترجم --------
    city = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)

    # -------- المترجم المعيّن بعد الاختيار --------
    translator = models.ForeignKey(Translator, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_requests")

    # -------- حالة الطلب --------
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)

    def __str__(self):
        return f"{self.company_name} - {self.request_type} - {self.status}"
    


    