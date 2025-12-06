from django.contrib import admin
from .models import TranslationRequest
# Register your models here.

@admin.register(TranslationRequest)
class TranslationRequestAdmin(admin.ModelAdmin):
    list_display = (
        "company_name",
        "company",
        "request_type",
        "status",
        "translator",
        "created_at",
    )
    
    list_filter = ("status", "request_type", "company", "translator")
    
    search_fields = ("company_name", "description")
    
    readonly_fields = ("created_at",)
    
    fieldsets = (
        ("Basic Info", {
            "fields": ("company", "company_name", "company_type", "request_type", "status")
        }),
        ("Translation Details", {
            "fields": ("language", "specialty", "file", "cost", "duration_days", "start_date")
        }),
        ("Location", {
            "fields": ("city", "location")
        }),
        ("Assignment", {
            "fields": ("translator",)
        }),
        ("Meta", {
            "fields": ("created_at",)
        }),
    )

    