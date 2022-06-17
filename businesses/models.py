from core import models as core_models
from django.core.exceptions import ValidationError
from django.db import models


class Category(core_models.TimeStampModel):
    category = models.CharField(max_length=50)
    subcategory = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ("category", "subcategory")


class Photo:
    file = models.ImageField(upload_to="business_photos")
    business = models.ForeignKey(
        "Business", related_name="photos", on_delete=models.CASCADE
    )


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

    business_type = models.CharField(
        choices=BUSINESS_TYPE_CHOICES, max_length=20, default=BUSINESS_TYPE_OFFLINE
    )

    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(choices=STATE_CHOICES, max_length=3)
    zipcode = models.CharField(max_length=5, validators=[zipcode_validator])
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    description = models.TextField()
    website = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(
        Category, related_name="businesses", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "users.User", related_name="businesses", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "Businesses"
