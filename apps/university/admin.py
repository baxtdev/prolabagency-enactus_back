from django.contrib import admin

from .models import University,UniversityDocuments
# Register your models here.

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    pass

@admin.register(UniversityDocuments)
class UniversityDocumentsAdmin(admin.ModelAdmin):
    pass
