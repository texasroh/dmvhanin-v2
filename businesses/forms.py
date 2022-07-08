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

    # rating = forms.ChoiceField(
    #     widget=forms.RadioSelect,
    #     choices=((i, i) for i in range(1, 6)),
    # )
