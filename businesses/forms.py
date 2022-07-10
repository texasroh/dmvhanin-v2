from django import forms

from . import models


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = (
            "rating",
            "review",
        )
        labels = {"rating": "평가", "review": "리뷰"}
        widgets = {"review": forms.Textarea(attrs={"rows": 5})}

    def clean_rating(self):
        return int(self.cleaned_data.get("rating"))

    def save(self):
        return super().save(commit=False)
