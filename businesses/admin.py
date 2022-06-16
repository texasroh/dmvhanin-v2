from django.contrib import admin

from . import models


@admin.register(models.Business)
class BusinessAdmin(admin.ModelAdmin):
    pass
