from django.shortcuts import render
from django.views.generic import DetailView, ListView, View

from . import models


class CategoryListView(ListView):
    model = models.Category
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    model = models.Category


class SubCategoryDetailView(View):
    def get(self, request, cat_slug, sub_slug):
        subcategory = models.SubCategory.objects.get(
            slug=sub_slug, category__slug=cat_slug
        )
        return render(
            request, "businesses/subcategory_detail.html", {"subcategory": subcategory}
        )
