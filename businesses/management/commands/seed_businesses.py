import pandas as pd
from businesses.models import Business, Category, SubCategory
from django.core.management.base import BaseCommand
from django.db import IntegrityError


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        data = pd.read_csv("businesses.csv")
        for idx, row in data.iterrows():
            sub_cat = SubCategory.objects.get(
                name=row["category2"], category__name=row["category1"]
            )
            i = 1
            slug = row["slug"]
            while True:
                try:
                    Business.objects.create(
                        name_kor=row["business_name_kor"],
                        name_eng=row["business_name_eng"],
                        slug=slug,
                        business_type=Business.BUSINESS_TYPE_OFFLINE,
                        description=row["description"],
                        address=row["address"],
                        city=row["city"],
                        state=row["state"],
                        zipcode=row["zipcode"],
                        phone_number=row["phone_number"],
                        email=row["email"],
                        website=row["website"],
                        is_active=True,
                        subcategory=sub_cat,
                    )
                    break
                except IntegrityError:
                    i += 1
                    slug = row["slug"] + "-" + str(i)
            print(idx)

        self.stdout.write(self.style.SUCCESS("Businesses created!"))
