from django.contrib import admin

from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category", "subcategory")


@admin.register(models.Business)
class BusinessAdmin(admin.ModelAdmin):
    pass
