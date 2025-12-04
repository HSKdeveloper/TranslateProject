from django.db import models
from companies.models import Language

# Create your models here.

class TranslationRequest(models.Model):

    # -------- Choices بطريقة TextChoice --------
    class RequestTypeChoices(models.TextChoices):
        INSTANT = "instant", "Instant Translation"   # ترجمة فورية
        HIRE = "hire", "Hire a Translator"           # طلب مترجم

    class CompnyTypeChoices(models.TextChoices):
        GOVERNMENT = 'government', 'Government'
        PRIVATE = 'private', 'Private'    

    # -------- الحقول المشتركة --------
    company_name = models.CharField(max_length=200)
    company_type = models.CharField(max_length=20, choices=CompnyTypeChoices.choices)
    request_type = models.CharField(max_length=20, choices=RequestTypeChoices.choices)

    # -------- معلومات عامة --------
    description = models.TextField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # -------- الترجمة الفورية --------
    language = models.ForeignKey(Language, on_delete=models.PROTECT, null=True,blank=True)
    specialty = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField(upload_to="pdf/", null=True, blank=True)
    duration_days = models.CharField(max_length=50, null=True, blank=True)

    # -------- طلب مترجم --------
    translator_name = models.CharField(max_length=100, null=True, blank=True)
    translator_specialty = models.CharField(max_length=100, null=True, blank=True)
    translator_start_date = models.DateField(null=True, blank=True)
    translator_duration_days = models.CharField(max_length=50, null=True, blank=True)
    translator_language = models.ManyToManyField(Language, related_name="translator_languages", blank=True)

    def __str__(self):
        return f"{self.company_name} - {self.request_type}"