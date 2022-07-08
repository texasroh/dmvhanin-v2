from core import models as core_models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(core_models.TimeStampModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"


class SubCategory(core_models.TimeStampModel):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )

    class Meta:
        verbose_name_plural = "Sub categories"
        unique_together = (("category", "slug"), ("category", "name"))

    def __str__(self):
        return f"{self.name}"


def zipcode_validator(zipcode):
    try:
        assert len(zipcode) == 5
        int(zipcode)
        return zipcode
    except (AssertionError, ValueError):
        raise ValidationError("Zipcode accept only five digits")


class Business(core_models.TimeStampModel):

    BUSINESS_TYPE_OFFLINE = "offline"
    BUSINESS_TYPE_ONLINE = "online"
    BUSINESS_TYPE_BOTH = "both"
    BUSINESS_TYPE_CHOICES = (
        (BUSINESS_TYPE_OFFLINE, "Off-line"),
        (BUSINESS_TYPE_ONLINE, "Online"),
        (BUSINESS_TYPE_BOTH, "Both"),
    )

    STATE_VA = "VA"
    STATE_MD = "MD"
    STATE_DC = "DC"
    STATE_CHOICES = (
        (STATE_VA, "Virginia"),
        (STATE_MD, "Mary Land"),
        (STATE_DC, "District of Columbia"),
    )

    name_kor = models.CharField(max_length=50)
    name_eng = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True)

    business_type = models.CharField(
        choices=BUSINESS_TYPE_CHOICES, max_length=20, default=BUSINESS_TYPE_OFFLINE
    )
    description = models.TextField()

    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(choices=STATE_CHOICES, max_length=3)
    zipcode = models.CharField(max_length=5, validators=[zipcode_validator])
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    average_rating = models.FloatField(default=0)
    total_review_count = models.IntegerField(default=0)

    subcategory = models.ForeignKey(
        SubCategory, related_name="businesses", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "users.User", related_name="businesses", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        verbose_name_plural = "Businesses"


class Photo(core_models.TimeStampModel):
    file = models.ImageField(upload_to="business_photos")
    business = models.ForeignKey(
        Business, related_name="photos", on_delete=models.CASCADE
    )


class Review(core_models.TimeStampModel):
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=((1, "형편없다"), (2, "별로다"), (3, "보통이다"), (4, "좋다"), (5, "아주좋다")),
    )
    review = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="business_reviews", on_delete=models.CASCADE
    )
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="reviews"
    )
    is_active = models.BooleanField(default=True)


class ReplayReview(core_models.TimeStampModel):
    replay = models.TextField()
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="replies"
    )
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="replies")
    is_active = models.BooleanField(default=True)
