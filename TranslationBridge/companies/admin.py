from django.contrib import admin
from .models import Country, City, Language, Company, TranslatorAccreditation
# Register your models here.


class TranslatorAccreditationInline(admin.TabularInline):
    model = TranslatorAccreditation
    extra = 1

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'city', 'rating')
    list_filter = ('country', 'city', 'rating')
    search_fields = ('name','city__name')
    inlines = [TranslatorAccreditationInline]


admin.site.register(Company, CompanyAdmin)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Language)
admin.site.register(TranslatorAccreditation)

