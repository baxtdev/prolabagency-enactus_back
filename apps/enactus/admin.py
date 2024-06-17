from django.contrib import admin

from .models import Project,Advertisement,NewsCategory,\
                    News,NewsPhoto,Event

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass

class NewsPhotoInline(admin.TabularInline):
    model = NewsPhoto
    extra = 0

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsPhotoInline]

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    pass



