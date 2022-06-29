from django.urls import path

from . import views

app_name = "businesses"

urlpatterns = [
    path("categories", views.CategoryListView.as_view(), name="categories"),
    path("<str:slug>", views.CategoryDetailView.as_view(), name="category"),
    path(
        "<str:cat_slug>/<str:sub_slug>",
        views.SubCategoryDetailView.as_view(),
        name="subcategory",
    ),
]
