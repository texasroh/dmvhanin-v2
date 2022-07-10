from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
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
        try:
            business = models.Business.objects.get(
                slug=biz_slug,
                subcategory__slug=sub_slug,
                subcategory__category__slug=cat_slug,
            )
        except models.Business.DoesNotExist:
            raise Http404()

        review_form = forms.CreateReviewForm()
        action = request.POST.get("action")
        if action == "review":
            review_form = forms.CreateReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save()
                review.user = request.user
                review.business = business
                review.save()

                business.add_review(review_form.cleaned_data.get("rating"))

        return redirect(
            reverse(
                "businesses:business",
                kwargs={
                    "cat_slug": cat_slug,
                    "sub_slug": sub_slug,
                    "biz_slug": biz_slug,
                },
            )
        )


# class BusinessDetailView(FormView):
#     form_class = forms.CreateReviewForm
#     template_name = "businesses/business_detail.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         try:
#             business = models.Business.objects.get(
#                 slug=self.kwargs.get("biz_slug"),
#                 subcategory__slug=self.kwargs.get("sub_slug"),
#                 subcategory__category__slug=self.kwargs.get("cat_slug"),
#             )
#             categories = models.Category.objects.all()
#         except models.Business.DoesNotExist:
#             raise Http404()

#         context["business"] = business
#         context["categories"] = categories

#         form2 = forms.CreateReviewForm()
#         context["form2"] = form2
#         return context

#     def form_valid(self, form):
#         print("form_valid called")
#         return super().form_valid(form)
