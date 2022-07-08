from django.contrib import admin

from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


@admin.register(models.SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "get_category")

    def get_category(self, obj):
        return obj.category.name


class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.Business)
class BusinessAdmin(admin.ModelAdmin):
    inlines = (PhotoInline,)
    list_display = (
        "name_kor",
        "name_eng",
        "total_review_count",
        "average_rating",
    )


@admin.register(models.Review, models.ReplayReview)
class ReviewAdmin(admin.ModelAdmin):
    pass
