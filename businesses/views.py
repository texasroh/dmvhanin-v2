from django.http import Http404
from django.shortcuts import render
from django.views.generic import DetailView, FormView, ListView, View

from . import forms, models


class CategoryListView(ListView):
    model = models.Category
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    model = models.Category


class SubCategoryDetailView(View):
    def get(self, request, cat_slug, sub_slug):
        try:
            subcategory = models.SubCategory.objects.get(
                slug=sub_slug, category__slug=cat_slug
            )
            categories = models.Category.objects.all()
        except models.SubCategory.DoesNotExist:
            raise Http404()

        return render(
            request,
            "businesses/subcategory_detail.html",
            {
                "categories": categories,
                "subcategory": subcategory,
            },
        )


class BusinessDetailView(View):
    def get(self, request, cat_slug, sub_slug, biz_slug):
        try:
            business = models.Business.objects.get(
                slug=biz_slug,
                subcategory__slug=sub_slug,
                subcategory__category__slug=cat_slug,
            )
            categories = models.Category.objects.all()
        except models.Business.DoesNotExist:
            raise Http404()

        review_form = forms.CreateReviewForm()

        return render(
            request,
            "businesses/business_detail.html",
            {
                "business": business,
                "categories": categories,
                "review_form": review_form,
            },
        )

    def post(self, request, cat_slug, sub_slug, biz_slug):
        pass
