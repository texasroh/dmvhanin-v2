from django.contrib import admin

from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category", "subcategory")


class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.Business)
class BusinessAdmin(admin.ModelAdmin):
    inlines = (PhotoInline,)
